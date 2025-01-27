from src.wolt_api import WoltAPI
import colorama
import webbrowser
from time import sleep

def main():
    wolt_api = WoltAPI()
    search_string = input('Welcome to Wolt Roulette! Please enter a complete address, including city: ')
    filter_kosher = input('Choose only from a list of kosher restaurants (yes/no)? ')
    while filter_kosher.lower().strip() not in ['yes', 'no']:
        filter_kosher = input('Choose only from a list of kosher restaurants (yes/no)? ')
    filter_kosher = True if filter_kosher == 'yes' else False  # convert to bool
    try:
        restaurant_list = wolt_api.get_restaurant_list(search_string)
        print(f'Found {len(restaurant_list)} restaurants')
        restaurant = wolt_api.choose_restaurant(restaurant_list, filter_kosher)
    except Exception as e:
        print(colorama.Fore.RED + f'An error occured -- {type(e)}: {e}' + colorama.Fore.RESET)
        return False

    print(f'The chosen restaurant link is {restaurant["link"]}.')
    for i in range(3):
        print(f'Opening in browser in {3-i} seconds.', end='\r')
        sleep(1)
    webbrowser.open(restaurant['link'])

if __name__ == "__main__":
    main()