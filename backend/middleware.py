from functools import wraps
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"message": "Token is missing!"}), 403

        try:
            data = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
            user_id = data["user_id"]
        except:
            return jsonify({"message": "Invalid token!"}), 403

        return f(user_id, *args, **kwargs)

    return decorated
