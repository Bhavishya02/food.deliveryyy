from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def geocode_location(location: str):
    geolocator = Nominatim(user_agent="my_app")
    try:
        location_result = geolocator.geocode(location)
        if location_result:
            return location_result.latitude, location_result.longitude
        else:
            raise ValueError(f"Location '{location}' not found. Please try a valid location.")
    except GeocoderTimedOut:
        raise ValueError("Geocoding service timed out. Please try again.")
