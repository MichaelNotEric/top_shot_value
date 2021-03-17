import datetime
import json
import requests

from bs4 import BeautifulSoup


def get_listing_page(url):
    if not str.startswith(url, "https://www.nbatopshot.com/listings/p2p/"):
        raise ValueError("User passed malformed URL")

    return requests.get(url.strip())

def print_listing_details(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    script = soup.find('script', id='__NEXT_DATA__')
    json_object = json.loads(script.contents[0])
    moment = json_object['props']['pageProps']['moment']
    play = moment['play']
    moments = moment['momentListings']
    title = soup.title
    price = str(title).split("-")[0].split("$")[1].strip()
    print(play['stats']['playerName'] + " " + play['stats']['playCategory'] + " - " + moment['set']['flowName'] + " " + str(moment['set']['flowSeriesNumber']))

def get_lowest_price_from_url(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    script = soup.find('script', id='__NEXT_DATA__')
    json_object = json.loads(script.contents[0])
    moment = json_object['props']['pageProps']['moment']
    play = moment['play']
    moments = moment['momentListings']
    title = soup.title
    price = str(title).split("-")[0].split("$")[1].strip()
    return price
	
def get_all_listings_from_url(url):
    if not str.startswith(url, "https://www.nbatopshot.com/listings/p2p/"):
        raise ValueError("User passed malformed URL")

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    script = soup.find('script', id='__NEXT_DATA__')
    json_object = json.loads(script.contents[0])
    moment = json_object['props']['pageProps']['moment']
    return moment

def price_lower_than_target(url, target):
    if not str.startswith(url, "https://www.nbatopshot.com/listings/p2p/"):
        raise ValueError("User passed malformed URL")
    if target < 0:
        raise ValueError("User passed invalid maxprice")

    page = get_listing_page(url)
    price = get_lowest_price_from_url(page)
    if not (float(price) < target):
        #print("{} is not less than {}".format(price, target))
        print("Latest price: {}          at {}".format(price, datetime.datetime.now().strftime("%b %d %Y %I:%M:%S %p")), end='\r')
    return float(price) < target
