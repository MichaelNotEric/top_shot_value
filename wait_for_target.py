import argparse
from os import system
import time
import webbrowser
import winsound

from listings import get_lowest_price_from_url, price_lower_than_target, print_listing_details, get_listing_page

parser = argparse.ArgumentParser(description="Wait for a topshot price")

# if you want to make this implicit/positional later, you can add required=True and remove the "-u" and the "--" in from of url
parser.add_argument("-u", "--url", type=str, help="URL of a moment (required)", required=True)

parser.add_argument("-t", "--target", type=float, help="Enter a target price", required=True)

args = parser.parse_args()

_ = system('cls')


page = get_listing_page(args.url)
print("Target Price: {}          ".format("{:.2f}".format(args.target)), end='')
print_listing_details(page)

found = False
while not found:
    try:
        found = price_lower_than_target(args.url, args.target)
    except:
        pass
    time.sleep(10)

if found:
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
    webbrowser.open_new_tab(args.url)