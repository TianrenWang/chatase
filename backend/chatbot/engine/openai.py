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
    input = f"Describe the most important piece of information needed to continue the conversation. If the conversation doesn't have a clear direction, respond with 'None':\n{messagesInString}\n{importantInformation}"

    return getSimpleCompletion(input), input


def getSophiaEmotion(messages):
    prompt = "The following is a conversation between Sophia (my girlfriend) and me. How should Sophia feel right now?"
    messagesInString = stringifyMessages(messages)
    input = f"{prompt}\n{messagesInString}\nSophia should feel:"
    return getSimpleCompletion(input), input


def extractMessagesFromText(text: str):
    prompt = "Extract the text messages from the text as a single string. Include emojis. Do not include phrases that ask for an input: "
    input = f"{prompt}{text}"
    completion = getSimpleCompletion(input)
    if completion[0] == "\"":
        completion = completion[1:]
    if completion[len(completion) - 1] == "\"":
        completion = completion[:-1]
    return completion, input
