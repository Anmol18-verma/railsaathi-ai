import requests

from firebase_config import FIREBASE_CONFIG


FIREBASE_SIGNUP_URL = (
    "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
)

FIREBASE_LOGIN_URL = (
    "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
)


def signup_user(email, password):
    url = FIREBASE_SIGNUP_URL + "?key=" + FIREBASE_CONFIG["apiKey"]

    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()

        return {
            "uid": result["localId"],
            "email": result["email"],
            "id_token": result["idToken"],
            "refresh_token": result["refreshToken"],
            "expires_in": result["expiresIn"]
        }

    return {
        "error": response.json().get("error", {}).get(
            "message",
            "Signup failed"
        )
    }


def login_user(email, password):
    url = FIREBASE_LOGIN_URL + "?key=" + FIREBASE_CONFIG["apiKey"]

    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()

        return {
            "uid": result["localId"],
            "email": result["email"],
            "id_token": result["idToken"],
            "refresh_token": result["refreshToken"],
            "expires_in": result["expiresIn"]
        }

    return {
        "error": response.json().get("error", {}).get(
            "message",
            "Login failed"
        )
    }
