import requests
from bs4 import BeautifulSoup
import datetime
from dateutil.relativedelta import relativedelta
import time

def get_valid_city(city):
    return city.replace(" ","-").replace("ą","a").replace("ę","e").replace("ć","c").replace("ń","n").replace("ó","o").replace("ś","s").replace("ó","o").replace("ź","z").replace("ż","z")

def get_numeric_value(area_or_price):
    try:
      return int(float(area_or_price[:-3].replace(",",".").replace(" ", "")))
    except:
      return 0

def get_otodom_price(element):
    price_found = element.find("li",class_="offer-item-price").text.strip()
    if price_found == "Zapytaj o cenę" or price_found == None:
      price = 0
    else:
      price = get_numeric_value(price_found)
    return price

def prepare_morizon_adress(city, price_from, price_to, area_from, area_to, days):
    # Filling URL address with variables 
    adress = "https://www.morizon.pl/mieszkania/"+str(city)+"/?ps%5Bprice_from%5D="+str(price_from)+"&ps%5Bprice_to%5D="+str(price_to)+"&ps%5Bliving_area_from%5D="+str(area_from)+"&ps%5Bliving_area_to%5D="+str(area_to)
    
    # Setting URL based on typed "days" variable
    if days != "":  
      if int(days) == 1:
        adress += "&ps%5Bdate_filter%5D=1"
      elif int(days) in range(2,8):
        adress += "&ps%5Bdate_filter%5D=7"
      elif int(days) in range(8,31):
        adress += "&ps%5Bdate_filter%5D=30"
      elif int(days) in range(31,91):
        adress += "&ps%5Bdate_filter%5D=90"
      elif int(days) in range(91,181):
        adress += "&ps%5Bdate_filter%5D=180"  
    return adress

def get_morizon_title(element):
    if element.find("h3",class_="single-result__category single-result__category--title") != None:
      offer_title = (element.find("h3",class_="single-result__category single-result__category--title")).find("p")
    else:
      offer_title = element.find("h2",class_="single-result__title")
    return offer_title

def get_morizon_price(element):
    price_found = element.find("p",class_="single-result__price").text.replace(u'\xa0'," ")
    if price_found == "Zapytaj o cenę" or price_found == None:
      price = 0
    else:
      price = get_numeric_value(price_found)
    return price
# Scraping functions

def scrap_otodom (city,price_from="",price_to="",area_from="0",area_to="",days=""):
    # Filling URL address with variables
    adress_city = get_valid_city(city)
    adress = "https://www.otodom.pl/sprzedaz/mieszkanie/"+str(adress_city)+"/?search%5Bcreated_since%5D="+str(days)+"&search%5Bfilter_float_price%3Afrom%5D="+str(price_from)+"&search%5Bfilter_float_price%3Ato%5D="+str(price_to)+"&search%5Bfilter_float_m%3Afrom%5D="+str(area_from)+"&search%5Bfilter_float_m%3Ato%5D="+str(area_to)+"&nrAdsPerPage=72" 

    # Connecting with page
    page = requests.get(adress)
    soup = BeautifulSoup(page.content,"html.parser")
    elements = soup.findAll("article",attrs={"class":"offer-item"})
    offers = []
    
    # Searching offer details
    for element in elements:
        city_name = city.title()
        if city_name in element.find("p",class_="text-nowrap").text.strip():
            offerTitle = element.find("span",class_="offer-item-title")
            price = get_otodom_price(element)
            area = get_numeric_value(element.find("li",class_="hidden-xs offer-item-area").text.strip())
            URL = element["data-url"]
            image = element.find("span",class_="img-cover lazy")['data-src']
            offers.append({"site":"otodom.pl","city": city_name,"title":offerTitle.text.strip(),"area":round(area),"price":round(price),"url":URL, "image":image})
    return offers

def scrap_morizon(city,price_from="",price_to="",area_from="0",area_to="",days=""):
    adress = prepare_morizon_adress(city, price_from, price_to, area_from, area_to, days)
    
    # Connecting with page
    page = requests.get(adress)
    soup = BeautifulSoup(page.content,"html.parser")
    elements = soup.findAll("div",attrs={"class":"row row--property-list"})
    offers = []

    # Searching offer details
    for element in elements:
      # Avoiding elements different from offers
      if element.find("div",attrs={"class":"description single-result__description"}) == None:
        continue
      else:
        # Finding proper title for offer
        if get_morizon_title(element) == None:
          continue
        else:
          offer_title = get_morizon_title(element)
        
        # Finding price of flat
        if element.find("p",class_="single-result__price") == None:
          continue
        else:
          price = get_morizon_price(element)

        # Setting city name
        city_name = city.capitalize()
        
        # Finding area of flat
        details = element.find("ul",class_="param list-unstyled list-inline").findAll("li")
        for detail in details:
          if detail.text.strip()[-2:] == "m²":
            area = get_numeric_value(detail.text.strip())
        
        # Finding URL adress of flat
        URL = element.find("a",href = True)["href"]

        # Finding image for offer
        image = element.find("meta")['content']
       
        # Adding offer to list
        offers.append({"site":"morizon.pl","city": city.title(),"title":offer_title.text.strip(),"area":round(area),"price":round(price),"url":URL, "image": image})
    return offers