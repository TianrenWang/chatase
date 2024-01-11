from ..models import Conversation, Message, GPTOutput
from .openai import openaiClient, getConvoProperties, getSophiaEmotion, getAntiHackingAction, SOPHIA_PROMPT
from .pinecone import getAppropriateBehaviour, getRelevantMemory, indexMemory
from typing import List
from openai.types.chat import ChatCompletionMessageParam
import datetime
import asyncio


def mapMessagesToOpenAIFormat(messages: List[Message], includeContext: bool = False) -> List[ChatCompletionMessageParam]:
    return [
        {
            'role': 'user' if message.isHuman else 'assistant',
            'content': message.context if includeContext and message.context else message.text,
        }
        for message in messages
    ]


def getOpenAIInput(messages: List[ChatCompletionMessageParam], memory: str):
    current_time = datetime.datetime.now().isoformat()
    system_message: ChatCompletionMessageParam = {
        'role': 'system',
        'content': f"{SOPHIA_PROMPT}" + f" The following is memory of a past conversation that may be useful:\n{memory}" if memory else "",
    }

    return [system_message] + messages


def getMessageFromText(text):
    start = -1
    result = ""
    for i in range(len(text)):
        if text[i] == '"':
            if start < 0:
                start = i
            else:
                if result == "":
                    result = text[start + 1:i]
                else:
                    result += " " + text[start + 1:i]
                start = -1
    return result


def getResponse(openaiInput):
    response = openaiClient.chat.completions.create(
        model="gpt-4",
        messages=openaiInput
    )
    context = response.choices[0].message.content
    finalMessage = getMessageFromText(context)
    return finalMessage, context


def generateMessage(conversation: Conversation) -> Message:
    print("Constructing Response")
    messages: List[Message] = list(
        conversation.messages.all().order_by('-createdAt')[:6])
    messages.reverse()
    textMessages = mapMessagesToOpenAIFormat(messages)
    messagesWithContext = mapMessagesToOpenAIFormat(messages, True)
    convoProperties, objectiveInput = getConvoProperties(
        textMessages)
    antiHackAction, antiHackInput = getAntiHackingAction(
        convoProperties['intention'])
    openaiInput = getOpenAIInput(messagesWithContext, None)
    if antiHackAction:
        openaiInput.append({
            "role": "user",
            "content": f"1337: {antiHackAction}",
        })
        return getResponse(openaiInput)

    topics = [convoProperties["important_information"]] + \
        convoProperties["topics"]
    memory = getRelevantMemory(topics, str(conversation.id))
    sophiaEmotion, emotionInput = getSophiaEmotion(messagesWithContext)
    sophiaBehaviour = asyncio.run(getAppropriateBehaviour(sophiaEmotion))
    openaiInput = getOpenAIInput(messagesWithContext, memory)

    if sophiaBehaviour:
        openaiInput.append({
            "role": "user",
            "content": f"1337: {sophiaBehaviour} Sophia does not know about the game.",
        })

    print("Generating final response")
    finalMessage, context = getResponse(openaiInput)

    memory = convoProperties["fact"]

    print("*******Indexing Memory*********")
    print(convoProperties)
    if memory:
        indexMemory(convoProperties["important_information"],
                    convoProperties["topics"], memory, str(conversation.id))
    else:
        print("No worthwhile memory to index")

    return finalMessage, context
