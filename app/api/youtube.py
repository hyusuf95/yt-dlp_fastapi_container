from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.services.youtube_service import download_video
from app.services.s3_service import upload_file_to_bucket

router = APIRouter()

# List of allowed server IPs
ALLOWED_SERVER_IPS = ["192.168.1.100", "192.168.1.101"]

# Input Model for YouTube Video URL
class VideoRequest(BaseModel):
    url: str
    subfolder: str = "uploads"

# Endpoint to download and convert YouTube video to MP3
@router.post("/convert")
async def convert_video(request: Request, video_request: VideoRequest):
    """
    Converts a YouTube video to MP3 format and uploads it to an S3-compatible storage service.
    """
    # Check if the client's IP is in the allowed list
    client_ip = request.client.host
    if client_ip not in ALLOWED_SERVER_IPS:
        raise HTTPException(status_code=403, detail="Forbidden: Access is restricted to specific servers.")

    try:
        # Step 1: Download the YouTube video and convert it to MP3
        mp3_file_path = await download_video(video_request.url)  # Calls the async download function

        # Step 2: Upload the MP3 file to S3 (or another cloud storage service)
        s3_url = upload_file_to_bucket(mp3_file_path, video_request.subfolder)  # Uploads the file and retrieves the public URL
        
        # Step 3: Return success response with file details
        return {
            "status": "success",
            "message": "Video successfully converted and uploaded",
            "file_path": mp3_file_path,
            "s3_url": s3_url  # Public URL of the uploaded MP3 file
        }

    except Exception as e:
        # Handle any errors during the process and raise an HTTP 500 error
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")
