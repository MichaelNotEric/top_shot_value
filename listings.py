import json
import requests

from bs4 import BeautifulSoup


def get_lowest_price_from_url(url):
    page = requests.get(url.strip())
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
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    script = soup.find('script', id='__NEXT_DATA__')
    json_object = json.loads(script.contents[0])
    moment = json_object['props']['pageProps']['moment']
    return moment
