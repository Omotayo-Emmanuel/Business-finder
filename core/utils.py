# core/utils.py
import webbrowser
import os
import logging
from functools import wraps
import time
import requests
from typing import Callable, Optional, Tuple, Any
# from business_finder_2.config.config import API_KEY


def configure_logging(log_file: str = 'business_finder.log', level: int = logging.INFO):
    """
    Configure logging for the application.

    Args:
        log_file (str): Path to log file
        level (int): Logging level (e.g., logging.INFO, logging.DEBUG)
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    logging.getLogger('requests').setLevel(logging.WARNING)


# Initialize logging when module is imported
configure_logging()


def log_errors(func: Callable) -> Callable:
    """
    Decorator to log exceptions that occur in functions.

    Args:
        func (Callable): Function to decorate

    Returns:
        Callable: Wrapped function with error logging
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            raise

    return wrapper


def api_error_handler(func: Callable) -> Callable:
    """
    Decorator specifically for handling API-related errors.

    Args:
        func (Callable): API calling function to decorate

    Returns:
        Callable: Wrapped function with API error handling
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed in {func.__name__}: {str(e)}")
            raise
        except ValueError as e:
            logging.error(f"API response parsing failed in {func.__name__}: {str(e)}")
            raise

    return wrapper


def log_error(error: Exception, context: str = "", raise_again: bool = False):
    """
    Standardized error logging function.

    Args:
        error (Exception): The error that occurred
        context (str): Additional context about where the error occurred
        raise_again (bool): Whether to re-raise the exception after logging
    """
    logging.error(f"{context}: {str(error)}", exc_info=True)
    if raise_again:
        raise error


def validate_location(location: Any) -> Tuple[bool, str]:
    """
    Validate location input.

    Args:
        location: Input to validate as a location

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not location:
        return False, "Location cannot be empty"
    if not isinstance(location, str):
        return False, "Location must be a string"
    if len(location.strip()) < 2:
        return False, "Location too short"
    return True, ""


def validate_api_key(key: Any) -> Tuple[bool, str]:
    """
    Validate API key format.

    Args:
        key: Input to validate as an API key

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not key:
        return False, "API key cannot be empty"
    if not isinstance(key, str):
        return False, "API key must be a string"
    if len(key) not in (32,48) :  # Geoapify keys are 32 or 48 chars
        return False, "Invalid API key length"
    return True, ""


def retry_api_call(max_retries: int = 3, delay: float = 1.0,
                   backoff: float = 2.0, exceptions: tuple = (requests.exceptions.RequestException,)):
    """
    Decorator for retrying API calls.

    Args:
        max_retries (int): Maximum number of retries
        delay (float): Initial delay between retries in seconds
        backoff (float): Multiplier for delay between retries
        exceptions (tuple): Exceptions to catch and retry on

    Returns:
        Callable: Decorated function with retry logic
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries, current_delay = 0, delay
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries == max_retries:
                        logging.error(f"Max retries ({max_retries}) exceeded for {func.__name__}")
                        raise
                    logging.warning(f"Retry {retries}/{max_retries} for {func.__name__} after {current_delay}s")
                    time.sleep(current_delay)
                    current_delay *= backoff
            return None

        return wrapper

    return decorator


# --------------------------
# 6. API Utilities
# --------------------------

@retry_api_call(max_retries=3, delay=1.0)
@api_error_handler
def make_api_request(url: str, params: dict, timeout: float = 10.0) -> requests.Response:
    """
    Make an API request with retry and error handling.

    Args:
        url (str): API endpoint URL
        params (dict): Request parameters
        timeout (float): Request timeout in seconds

    Returns:
        requests.Response: API response
    """
    return requests.get(url, params=params, timeout=timeout)


def open_in_browser(url: str):
    """
    Open a URL in the system's default web browser.

    Args:
        url (str): The URL to open
    """
    try:
        webbrowser.open(url)
    except Exception as e:
        log_error(e, "Failed to open URL in browser")


def save_map_html(lat: float, lon: float, businesses: list, api_key: str, filename: str = "static/map.html"):
    """
    Generate and save an HTML file with a map showing business locations.

    Args:
        lat (float): Center point latitude
        lon (float): Center point longitude
        businesses (list): List of Business objects
        api_key (str): Geoapify API Key
        filename (str): Output file path
    """
    try:
        markers = "".join(
            f"markers=lonlat:{b.lon},{b.lat};color:blue;text:{i + 1};size:small&"
            for i, b in enumerate(businesses)
        )

        html_content = f"""<!DOCTYPE html>
        <html>
        <head><title>Business Locations</title></head>
        <body>
            <h2>Business Locations</h2>
            <img src="https://maps.geoapify.com/v1/staticmap?style=osm-carto&width=800&height=600&{markers}center=lonlat:{lon},{lat}&zoom=14&apiKey={api_key}" 
            alt="Business Locations Map" style="width:100%; max-width:800px;">
            <ol>{"".join(f"<li>{b.name} - {b.address}</li>" for b in businesses)}</ol>
        </body>
        </html>"""

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            f.write(html_content)
    except Exception as e:
        log_error(e, "Failed to generate map HTML")


def time_function(func: Callable) -> Callable:
    """
    Decorator to measure and log function execution time.

    Args:
        func (Callable): Function to time

    Returns:
        Callable: Wrapped function with timing
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.debug(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result

    return wrapper