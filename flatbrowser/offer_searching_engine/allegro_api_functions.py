import requests
import json
import os.path
import pathlib
import webbrowser
from decouple import config
from http.server import BaseHTTPRequestHandler, HTTPServer
from main.models import RefreshToken

DEFAULT_OAUTH_URL = 'https://allegro.pl/auth/oauth'
DEFAULT_API_URL = 'https://api.allegro.pl/'
DEFAULT_REDIRECT_URI = 'http://localhost:8000'
client = config('client')
secret = config('secret')


def get_access_code(client_id, redirect_uri=DEFAULT_REDIRECT_URI, oauth_url=DEFAULT_OAUTH_URL):
    auth_url = '{}/authorize' \
               '?response_type=code' \
               '&client_id={}' \
               '&redirect_uri={}'.format(oauth_url, client_id, redirect_uri)

    parsed_redirect_uri = requests.utils.urlparse(redirect_uri)
    server_address = parsed_redirect_uri.hostname, parsed_redirect_uri.port

    class AllegroAuthHandler(BaseHTTPRequestHandler):
        def __init__(self, request, address, server):
            super().__init__(request, address, server)

        def do_GET(self):
            self.send_response(200, 'OK')
            self.send_header('Content-Type', 'text/html')
            self.end_headers()

            self.server.path = self.path
            self.server.access_code = self.path.rsplit('?code=', 1)[-1]

    webbrowser.open(auth_url)
    httpd = HTTPServer(server_address, AllegroAuthHandler)
    httpd.handle_request()
    httpd.server_close()
    _access_code = httpd.access_code
    return _access_code


def sign_in(client_id, client_secret, access_code, redirect_uri=DEFAULT_REDIRECT_URI, oauth_url=DEFAULT_OAUTH_URL):
    token_url = oauth_url + '/token'
    access_token_data = {'grant_type': 'authorization_code',
                         'code': access_code,
                         'redirect_uri': redirect_uri}

    response = requests.post(url=token_url,
                             auth=requests.auth.HTTPBasicAuth(client_id, client_secret),
                             data=access_token_data)
    new_refresh_token = RefreshToken.objects.all().first()
    new_refresh_token.refresh_token = response.json()['refresh_token']
    new_refresh_token.save()


def refresh_token(client_id, client_secret, refresh_token, oauth_url=DEFAULT_OAUTH_URL):
    try:
        token_url = oauth_url + '/token'

        access_token_data = {'grant_type': 'refresh_token',
                             'refresh_token': refresh_token}

        response = requests.post(url=token_url,
                                 auth=requests.auth.HTTPBasicAuth(client_id, client_secret),
                                 data=access_token_data)

        new_refresh_token = RefreshToken.objects.all().first()
        new_refresh_token.refresh_token = response.json()['refresh_token']
        new_refresh_token.save()

    except:
        pass


def get_current_token(client_id, client_secret, oauth_url=DEFAULT_OAUTH_URL):
    token_url = oauth_url + '/token'
    access_token_data = {'grant_type': 'client_credentials'}

    response = requests.post(url=token_url,
                             auth=requests.auth.HTTPBasicAuth(client_id, client_secret),
                             data=access_token_data)

    return response.json()['access_token']


def get_refresh_token():
    return RefreshToken.objects.all().first().refresh_token


def get_offer_details(data, offer_type, offer_number):
    try:
        offer_title = data['items'][offer_type][offer_number]['name']
        price = data['items'][offer_type][offer_number]['sellingMode']['price']['amount']
        URL = data['items'][offer_type][offer_number]['vendor']['url']
        image = data['items'][offer_type][offer_number]['images'][0]['url']
        return {"title": offer_title, "price": int(float(price)), "url": URL, "image": image}
    except:
        pass


def get_available_offers(data, city, area_from):
    offers = []
    try:
        for offer_number in range(len(data['items']['regular'])):
            try:
                offer = get_offer_details(data, 'regular', offer_number)
                offer["area"] = area_from
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
    except:
        return offers


def get_from_allegro_api(city, price_from='', price_to='', area_from=0, area_to='', days=''):
    paramethers = {"category.id": 112739, "location.city": str(city), "price.from": str(price_from),
                   "price.to": str(price_to), "parameter.236.from": str(area_from), "parameter.236.to": str(area_to),
                   "startingTime": "P" + str(days) + "D"}

    headers = {}
    headers['charset'] = 'utf-8'
    headers['Accept-Language'] = 'pl-PL'
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/vnd.allegro.public.v1+json'
    headers['Authorization'] = "Bearer {}".format(get_current_token(client, secret))

    with requests.Session() as session:
        session.headers.update(headers)
        try:
            response = session.get(DEFAULT_API_URL + 'offers/listing', params=paramethers)

            if response.status_code == 401:
                refresh_token(client, secret, get_refresh_token())
                headers['Authorization'] = "Bearer {}".format(get_current_token(client, secret))
                session.headers.update(headers)
                response = session.get(DEFAULT_API_URL + 'offers/listing', params=paramethers)

            data = response.json()
            offers = get_available_offers(data, city, area_from)
            return offers

        except:
            return []

# sign_in(client, secret, get_access_code(client))
