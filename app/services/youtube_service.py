import os
import tempfile
import shutil
from yt_dlp import YoutubeDL

async def download_video(url: str) -> str:
    # Create a temporary directory to store the downloaded files
    temp_dir = tempfile.mkdtemp()

    try:
        # Configure yt-dlp options to download audio only and save as MP3
        ydl_opts = {
            'format': 'bestaudio/best',  # Best audio quality available
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
            'outtmpl': os.path.join(temp_dir, '%(id)s.%(ext)s'),  # Use video ID as the filename
            'noplaylist': True,  # Ensure only the single video is downloaded
        }

        # Download and process the video/audio
        with YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=True)
                
                # Validate the extracted info
                if not info:
                    raise ValueError("Failed to extract video information. Please check the URL.")  # Raise error for invalid info
                
                # Prepare the filename and ensure it exists
                filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')

                if not os.path.exists(filename):
                    raise FileNotFoundError(f"Downloaded file not found: {filename}")
                
                return filename
            
            except Exception as e:
                # Log the error and clean up the temporary directory
                print(f"Error during video download: {str(e)}")
                shutil.rmtree(temp_dir, ignore_errors=True)
                raise ValueError(f"Video download failed: {str(e)}")  # Provide a clear error message

    except Exception as e:
        # Clean up the temporary directory if something goes wrong
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise ValueError(f"Error downloading video: {str(e)}")  # Avoid treating exceptions as subscriptable objects [[7]]