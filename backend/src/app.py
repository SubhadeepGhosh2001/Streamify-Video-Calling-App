from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.chat_routes import chat_bp
import os
from lib.db import connect_db

# Load environment variables
load_dotenv()
PORT = int(os.getenv("PORT", 5000))
NODE_ENV = os.getenv("NODE_ENV", "development")

app = Flask(__name__, static_folder="../frontend/dist", static_url_path="")
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

# Register blueprints (modular routes)
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(user_bp, url_prefix="/api/users")
app.register_blueprint(chat_bp, url_prefix="/api/chat")

# Connect to DB
connect_db()

# Serve frontend in production
if NODE_ENV == "production":
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, "index.html")

# Start server
if __name__ == "__main__":
    app.run(port=PORT, debug=(NODE_ENV == "development"))
