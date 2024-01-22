import os
from .models import APIKey
from rest_framework_api_key.permissions import BaseHasAPIKey, KeyParser
from rest_framework import authentication, exceptions, permissions
from django.contrib.auth import get_user_model
from dotenv import load_dotenv
load_dotenv()

UserModel = get_user_model()


class BearerKeyParser(KeyParser):
    keyword = "Bearer"


class HasAPIKey(BaseHasAPIKey):
    model = APIKey  # Or a custom model
    key_parser = BearerKeyParser()


class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if not "HTTP_AUTHORIZATION" in request.META:
            raise exceptions.AuthenticationFailed('No API key was provided')
        key = request.META["HTTP_AUTHORIZATION"].split()[1]

        try:
            apiKey = APIKey.objects.get_from_key(key)
        except:
            raise exceptions.AuthenticationFailed(
                'Provided API key is invalid')

        try:
            user = apiKey.user
        except UserModel.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)


class FromPoe(permissions.BasePermission):
    def has_permission(self, request, view):
        if not "HTTP_AUTHORIZATION" in request.META:
            return False

        splitItems = request.META["HTTP_AUTHORIZATION"].split()
        if len(splitItems) < 2 or len(splitItems) > 2:
            return False

        key = splitItems[1]

        if key != os.getenv("POE_ACCESS_KEY"):
            return False
        return True


class PoeAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        user = UserModel.objects.get(email=os.getenv("POE_USER_EMAIL"))
        return (user, None)
