import csv
import getopt
import json
import matplotlib.pyplot as plt
import numpy as np
import requests
import sys

from bs4 import BeautifulSoup
from listings import get_lowest_price_from_url
from utils import time_func


plt.style.use('seaborn-whitegrid')

def write_prices():
    with open("input.txt") as infile, open("output.txt", "w") as outfile:
        lines = infile.readlines()
        for line in lines:
            price = get_lowest_price_from_url(line)		
            outfile.write(price + "\n")

time_func("fetch the list of prices", write_prices)
