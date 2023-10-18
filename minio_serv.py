from minio import Minio
from minio.error import S3Error
import requests
from PIL import Image
import json
import os

client = Minio(
        "localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
)

found = client.bucket_exists("images")
if not found:
    client.make_bucket("images")
    
    