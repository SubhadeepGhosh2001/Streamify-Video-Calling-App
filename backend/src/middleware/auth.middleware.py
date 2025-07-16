import jwt
from flask import request, jsonify, g
from functools import wraps
from models import User  # your SQLAlchemy User model
import os

def protect_route(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('jwt')

        if not token:
            return jsonify({"message": "Unauthorized - No token provided"}), 401

        try:
            decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])

            user = User.query.get(decoded.get("userId"))
            if not user:
                return jsonify({"message": "Unauthorized - User not found"}), 401

            # Attach user object to `g` (Flask’s request context)
            g.user = user

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
        except Exception as e:
            print("Error in protect_route middleware:", str(e))
            return jsonify({"message": "Internal Server Error"}), 500

        return f(*args, **kwargs)

    return decorated_function
