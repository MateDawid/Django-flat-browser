from django.shortcuts import render, redirect
from datetime import datetime
from datetime import timedelta

from .models import Flat, SearchingResult
from .forms import SearchForm
from offer_searching_engine.scrapping_functions import scrap_otodom, scrap_morizon
from offer_searching_engine.allegro_api_functions import get_from_allegro_api

def search_flats(request):
    form = SearchForm(request.POST or None, request.FILES or None)
    flats_found = []
    if form.is_valid():
        user_search = SearchingResult()
        user_search.save()
        city = form.data["city"]
        min_price = form.data["min_price"]
        max_price = form.data["max_price"]
        min_area = form.data["min_area"]
        max_area = form.data["max_area"]
        days_from_publication = form.data["days_from_publication"]
        found_offers = scrap_otodom(city,min_price,max_price,min_area,max_area,days_from_publication) + scrap_morizon(city,min_price,max_price,min_area,max_area,days_from_publication) + get_from_allegro_api(city,min_price,max_price,min_area,max_area,days_from_publication)
        
        for offer in found_offers:
            if Flat.objects.filter(image=offer["image"]).count() >= 1:
                user_search.results.add(Flat.objects.get(image=offer["image"]))
            else:
                new_flat = Flat() 
                new_flat.site = offer["site"]
                new_flat.city = offer["city"]
                new_flat.title = offer["title"]
                new_flat.area = offer["area"]
                new_flat.price = offer["price"]
                new_flat.url = offer["url"]
                new_flat.image = offer["image"]
                new_flat.save()
                user_search.results.add(new_flat)
        

        flats_found = user_search.results.all()
        return render(request, 'main/result.html', {"form":form, "flats_found":flats_found})
    return render(request, 'main/result.html', {"form":form, "flats_found":flats_found })



