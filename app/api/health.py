from fastapi import APIRouter, Request
from app.utils.health_check import check_required_tools

router = APIRouter()

@router.get("/health")
async def health_check(request: Request):
    """
    Health check endpoint to ensure ffmpeg is installed and the service is running.
    """
    # Check if ffmpeg is installed
    check_required_tools(["ffmpeg", 'yt-dlp'])

    return {"status": "healthy"}
