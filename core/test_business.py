from config.config import Config
from business import Business
import requests
# Load API keys
config = Config()
geoapify_key = config.get_api_key("geoapify")
fsq_key = config.get_api_key("foursquare")

#  Set up your location
user_cords = (9.0579, 7.4951)

url = "https://api.geoapify.com/v2/places"
params = {
    "categories": "catering.restaurant",
    "filter": f"circle:{user_cords[1]},{user_cords[0]},1000",
    "bias": f"proximity:{user_cords[1]},{user_cords[0]}",
    "limit": 5,
    "apiKey": geoapify_key
}

try:
    response = requests.get(url, params=params)
    data = response.json()

    if "features" not in data or not data["features"]:
        print("❌ No businesses found in your area.")
    else:
        print(f"✅ Found {len(data['features'])} nearby businesses:\n")

        for i, feature in enumerate(data["features"], 1):
            # Create a Business object from Geoapify response
            business = Business.from_geoapify(feature)

            print(f"🔹 Business #{i}")
            print(business.get_details())

            # Fetch and attach Foursquare rating
            rating = business.fetch_rating_from_foursquare(fsq_key)
            if rating:
                business.set_rating(rating)
                print(f"⭐ Rating (Foursquare): {rating/2}/10")
            else:
                print("⭐ Rating not available on Foursquare")

            # Attempt to get directions from user to business
            print("\n📍 Directions:")
            directions = business.get_directions(user_cords, geoapify_key)
            print(directions)
            print("-" * 50)

except Exception as e:
    print(f"⚠️ An error occurred while fetching business data: {e}")