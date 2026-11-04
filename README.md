# Location-Based Business Finder

## Overview
A Python application to search for businesses near a specified location using APIs and display results in a GUI with a map view.

## Setup
1. Install Python 3.x.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:pip install -r requirements.txt


Set up API keys (e.g., Geoapify):
Sign up at https://www.geoapify.com.
Set the keys as environment variables:
```bash
GEOAPIFY_API_KEY="your-api-key-here"
FOURSQUARE_API_KEY="your-foursquare-key"
```




Run the application:
```bash
streamlit run main.py
```



Folder Structure

config/: Stores configuration settings.
core/: Contains core logic (LocationManager, Business, BusinessFinder, GUIManager).
static/: Stores generated map files.
main.py: Application entry point.
requirements.txt: Lists dependencies.

Usage

Enter a location (e.g., "San Francisco, CA") in the GUI.
Click "Search" to find nearby businesses.
View results in a table and an interactive map.

