from fastapi import FastAPI
from app.api import health, youtube

app = FastAPI()



# Include the health check routes
app.include_router(health.router)

# Include the YouTube-to-MP3 conversion routes
app.include_router(youtube.router)