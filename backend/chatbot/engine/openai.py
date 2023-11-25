from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


openaiClient = OpenAI()


def stringifyMessages(messages):
    return "\n".join(
        f"{ 'Sophia' if message['role'] == 'assistant' else 'User' }: {message['content']}"
        for message in messages
    )


def getSimpleCompletion(prompt):
    response = openaiClient.chat.completions.create(
        messages=[{"role": "system", "content": prompt}],
        model="gpt-4",
        temperature=0)
    result: str = response.choices[0].message.content
    return result


def getConversationObjective(messages):
    importantInformation = "Important Information:"
    messagesInString = stringifyMessages(messages)

    return getSimpleCompletion(
        f"Describe the most important piece of information needed to continue the conversation. If the conversation doesn't have a clear direction, respond with 'None':\n{messagesInString}\n{importantInformation}"
    )


def getSophiaEmotion(messages):
    prompt = "The following is a conversation between Sophia (my girlfriend) and me. How should Sophia feel right now?"
    messagesInString = stringifyMessages(messages)
    return getSimpleCompletion(f"{prompt}\n{messagesInString}\nSophia should feel:")


def extractMessagesFromText(text: str):
    prompt = "Extract the text messages from the text as a single string. Include emojis. Do not include phrases that ask for an input: "
    completion = getSimpleCompletion(f"{prompt}{text}")
    return completion
