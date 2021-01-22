import requests
import json
import os.path
import pathlib

DEFAULT_OAUTH_URL = 'https://allegro.pl/auth/oauth'
DEFAULT_API_URL = 'https://api.allegro.pl/'
client = "1314c86f6d4c421b8738c2438073533b"
secret = "i7MkPimYuHmxEzj7vsx0x6oPPHbuzm13HczpB0eSMOY82dxlTA1i2G1d6tHdsUZZ"

def refresh_token(client_id, client_secret, refresh_token, oauth_url=DEFAULT_OAUTH_URL):
    token_url = oauth_url + '/token'

    access_token_data = {'grant_type': 'refresh_token',
                         'refresh_token': refresh_token}

    response = requests.post(url=token_url,
                             auth=requests.auth.HTTPBasicAuth(client_id, client_secret),
                             data=access_token_data)

    with open(os.path.join(pathlib.Path(__file__).parent.absolute(), 'access.json'), 'w') as json_file:
        json.dump(response.json(), json_file)

def get_current_token():
    with open(os.path.join(pathlib.Path(__file__).parent.absolute(), 'access.json')) as f:
        data = json.load(f)
        return data['access_token']

def get_refresh_token():
    with open(os.path.join(pathlib.Path(__file__).parent.absolute(), 'access.json')) as f:
        data = json.load(f)
        return data['refresh_token']

def get_offer_details(data, offer_type, offer_number):
    offer_title = data['items'][offer_type][offer_number]['name']
    area = 0
    price = data['items'][offer_type][offer_number]['sellingMode']['price']['amount']
    URL = data['items'][offer_type][offer_number]['vendor']['url']
    image = data['items'][offer_type][offer_number]['images'][0]['url']
    return {"title": offer_title,"area": area,"price": round(int(price)),"url": URL, "image": image}

def get_available_offers(data, city):
    offers = []
    for offer_number in range(len(data['items']['regular'])):
        try:
            offer = get_offer_details(data, 'regular', offer_number)
            offer["site"] = "allegro.pl"
            offer["city"] = city.title()
            offers.append(offer)
        except:
            continue
    for offer_number in range(len(data['items']['promoted'])):
        try:
            offer = get_offer_details(data, 'promoted', offer_number)
            offer["site"] = "allegro.pl"
            offer["city"] = city.title()
            offers.append(offer)
        except:
            continue
    return offers


def get_from_allegro_api(city, price_from='', price_to='', area_from='', area_to='', days=''):
    paramethers = {"category.id": 112739, "location.city": str(city), "price.from": str(price_from), "price.to": str(price_to), "parameter.236.from": str(area_from),"parameter.236.to": str(area_to), "startingTime": "P"+str(days)+"D"}
    
    headers = {}
    headers['charset'] = 'utf-8'
    headers['Accept-Language'] = 'pl-PL'
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/vnd.allegro.public.v1+json'
    headers['Authorization'] = "Bearer {}".format(get_current_token())

    with requests.Session() as session:
        session.headers.update(headers)
        response = session.get(DEFAULT_API_URL + 'offers/listing', params=paramethers)
        data = response.json()

        if response.status_code == 401:
            refresh_token(client, secret, get_refresh_token())
            headers['Authorization'] = "Bearer {}".format(get_current_token())
            session.headers.update(headers)
            response = session.get(DEFAULT_API_URL + 'offers/listing', params=paramethers)
            data = response.json()
            offers = get_available_offers(data, city)
            return offers
        else:
            offers = get_available_offers(data, city)
            return offers