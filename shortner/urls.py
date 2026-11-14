from django.urls import path
from .views import ShortURLView , redirect_url
urlpatterns = [
    path('test/',ShortURLView.as_view()),
    path('<str:code>/', redirect_url),
]