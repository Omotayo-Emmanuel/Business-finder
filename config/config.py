import os # to be able to interact with environment Variables
from dotenv import load_dotenv # to load Variables from .env file into the environment


class Config:
    """Handles configuration settings, such as API keys and defualts, securely."""

    def __init__(self) -> None:
        """Initialize configuration by loading environment variables and setting defaults.
        This allows sensitive data like our API KEYS to be kept outside the codebase.
        """
        load_dotenv() # Loads key-value pairs

        # Loading the API keys from environment
        self.geoapify_key = os.getenv("GEOAPIFY_API_KEY")
        self.foursquare_key = os.getenv("FOURSQUARE_API_KEY")
        #self.google_key = os.getenv("GOOGLE_API_KEY")

        # Default search setting for business finder
        self.default_radius  = 5000 # Radius in meters
        self.default_category = "restaurant" # Default type of business to search for

        # Default map settings for folium
        self.zoom_level = 15 # Ideal for the business location and navigation
        self.map_tile = "OpenStreetMap" # Using the default OpenstreetMap for simplicity and reliability
        self.map_output_file = "business_results_map.html" # Output HTML file name
        self.marker_color = "green" # using this as my default color for business markers



    def get_api_key(self, service:str  = "geoapify") -> str:
        """Return the API key for external services.
        :param service: either "geoapify" or "Foursquare"
        :return: API key as a string"""

        if service == "geoapify":
            return self.geoapify_key
        elif service == "foursquare":
            return self.foursquare_key
        else:
            raise ValueError("Unsupported services: it is either 'geoapify' or 'google'")

    def get_default_settings(self) -> dict:

        """
        This will return a dictionary of default business search settings.
        Useful for Customizing searches without hardcoding values elsewhere.
        """

        return {
            "radius": self.default_radius,
            "category": self.default_category
        }

    def get_map_settings(self) -> dict:
        """
        Return a Dictionary of map display settings
        These values are used when generating the folium map
        """

        return {
            "zoom": self.zoom_level,
            "tile": self.map_tile,
            "output_file": self.map_output_file,
            "marker_color": self.marker_color
        }


