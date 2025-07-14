from config.config import Config
from business_finder import BusinessFinder
from location_manager import LocationManager

# Load configuration and API keys
config = Config()
geoapify_key = config.get_api_key("geoapify")
foursquare_key = config.get_api_key("foursquare")

# Convert address to coordinates
address = "Wuye, Abuja, Nigeria"
location_data = LocationManager.geocode_address(address, geoapify_key)

if location_data:
    user_coords = (location_data['lat'], location_data['lon'])
    print(f"📍 Coordinates for {address}: {user_coords}")

    # Instantiate BusinessFinder with Geoapify API key
    finder = BusinessFinder(geoapify_key)

    # Search for businesses (e.g., catering services)
    businesses = finder.search_businesses(user_coords, business_type="catering", radius=2000)

    if businesses:
        print(f"\n✅ Found {len(businesses)} businesses near {address}:\n")
        for i, biz in enumerate(businesses, 1):
            # Fetch Foursquare rating using your built-in method
            rating = biz.fetch_rating_from_foursquare(foursquare_key)

            print(f"🔹 Business #{i}")
            print(biz.get_details())  # Assuming get_details shows rating
            print("-" * 50)
    else:
        print("❌ No businesses found.")

else:
    print(f"⚠️ Couldn't geocode location: {address}")
