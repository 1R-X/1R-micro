from flask import Flask
from micro_core.api import api
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(api)

# Configure CORS to allow requests from your React frontend
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


from flask import make_response

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/objects', methods=['OPTIONS'])
def options():
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",   # Listen on all interfaces
        port=2691,        # Default port
        debug=True        # Enable auto-reload and error logs
    )
