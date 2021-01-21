from django.shortcuts import render, redirect

from .models import Flat
from .forms import SearchForm
from offer_searching_engine.scrapping_functions import scrap_otodom, scrap_morizon
from offer_searching_engine.allegro_api_functions import get_from_allegro_api

def search_flats(request):
    form = SearchForm(request.POST or None, request.FILES or None)
    flats_found = Flat.objects.all()
    if form.is_valid():
        city = form.data["city"]
        min_price = form.data["min_price"]
        max_price = form.data["max_price"]
        min_area = form.data["min_area"]
        max_area = form.data["max_area"]
        days_from_publication = form.data["days_from_publication"]
        found_offers = scrap_otodom(city,min_price,max_price,min_area,max_area,days_from_publication) + scrap_morizon(city,min_price,max_price,min_area,max_area,days_from_publication) + get_from_allegro_api(city,min_price,max_price,min_area,max_area,days_from_publication)
        
        for offer in found_offers:
            if Flat.objects.filter(url=offer["url"]).count() >= 1:
                continue
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
        
        flats_found = Flat.objects.all()
        return render(request, 'main/result.html', {"form":form, "flats_found":flats_found})
    return render(request, 'main/result.html', {"form":form, "flats_found":flats_found })



