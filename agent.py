import json
from google import genai
from google.cloud import firestore
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from google.cloud.firestore_v1.vector import Vector
from google.adk.agents import LlmAgent
from google.adk.apps import App


def get_railway_information(query: str) -> str:
    """Retrieves relevant Indian railway information from Firestore."""
    try:
        db = firestore.Client(database="coffee-menu")
        client = genai.Client()

        response = client.models.embed_content(
            model="text-embedding-005",
            contents=query,
        )

        query_vector = response.embeddings[0].values

        results = db.collection("menu").find_nearest(
            vector_field="embedding",
            query_vector=Vector(query_vector),
            distance_measure=DistanceMeasure.COSINE,
            limit=5,
        ).stream()

        railway_data = []

        for doc in results:
            item = doc.to_dict()
            item.pop("embedding", None)
            railway_data.append(item)

        return json.dumps(railway_data)

    except Exception as e:
        return json.dumps({
            "error": f"Could not retrieve railway information: {str(e)}"
        })


railsaathi_agent = LlmAgent(
    name="railsaathi_agent",
    model="gemini-3.5-flash",
    instruction="""You are RailSaathi AI, a helpful Indian railway travel assistant.

Your job is to help passengers with railway information such as:
- RAC and waiting list
- Train classes
- PNR and reservation concepts
- Cancellation and refunds
- Luggage
- Passenger safety
- Journey preparation

IMPORTANT RULES:
1. Use only information returned by get_railway_information().
2. Never invent railway rules, train information, prices, schedules or policies.
3. If the available information does not answer the question, clearly say that the information is not available in the knowledge base.
4. Be concise, friendly and professional.
5. For safety-related questions, prioritize safe passenger behavior.
6. Do not claim to provide live train status or live PNR status.
7. For live or official railway information, direct the user to official Indian Railways services.
""",
    tools=[get_railway_information]
)


app = App(
    name="railsaathi_ai_app",
    root_agent=railsaathi_agent
)
