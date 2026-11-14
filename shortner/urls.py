from django.urls import path
from .views import ShortURLView , redirect_url , ShortURLDetailView
urlpatterns = [
    path('test/',ShortURLView.as_view()),
    path('<str:code>/', redirect_url),
    path('delete/<int:pk>/',ShortURLDetailView.as_view() ),

]