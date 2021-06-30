import base64
from app.models import User
from app.extensions import db
from werkzeug.security import generate_password_hash
from unittest.mock import Mock, patch

def test_register(client):
    data ={
        "email": "samu06.carlos@gmail.com",
        "password": "19735"
    }

    response = client.post("/api/auth/register", data=data)
    result = response.get_json()
    assert result["message"] == "user registered"

@patch("app.resources.auth.create_access_token")
def test_login(create_access_token_mock, client):
    create_access_token_mock.return_value = "oi123"
    user = User(email="samu06.carlos@gmail.com", password=generate_password_hash("19735"))
    db.session.add(user)
    db.session.commit()

    headers = {
        "Authorization": "Basic " + "samu06.carlos@gmail.com:19735"
    }

    response = client.get("/api/auth/login", headers=headers)
    result = response.get_json()
    token = result["access_token"]
    assert token == "oi123"
