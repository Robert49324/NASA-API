from minio import Minio
from minio.error import S3Error
import requests
from PIL import Image
import json
import os
import schedule
import time
from minio_serv import client
import psycopg2

conn = None

while conn==None:
    try:
        conn = psycopg2.connect(database="images",
                        host="database",
                        user="postgres",
                        password="postgres",
                        port="5432")
    except:
        time.sleep(5)
        
def load():
    with conn.cursor() as cursor:
        cursor.execute('''SELECT EXISTS (
                      SELECT 1
                      FROM information_schema.tables
                      WHERE table_schema = 'public' AND
                            table_type = 'BASE TABLE' AND
                            table_name = 'images'
                    );''')
        if not cursor.fetchone()[0]:
            cursor.execute('''CREATE TABLE images (  
                  id serial PRIMARY KEY,
                  link VARCHAR(255),
                  date DATE DEFAULT current_date
                  );''')
            conn.commit()
    
    response = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY")
    img = Image.open(requests.get(response.json()["hdurl"], stream = True).raw)
    img.save("temp/" + os.path.basename(response.json()["hdurl"]))

    client.fput_object("images", os.path.basename(response.json()["hdurl"]), "temp/" + os.path.basename(response.json()["hdurl"]), content_type="image/jpg")
    
    with conn.cursor() as cursor:
        ins = 'INSERT INTO images (link) VALUES(%s)'
        cursor.execute(ins,("127.0.0.1:9000/images/" + os.path.basename(response.json()["hdurl"]),))
        conn.commit()
        
    os.remove("temp/" + os.path.basename(response.json()["hdurl"]))

if __name__ == "__main__":
    try:
        desired_time = "23:00"

        schedule.every().day.at(desired_time).do(load)

        while True:
            schedule.run_pending()
            time.sleep(1)
    except S3Error as exc:
        print("Error occurred.", exc)