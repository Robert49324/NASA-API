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

conn = psycopg2.connect(database="images",
                        host="localhost",
                        user="postgres",
                        password="postgres",
                        port="5433")

def load():
    with conn.cursor() as cursor:
        cursor.execute('''SELECT EXISTS (
                          SELECT FROM 
                            information_schema.tables 
                          WHERE 
                            table_schema LIKE 'public' AND 
                            table_type LIKE 'BASE TABLE' AND
                            table_name = 'actor'
                          );''')
        if cursor.fetchall()[0] == False:
            cursor.execute('''CREATE TABLE images(  
                      id serial PRIMARY KEY,
                      link VARCHAR(255),
                      data DATE DEFAULT current_date
                      );''')
            conn.commit()
    
    response = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY")
    img = Image.open(requests.get(response.json()["hdurl"], stream = True).raw)
    img.save("temp/" + os.path.basename(response.json()["hdurl"]))

    client.fput_object("images", os.path.basename(response.json()["hdurl"]), "temp/" + os.path.basename(response.json()["hdurl"]))
    
    with conn.cursor() as cursor:
        ins = 'INSERT INTO images (link) VALUES(%s)'
        cursor.execute(ins,("images/" + os.path.basename(response.json()["hdurl"]),))
        conn.commit()
        
    os.remove("temp/" + os.path.basename(response.json()["hdurl"]))

if __name__ == "__main__":
    try:
        desired_time = "11:49"

        schedule.every().day.at(desired_time).do(load)

        while True:
            schedule.run_pending()
            time.sleep(1)
    except S3Error as exc:
        print("Error occurred.", exc)