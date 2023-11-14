from .apikeys.auth import HasAPIKey, APIKeyAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


client = OpenAI()


class Chat(APIView):
    permission_classes = [HasAPIKey]
    authentication_classes = (APIKeyAuthentication,)

    def post(self, request):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "How are you doing son?"}
            ]
        )
        return Response({"message": response.choices[0].message.content}, status=status.HTTP_200_OK)
