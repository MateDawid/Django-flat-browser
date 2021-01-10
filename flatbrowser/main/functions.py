import requests
from bs4 import BeautifulSoup
import datetime
from dateutil.relativedelta import relativedelta

def scrap_otodom (city,price_from,price_to,area_from,area_to,days):
    # Filling URL address with variables
    adress_city = city.replace(" ","-").replace("ą","a").replace("ę","e").replace("ć","c").replace("ń","n").replace("ó","o").replace("ś","s").replace("ó","o").replace("ź","z").replace("ż","z")
    adress = "https://www.otodom.pl/sprzedaz/mieszkanie/"+adress_city+"/?search%5Bcreated_since%5D="+days+"&search%5Bfilter_float_price%3Afrom%5D="+price_from+"&search%5Bfilter_float_price%3Ato%5D="+price_to+"&search%5Bfilter_float_m%3Afrom%5D="+area_from+"&search%5Bfilter_float_m%3Ato%5D="+area_to+"&nrAdsPerPage=72" 

    # Connecting with page
    page = requests.get(adress)
    soup = BeautifulSoup(page.content,"html.parser")
    elements = soup.findAll("article",attrs={"class":"offer-item"})
    offers = []
    
    # Searching offer details
    for element in elements:
        city_name = city.title()
        if city_name in str(element.find("p",class_="text-nowrap").text.strip()):
            offerTitle = element.find("span",class_="offer-item-title")
            price_found = element.find("li",class_="offer-item-price").text.strip()
            price = float(price_found[:-3].replace(",",".").replace(" ", ""))
            area_found = element.find("li",class_="hidden-xs offer-item-area").text.strip()
            area = float(area_found[:-3].replace(",",".").replace(" ", ""))
            URL = element["data-url"]
            offers.append({"site":"otodom.pl","city": city.title(),"title":offerTitle.text.strip(),"area":round(area),"price":round(price),"url":URL})
    return offers

def scrap_olx(city,price_from,price_to,area_from,area_to,days):
    
    # Creating dictionary with names of moths, which will be used to define offer date
    months_numbers = {"stycznia":1,"lutego":2,"marca":3,"kwietnia":4,"maja":5,"czerwca":6,"lipca":7,"sierpnia":8,"września":9,"października":10,"listopada":11,"grudnia":12}

    # Filling URL address with variables 
    adress_city = city.replace(" ","-").replace("ą","a").replace("ę","e").replace("ć","c").replace("ń","n").replace("ó","o").replace("ś","s").replace("ó","o").replace("ź","z").replace("ż","z")
    adress = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/"+adress_city+"/?search%5Bfilter_float_price%3Afrom%5D="+price_from+"&search%5Bfilter_float_price%3Ato%5D="+price_to+"&search%5Bfilter_float_m%3Afrom%5D="+area_from+"&search%5Bfilter_float_m%3Ato%5D="+area_to+"&view=list"

    # Connecting with page
    page = requests.get(adress)
    soup = BeautifulSoup(page.content,"html.parser")
    elements = soup.findAll("tr",attrs={"class":"wrap"})
    offers = []

    # Searching offer details
    for element in elements:
        # Eliminating offers different from olx service
        URL = element.find("a",href = True)["href"] 
        if URL.startswith("https://www.olx.pl/"):
         
          # Finding title and price of flat
          offerTitle = element.find("h3",class_="lheight22 margintop5")
          price_found = element.find("p",class_="price").text.strip()
          price = float(price_found[:-3].replace(",",".").replace(" ", ""))
          
          # Searching for area on offer adress
          offerPage = requests.get(URL)
          offerSoup = BeautifulSoup(offerPage.content,"html.parser")
          index = 0
          details = offerSoup.findAll("li",class_="offer-details__item")
          for i in range (len(details)):
            if details[i].find("span",class_="offer-details__name").text.strip() == "Powierzchnia":
              index = i
          area_found = offerSoup.findAll("strong",class_="offer-details__value")[index].text.strip()
          area = float(area_found[:-3].replace(",",".").replace(" ", ""))
          
          # Finding offer date
          offerDate = ((offerSoup.find("li",class_="offer-bottombar__item")).find("strong")).text.strip()[9:]
          moth_number = months_numbers[(offerDate[2:-4]).strip()]
          # Converting date into proper format
          if days != "":
            if datetime.date(int(offerDate[-4:]),int(moth_number),int(offerDate[:2]))+relativedelta(days=int(days))>datetime.date.today():
              offers.append({"site":"olx.pl","title":offerTitle.text.strip(),"area":area.text.strip(),"price":price.text.strip(),"url":URL})
            else:
              continue
          else:
            offers.append({"site":"olx.pl","city": city.title(),"title":offerTitle.text.strip(),"area":round(area),"price":round(price),"url":URL})
        else:
          continue
    return offers

def scrap_morizon (city,price_from,price_to,area_from,area_to,days):
    # Filling URL address with variables 
    adress = "https://www.morizon.pl/mieszkania/"+city+"/?ps%5Bprice_from%5D="+price_from+"&ps%5Bprice_to%5D="+price_to+"&ps%5Bliving_area_from%5D="+area_from+"&ps%5Bliving_area_to%5D="+area_to
    
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
      
    # Connecting with page
    page = requests.get(adress)
    soup = BeautifulSoup(page.content,"html.parser")
    elements = soup.findAll("section",attrs={"class":"single-result__content single-result__content--height"})
    offers = []

    # Searching offer details
    for element in elements:
      # Avoiding elements different from offers
      if element.find("div",attrs={"class":"description single-result__description"}) == None:
        continue
      else:
        # Setting city name
        city_name = city.capitalize()

        # Finding proper title for offer
        if element.find("h3",class_="single-result__category single-result__category--title") != None:
          offerTitle = (element.find("h3",class_="single-result__category single-result__category--title")).find("p")
        else:
          offerTitle = element.find("h2",class_="single-result__title")
        
        # Finding price of flat
        price_found = element.find("p",class_="single-result__price").text.replace(u'\xa0'," ")
        price = float(price_found[:-3].replace(",",".").replace(" ", ""))
        
        # Finding area of flat
        details = element.find("ul",class_="param list-unstyled list-inline").findAll("li")
        for detail in details:
          if detail.text.strip()[-2:] == "m²":
            area_found = detail.text.strip()
            area = float(area_found[:-3].replace(",",".").replace(" ", ""))
        
        # Finding URL adress of flat
        URL = element.find("a",href = True)["href"]
       
        # Adding offer to list
        offers.append({"site":"morizon.pl","city": city.title(),"title":offerTitle.text.strip(),"area":round(area),"price":round(price),"url":URL})
    return offers

def scrap_all(city,price_from,price_to,area_from,area_to,days):
    offers = []
    for element in scrap_otodom(city.lower(),price_from,price_to,area_from,area_to,days):
        offers.append(element)
    for element in scrap_olx(city.lower(),price_from,price_to,area_from,area_to,days):
        offers.append(element)
    for element in scrap_morizon(city.lower(),price_from,price_to,area_from,area_to,days):
        offers.append(element)
    return offers