import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv(override=True)

app = FastAPI()

# Read allowed IPs from .env
ALLOWED_IPV4 = set(os.getenv("ALLOWED_IPV4", "").split(","))
ALLOWED_IPV6 = set(os.getenv("ALLOWED_IPV6", "").split(","))

# Create logs folder if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Set up logging with both console and file logging
log_file = "logs/app.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Console logging
        logging.FileHandler(log_file, mode="a")  # File logging (appends to file)
    ]
)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def restrict_to_public_ip(request: Request, call_next):
    client_ip = request.headers.get("X-Forwarded-For", request.client.host)

    # Allow if the IP is in either the IPv4 or IPv6 allowed lists
    if client_ip not in ALLOWED_IPV4 and client_ip not in ALLOWED_IPV6:

        # Log the rejected request
        logger.info(f"Request from {client_ip} denied access")

        return JSONResponse(status_code=403, content={"detail": "Access denied"})

    response = await call_next(request)
    return response

from app.api import health, youtube
app.include_router(health.router)
app.include_router(youtube.router)
