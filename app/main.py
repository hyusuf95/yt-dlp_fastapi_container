import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)


app = FastAPI()

# Read allowed IPs from .env
ALLOWED_IPV4 = set(os.getenv("ALLOWED_IPV4", "").split(","))
ALLOWED_IPV6 = set(os.getenv("ALLOWED_IPV6", "").split(","))




@app.middleware("http")
async def restrict_to_public_ip(request: Request, call_next):
    print(f"Allowed IPv4: {ALLOWED_IPV4}")
    print(f"Allowed IPv6: {ALLOWED_IPV6}")
    client_ip = request.headers.get("X-Forwarded-For", request.client.host)

    # Allow if the IP is in either the IPv4 or IPv6 allowed lists
    if client_ip not in ALLOWED_IPV4 and client_ip not in ALLOWED_IPV6:
        return JSONResponse(status_code=403, content={"detail": "Access denied"})

    response = await call_next(request)
    return response


from app.api import health, youtube
app.include_router(health.router)
app.include_router(youtube.router)