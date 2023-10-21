from flask import Flask, request, redirect
import psycopg2
import time

app = Flask(__name__)

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
    
@app.route("/")
def home():
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
    date = request.args.get('date')
    with conn.cursor() as cursor:
        select ="SELECT link FROM images WHERE date=%s"
        cursor.execute(select,(date,))
        result = cursor.fetchone()
        if result:
            link = result[0]
            if not link.startswith('http://') and not link.startswith('https://'):
                link = 'http://' + link
            return redirect(link)
        else:
            return "URL не найден"
            
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)