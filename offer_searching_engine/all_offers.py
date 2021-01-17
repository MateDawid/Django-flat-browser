from scrapping_functions import scrap_otodom, scrap_morizon
from allegro_api_functions import get_from_allegro_api

def get_all_offers(city,price_from="",price_to="",area_from="",area_to="",days=""):
    offers = []
    for element in scrap_otodom(city.lower(),price_from,price_to,area_from,area_to,days):
        offers.append(element)
    for element in scrap_morizon(city.lower(),price_from,price_to,area_from,area_to,days):
        offers.append(element)
    for element in get_from_allegro_api(city.lower(),price_from,price_to,area_from,area_to,days):
        offers.append(element)
    return offers