import argparse

from analyze_listing import analyze_and_display_listing
from graphing import graph_listing
from utils import time_func


parser = argparse.ArgumentParser(description="Analyze a TopShot Listing")

# if you want to make this implicit/positional later, you can add required=True and remove the "-u" and the "--" in from of url
parser.add_argument("-u", "--url", type=str, help="URL of a moment (required)", required=True)

parser.add_argument("-m", "--maxprice", type=int, help="Enter a maximum price you are willing to spend", required=False)
parser.add_argument("-a", "--all", action='store_const', const=True, default=False, help="Use this flag if you want to display all listings, ignoring value", required=False)
parser.add_argument("-g", "--graph", action='store_const', const=True, default=False, help="Use this flag if you want to visually display the results in a graph", required=False)

args = parser.parse_args()

try:
    listings = time_func("analyze the listing", analyze_and_display_listing, args.url, args.maxprice, args.all)
except ValueError as e:
    print(e)

if args.graph:
    time_func("graph the listing", graph_listing, listings)
