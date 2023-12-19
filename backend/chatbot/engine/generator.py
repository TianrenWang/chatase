from ..models import Conversation, Message, GPTOutput
from .openai import openaiClient, getConversationObjective, getSophiaEmotion, getAntiHackingAction, SOPHIA_PROMPT
from .pinecone import getAppropriateBehaviour
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


def getOpenAIInput(messages: List[ChatCompletionMessageParam], relevant_past_messages: str):
    current_time = datetime.datetime.now().isoformat()
    system_message: ChatCompletionMessageParam = {
        'role': 'system',
        'content': f"{SOPHIA_PROMPT} The following are messages sent in the past that might be relevant:\n{relevant_past_messages if relevant_past_messages else ''}\nIt is currently {current_time}",
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
    userIntention, conversationObjective, objectiveInput = getConversationObjective(
        textMessages)
    antiHackAction, antiHackInput = getAntiHackingAction(userIntention)
    openaiInput = getOpenAIInput(messagesWithContext, None)
    if antiHackAction:
        openaiInput.append({
            "role": "user",
            "content": f"1337: {antiHackAction}",
        })
        return getResponse(openaiInput)

    sophiaEmotion, emotionInput = getSophiaEmotion(messagesWithContext)
    sophiaBehaviour = asyncio.run(getAppropriateBehaviour(sophiaEmotion))

    if sophiaBehaviour:
        openaiInput.append({
            "role": "user",
            "content": f"1337: {sophiaBehaviour}",
        })

    print("Generating final response")
    finalMessage, context = getResponse(openaiInput)

    GPTOutput.objects.create(
        message=messages[len(messages) - 1],
        objectiveInput=objectiveInput,
        objectiveOutput=conversationObjective,
        emotionInput=emotionInput,
        emotionOutput=sophiaEmotion,
        behaviourOutput=sophiaBehaviour,
        gptInput=openaiInput,
        gptOutput=context,
        extractionInput="",
        extractionOutput=finalMessage
    )

    return finalMessage, context
