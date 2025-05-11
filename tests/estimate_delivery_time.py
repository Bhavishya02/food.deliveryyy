def estimate_delivery_time(distance_km: float, avg_speed_kmph: float = 30.0) -> int:
  
    if avg_speed_kmph == 0:
        return 9999  
    return int((distance_km / avg_speed_kmph) * 60)
