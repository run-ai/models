import os
from flask import Flask, jsonify
import requests

app = Flask(__name__)
port = int(os.getenv("PORT", 3000))
flask_port = int(os.getenv("READINESS_PORT", "3001"))

@app.route('/ready')
def check_ready():
    try:
        response1 = requests.post(f'http://localhost:{port}/api/models', data="{}", timeout=60)
        response2 = requests.get('http://localhost:8000/v1/models', timeout=60)

        if response1.status_code != 200 or response2.status_code != 200:
            return jsonify({'message': 'Endpoints are not ready'}), 503
        else:
            return jsonify({'message': 'Both endpoints are ready'}), 200
    except Exception as e:
        return jsonify({'message': 'Endpoints are not ready'}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=flask_port)

