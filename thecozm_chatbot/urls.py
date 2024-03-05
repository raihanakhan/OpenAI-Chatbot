from django.urls import path

from .views import ChatbotAPIView, LoginAPIView, RegisterAPIView, LogoutAPIView

urlpatterns = [
    path('', ChatbotAPIView.as_view(), name='chatbot'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('register', RegisterAPIView.as_view(), name='register'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
]