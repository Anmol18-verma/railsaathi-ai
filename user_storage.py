import requests

PROJECT_ID = "railsaathi-ai"
DATABASE_ID = "coffee-menu"

def save_chat(uid, id_token, user_message, assistant_message):
    url = (
        f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}"
        f"/databases/{DATABASE_ID}/documents/users/{uid}/chats"
    )

    data = {
        "fields": {
            "user_message": {"stringValue": user_message},
            "assistant_message": {"stringValue": assistant_message}
        }
    }

    requests.post(
        url,
        json=data,
        headers={"Authorization": f"Bearer {id_token}"}
    )


def get_chat_history(uid, id_token):
    url = (
        f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}"
        f"/databases/{DATABASE_ID}/documents/users/{uid}/chats"
    )

    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {id_token}"}
    )

    if response.status_code != 200:
        return []

    documents = response.json().get("documents", [])

    history = []

    for document in documents:
        fields = document.get("fields", {})

        history.append({
            "user_message": fields.get("user_message", {}).get("stringValue", ""),
            "assistant_message": fields.get("assistant_message", {}).get("stringValue", "")
        })

    return history
