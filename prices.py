import csv
import getopt
import json
import matplotlib.pyplot as plt
import numpy as np
import requests
import sys

from bs4 import BeautifulSoup
from utils import time_func


plt.style.use('seaborn-whitegrid')

def get_price_from_url(url):
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

def write_prices():
    with open("input.txt") as infile, open("output.txt", "w") as outfile:
        lines = infile.readlines()
        for line in lines:
            price = get_price_from_url(line)		
            outfile.write(price + "\n")

time_func("fetch the list of prices", write_prices)