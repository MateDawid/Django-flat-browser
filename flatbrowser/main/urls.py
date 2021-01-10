from django.urls import path
from .views import search_flats

urlpatterns = [
    path('', search_flats, name = "search_flats")
]