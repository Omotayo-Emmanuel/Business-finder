from typing import Tuple
import folium

import streamlit as st # GUI Library for our Web app
import streamlit.components.v1 as components  # Needed to render custom HTML
from streamlit_geolocation import streamlit_geolocation


# project modules
import os
from config.config import Config
from core.business_finder import BusinessFinder
from core.location_manager import LocationManager
from core.constant import match_category
from core.utils import save_map_html

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

    def display_businesses(self, businesses: list, user_coords: Tuple[float, float]):
        """
        Display a list of businesses in a structured Streamlit format.

        Args:
            businesses (list): List of Business objects.
            user_coords (tuple): User's coordinates for generating directions.
        """

        # Store businesses and user_coords in session state
        st.session_state['current_businesses'] = businesses
        st.session_state['user_coords'] = user_coords

        # Looping through each business found in the list and display their details
        for i, business in enumerate(businesses, 1):
            st.markdown(f"---")
            # Display the business name as a subheading with its number
            st.subheader(f"{i}. {business.name}")
            # Show business address
            st.write(f"**Address:** {business.address}")
            # Show distance from user (rounded to nearest meter)
            st.write(f"**Distance:** {int(business.distance_m)} meters")
            # Show the rating, if available. Fallback message if not rated
            if business.rating:
                st.write(f"**Rating:** {business.rating}/5")
            else:
                st.write("Rating: Not available")

            # Initialize session state for this business's directions
            if f"directions_{i}" not in st.session_state:
                st.session_state[f"directions_{i}"] = {
                    "mode": "walk",
                    "steps": None,
                    "index": 5
                }

            # Use an expandable section for displaying directions (optional for users)
            with st.expander("Directions"):
                # Get current state for this business
                dir_state = st.session_state[f"directions_{i}"]
                # added this to be able to change the direction type
                travel_mode = st.selectbox("Choose mode of travel",
                                           ["walk", "drive", "bike"],
                                           index=["walk", "drive", "bike"].index(dir_state["mode"]),
                                           key=f"mode_select_{i}" )

            # Update session state when travel mode changes
            if travel_mode != dir_state["mode"]:
                dir_state["mode"] = travel_mode
                dir_state["steps"] = None  # Clear old directions
                dir_state[f"directions_{i}"] = dir_state

            if st.button("Get Directions", key=f"directions_btn_{i}"):
                # Use business method to fetch directions from user location to business
                directions = business.get_directions(user_coords,
                                                     self.geoapify_key,
                                                     dir_state["mode"])

                dir_state["steps"] = directions if isinstance(directions, list) else [str(directions)]
                dir_state["index"] = 5
                st.session_state[f"directions_{i}"] = dir_state

                # Display directions if available
            if dir_state["steps"]:
                for j, step in enumerate(dir_state["steps"][:dir_state["index"]], 1):
                    st.markdown(f"{j}. {step}")

                if dir_state["index"] < len(dir_state["steps"]):
                    if st.button("Show More Directions", key=f"more_{i}"):
                        dir_state["index"] += 5
                        st.session_state[f"directions_{i}"] = dir_state
            # Provide a clickable link to view the business on OpenStreetMap
            map_url = f"https://www.openstreetmap.org/?mlat={business.latitude}&mlon={business.longitude}#map=18"
            st.markdown(f"[View on Map]({map_url})", unsafe_allow_html=True)

    def render_map(self, user_coords: Tuple[float, float], businesses: list):
        """
        Generate and display a map with business locations.

        Args:
            user_coords (tuple): (lat, lon) of the user's location to center the map.
            businesses (list): List of Business objects to display on map.
        """
        try:
            os.makedirs("static", exist_ok=True) # Ensure the 'static' directory exists
            map_file = "static/map.html"  # Where the HTML map is saved

            # Save map HTML using the utility
            save_map_html(user_coords[0], user_coords[1], businesses,self.geoapify_key ,filename=map_file)

            # Read and display the map in Streamlit
            with open(map_file, 'r', encoding='utf-8') as file:
                map_html = file.read()
                components.html(map_html, height=600, scrolling=True)

        except Exception as e:
            st.error("Failed to load map.")
            st.exception(e)


    def run_app(self):
        """Launches the Business Finder app interface using Streamlit.
        Allows user to provide their location (auto/manual),
        input a business type, and view nearby business results.
        """
        # setting the streamlit page configuration
        st.set_page_config(page_title= "Services at Your Door Step", layout="centered")

        # Display or main title and description
        st.title("Businesses close-by")
        st.markdown("Enter your location and insert a business type to discover nearby places!")

        # Check if we have existing search results to display
        if 'current_businesses' in st.session_state and 'user_coords' in st.session_state:
            self.display_businesses(st.session_state['current_businesses'], st.session_state['user_coords'])
            return  # Skip the search form if we're showing results

        # Creating a radio button for user to choose between automatic and manual
        location_method = st.radio("How would you like to set current location?",("Use my current location", "Enter location manually"))

        # Initialize location variables
        location_input = ""
        user_coords = None  # this would hold our lat, lon

        if location_method == "Use my current location":
            # Use streamlit-geolocation for browser-based location
            location = streamlit_geolocation()
            if location:
                lat = location.get("latitude")
                lon = location.get("longitude")
                if lat is not None and lon is not None:
                    user_coords = (lat, lon)
                    st.success(f"Location detected: ({lat:.4f}, {lon:.4f})")
                else:
                    st.warning("Coordinates could not be retrieved.")
            else:
                 st.warning("Unable to access location. Please allow location permission or try manual entry.")

        elif location_method == "Enter location manually":
            # Manual location input
            location_input = st.text_input("Enter your location (e.g., Wuye, Abuja)")
            if location_input:
                result = LocationManager.geocode_address(location_input, self.geoapify_key)
                if result:
                    user_coords = (result["lat"], result["lon"])
                    st.success(f"Location found: {result['address']}")
                else:
                    st.error("Location not found. Please check the address and try again.")
        if user_coords:
            # collecting the type of business the user want to search for
            category_input = st.text_input("What type of business are you looking for? (e.g., buka, clinic, hotel)")

            # This below will be handling our search
            if st.button("Search"):
                if not user_coords:
                    st.warning("Location is missing. Please provide or allow location access.")
                    return # To prevent the app from continuing with a search when the input is invalid

                if not category_input:
                    st.warning("Please enter a business type.")
                    return

                # Matching the user's input to Geoapify categories
                matched_category = match_category(category_input)
                if not matched_category:
                    st.error("We couldn't recognize that business/service type. Please try again.")
                    return

                st.info(f"Searching for `{matched_category}` businesses  near your location...")

                # Perform the search Using Business finder
                businesses = self.business_finder.search_businesses(user_coords, matched_category)

                # This is for the display of results
                if not businesses:
                    st.warning("No businesses found in that area.")
                    return

                # Optionally sort by distance (default behavior)
                sorted_businesses = self.business_finder.sort_by_distance(businesses)

                # Optional: render map of business locations
                self.render_map(user_coords, sorted_businesses, )

                # Show business details
                self.display_businesses(sorted_businesses, user_coords)

