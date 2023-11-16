from .apikeys.auth import HasAPIKey, APIKeyAuthentication
from .apikeys.models import APIKey as APIKeyModel
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


client = OpenAI()


class APIKey(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        api_key, key = APIKeyModel.objects.create_key(user=request.user)
        return Response({"key": key}, status=status.HTTP_200_OK)


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
