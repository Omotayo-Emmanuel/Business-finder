# core/location_manager.py
import requests
from business_finder_2.config.config import API_KEY, GEOCODE_ENDPOINT


class LocationManager:
    """
    A class to handle geocoding operations (address to coordinates conversion).

    This class provides static methods for interacting with the Geoapify
    geocoding API to convert human-readable addresses to geographic coordinates.
    """

    @staticmethod
    def geocode_address(address):
        """
        Convert a human-readable address to geographic coordinates.

        Args:
            address (str): The address to geocode (e.g., "1600 Pennsylvania Ave NW, Washington, DC")

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
            'apiKey': API_KEY,
            'format': 'json',
            'limit': 1
        }

        try:
            print(f"Attempting to geocode: {address}")  # Debug print
            response = requests.get(GEOCODE_ENDPOINT, params=params, timeout=10)
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