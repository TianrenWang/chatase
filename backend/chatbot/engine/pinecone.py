from .openai import openaiClient
import uuid
import asyncio
import os
import pinecone
from dotenv import load_dotenv
load_dotenv()

USER_NAMESPACE = "user_memories_"

pinecone.init(
    api_key=os.environ['PINECONE_API_KEY'],
    environment=os.environ['PINECONE_ENVIRONMENT'])

index = pinecone.Index(os.environ['PINECONE_INDEX_NAME'])


def getOpenAIEmbedding(text):
    response = openaiClient.embeddings.create(
        input=text, model="text-embedding-ada-002"
    )
    return response.data[0].embedding


def indexMemory(summary: str, keywords: list[str], memory: str, conversationId: str):
    summaryVector = getOpenAIEmbedding(summary)
    namespace = USER_NAMESPACE + conversationId
    vectors = []

    queryResponse = index.query(
        vector=summaryVector,
        top_k=10,
        namespace=namespace,
        include_metadata=True,
        include_values=True
    )

    for summaryMatch in queryResponse["matches"]:
        if summaryMatch["score"] > 0.98:
            return
        elif summaryMatch["score"] > 0.87:
            metadata = summaryMatch["metadata"]
            vectors.append({
                "id": summaryMatch["id"],
                "values": summaryMatch["values"],
                "metadata": {
                    "indexText": metadata["indexText"],
                    "memory": metadata["memory"] + [memory],
                },
            })

    vectors.append({
        "id": str(uuid.uuid4()),
        "values": summaryVector,
        "metadata": {
            "indexText": summary,
            "memory": [memory],
        },
    })

    queryResponses = asyncio.run(
        _batchQuery(keywords, conversationId))
    for response, keyword in zip(queryResponses, keywords):
        vector = response[1]
        matches = response[0]
        hasExactMatch = False
        for match in matches:
            if match["score"] > 0.98:
                hasExactMatch = True
            if match["score"] > 0.95:
                vectors.append({
                    "id": match["id"],
                    "values": match["values"],
                    "metadata": {
                        "indexText": keyword,
                        "memory": match["metadata"]["memory"] + [memory],
                    },
                })

        if not hasExactMatch:
            vectors.append({
                "id": str(uuid.uuid4()),
                "values": vector,
                "metadata": {
                    "indexText": keyword,
                    "memory": [memory],
                },
            })

    index.upsert(vectors, namespace)


def getRelevantMemory(queryTexts: list[str], conversationId: str):
    queryResponses = asyncio.run(_batchQuery(queryTexts, conversationId))
    bestMatch = None
    for response in queryResponses:
        matches = response[0]
        for match in matches:
            if match["score"] > 0.87:
                if not bestMatch or match["score"] > bestMatch["score"]:
                    bestMatch = match
    return "\n".join(bestMatch["metadata"]["memory"]) if bestMatch else None


async def _batchQuery(queryTexts: list[str], conversationId: str):
    tasks = []
    for text in queryTexts:
        tasks.append(asyncio.ensure_future(
            _queryWithOneText(text, conversationId)))

    return await asyncio.gather(*tasks)


async def _queryWithOneText(queryText: str, conversationId: str):
    vector = getOpenAIEmbedding(queryText)
    query_response = index.query(
        vector=vector,
        top_k=10,
        include_metadata=True,
        include_values=True,
        namespace=USER_NAMESPACE + conversationId
    )
    return query_response["matches"], vector


async def getAppropriateBehaviour(emotion):
    vector = getOpenAIEmbedding(emotion)
    query_response = index.query(
        vector=vector, top_k=1, include_metadata=True, namespace="sophia_personality")

    closest_match = None
    matches = query_response["matches"]
    if len(matches) and matches[0]["score"] > 0.85:
        closest_match = matches[0]

    return closest_match["metadata"]["behaviour"] if closest_match else ""
