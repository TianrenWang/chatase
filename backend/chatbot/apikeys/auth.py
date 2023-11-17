from .models import APIKey
from rest_framework_api_key.permissions import BaseHasAPIKey, KeyParser
from rest_framework import authentication, exceptions
from django.contrib.auth import get_user_model

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
