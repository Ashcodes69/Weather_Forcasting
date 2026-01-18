import requests

# Get cordinates of the location like latitude, longitude
def get_geocoding(name):
    if not name:
        return None
    try:
        res = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": name,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=7
        )

    except requests.exceptions.RequestException:
        return None
    
    if res.status_code != 200:
        return None
    
    data = res.json()

    if "results" not in data or len(data["results"]) == 0:
        return None

    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]

    if latitude is None or longitude is None:
        return None
    
    return latitude, longitude
    
# Get the weather updates json
def weather_forcast(name):
    latitude, longitude = get_geocoding(name)
    if latitude is None or longitude is None:
        return None
    try:
        res = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "hourly": "temperature_2m,rain,precipitation_probability,wind_speed_10m,weather_code",
                "current_weather": "true",
                "timezone": "auto"
            },
            timeout = 7
        )
    except requests.exceptions.RequestException:
        return None
    
    if res.status_code != 200:
        return None
    
    data = res.json()
    return data

weather_forcast("Ranchi")
