from fastapi import UploadFile, HTTPException
import boto3
from botocore.client import Config

from app.config.settings import storage_settings

s3 = boto3.client(
    's3',
    endpoint_url=storage_settings.ENDPOINT_URL,
    region_name=storage_settings.REGION_NAME,
    aws_access_key_id=storage_settings.KEY_ID,
    aws_secret_access_key=storage_settings.SECRET_KEY,
    config=Config(s3={'addressing_style': 'path'})
)


async def upload_file(file: UploadFile, filename: str):
    s3.upload_fileobj(file.file, storage_settings.BUCKET_NAME, filename)


async def read_file(filename: str):
    return s3.get_object(Bucket=storage_settings.BUCKET_NAME, Key=filename).get('Body')


async def remove_file(filename: str):
    try:
        s3.delete_object(Bucket=storage_settings.BUCKET_NAME, Key=filename)
    except Exception as err:
        raise HTTPException(status_code=400, detail="BUCKET_ERROR")
