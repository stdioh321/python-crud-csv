import os
from flask import Flask
from dotenv import load_dotenv
from src.controller.csv import csv_bp
from src.controller.collection import collection_bp

load_dotenv()
PORT = int(os.getenv('PORT'))

app = Flask(__name__)

app.register_blueprint(csv_bp, url_prefix='/api')
app.register_blueprint(collection_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(port=PORT, host="0.0.0.0")
