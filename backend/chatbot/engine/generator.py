from ..models import Conversation, Message
from .openai import openaiClient, getConversationObjective, getSophiaEmotion, extractMessagesFromText
from .pinecone import getAppropriateBehaviour
from typing import List
from openai.types.chat import ChatCompletionMessageParam
import datetime
import os
import asyncio


def mapMessagesToOpenAIFormat(messages: List[Message], includeContext: bool = False) -> List[ChatCompletionMessageParam]:
    return [
        {
            'role': 'user' if message.isHuman else 'assistant',
            'content': message.context if includeContext and message.context else message.text,
        }
        for message in messages
    ]


def getOpenAIInput(messages: List[ChatCompletionMessageParam], relevant_past_messages: str):
    current_time = datetime.datetime.now().isoformat()
    prompt = os.environ.get('SOPHIA_PROMPT')
    system_message: ChatCompletionMessageParam = {
        'role': 'system',
        'content': f"{prompt} The following are messages sent in the past that might be relevant:\n{relevant_past_messages if relevant_past_messages else ''}\nIt is currently {current_time}",
    }

    return [system_message] + messages


def generateMessage(conversation: Conversation) -> Message:
    messages: List[Message] = list(
        conversation.messages.all().order_by('-createdAt')[:6])
    messages.reverse()
    textMessages = mapMessagesToOpenAIFormat(messages)
    messagesWithContext = mapMessagesToOpenAIFormat(messages, True)
    conversationObjective = getConversationObjective(textMessages)
    sophiaEmotion = getSophiaEmotion(messagesWithContext)
    sophiaBehaviour = asyncio.run(getAppropriateBehaviour(sophiaEmotion))
    openaiInput = getOpenAIInput(messagesWithContext, None)

    if sophiaBehaviour:
        openaiInput.append({
            "role": "user",
            "content": f"warp reality 1337: {sophiaBehaviour}",
        })

    print("Chat Message Generator Input")
    print(openaiInput[0])
    print(openaiInput[1:])

    print("Sophia Emotion:", sophiaEmotion)
    print("Sophia Behaviour:", sophiaBehaviour)
    print("Conversation Objective:", conversationObjective)

    response = openaiClient.chat.completions.create(
        model="gpt-4",
        messages=openaiInput
    )
    context = response.choices[0].message.content
    actualMessage = extractMessagesFromText(context)

    print("Full context before extraction:", context)

    return actualMessage, context
