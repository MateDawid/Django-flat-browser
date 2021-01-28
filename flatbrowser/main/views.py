from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date
from datetime import timedelta

from .models import Flat, WatchedList
from .forms import SearchForm, RegistrationForm, LoginForm
from offer_searching_engine.scrapping_functions import scrap_otodom, scrap_morizon
from offer_searching_engine.allegro_api_functions import get_from_allegro_api

def render_home_page(request):
    form = SearchForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            request.session['render_home_page'] = request.POST
            return redirect(search_flats)
    return render(request,"main/home.html", {"form":form})

def search_flats(request):
    flats_found = []
    flat_ids = []
    form = SearchForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            request.session['render_home_page'] = request.POST
            return redirect(search_flats)

    if request.session.get('render_home_page'):
        home_form = request.session.get('render_home_page')
        city = home_form["city"]
        min_price = home_form["min_price"]
        max_price = home_form["max_price"]
        min_area = home_form["min_area"]
        max_area = home_form["max_area"]
        days_from_publication = int(home_form["days_from_publication"]) if home_form["days_from_publication"] != "" else home_form["days_from_publication"]
    
    found_offers = scrap_otodom(city,min_price,max_price,min_area,max_area,days_from_publication) + scrap_morizon(city,min_price,max_price,min_area,max_area,days_from_publication) + get_from_allegro_api(city,min_price,max_price,min_area,max_area,days_from_publication)
        
    for offer in found_offers:
        if Flat.objects.filter(image=offer["image"]).count() >= 1:
            already_found_flat = Flat.objects.get(image=offer["image"])
            already_found_flat.date = date.today() - timedelta(days=days_from_publication) if isinstance(days_from_publication, int) else date.today()
            already_found_flat.save()
            flat_ids.append(already_found_flat.id)
        else:
            new_flat = Flat() 
            new_flat.site = offer["site"]
            new_flat.city = offer["city"]
            new_flat.title = offer["title"]
            new_flat.area = offer["area"] if offer["area"] != "" else 0
            new_flat.price = offer["price"]
            new_flat.url = offer["url"]
            new_flat.image = offer["image"]
            new_flat.date = date.today() - timedelta(days=days_from_publication) if isinstance(days_from_publication, int) else date.today()
            new_flat.save()
            flat_ids.append(new_flat.id)
        
    flats_found = Flat.objects.filter(id__in=flat_ids)
    return render(request, 'main/result.html', {"form":form, "flats_found":flats_found})

def register(request):
    form = SearchForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save()
            messages.success(request, 'Konto zostało utworzone!')
            user = authenticate(request, username=reg_form.cleaned_data['username'],password=reg_form.cleaned_data['password1'])
            users_watched_list = WatchedList()
            users_watched_list.user = user
            users_watched_list.save()
            login(request, user)
            return redirect(render_home_page)
    else:
        reg_form = RegistrationForm()
    return render(request, 'main/registration.html', {'reg_form': reg_form, 'form': form})

def log_in(request):
    form = SearchForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, username=login_form.cleaned_data['username'],password=login_form.cleaned_data['password'])
            login(request, user)
            return redirect(render_home_page)                         
    else: 
        login_form = LoginForm()
    return render(request, 'main/login.html', {'login_form': login_form, 'form': form})

@login_required
def log_out(request):
    logout(request)
    return redirect(render_home_page)

@login_required
def display_watched_list(request):
    return 0

@login_required
def add_to_watched_list(request):
    return 0

@login_required
def delete_from_watched_list(request):
    return 0