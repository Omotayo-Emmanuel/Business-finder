from typing import Tuple
import folium
import requests

import streamlit as st # GUI Library for our Web app
from haversine import haversine
from streamlit_folium import folium_static
from streamlit_geolocation import streamlit_geolocation


# project modules
import os
from config.config import Config
from core.business import Business
from core.business_finder import BusinessFinder
from core.location_manager import LocationManager
from core.constant import match_category
from config.utils import get_location_from_ip
from config.utils import save_map_html

class GUIManager:
    """Manages the graphical user interface for the application."""

    def __init__(self):
        """
        Initialize the GUI manager:
        - Load API keys from config.
        - Instantiate BusinessFinder with Geoapify key.
        """
        self.config = Config()

        # Loading my api keys securely
        self.geoapify_key = self.config.get_api_key("geoapify")
        self.foursquare_key = self.config.get_api_key("foursquare")

        # Instantiate my busines finder with geoapify key
        self.business_finder = BusinessFinder(self.geoapify_key)

    def get_realtime_directions(self, business, travel_mode):
        """
        Continuously updates and displays navigation directions from the user's real-time position
        to the selected business using Geoapify.

        This function uses `streamlit_geolocation()` to detect changes in the user's location
        and fetches updated directions whenever the user moves significantly (50+ meters).

        Args:
            business (Business): The business object the user wants to navigate to.
            travel_mode (str): The selected travel method ('walk', 'drive', 'bike').

        Returns:
            list: A list of updated direction instructions or previously cached directions.
        """

        # --- Track and initialize the user's last known location ---
        # If this is the first time tracking, use the current static location as the starting point
        if 'last_known_location' not in st.session_state:
            st.session_state.last_known_location = st.session_state.user_coords

        # --- Set up a Streamlit container to display tracking UI ---
        with st.container():
            st.write("**Live Location Tracking**")

            # Call the geolocation widget with a unique key (based on business name)
            # This widget will auto-update as the user moves
            location = streamlit_geolocation()


            # If location was successfully retrieved and contains latitude
            if location and location.get("latitude"):
                current_location = (location["latitude"], location["longitude"])

                # Only update directions if the user moved more than 50 meters
                if haversine(current_location, st.session_state.last_known_location) > 0.05:  # 0.05 km = 50 meters
                    # Update last known location to this new position
                    st.session_state.last_known_location = current_location

                    # Show a loading spinner while fetching updated directions
                    with st.spinner("Updating directions..."):
                        directions = business.get_directions(
                            current_location,  # Live location
                            self.geoapify_key,  # API key for Geoapify routing
                            travel_mode  # Mode of travel: walk, drive, etc.
                        )

                        # Save the latest directions in session state (associated with this business)
                        st.session_state[f"directions_{business.name}"] = directions

                        # Immediately refresh the UI to reflect new directions
                        st.rerun()

            # Display the user's live coordinates to give visual feedback
            st.write(f"📍 Your position: {current_location[0]:.5f}, {current_location[1]:.5f}")

            #
            # If user clicks stop, remove the stored last known location and rerun the app
            if st.button("Stop Tracking", key=f"stop_{business.name}"):
                del st.session_state.last_known_location
                st.rerun()
        # Return updated directions from session state (or empty if none exists yet)
        return st.session_state.get(f"directions_{business.name}", [])

    def display_businesses(self, businesses: list, user_coords: Tuple[float, float]):
        """
        Display a list of businesses in a structured Streamlit format.

        Args:
            businesses (list): List of Business objects.
            user_coords (tuple): User's coordinates for generating directions.
        """

        # Store businesses and user coordinates in session_state for access in other parts of the app
        st.session_state['current_businesses'] = businesses
        st.session_state['user_coords'] = user_coords

        # Loop through each business and render its info block on the UI
        for i, business in enumerate(businesses, 1):
            st.markdown(f"---")  # Separator between each business listing
            st.subheader(f"{i}. {business.name}")  # Business number and name

            # Display basic information about the business
            st.write(f"**Address:** {business.address}")
            st.write(f"**Distance:** {int(business.distance_m)} meters")

            rating = business.rating
            if rating is None and self.foursquare_key:
                rating = business.fetch_rating_from_foursquare(self.foursquare_key)
            st.write(f"**Rating:** {rating}/5" if rating else "**Rating:** Not available")

            # Optional contact fields: displayed only if present on the object
            if hasattr(business, "phone") and business.phone:
                st.write(f"**Phone:** {business.phone}")
            if hasattr(business, "email") and business.email:
                st.write(f"**Email:** {business.email}")
            if hasattr(business, "website") and business.website:
                st.markdown(f"**Website:** [Visit Site]({business.website})", unsafe_allow_html=True)

            # Initialize direction-related session state if not already created
            if f"directions_{i}" not in st.session_state:
                st.session_state[f"directions_{i}"] = {
                    "mode": "walk",  # Default travel mode
                    "steps": None,  # To store turn-by-turn instructions
                    "index": 5,  # For paginated display (if needed)
                    "live_tracking": False,  # Placeholder for live tracking logic
                    "last_location": user_coords  # Store last known user location
                }

            # Create an expandable section for route options and map
            with st.expander("Directions"):

                # User selects the travel mode (radio button), key is unique per business
                travel_mode = st.radio(
                    "Travel mode",
                    ["walk", "drive"],
                    key=f"travel_mode_{i}"
                )

                # Save selected mode into session state (ensures persistence on rerun)
                st.session_state[f"directions_{i}"]["mode"] = travel_mode

                # Button to trigger the fetching and display of route directions
                if st.button("Get Directions", key=f"get_dir_btn{i}"):
                    with st.spinner("Fetching directions..."):
                        try:
                            # Construct request URL to Geoapify Routing API
                            route_url = (
                                f"https://api.geoapify.com/v1/routing?"
                                f"waypoints={user_coords[0]},{user_coords[1]}|{business.latitude},{business.longitude}"
                                f"&mode={travel_mode}&apiKey={self.geoapify_key}"
                            )
                            # Send request to Geoapify
                            response = requests.get(route_url)

                            # Raise an exception if the response is not 2xx
                            response.raise_for_status()
                            data = response.json()

                            # Check if route data was returned
                            if data.get("features"):
                                feature = data["features"][0]

                                # Turn-by-turn instruction section
                                st.subheader("Turn-by-Turn Directions")
                                for leg in feature["properties"]["legs"]:
                                    for j, step in enumerate(leg["steps"], 1):
                                        instruction = step.get("instruction", {}).get("text", "Continue")
                                        distance = step.get("distance", 0)
                                        st.markdown(f"**{j}. {instruction}** ({int(distance)}m)")

                                # Initialize map centered at user location
                                route_map = folium.Map(location=[user_coords[0], user_coords[1]], zoom_start=13)
                                # Retrieve route coordinates from Geoapify response
                                coordinates = feature["geometry"].get("coordinates", [])
                                route_path = []

                                # Handle LineString type (flat list of lon, lat)
                                if all(isinstance(coord, list) and len(coord) == 2 and isinstance(coord[0],
                                                                                                  (int, float)) for
                                       coord in coordinates):
                                    route_path = [[coord[1], coord[0]] for coord in
                                                  coordinates]  # Swap [lon, lat] → [lat, lon]

                                # Handle MultiLineString type (nested list of [lon, lat])
                                elif all(isinstance(segment, list) for segment in coordinates):
                                    for segment in coordinates:
                                        for coord in segment:
                                            if len(coord) == 2:
                                                route_path.append([coord[1], coord[0]])

                                # Draw the route on the map
                                folium.PolyLine(route_path, color='blue', weight=4).add_to(route_map)

                                # Mark user's origin location
                                folium.Marker(
                                    location=[user_coords[0], user_coords[1]],
                                    popup="Your Location",
                                    icon=folium.Icon(color="green", icon="user")
                                ).add_to(route_map)

                                # Mark destination business location
                                folium.Marker(
                                    location=[business.latitude, business.longitude],
                                    popup=business.name,
                                    icon=folium.Icon(color="red", icon="briefcase")
                                ).add_to(route_map)

                                # Render the map in the Streamlit app
                                folium_static(route_map, width=700, height=400)

                            else:
                                st.warning("No route data received from Geoapify.")

                        # Catch common request failure scenarios
                        except requests.exceptions.RequestException as e:
                            st.error("Network error while contacting Geoapify.")
                            st.exception(e)

                        # Catch all other unexpected errors
                        except Exception as e:
                            st.error("An unexpected error occurred while retrieving directions.")
                            st.exception(e)

                # Optional: Refresh button to re-trigger the logic
                if st.button("Refresh Directions", key=f"refresh_{i}"):
                    st.rerun()

            # Always provide a fallback link to OpenStreetMap for external viewing
            map_url = f"https://www.openstreetmap.org/?mlat={business.latitude}&mlon={business.longitude}#map=18"
            st.markdown(f"[View on Map]({map_url})", unsafe_allow_html=True)

    def render_map(self, user_coords: Tuple[float, float], businesses: list) -> None:
        """
        Generate and display an interactive Folium map in Streamlit showing user location
        and nearby businesses with markers and connecting lines.
        Args:
            user_coords (tuple): (lat, lon) of the user's location to center the map.
            businesses (list): List of Business objects to display on map.
        """
        try:
            # Initializing the map centered at the user's current location wih a moderate zoom level
            user_map = folium.Map(location=user_coords, zoom_start=14)

            # Adding marker for the user's location (green, labeled "Your Location")
            folium.Marker(  # This is the marker function in folium
                location=user_coords,
                popup="Your Location",
                icon=folium.Icon(color="green", icon="user")
            ).add_to(user_map)

            # Looping through each business to add its own marker on the map
            for i, business in enumerate(businesses, 1):
                folium.Marker(
                    location=(business.latitude, business.longitude),
                    popup=business.name,  # Show business name on click
                    color="red",
                    icon=folium.Icon(color="red", icon="info-sign")  # Red icon for businesses
                ).add_to(user_map)

            # Draw a straight line (polyline) from the user's location to each business location
            for business in businesses:
                folium.PolyLine(
                    locations=[user_coords, (business.latitude, business.longitude)],
                    color='gray',
                    weight=2,
                    opacity=0.7
                ).add_to(user_map)

            # Display the entire map within Streamlit using the folium_static function
            folium_static(user_map, width=800, height=500)

        except Exception as e:
            st.error("Failed to load interactive map.")
            st.exception(e)

    def run_app(self):
        """
    Main method that runs the entire Streamlit app:
    - Takes user location (auto/manual)
    - Accepts business type as input
    - Shows map and business results
    """
        # Configure the page to use wide layout and set the title
        st.set_page_config(page_title="Services at Your Door Step", layout="wide")

        # Display the main title and brief instructions
        st.title("📍 Nearby Businesses")  # Using an emoji for visual appeal
        st.write("Enter your location and a business type to discover nearby places!")  # Simple user guidance

        # Create a sidebar container for all search controls
        with st.sidebar:
            # Section header for search settings
            st.subheader("Search Settings")

            # Radio button to choose location method - I'm storing this in session state
            location_method = st.radio(
                "Location Method:",
                ("Use my current location", "Enter location manually"),
                key="location_method"  # Using key to maintain state between reruns
            )

            # Initialize variable to store coordinates
            user_coords = None

            # Handle automatic location detection
            if location_method == "Use my current location":
                # Get browser's geolocation - this prompts user for permission
                location = streamlit_geolocation()

                if location:  # If user granted permission
                    lat = location.get("latitude")
                    lon = location.get("longitude")

                    if lat is not None and lon is not None:  # Valid coordinates received
                        # Check for (0,0) which often indicates failed GPS
                        if (lat, lon) == (0.0, 0.0):
                            st.warning("Your location could not be detected accurately. Trying IP-based fallback...")

                            # Fallback to IP geolocation since GPS failed
                            ip_coords = get_location_from_ip(self.geoapify_key)

                            if ip_coords:  # If IP geolocation worked
                                user_coords = ip_coords
                                st.session_state.user_coords = user_coords  # Store in session
                                st.success(f"IP-based location detected: ({user_coords[0]:.4f}, {user_coords[1]:.4f})")
                            else:
                                st.error("Automatic location detection failed. Please enter your location manually.")
                        else:
                            # Good coordinates from browser GPS
                            user_coords = (lat, lon)
                            st.session_state.user_coords = user_coords
                            st.success(f"Location detected: ({lat:.4f}, {lon:.4f})")
                    else:
                        st.warning("Incomplete coordinates received. Please try manual location.")
                else:
                    st.warning("Unable to access your location. Please allow browser permission or try manual entry.")

            # Handle manual location entry
            elif location_method == "Enter location manually":
                location_input = st.text_input("Enter location (e.g., Wuye, Abuja)")

                if location_input:  # Only geocode if user entered something
                    result = LocationManager.geocode_address(location_input, self.geoapify_key)

                    if result:  # Successful geocoding
                        user_coords = (result["lat"], result["lon"])
                        st.session_state.user_coords = user_coords
                        st.success(f"Location found: {result['address']}")  # Show formatted address
                    else:
                        st.error("Location not found. Please check the address and try again.")

            # Business search section - only show if we have coordinates
            if user_coords or 'user_coords' in st.session_state:
                # Use current or stored coordinates
                current_coords = user_coords if user_coords else st.session_state.user_coords

                # Input for business type
                category_input = st.text_input("Business type (e.g., hotel, clinic)")

                # Search button handler
                if st.button("Search Businesses"):
                    if not category_input:
                        st.warning("Please enter a business type.")
                    else:
                        # Match input to known categories
                        matched_category = match_category(category_input)

                        if not matched_category:
                            st.error("Business type not recognized. Please try again.")
                        else:
                            # Show loading spinner during search
                            with st.spinner(f"Searching for {matched_category}..."):
                                businesses = self.business_finder.search_businesses(current_coords, matched_category)

                                if not businesses:
                                    st.warning("No businesses found in that area.")
                                else:
                                    # Store sorted results and refresh the page
                                    st.session_state.current_businesses = self.business_finder.sort_by_distance(
                                        businesses)
                                    st.rerun()  # Refresh to show results

        # Main content area - only show if we have search results
        if 'current_businesses' in st.session_state and 'user_coords' in st.session_state:
            # Display the interactive map at the top
            self.render_map(st.session_state.user_coords, st.session_state.current_businesses)

            # Show results header
            st.subheader("Search Results")

            # Display all business listings
            self.display_businesses(st.session_state.current_businesses, st.session_state.user_coords)

            # New search button to reset everything
            if st.button("New Search"):
                # Clear stored results and coordinates
                for key in ['current_businesses', 'user_coords']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()  # Refresh to show empty search form