import os
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token, decode_token

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

with app.app_context():
    token = create_access_token(identity="123", additional_claims={"test_claim": True})
    print("Token created")
    decoded = decode_token(token)
    print("Decoded payload:", decoded)
    print("test_claim exists directly:", "test_claim" in decoded)
