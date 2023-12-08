from django.urls import path
from . import views

urlpatterns = [
    path('chat', views.Chat.as_view(), name='chat'),
    path('apikey', views.APIKey.as_view(), name='apikey'),
    path('test_chat', views.TestChat.as_view()),
]
