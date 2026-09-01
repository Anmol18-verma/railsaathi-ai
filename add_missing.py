import os
from google import genai
from google.cloud import firestore
from google.cloud.firestore_v1.vector import Vector

db = firestore.Client(database="coffee-menu")
client = genai.Client(
    vertexai=True,
    project=os.environ.get("PROJECT_ID"),
    location=os.environ.get("REGION", "us-central1")
)

items = [
    {
        "name": "PNR",
        "description": "A PNR is the Passenger Name Record number associated with a railway booking. It can be used to check reservation and journey status through official railway services.",
        "tags": ["PNR", "reservation", "status"]
    },
    {
        "name": "Luggage",
        "description": "Passengers should follow applicable Indian Railways luggage and baggage rules. Permitted luggage limits can vary by travel class and railway regulations.",
        "tags": ["luggage", "baggage", "travel"]
    },
    {
        "name": "Passenger Safety",
        "description": "Passengers should keep valuables secure, avoid boarding or getting down from a moving train, follow railway staff instructions and use official railway channels for emergencies or assistance.",
        "tags": ["safety", "passenger", "emergency"]
    }
]

for item in items:
    text = f"{item['name']}: {item['description']}"

    response = client.models.embed_content(
        model="text-embedding-005",
        contents=text
    )

    item["embedding"] = Vector(response.embeddings[0].values)

    doc_id = item["name"].lower().replace(" ", "-")
    db.collection("menu").document(doc_id).set(item)

print("Added missing Railway knowledge successfully!")
