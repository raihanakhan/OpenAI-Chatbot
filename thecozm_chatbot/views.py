import openai
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView

from .models import TheCozmChat
from .serializers import ConversationSerializer
from .utils import ask_openai
from django.conf import settings
import constants

openai.api_key = settings.OPEN_API_KEY


class ChatbotAPIView(APIView):
    def get(self, request, *args, **kwargs):
        chats = TheCozmChat.objects.filter(user=request.user) if request.user.is_authenticated else []
        return render(request, 'thecozm_chatbot.html', {'chats': chats})

    def post(self, request, *args, **kwargs):
        message = request.data.get('message')
        user = request.user
        conversation = []
        user_message = [
            {
                "role": "user",
                "content": message
            }
        ]

        if user.is_authenticated:
            chats = TheCozmChat.objects.filter(user=user)
            conversation = ConversationSerializer(chats, many=True).data
            conversation.extend(user_message)

        response = ask_openai(conversation) if conversation else ask_openai(user_message)
        # response = "Please provide valid API Key"

        chat = TheCozmChat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        return render(request, 'login.html')


class RegisterAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password == confirm_password:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except Exception as e:
                error_message = 'Error creating account'
                # return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
                return render(request, 'register.html', {'error_message': error_message},
                              status=status.HTTP_401_UNAUTHORIZED)
        else:
            error_message = 'Passwords do not match'
            return render(request, 'register.html', {'error_message': error_message})


class LogoutAPIView(APIView):
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return redirect('login')
