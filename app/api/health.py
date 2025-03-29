import shutil
from fastapi import APIRouter, HTTPException, Request

router = APIRouter()

# List of allowed server IPs


@router.get("/health")
async def health_check(request: Request):
    """
    Health check endpoint to ensure ffmpeg is installed and the service is running.
    """
    # Check if the client's IP is in the allowed list
    public_ip = request.client.host

    
    ffmpeg_path = shutil.which("ffmpeg")
    
    if ffmpeg_path is None:
        raise HTTPException(status_code=500, detail="ffmpeg is not installed")
    
    return {"status": "ok"}
