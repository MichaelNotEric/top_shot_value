import argparse
from os import system, name
import datetime
import time
import webbrowser
if name == 'nt':
    import winsound

from listings import get_lowest_price_from_url, price_lower_or_equal_to_target, print_listing_details, get_listing_page, get_all_listings_below_target_price_and_serial
from graphing import graph_price_at_time

parser = argparse.ArgumentParser(description="Wait for a topshot price")

# if you want to make this implicit/positional later, you can add required=True and remove the "-u" and the "--" in from of url
parser.add_argument("-u", "--url", type=str, help="URL of a moment (required)", required=True)

parser.add_argument("-t", "--target", type=float, help="Enter a target price", required=True)

parser.add_argument("-s", "--serial", type=int, default=None, help="Maximum serial number", required=False)

parser.add_argument("-i", "--interval", type=int, default=10, help="Polling interval in seconds", required=False)

args = parser.parse_args()

# for windows
if name == 'nt':
    _ = system('cls')
# for mac and linux(here, os.name is 'posix')
else:
    _ = system('clear')


page = get_listing_page(args.url)
print("Target Price: {}          ".format("{:.2f}".format(args.target)), end='')
if args.serial:
    print("\nTarget Serial: {}".format(args.serial))
print_listing_details(page)

if args.interval < 1:
    interval = 10
else:
    interval = args.interval

	
listings = []
moment = None
play = None
moments	= None
	
found = False
found_serial = False
graph = None
while not found and not found_serial:
    try:
        if not args.serial:
            found, price = price_lower_or_equal_to_target(args.url, args.target)
            if found: break
        else:
            listings, moment, play, moments, jersey_listing = get_all_listings_below_target_price_and_serial(args.url, args.target, args.serial)
            found_serial = len(listings) > 0
            if found_serial: break
            #graph_price_at_time(graph, datetime.datetime.now(), price)
    except:
        print("\nOops")
    time.sleep(args.interval)
	
if (found_serial):
    print("\n" + play['stats']['playerName'] + " " +
        play['stats']['playCategory'] + " - " +
        moment['set']['flowName'] + " (" +
        str(moment['set']['flowSeriesNumber']) + ")")

    print(str(moment['circulationCount']) + " copies exist")

    print(str(moment['momentListingCount']) +
        " copies are listed for sale between $" +
        str(int(float(moment['priceRange']['min']))) +
        " and $" + str(int(float(moment['priceRange']['max']))))

    if jersey_listing:
        print("#" + str(jersey_listing[0]) + " - $" +
            str(jersey_listing[1]) + " (Jersey Number)\n")

    for l in listings:
        print("#" + str(l[0]) + " - $" + str(l[1]))
		
    if name == 'nt':
        winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
	# TODO else for linux/mac (find a library or whatever)
    webbrowser.open_new_tab(args.url)		


if found:
    if name == 'nt':
        winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
	# TODO else for linux/mac (find a library or whatever)
    webbrowser.open_new_tab(args.url)