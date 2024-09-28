import bcrypt
import jwt
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId

class AuthService:
    def __init__(self, db):
        self.db = db

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def verify_password(self, password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed)

    def create_user(self, email, password):
        if self.db.users.find_one({"email": email}):
            return {"message": "User already exists"}, 400

        hashed_password = self.hash_password(password)
        user_id = self.db.users.insert_one({
            "email": email,
            "password": hashed_password,
            "createdAt": datetime.now()
        }).inserted_id
        print(email)
        return {"message": "User registered successfully", "user_id": str(user_id)}, 201

    def login_user(self, email, password):
        user = self.db.users.find_one({"email": email})
        if user and self.verify_password(password, user['password']):
            token = jwt.encode({
                "user_id": str(user["_id"]),
                "exp": datetime.utcnow() + timedelta(hours=2)
            }, "your_secret_key", algorithm="HS256")
            print(user)
            return token, user["_id"]
        return None, None