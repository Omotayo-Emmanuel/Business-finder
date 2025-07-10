# core/location_manager.py
import requests
import  logging  # Used for structured and scalable logging instead of print statements
# Removed this:
# from business_finder_2.config.config import API_KEY

# Reason:
# Hardcoding or importing sensitive keys like API_KEY directly into multiple files is insecure and breaks reusability.
# Instead, we now pass the API key as a method argument for better modularity and security.


class LocationManager:
    """
    A class to handle geocoding operations (address to coordinates conversion).

    This class provides static methods for interacting with the Geoapify
    geocoding API to convert human-readable addresses to geographic coordinates.
    """

    # Instead of importing the endpoint from another file, we define it here so that the class is self-contained and reusable.
    # This also makes it easier to override or test if needed.

    GEOCODE_ENDPOINT = "https://api.geoapify.com/v1/geocode/search"

    @staticmethod
    def geocode_address(address: str, api_key: str) ->dict|None :
        """
        Convert a human-readable address to geographic coordinates.

        Args:
            address (str): The address to geocode (e.g., "1600 Pennsylvania Ave NW, Washington, DC")
            api_key (str): Geoapify API key
        Returns:
            dict: Dictionary containing:
                - 'lat': Latitude coordinate
                - 'lon': Longitude coordinate
                - 'address': Formatted address string
            None: If geocoding fails or address not found

        Raises:
            Prints error message to console if API request fails
        """
        params = {
            'text': address,
            'apiKey': api_key,
            'format': 'json',
            'limit': 1
        }

        try:
            print(f"Attempting to geocode: {address}")  # Debug print
            response = requests.get(LocationManager.GEOCODE_ENDPOINT, params=params, timeout=10)
            print(f"API Response Status: {response.status_code}")  # Debug

            response.raise_for_status()
            data = response.json()

            print(f"API Response Data: {data}")  # Debug

            if not data.get('results'):
                print("No results found in API response")
                return None

            result = data['results'][0]
            return {
                'lat': result['lat'],
                'lon': result['lon'],
                'address': result['formatted']
            }

        except requests.exceptions.RequestException as e:
            print(f"Network error during geocoding: {e}")
            return None
        except (KeyError, IndexError) as e:
            print(f"Data parsing error: {e}")
            return None