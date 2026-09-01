# seed.py
import json
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

with open("menu.json", "r") as f:
    menu_items = json.load(f)

for item in menu_items:
    # Use the item name as the document ID
    doc_id = item["name"].lower().replace(" ", "-")

    # Create text for the embedding
    text_to_embed = f"{item['name']}: {item['description']}"

    response = client.models.embed_content(
        model="text-embedding-005",
        contents=text_to_embed,
    )

    embedding = response.embeddings[0].values

    # Add embedding to the Firestore document
    item["embedding"] = Vector(embedding)

    db.collection("menu").document(doc_id).set(item)

print("Firestore menu collection seeded with vector embeddings successfully!")
