import os
import boto3
from botocore.client import Config
import logging
from dotenv import load_dotenv

# Enable boto3 debugging logs
logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env file
load_dotenv()

def upload_file_to_bucket(file_path: str, subfolder: str) -> str:
    try:
        # Fetch environment variables from .env
        access_key = os.getenv("HETZNER_ACCESS_KEY_ID")
        secret_key = os.getenv("HETZNER_SECRET_ACCESS_KEY")
        region = os.getenv("HETZNER_DEFAULT_REGION")
        bucket_name = os.getenv("HETZNER_BUCKET")
        endpoint_url = os.getenv("HETZNER_ENDPOINT")
        
        # Ensure that the required environment variables are set
        if not access_key or not secret_key or not bucket_name or not endpoint_url:
            raise ValueError("Missing environment variables. Please check your .env file.")

        # Initialize the S3 client for Hetzner's Object Storage
        s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
            config=Config(
                signature_version='s3v4',  # Ensure S3v4 signature is used
                retries={'max_attempts': 5, 'mode': 'standard'},
                s3={'addressing_style': 'virtual'}  # Virtual addressing style
            )
        )

        # Ensure subfolder is properly formatted with a trailing slash
        if subfolder and not subfolder.endswith('/'):
            subfolder += '/'

        object_name = subfolder + os.path.basename(file_path)  # Combine subfolder and file name

        # Validate inputs
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        if not bucket_name:
            raise ValueError("Bucket name is missing. Please check your environment variables.")

        # Upload the file to the specified S3 bucket
        with open(file_path, "rb") as file_data:
            s3_client.upload_fileobj(file_data, bucket_name, object_name)

        #delete the local file after upload
        os.remove(file_path)
        
        # Generate a public URL for the uploaded file
        return f"{endpoint_url}/{bucket_name}/{object_name}"
    
    except Exception as e:
        # Log the full traceback for debugging
        import traceback
        traceback.print_exc()
        # Raise a detailed error message if upload fails
        raise ValueError(f"S3 upload failed: {str(e)}. Please verify your credentials, endpoint URL, and bucket name.")
