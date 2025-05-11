from sqlalchemy.orm import Session
from app.models import rider as rider_models
from app.schemas.rider import RiderCreate, Location, RiderOut
from geopy.distance import geodesic
from sqlalchemy import func
import math
from app.models import order as order_models
from app.schemas import rider as rider_schemas
from geopy.geocoders import Nominatim

EARTH_RADIUS_KM = 6371.0 


from geopy.geocoders import Nominatim

def get_coordinates_from_address(address: str):
    geolocator = Nominatim(user_agent="food-delivery-app")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        raise ValueError("Could not geocode the address")


def create_rider(db: Session, rider: RiderCreate) -> RiderOut:
    geolocator = Nominatim(user_agent="rider_registration")
    location = geolocator.geocode(rider.location)

    if location is None:
        raise ValueError("Could not geocode the address provided.")

    db_rider = rider_models.Rider(
        name=rider.name,
        email=rider.email,
        password=rider.password,
        current_latitude=location.latitude,
        current_longitude=location.longitude,
        is_available=rider.availability,
        current_load=0,
        stars=5.0
    )

    db.add(db_rider)
    db.commit()
    db.refresh(db_rider)

    return RiderOut(
        id=db_rider.id,
        name=db_rider.name,
        stars=db_rider.stars,
        availability=db_rider.is_available,
        location=Location(
            latitude=db_rider.current_latitude,
            longitude=db_rider.current_longitude
        )
    )

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return EARTH_RADIUS_KM * c


def get_nearest_rider(db: Session, location: Location, max_distance_km: float = 0.5):
    lat_min = location.latitude - (max_distance_km / EARTH_RADIUS_KM) * (180 / math.pi)
    lat_max = location.latitude + (max_distance_km / EARTH_RADIUS_KM) * (180 / math.pi)
    lon_min = location.longitude - (max_distance_km / EARTH_RADIUS_KM) * (180 / math.pi) / math.cos(math.radians(location.latitude))
    lon_max = location.longitude + (max_distance_km / EARTH_RADIUS_KM) * (180 / math.pi) / math.cos(math.radians(location.latitude))

    available_riders = db.query(rider_models.Rider).filter(
        rider_models.Rider.is_available == True,
        rider_models.Rider.current_latitude >= lat_min,
        rider_models.Rider.current_latitude <= lat_max,
        rider_models.Rider.current_longitude >= lon_min,
        rider_models.Rider.current_longitude <= lon_max
    ).all()

    if not available_riders:
        return None

    nearest_rider = None
    min_distance = float('inf')

    user_location = (location.latitude, location.longitude)

    for rider in available_riders:
        rider_location = (rider.current_latitude, rider.current_longitude)
        distance = geodesic(user_location, rider_location).km

        if distance < min_distance:
            min_distance = distance
            nearest_rider = rider

    return nearest_rider


def get_rider_by_id(db: Session, rider_id: int):
    return db.query(rider_models.Rider).filter(rider_models.Rider.id == rider_id).first()


def update_availability(db: Session, rider_id: int, is_available: bool):
    rider = db.query(rider_models.Rider).filter(rider_models.Rider.id == rider_id).first()
    if rider:
        rider.is_available = is_available
        db.commit()
        db.refresh(rider)
    return rider


def get_available_riders(db: Session):
    return db.query(rider_models.Rider).filter(rider_models.Rider.is_available == True).all()

def assign_rider_to_order(db: Session, order_id: int, location: rider_schemas.Location):
    rider = get_nearest_rider(db, location)
    
    if rider:
        order = db.query(order_models.Order).filter(order_models.Order.id == order_id).first()
        
        if not order:
            return None  

        order.rider_id = rider.id
        
        rider.is_available = False

        db.commit()
        db.refresh(order)
        db.refresh(rider)
        
        return order 

    else:
        return None 