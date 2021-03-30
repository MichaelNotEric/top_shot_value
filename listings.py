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
	
def get_all_listings_below_target_price_and_serial(url, max_price, max_serial):
    if not str.startswith(url, "https://www.nbatopshot.com/listings/p2p/"):
        raise ValueError("User passed malformed URL")
    if (max_price and max_price < 0) or not max_price:
        raise ValueError("User passed invalid maxprice")
    if (max_serial and max_serial < 0):
        raise ValueError("User passed invalid maxserial")
		
    listings = []
    moment = get_all_listings_from_url(url)
    play = moment['play']
    moments = moment['momentListings']
		
    # add each listing at or below max price if it was passed in
    for m in moments:
        serial = int(float(m['moment']['flowSerialNumber']))
        price = int(float(m['moment']['price']))
        if price <= max_price and ((serial <= max_serial) or not max_serial):
            listings.insert(0,(serial, price))

    # remove listings of equal or higher price but higher serial number
    i = 0
    while i < len(listings):
        for l in listings:
            try:
                if (listings[i][1] >= l[1] and listings[i][0] > l[0] and
                listings[i][0] != int(play['stats']['jerseyNumber'])):
                    listings.pop(i)
                    i = i - 1
            except:
                print("\nSomething went wrong. Please wait a moment and try again.")
                sys.exit(2)
        i = i + 1
		
    jersey_listing = None
    i = 0
    while i < len(listings):
        if listings[i][0] == int(play['stats']['jerseyNumber']):
            jersey_listing = "#" + str(listings[i][0]) + " - $" + str(listings[i][1])
            jersey_listing = (listings[i][0],listings[i][1])
            listings.pop(i)
            i = i - 1

        i = i + 1
    if len(listings) == 0:
        page = get_listing_page(url)
        price = get_lowest_price_from_url(page)
        print("Latest price: {}          at {}".format(price, datetime.datetime.now().strftime("%b %d %Y %I:%M:%S %p")), end='\r')		
    return listings, moment, play, moments, jersey_listing
		
def price_lower_or_equal_to_target(url, target):
    if not str.startswith(url, "https://www.nbatopshot.com/listings/p2p/"):
        raise ValueError("User passed malformed URL")
    if target < 0:
        raise ValueError("User passed invalid maxprice")

    page = get_listing_page(url)
    price = get_lowest_price_from_url(page)
    if not (float(price) <= target):
        #print("{} is not less than {}".format(price, target))
        print("Latest price: {}          at {}".format(price, datetime.datetime.now().strftime("%b %d %Y %I:%M:%S %p")), end='\r')
    return ((float(price) <= target), price)
