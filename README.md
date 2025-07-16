Location Based Business Finder

A Python-based web application that helps users find nearby businesses (e.g., restaurants, bukas, pharmacies) using the Geoapify and Foursquare APIs, with a Streamlit interface for interactive maps and navigation. Built with Object-Oriented Programming (OOP), this project is tailored for Nigerian users, supporting local business categories like “buka” and “suya_spot,” and features live location tracking for real-time navigation.
Table of Contents

Features
Installation
Usage
Project Structure
File Descriptions
Known Issues
Contributing
License

Features

Search Nearby Businesses: Find businesses by location (automatic via browser/IP or manual input) and category (e.g., “restaurant,” “buka”).
Nigerian-Specific Categories: Supports local terms like “catering.buka,” “commercial.petty_trader,” and “catering.suya_spot.”
Interactive Maps: Displays businesses on a Folium map with user and business markers, connected by lines.
Turn-by-Turn Directions: Provides navigation instructions from the user’s location to a selected business using Geoapify.
Live Location Tracking: Updates directions in real-time as the user moves (using browser geolocation).
Robust Error Handling: Manages API failures, invalid inputs, and geolocation issues with user-friendly feedback.
Map Export: Saves maps to static/map.html for offline viewing (optional).

Installation

Clone the Repository:
git clone https://github.com/yourusername/location-based-business-finder.git
cd location-based-business-finder


Set Up a Virtual Environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install streamlit folium streamlit-folium streamlit-geolocation requests python-dotenv haversine


Configure API Keys:

Sign up for Geoapify and Foursquare to get API keys.
Create a .env file in the project root:GEOAPIFY_API_KEY=your_geoapify_key
FOURSQUARE_API_KEY=your_foursquare_key





Usage

Run the Application:
streamlit run main.py


This opens the app in your default browser (e.g., http://localhost:8501).


Search for Businesses:

Location: Choose “Use my current location” (browser geolocation or IP fallback) or enter an address (e.g., “Wuye, Abuja”).
Business Type: Enter a category (e.g., “buka,” “pharmacy”). The app fuzzy-matches to valid categories.
Click “Search Businesses” to view results.


View Results:

See businesses on an interactive Folium map with markers and connecting lines.
Browse a list with details (name, address, distance, rating, contact info).
Click “Get Directions” for turn-by-turn navigation or enable live tracking.


Export Map (Optional):

Maps can be saved to static/map.html for offline viewing (requires enabling in code).



Project Structure
location-based-business-finder/
├── config/
│   ├── config.py          # API key and settings management
│   ├── utils.py           # Utility functions (API requests, logging, map export)
├── core/
│   ├── business.py        # Business class for data and directions
│   ├── business_finder.py # Business search and filtering
│   ├── constant.py        # Geoapify categories and fuzzy matching
│   ├── gui_manager.py     # Streamlit GUI and map rendering
│   ├── location_manager.py # Address geocoding
├── static/
│   ├── map.html           # Exported Folium map (optional)
├── .env                   # API keys (not tracked)
├── business_finder.log    # Error log file
├── main.py                # Application entry point
├── README.md              # This file

File Descriptions

config.py:

Purpose: Manages API keys and default settings.
Functionality: Loads Geoapify/Foursquare keys from .env, provides defaults (radius: 1000m, category: “restaurant,” limit: 10).
Role: Supplies configuration to all components.


utils.py:

Purpose: Provides utility functions for backend operations.
Functionality: Handles API requests (make_api_request), IP geolocation (get_location_from_ip), error logging (log_error), and map export (save_map_html).
Role: Supports robust API calls and fallbacks.


location_manager.py:

Purpose: Converts addresses to coordinates.
Functionality: Uses Geoapify to geocode addresses (e.g., “Lagos, Nigeria” → (lat, lon)).
Role: Provides coordinates for searches and maps.


business_finder.py:

Purpose: Searches and processes businesses.
Functionality: Queries Geoapify for businesses, creates Business objects, filters by rating, sorts by distance.
Role: Powers the core search functionality.
Note: Contains a bug in filter_by_rating (see Known Issues).


business.py:

Purpose: Represents a business with attributes and methods.
Functionality: Stores details (name, address, etc.), fetches directions, and gets Foursquare ratings.
Role: Models business data for display and navigation.


constant.py:

Purpose: Defines Geoapify categories and maps user inputs.
Functionality: Lists categories (e.g., “catering.buka”), fuzzy-matches inputs (e.g., “pharmacy” → “healthcare.pharmacy”).
Role: Validates categories, supporting Nigerian terms.


gui_manager.py:

Purpose: Manages the Streamlit web interface.
Functionality: Handles location/category input, displays maps and business lists, provides directions and live tracking.
Role: Creates the user-facing experience.


main.py:

Purpose: Entry point for the application.
Functionality: Launches the app by running GUIManager.run_app.
Role: Starts the Streamlit app.



Known Issues

Bug in business_finder.py:
In filter_by_rating, the line filtered.append(Business) incorrectly appends the Business class instead of the business instance. This may cause filtering to fail.
Fix: Change to filtered.append(business).
Impact: Filtering by rating may not work until fixed.


Foursquare Integration: The Foursquare API key is loaded but not fully utilized (e.g., fetch_rating_from_foursquare is optional).
Live Tracking: May not work reliably on desktop browsers without GPS; best on mobile devices.

Contributing
We welcome contributions! To contribute:

Fork the repository.
Create a branch: git checkout -b feature/your-feature.
Commit changes: git commit -m "Add your feature".
Push to the branch: git push origin feature/your-feature.
Open a pull request.

Please follow these guidelines:

Fix the business_finder.py bug as a priority.
Add tests (e.g., unit tests for BusinessFinder or LocationManager).
Enhance features (e.g., add “bike” travel mode, improve live tracking).
Document changes clearly.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Developed by: [Group 6 Cohort 26 Python Advanced]Last Updated: July 16, 2025Contact: [Your Email or GitHub Issues]
