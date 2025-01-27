import requests
from os import path
import colorama
import random
from datetime import datetime

class WoltAPI:
    BASE_URL = 'https://restaurant-api.wolt.com/v1/'
    CONSUMER_API = 'https://consumer-api.wolt.com/v1/'
    def __init__(self):
        """
        Initialize a new Requests Session. Using this, we can be sure we are not opening/using unneccessary resources for multiple API requests.
        In addition, initialize a new seed for the Random library, to ensure proper randomness. Uses the current time to initialize.
        """
        self.request_handler = requests.session()
        random.seed(datetime.timestamp(datetime.now()))

    def handle_request(self, **kwargs):
        """
        Perform an arbitrary GET request, and return the data if the request is successful.
        Return the data in JSON format.
        NOTE: This assumes the data being returned by the webserver is in JSON format. If it is not, this function will raise an Exception.
        """
        url = kwargs.get('url')
        params = kwargs.get('params')
        response = self.request_handler.get(url=url, params=params)
        if not response.status_code == 200:
            print(colorama.Fore.RED + f'Request to {url} returned status code {response.status_code} -- {response.text}' + colorama.Fore.RESET)
            return False
        return response.json()

    def get_place_id(self, search_string: str):
        """
        Retrieve a Place ID for an address (or partial address) from the Wolt API.
        Retrieves the "best match" place for the search string (NOTE: May not be accurate).
        """
        request_url = path.join(self.BASE_URL, 'google/places/autocomplete/json')
        params = {'input': search_string}  # input for the API
        response = self.handle_request(url=request_url, params=params)
        if not response:
            raise Exception(f'Place ID not found for {search_string}.')
        address = response['predictions'][0]
        print(f'Retrieved place id for {colorama.Fore.BLUE + address['description'] + colorama.Fore.RESET}')
        return address['place_id']

    def get_geo_coordinates(self, search_string: str):
        """
        Retrieve the longitude and latitude for a given location.
        """
        place_id = self.get_place_id(search_string)
        request_url = path.join(self.BASE_URL, 'google/geocode/json')
        params = {'place_id': place_id}
        response = self.handle_request(url=request_url, params=params)
        if not response:
            raise Exception(f'Could not retrieve coordinates for {search_string} with place ID {place_id}')
        location = response['results'][0]
        return {'latitude': location['geometry']['location']['lat'], 'longitude': location['geometry']['location']['lng']}
    
    def get_restaurant_list(self, search_string: str):
        """
        Retrieve a list of restaurants that will deliver to the location identified by the search_string.
        """
        request_url = path.join(self.CONSUMER_API, 'pages/front')
        location = self.get_geo_coordinates(search_string)
        if not location:
            raise Exception(f'Invalid search query: {search_string}')
        
        params = {'lat': location['latitude'], 'lon': location['longitude']}
        response = self.handle_request(url=request_url, params=params)
        if not response:
            raise Exception(f'Could not retrieve restaurant list for {search_string}')

        city_name = response['city']
        if response['city_data'].get('slug') == 'out-of-reach':
            raise Exception("Location is not in a valid area")
        country_code = response['city_data']['country_code_alpha3'].lower()
        restaraunt_lists = [i for i in response['sections'] if i.get('template') == 'venue-list']
        restaraunt_lists = [i.get('items') for i in restaraunt_lists if i.get('items')]
        restaurants = []
        for lst in restaraunt_lists:
            [restaurants.append(i.get('venue')) for i in lst if i.get('venue')]
        # manually build the link for the restaurant
        [i.update({'link': '/'.join(['https://wolt.com', country_code, city_name, i.get("slug")])}) for i in restaurants]

        return restaurants
    

    def choose_restaurant(self, restaurant_list: list, filter_kosher=False):
        """
        From a list of restaurants, randomly choose one. If necessary, filter the list beforehand.
        """
        if not restaurant_list:
            raise Exception(colorama.Fore.MAGENTA + 'No Restaurants deliver to the entered address at this time' + colorama.Fore.RESET)

        if filter_kosher:
            print('Filtering for kosher results')
            restaurant_list = [i for i in restaurant_list if 'kosher' in [j.lower() for j in i.get('tags')]]
        chosen_restaurant = random.choice(restaurant_list)
        print(f'Chose restaraunt {chosen_restaurant["name"]}, which delivers to your area.')
        return chosen_restaurant
    

