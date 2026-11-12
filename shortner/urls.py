from django.urls import path
from .views import ShortURLView
urlpatterns = [
    path('test/',ShortURLView.as_view()),
]