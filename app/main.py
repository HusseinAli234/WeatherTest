from fastapi import FastAPI
from app.core.config import settings
from app.api.auth import router as auth
from app.api.weather import router as weather

app = FastAPI(
    title = settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url =f"{settings.API_V1_STR}/openapi.json"
)


# app.add_middleware(
#     CORS
# )


app.include_router(auth)
app.include_router(weather)



@app.get("/health")
async def health_check():
    return {"status": "healthy","database":"connected"}
