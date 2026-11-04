# Nigeria Business Finder

A Streamlit application for finding nearby businesses in Nigeria. Search by
location and business type, view results on an interactive map, and request
walking or driving directions.

## Features

- Detect the user's location through the browser or accept a manually entered address.
- Search Geoapify Places by business category and radius.
- Sort results by distance.
- Display business details, ratings, contact information, and websites when available.
- Show nearby businesses on an interactive Folium map.
- Open a business location in Google Maps.
- Request turn-by-turn directions through Geoapify.

## Requirements

- Python 3.10 or newer
- A Geoapify API key
- A Foursquare API key (optional; used to retrieve additional ratings)

## Local setup

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure API keys

Copy [.env.example](.env.example) to `config/.env` and replace the placeholder
values:

```dotenv
GEOAPIFY_API_KEY=your-geoapify-api-key
FOURSQUARE_API_KEY=your-foursquare-api-key
```

Keep `config/.env` private. Do not commit API keys or paste them into generated
map files.

Get a Geoapify key from [geoapify.com](https://www.geoapify.com/). Foursquare
ratings are optional, but the application expects the variable to exist when
the configuration is loaded.

### 4. Start the application

```bash
streamlit run main.py
```

Streamlit will print a local URL, normally `http://localhost:8501`.

## Using the application

1. Choose **Use my current location** and allow browser location access, or
   choose **Enter location manually**.
2. Enter a business type such as `restaurant`, `pharmacy`, `hotel`, or `clinic`.
3. Select **Search Businesses**.
4. Review the results, map markers, ratings, and available contact details.
5. Expand **Directions** for a selected business to request a route.

Browser geolocation requires HTTPS when the app is deployed. Manual location
entry works without browser location permission.

## Deployment

The app is a long-running Streamlit process, not a static site. Streamlit
Community Cloud is the simplest deployment option:

1. Push the repository to GitHub.
2. Create a new app in Streamlit Community Cloud.
3. Select `main.py` as the entry point.
4. Add `GEOAPIFY_API_KEY` and `FOURSQUARE_API_KEY` as deployment secrets.
5. Deploy using the dependencies in `requirements.txt`.

In Streamlit Cloud, open **Manage app > Settings > Secrets** and enter:

```toml
GEOAPIFY_API_KEY = "your-new-geoapify-api-key"
FOURSQUARE_API_KEY = "your-new-foursquare-api-key"
```

The names are case-sensitive. Save the secrets, then reboot the app. Do not
include a `[secrets]` section, commit these values to GitHub, or add spaces
inside the key values.

For other hosts, use this start command:

```bash
streamlit run main.py --server.address 0.0.0.0 --server.port $PORT
```

Free hosting and API plans may impose sleep, resource, request, or quota
limits. Geoapify and Foursquare usage is subject to each provider's terms and
rate limits.

## Project structure

```text
business_finder/
├── config/
│   ├── config.py          # Environment variables and application settings
│   └── utils.py           # API, logging, and map utilities
├── core/
│   ├── business.py        # Business model and directions/ratings
│   ├── business_finder.py # Geoapify business searches
│   ├── constant.py        # Supported business categories
│   ├── gui_manager.py     # Streamlit interface
│   └── location_manager.py# Address geocoding
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
└── .env.example           # Environment variable template
```

## Troubleshooting

- **Missing module:** activate the virtual environment and run
  `python -m pip install -r requirements.txt`.
- **API key error:** confirm the variable names exactly match
  `GEOAPIFY_API_KEY` and `FOURSQUARE_API_KEY`, then save them under
  **Manage app > Settings > Secrets** and reboot the app.
- **No results:** try a broader business category or a different location.
- **Location unavailable:** allow browser permission or use manual location entry.
- **429/rate-limit response:** wait and retry, or check the provider's API quota.
