from pydantic import BaseModel

class YouTubeRequest(BaseModel):
    url: str  # The YouTube URL to download

class YouTubeResponse(BaseModel):
    mp3_url: str  # The URL of the uploaded MP3 file
