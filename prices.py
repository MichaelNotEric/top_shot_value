import csv
import json
import sys
import getopt
import requests
from bs4 import BeautifulSoup

import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np

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

with open("input.txt") as infile, open("output.txt", "w") as outfile:
    lines = infile.readlines()
    for line in lines:
        price = get_price_from_url(line)		
        outfile.write(price + "\n")