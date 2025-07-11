import requests #Used to make HTTP requsets to our API
from unicodedata import category
from haversine import haversine
from typing import Tuple, Optional


class Business:
    """Represents a single business entity with details like name, address, and coordinates."""

    def __init__(self, name, address, coordinates,distance_m, category, rating=None):
        """Initialize a business object with provided details.

        Args:
            name (str): Name of the business.
            address (str): Address of the business.
            coordinates (tuple): (latitude, longitude) of the business.
            rating (float, optional): Rating of the business.
            distance_m (float): Distance from user''s location in meters.
            category (str): Type/category of the business (e.g restaurant)
            rating (float, optional): Rating of the business.
        """
        self.name  = name
        self.address = address
        self.latitude, self.longitude = coordinates # Coordinates in (latitude, longitude) order
        self.distance_m = distance_m # How far the business is from the user
        self.category = category
        self.rating = rating

    def set_rating(self, rating) -> None:
        """
        Attach  user review-style rating
        """
        self.rating = rating

    def get_details(self) -> str:
        """Returns a human-readable string with all known details of the business.

        Returns:
            str: Formatted string containing business details.
        """
        details = f"{self.name}\n"
        details += f"Address: {self.address}\n"
        details += f"Distance: {self.distance_m} meters\n"
        details += f"Category: {self.category}\n"

        if self.rating: # Only show if rating is available
            details += f"Rating: {self.rating}/10 "
        return details

    def get_directions(self, start_cords, api_key, mode =  "walk") ->list | str:
        """Fetch directions from a starting point to this business using Geoapify Routing API.

        Args:
            start_cords (tuple): Starting (latitude, longitude).
            api_key (str): API key for directions service.
            mode (str): Travel mode ('walk', 'drive', 'bike').

        Returns:
            list or string: List of step instruction strings, or a list with a single error message.
        """
        # API endpoint for Geoapify routing
        url = "https://api.geoapify.com/v1/routing"

        # Made a query parameters variable to include the start and destination coordinates, mode of travel, and API key
        query_param ={
            # this defines our
            "waypoints": f"{start_cords[0]},{start_cords[1]}|{self.latitude},{self.longitude}",
            "mode" : mode,
            "apiKey": api_key
        }

        try:
            # Use Get request to ask Geoapify for directions
            response  = requests.get(url, params=query_param)

            # Check if the request was successful
            if response.status_code != 200:
                return [f"Error: Received status code {response.status_code} from Geoapify"]

            data = response.json() # Parse the JSON (make it in a format python will understand)

            # Checking if the response contains valid directions
            if "features" in data and data["features"]:
                steps = data["features"][0]["properties"]["legs"][0].get("steps", [])
                if not steps:
                    return ["No route steps found."]

                return [step.get("instruction", {}).get("text", "No instruction") for step in steps]

            return ["Directions aren't available."]
        except Exception as e:
            return f"Error while fetching directions: {str(e)}"

    def fetch_rating_from_foursquare(self, fsq_api_key) -> float|None:
        """
        Using Foursquare API to search for this business and fetch its user rating (if available).

        Args:
            fsq_api_key (str): Foursquare API key

        Returns:
            float or None: Rating value or None if not found.
        """
        # Searching for the business on FOURSQUARE by name and location
        search_url = "https://api.foursquare.com/v3/places/search"
        headers = {
            "Accept": "application/json",
            "Authorization": fsq_api_key # API key for authentication
        }

        params = {
            "query": self.name, # Search by business name
            "ll": f"{self.latitude}, {self.longitude}", # Lat/Lon Location for precise matching
            "limit": 1 # TO get the closest match
        }

        try:
            # Send search request to Foursquare
            search_response = requests.get(search_url, headers=headers, params= params)
            search_data = search_response.json()
            results = search_data.get("results", [])

            if not results:
                return None # When there's no matching business found

            # Extract the Foursquare ID of the matched business
            fsq_id = results[0]["fsq_id"]

            # Using the fdq_id to fetch the business details
            details_urls = f"https://api.foursquare.com/v3/places/{fsq_id}"
            details_response = requests.get(details_urls, headers=headers)
            details_data = details_response.json()

            # Extract the ratings field if it exists
            rating = details_data.get("rating")
            if rating:
                self.set_rating(rating) # Update the business Object with the fetched rating
                return rating

            return None # No rating in the response
        except Exception as e:
            print(f"Error fetching Foursquare rating: {str(e)}")
            return None

    @classmethod # showing that this method belongs the class not just an individual object
    def from_geoapify(cls, data:dict, user_coords:Optional[Tuple[float, float]] = None):
        """
        Factory method to create a Business object directly from Geoapify API response.

        Args:
            data (dict): A single Geoapify result (from features list).
            user_coords (tuple, optional): User's (lat, lon) for distance calculation fallback.
        Returns:
            Business: A new Business instance.
        """

        # Get the 'properties' section which contains most of the business info
        properties = data.get("properties", {}) # puts all the business info inside a property section
        name = properties.get("name", "Unnamed Business") # Default if name is missing
        address = properties.get("formatted", "No address") # Default if address is missing

        # Extract coordinates and revers them to (lat, lon)
        lat = data["geometry"]["coordinates"][1]
        lon = data["geometry"]["coordinates"][0]

        # Distance from user location using geoapify provides this automatically
        distance  = properties.get("distance")

        # if not provided, compute it manually
        if distance is None and user_coords:
            distance = haversine(user_coords, (lat, lon)) * 1000  # in meters
        elif distance is None:
            distance = 0  # fallback if no user_coords

        # Trying to extract the business category
        business_category = properties.get("categories", ["unknown"])[0].split("/")[-1]

        # Creating and return a new Business object with the extracted data
        return cls(name, address, (lat,lon), round(distance,2) ,business_category)



