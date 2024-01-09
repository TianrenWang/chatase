from .openai import openaiClient
from ..models import Message
import os
import pinecone
from dotenv import load_dotenv
load_dotenv()

pinecone.init(
    api_key=os.environ['PINECONE_API_KEY'],
    environment=os.environ['PINECONE_ENVIRONMENT'])

index = pinecone.Index("sophists")


def getOpenAIEmbedding(text):
    response = openaiClient.embeddings.create(
        input=text, model="text-embedding-ada-002"
    )
    return response.data[0].embedding


"""
We currently do not need to use this function because I haven't
figured out the best way to utilize the indexed memory.
"""


def indexMessage(message: Message):
    conversation = message.conversation
    vector = getOpenAIEmbedding(message.text)
    query_response = index.query(
        vector=vector, top_k=1, namespace=conversation.id)
    if query_response["matches"] and query_response["matches"][0]["score"] > 0.98:
        return

    # Index the message if it isn't a duplicate
    vectors = [
        {
            "id": message.id,
            "values": vector,
            "metadata": {
                "isAIMessage": not message.isHuman,
                "createdAt": message.createdAt,
                "text": message.text,
                "name": message.conversation.name,
                "context": message.context,
            },
        },
    ]
    index.upsert(vectors, conversation.id)


def getMostRelevantVectorsAsString(queryText: str, conversationId: str):
    vector = getOpenAIEmbedding(queryText)
    query_request = {
        "vector": vector,
        "top_k": 5,
        "include_metadata": True,
        "namespace": conversationId,
    }
    query_response = index.query(query_request)
    return '\n'.join(
        f'{match["metadata"]["userId"] != os.environ["SOPHIA_ID"] and "me" or "Sophia"} on {match["metadata"]["createdAt"]}: {match["metadata"]["text"]}'
        if match["score"] > 0.85 else "" for match in query_response["matches"]
    )

# Function to get appropriate behavior based on emotion


async def getAppropriateBehaviour(emotion):
    vector = getOpenAIEmbedding(emotion)
    query_response = index.query(
        vector=vector, top_k=1, include_metadata=True, namespace="sophia_personality")

    closest_match = None
    if query_response["matches"][0]["score"] > 0.85:
        closest_match = query_response["matches"][0]

    return closest_match["metadata"]["behaviour"] if closest_match else ""
