

```markdown
# Location Based Business Finder

Welcome to Location Based Business Finder, a Python-based web application designed to help users discover nearby businesses, such as restaurants, bukas, and pharmacies, with interactive maps and real-time navigation. Built using Streamlit and powered by Geoapify and Foursquare APIs, this project is tailored for Nigerian users, supporting local business categories like "buka" and "suya_spot." The application features an intuitive interface, live location tracking, and turn-by-turn directions, all developed with Object-Oriented Programming (OOP) principles for modularity and scalability.

## Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [File Descriptions](#file-descriptions)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features
- **Find Nearby Businesses**: Search for businesses by location (automatic via browser/IP or manual input) and category (e.g., "restaurant," "buka").
- **Nigerian-Specific Categories**: Supports local terms like "catering.buka," "catering.suya_spot," and "commercial.petty_trader" for a tailored experience.
- **Interactive Maps**: Visualize businesses on a Folium map with user and business markers connected by lines.
- **Turn-by-Turn Directions**: Get detailed navigation instructions from your location to a selected business using Geoapify.
- **Live Location Tracking**: Update directions in real-time as you move, leveraging browser geolocation.
- **User-Friendly Interface**: Built with Streamlit for a seamless, browser-based experience.
- **Map Export**: Save maps to static/map.html for offline viewing.
- **Robust Error Handling**: Manages invalid inputs, API failures, and geolocation issues with clear feedback.

## Demo
1. Run the app with `streamlit run main.py`.
2. Enter a location (e.g., "Wuye, Abuja") or use automatic detection.
3. Search for a category (e.g., "buka").
4. View businesses on an interactive map and click "Get Directions" for navigation.

*Note: Live tracking works best on mobile devices with GPS enabled.*

## Installation
Follow these steps to set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/location-based-business-finder.git
   cd location-based-business-finder
   ```

2. **Set Up a Virtual Environment (recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install streamlit folium streamlit-folium streamlit-geolocation requests python-dotenv haversine
   ```

4. **Configure API Keys**:
   - Sign up for Geoapify and Foursquare to obtain API keys.
   - Create a `.env` file in the project root with the following:
     ```
     GEOAPIFY_API_KEY=your_geoapify_key
     FOURSQUARE_API_KEY=your_foursquare_key
     ```

## Usage
1. **Launch the Application**:
   ```bash
   streamlit run main.py
   ```
   This opens the app in your default browser (e.g., `http://localhost:8501`).

2. **Search for Businesses**:
   - **Location**: Select "Use my current location" for automatic detection (browser or IP-based) or enter an address manually (e.g., "Lagos, Nigeria").
   - **Business Type**: Input a category (e.g., "buka," "pharmacy"). The app uses fuzzy matching to handle variations or misspellings.
   - Click "Search Businesses" to view results.

3. **Explore Results**:
   - View businesses on an interactive Folium map with markers for your location (green) and businesses (red), connected by gray lines.
   - Browse a detailed list with business names, addresses, distances, ratings, and contact info (phone, email, website if available).
   - Expand the "Directions" section to select a travel mode ("walk" or "drive") and click "Get Directions" for turn-by-turn instructions.
   - Enable live tracking to update directions as you move (ideal for mobile devices).

4. **Export Map (Optional)**:
   - Save the map to `static/map.html` for offline viewing by enabling the `save_map_html` function in `utils.py`.

## Project Structure
```
location-based-business-finder/
├── config/
│   ├── config.py          # API key and settings management
│   ├── utils.py           # Utility functions for API calls, logging, and map export
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
├── README.md              # Project documentation
├── LICENSE                # MIT License file
├── requirements.txt       # Dependencies list
```

## File Descriptions
### config.py:
- Manages API keys (Geoapify, Foursquare) and default settings (search radius: 1000m, default category: "restaurant," limit: 10).
- Loads keys from `.env` for security and provides defaults for consistent searches.

### utils.py:
- Offers utility functions: `make_api_request` for reliable API calls with retries, `get_location_from_ip` for IP-based geolocation, `log_error` for logging to `business_finder.log`, and `save_map_html` for exporting Folium maps.

### location_manager.py:
- Converts addresses (e.g., "Wuye, Abuja") to coordinates using Geoapify's geocoding API, returning latitude, longitude, and formatted address.

### business_finder.py:
- Searches for businesses near a location using Geoapify's Places API, creates Business objects, and supports filtering by rating and sorting by distance.

### business.py:
- Represents a business with attributes (name, address, coordinates, etc.) and methods to fetch directions (Geoapify) and ratings (Foursquare).

### constant.py:
- Defines Geoapify categories, including Nigerian-specific ones (e.g., "catering.buka"), and fuzzy-matches user inputs to valid categories.

### gui_manager.py:
- Manages the Streamlit interface, handling location/category input, displaying interactive maps and business lists, and providing directions with live tracking.

### main.py:
- The entry point that launches the app by initializing `GUIManager` and calling `run_app`.

## Contributing
We welcome contributions to enhance the Location Based Business Finder! To contribute:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit changes: `git commit -m "Add your feature"`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a pull request with a clear description of your changes.

**Contribution Ideas**:
- Add support for additional travel modes (e.g., "bike," "tricycle").
- Enhance live tracking for better desktop compatibility.
- Integrate more Foursquare features (e.g., reviews).
- Write unit tests for `BusinessFinder` and `LocationManager`.

Please adhere to our Code of Conduct and ensure code is well-documented.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
- **Project Maintainers**: [Group 6 | Python Advanced | Cohort 26]
- **GitHub**: [Davidayo123](https://github.com/Davidayo123)
- **Issues**: Report bugs or suggest features via [GitHub Issues](https://github.com/Davidayo123/location-based-business-finder/issues)

**Contributors**:
- Ayotunde David Anointing: [ayotundeferanmi09@gmail.com](mailto:ayotundeferanmi09@gmail.com)
- Omotayo Emmanuel Ayomide: [ayotundeferanmi09@gmail.com](mailto:ayotundeferanmi09@gmail.com)
- Austine Victor Eshorameh: [austinev698@gmail.com](mailto:austinev698@gmail.com)
- Momoh Muhammad Mubarak: [Mubby1708@gmail.com](mailto:Mubby1708@gmail.com)

**Developed by**: [Group 6 | Python Advanced | Cohort 26]  
**Last Updated**: July 16, 2025  

*Star this repository if you find it useful! 🌟*
```
