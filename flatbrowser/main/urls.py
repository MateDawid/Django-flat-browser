from django.urls import path
from .views import search_flats, render_home_page

urlpatterns = [
    path('', render_home_page, name="render_home_page"),
    path('results/', search_flats, name = "search_flats")

]