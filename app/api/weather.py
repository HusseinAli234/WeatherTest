from fastapi import APIRouter, HTTPException
from app.service.weather_service import get_from_cache,fetch_weather_from_api,normalize_weather,save_to_cache
import httpx
from fastapi import APIRouter, Depends
from app.api.deps import get_current_user 
from app.models.user import User
router = APIRouter()

@router.get("/weather")
async def get_weather(city: str,user: User = Depends(get_current_user)):
    cached = get_from_cache(city)
    if cached:
        return {"source": "cache", "data": cached}

    try:
        raw = await fetch_weather_from_api(city)
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=404, detail="City not found")

    data = normalize_weather(raw)
    save_to_cache(city, data)

    return {"source": "api", "data": data}
