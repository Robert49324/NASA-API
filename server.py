from flask import Flask, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="images",
                        host="database",
                        user="postgres",
                        password="postgres",
                        port="5432")
    
@app.route("/")
def home():
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