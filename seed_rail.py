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

railway_data = [
    {
        "name": "RAC",
        "description": "Reservation Against Cancellation (RAC) allows a passenger to travel with a reserved seat, subject to Indian Railways rules. A full berth may become available if another passenger cancels.",
        "tags": ["reservation", "RAC", "ticket"]
    },
    {
        "name": "Waiting List",
        "description": "A waitlisted railway ticket means a confirmed berth or seat has not yet been allotted. Confirmation depends on cancellations and railway reservation rules.",
        "tags": ["reservation", "WL", "ticket"]
    },
    {
        "name": "1A First AC",
        "description": "First AC (1A) is a premium railway class with air-conditioned accommodation and private or shared cabins depending on the train.",
        "tags": ["class", "1A", "AC"]
    },
    {
        "name": "2A Second AC",
        "description": "Second AC (2A) is an air-conditioned sleeping class generally arranged with berths in bays and curtains for privacy.",
        "tags": ["class", "2A", "AC"]
    },
    {
        "name": "3A Third AC",
        "description": "Third AC (3A) is an air-conditioned sleeping class with multiple berths arranged in bays.",
        "tags": ["class", "3A", "AC"]
    },
    {
        "name": "Sleeper Class",
        "description": "Sleeper Class (SL) is a non-air-conditioned sleeping class with reserved berths.",
        "tags": ["class", "SL", "sleeper"]
    },
    {
        "name": "Cancellation and Refund",
        "description": "Railway ticket cancellation and refund amounts depend on ticket type, timing of cancellation, train rules and applicable Indian Railways policies.",
        "tags": ["cancellation", "refund", "ticket"]
    },
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

# Remove old coffee documents
for doc in db.collection("menu").stream():
    doc.reference.delete()

for item in railway_data:
    doc_id = item["name"].lower().replace(" ", "-")

    text = f"{item['name']}: {item['description']}"

    response = client.models.embed_content(
        model="text-embedding-005",
        contents=text
    )

    embedding = response.embeddings[0].values
    item["embedding"] = Vector(embedding)

    db.collection("menu").document(doc_id).set(item)

print("RailSaathi railway knowledge seeded successfully!")
print("Documents:", len(railway_data))
