from google.cloud import firestore


db = firestore.Client(database="coffee-menu")


def save_chat(uid, user_message, assistant_message):

    chat_ref = (
        db.collection("users")
        .document(uid)
        .collection("chats")
        .document()
    )

    chat_ref.set({
        "user_message": user_message,
        "assistant_message": assistant_message,
        "created_at": firestore.SERVER_TIMESTAMP
    })


def get_chat_history(uid):

    chats = (
        db.collection("users")
        .document(uid)
        .collection("chats")
        .order_by("created_at")
        .stream()
    )

    history = []

    for chat in chats:
        history.append(chat.to_dict())

    return history
