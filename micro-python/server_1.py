from flask import Flask
from micro_core.api import api

app = Flask(__name__)
app.register_blueprint(api)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",   # Listen on all interfaces
        port=5001,        # Default port
        debug=True        # Enable auto-reload and error logs
    )
