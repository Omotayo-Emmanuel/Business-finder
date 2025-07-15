from core.business import Business
from typing import List, Tuple, Any
from config.utils import make_api_request, log_error, validate_api_key
import requests


class BusinessFinder:
    """Manages searching for businesses near a location using an API."""

    def __init__(self, api_key) -> None:
        """Initialize with an API key for place search services.

        Args:
            api_key (str): API key for external place search services.

        """
        is_valid, msg = validate_api_key(api_key)
        if not is_valid:
            raise ValueError(f"We have a Geoapify API key Error: {msg}")

        self.api_key = api_key


    def search_businesses(self, coords: Tuple[float, float], business_type: str, radius: int =10000) -> list[Any]:
        """Search for businesses near the given coordinates.

        Args:
            coords (tuple): (latitude, longitude) of the search center.
            radius (int): Search radius in meters.
            business_type (str): Optional filter for business type (e.g., 'restaurant').

        Returns:
            list: List of Business objects
        """
        url = "https://api.geoapify.com/v2/places"
        lat, lon = coords

        query_params = {
            "categories": business_type,
            "filter": f"circle:{lon},{lat},{radius}",
            "bias": f"proximity:{lon},{lat}",
            "limit": 20,
            "apiKey": self.api_key
        }

        try:
            response = make_api_request(url, query_params)
            data = response.json()

            if "features" not in data or not data["features"]:
                print(" No businesses found.")
                return []
            return self.parse_results(data, coords)

        except Exception as e:
            log_error(e, "Failed, to search businesses from Geoapify")
            return []

    def parse_results(self, data, user_coords: Tuple|None) ->  list:
        """Parse API response into a list of Business objects.

        Args:
            data (dict): Raw API response data.
            user_coords (tuple): User's (latitude, longitude) for distance calculation.

        Returns:
            list: List of (Business, distance) tuples.
        """
        businesses = []

        for feature in data.get("features", []):
            try:
                business = Business.from_geoapify(feature, user_coords)
                businesses.append(business)
            except Exception as e:
                log_error(e, "Failed to parse a business feature")

        return businesses

    @staticmethod
    def filter_by_rating(businesses: List, min_rating: float = 2.5) -> List:
        """
        Filter out businesses that have no rating or have ratings below the minimum threshold.
        Converts Foursquare ratings (out of 10) to a common /5 scale for filtering.

        Args:
            businesses (List[Business]): List of business objects to filter.
            min_rating (float): Minimum acceptable rating on a 5-point scale.

        Returns:
            List[Business]: Filtered list of businesses with ratings >= min_rating.
        """

        filtered = [] # storing the filtered businesses into a list

        for business in businesses:
            # Only considering businesses that have a rating
            if business.rating is not None: # Calling business.rating from our business class
                # Converting /10 rating to /5
                rating_out_of_5  = business.rating / 2

                # If it passes the minimum threshold, keep it
                if rating_out_of_5 >= min_rating:
                    filtered.append(Business)

        return filtered

    def sort_by_distance(self, businesses:list) -> list:
        """
        Sort a list of business by their distance from the user.

        Args:
            businesses (list): List of Business objects, each with a 'distance_m' attribute.

        Returns:
            list: Businesses sorted from nearest to farthest.
        """

        if not businesses:
            return []

        ## Sort businesses by their 'distance_m' attribute in ascending order
        sorted_businesses = sorted(businesses, key=lambda b: b.distance_m)

        return sorted_businesses



