from .auth.auth import HasAPIKey, APIKeyAuthentication, FromPoe, PoeAuthentication
from .auth.models import APIKey as APIKeyModel
from .models import Conversation, Message
from .engine.generator import generateMessage
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from django.core.exceptions import ValidationError


class APIKey(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        api_key, key = APIKeyModel.objects.create_key(
            user=request.user, name="Just a key")
        return Response({"key": key}, status=status.HTTP_200_OK)


class Chat(APIView):
    permission_classes = [HasAPIKey]
    authentication_classes = (APIKeyAuthentication,)

    def get(self, request):
        if not "conversationId" in request.query_params:
            return Response({"message": "You must include 'conversationId' in request query."}, status=status.HTTP_400_BAD_REQUEST)

        conversationId = request.query_params["conversationId"]

        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        try:
            user = APIKeyModel.objects.get_from_key(key).user
            conversation = Conversation.objects.get(
                pk=conversationId, user=user)
            Message.objects.create(
                text=request.data["text"], context="", conversation=conversation, isHuman=True)

            actualMessage, context = generateMessage(conversation)
            Message.objects.create(
                text=actualMessage, context=context, conversation=conversation)
        except Conversation.DoesNotExist:
            return Response(
                {"message": f"Conversation with ID {conversationId} does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError:
            return Response(
                {"message": f"Conversation ID {conversationId} is malformed"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"message": f"Sorry, something wrong happened in the server. Please let Frank know about this. {str(e)}."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response({"message": actualMessage}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            if not "username" in request.data:
                return Response({"message": "You must provide the 'username' field in the body."}, status=status.HTTP_400_BAD_REQUEST)
            key = request.META["HTTP_AUTHORIZATION"].split()[1]
            user = APIKeyModel.objects.get_from_key(key).user
            conversation = Conversation.objects.create(
                name=request.data["username"], user=user)

            conversation.save()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"conversationId": conversation.id}, status=status.HTTP_200_OK)


class TestChat(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        try:
            if not "conversationId" in request.query_params:
                conversation = Conversation.objects.create(
                    name="_test_channel", user=request.user)
            else:
                conversation = Conversation.objects.get(
                    pk=request.query_params["conversationId"], user=request.user)
            Message.objects.create(
                text=request.data["text"], context="", conversation=conversation, isHuman=True)

            actualMessage, context = generateMessage(conversation)
            Message.objects.create(
                text=actualMessage, context=context, conversation=conversation)
        except Exception as e:
            return Response(
                {"message": f"Sorry, something wrong happened in the server. Please let Frank know about this. {str(e)}."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response({"message": actualMessage, "conversationId": conversation.id}, status=status.HTTP_200_OK)


class PoeChat(APIView):
    permission_classes = (FromPoe,)
    authentication_classes = (PoeAuthentication,)

    def post(self, request):
        print("*******************")
        print(request.data)
        print(request.META)
        return Response({"text": "conversationId"}, status=status.HTTP_200_OK)
