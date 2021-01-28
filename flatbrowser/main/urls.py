from django.urls import path
from .views import search_flats, render_home_page, register, log_in, log_out, display_watched_list

urlpatterns = [
    path('', render_home_page, name="render_home_page"),
    path('results/', search_flats, name = "search_flats"),
    path('register/', register, name= "register"),
    path('login/', log_in, name="log_in"),
    path('logout/', log_out, name="log_out"),
    path('watched/', display_watched_list, name="display_watched_list")
]