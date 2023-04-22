import os
from flask import Flask
from dotenv import load_dotenv
from src.controller.csv import csv_bp
from src.controller.collection import collection_bp
from flasgger import Swagger
from flask import Flask


load_dotenv()
PORT = int(os.getenv('PORT'))

app = Flask(__name__)

app.register_blueprint(csv_bp, url_prefix='/api')
app.register_blueprint(collection_bp, url_prefix='/api')


# Configure the Flask app
app.config['SWAGGER'] = {
    'title': 'Api CRUD for CSV',
    'uiversion': 3,
    'servers': [
        {'url': 'http://localhost:5050', 'description': 'Local server 01'},
        {'url': 'http://localhost:5051', 'description': 'Local server 02'},
    ],
}


# Create a Swagger instance
swagger = Swagger(app)


@app.route('/health')
@app.route('/')
def health():
    """
    A simple endpoint that returns a ok message.
    ---
    responses:
        200:
            description: ok message
    """
    return 'ok', 200


if __name__ == '__main__':
    app.run(port=PORT, host="0.0.0.0")
