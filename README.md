# Location-Based Business Finder

A Python application that finds businesses near a specified location using Geoapify API, with a user-friendly Streamlit GUI. Features include business search, distance calculation, ratings, and interactive maps.

## Features

- **Location-Based Search**: Find businesses by category near any address or your current location
- **Interactive Maps**: Visualize business locations with Folium/Geoapify maps
- **Business Details**: View names, addresses, distances, and ratings
- **Directions**: Get step-by-step directions to any business
- **Smart Category Matching**: Fuzzy-matches user input to 200+ business categories
- **Secure Configuration**: API keys stored in `.env` file
- **Error Handling**: Robust logging and retry mechanisms for API calls

## Project Structure

```text
business_finder/
├── config/
│   ├── .env               # Environment variables (API keys)
│   └── config.py          # Configuration settings loader
├── core/
│   ├── __init__.py        # Package initialization
│   ├── business.py        # Business entity class
│   ├── business_finder.py # Business search logic
│   ├── constant.py        # Geoapify category definitions
│   ├── gui_manager.py     # Streamlit GUI implementation
│   ├── location_manager.py# Geocoding functionality
│   └── utils.py           # Utilities and error handling
├── static/                # Generated HTML/CSS/JS files
│   └── map.html           # Interactive map output
├── main.py                # Application entry point
├── requirements.txt       # Dependency list
└── README.md              # This documentation
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/business-finder.git
   cd business-finder
   ```

2. **Set up environment**
   - Create `.env` file in `config/` with your API keys:
     ```ini
     GEOAPIFY_API_KEY=your_geoapify_key_here
     FOURSQUARE_API_KEY=your_foursquare_key_here
     ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

Run the application:
```bash
streamlit run main.py
```

### Application Flow:
1. **Choose location method**:
   - Automatic (browser geolocation)
   - Manual address entry

2. **Enter business type** (e.g., "restaurant", "pharmacy")

3. **View results**:
   - List of nearby businesses
   - Interactive map
   - Distance and rating information
   - Directions to each business

## 🔧 Dependencies

- Python 3.8+
- Core Packages:
  - `streamlit` (GUI)
  - `folium` (Mapping)
  - `requests` (API calls)
  - `python-dotenv` (Environment variables)
  - `haversine` (Distance calculation)

See full list in [requirements.txt](requirements.txt)

## 🌟 Key Components

### 1. Business Class (`core/business.py`)
- Represents individual businesses with:
  - Name, address, coordinates
  - Distance calculation
  - Rating fetching (Foursquare API)
  - Directions generation

### 2. Business Finder (`core/business_finder.py`)
- Handles Geoapify API interactions
- Implements search, filtering, and sorting
- Uses retry logic for robust API calls

### 3. GUI Manager (`core/gui_manager.py`)
- Streamlit-based interface with:
  - Location input (auto/manual)
  - Category matching
  - Results display with maps
  - Responsive design

### 4. Utilities (`core/utils.py`)
- API error handling
- Request retries
- Map generation
- Comprehensive logging

## 📝 Example Usage

```python
# Sample business search
finder = BusinessFinder(api_key)
businesses = finder.search_businesses(
    coords=(9.0765, 7.3986),  # Abuja coordinates
    business_type="restaurant",
    radius=5000  # 5km radius
)
```

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📧 Contact


Ayotunde David Anointing - ayotundeferanmi09@gmail.com
Momoh Muhammad Mubarak - Mubby1708@gmail.com

Project Link: [https://github.com/Omotayo-Emmanuel/Business-finder](https://github.com/Omotayo-Emmanuel/Business-finder)
