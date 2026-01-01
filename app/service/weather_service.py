import httpx
from app.core.config import settings
from datetime import datetime, timedelta

async def fetch_weather_from_api(city: str) -> dict:
    params = {
        "q": city,
        "appid": settings.OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "ru",
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(settings.OPENWEATHER_URL, params=params)

    response.raise_for_status()
    return response.json()

def normalize_weather(data: dict) -> dict:
    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
    }



CACHE_TTL = timedelta(minutes=10)
cache = {}

def get_from_cache(city: str):
    entry = cache.get(city.lower())
    if not entry:
        return None
    if entry["expires_at"] < datetime.utcnow():
        del cache[city.lower()]
        return None
    return entry["data"]


def save_to_cache(city: str, data: dict):
    cache[city.lower()] = {
        "data": data,
        "expires_at": datetime.utcnow() + CACHE_TTL
    }
