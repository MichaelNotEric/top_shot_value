from listings import get_lowest_price_from_url, get_listing_page
from utils import time_func


def write_prices():
    with open("input.txt") as infile, open("output.txt", "w") as outfile:
        lines = infile.readlines()
        for line in lines:
		    page = get_listing_page(line)
            price = get_lowest_price_from_url(page)
            outfile.write(price + "\n")
            print('.', end='')

time_func("fetch the list of prices", write_prices)
