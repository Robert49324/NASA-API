from minio import Minio
from minio.error import S3Error
import requests
from PIL import Image
import json
import os
import schedule
import time
from minio_serv import client

def main():
    response = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY")
    img = Image.open(requests.get(response.json()["hdurl"], stream = True).raw)
    img.save("temp/" + os.path.basename(response.json()["hdurl"]))

    client.fput_object("bucket", os.path.basename(response.json()["hdurl"]), "" + os.path.basename(response.json()["hdurl"]))
    
    os.remove("temp/" + os.path.basename(response.json()["hdurl"]))


if __name__ == "__main__":
    try:
        desired_time = "23:00"

        schedule.every().day.at(desired_time).do(main)

        while True:
            schedule.run_pending()
            time.sleep(60)
    except S3Error as exc:
        print("Error occurred.", exc)