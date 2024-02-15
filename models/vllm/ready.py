from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/ready')
def check_ready():
    try:
        response1 = requests.post('http://localhost:3000/api/models', data="{}", timeout=60)
        response2 = requests.get('http://localhost:8000/v1/models', timeout=60)

        if response1.status_code == 200 and response2.status_code == 200:
            return jsonify({'message': 'Both endpoints are ready'}), 200
    except:
        pass
    return jsonify({'message': 'Endpoints are not ready'}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0')

