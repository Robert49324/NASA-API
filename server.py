from flask import Flask

app = Flask(__name__)
app.secret_key = "fregcewrg"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)