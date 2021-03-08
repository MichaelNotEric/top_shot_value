import csv
import getopt
import json
import requests
import sys

from analyze_listing import analyze__and_display_listing
from bs4 import BeautifulSoup
from graph_listing import graph_listing
from utils import time_func


listings = []
url = ''
max_price = None
all_listings = False
graph = False

argv = sys.argv[1:]
short_options = "hagm:u:"
long_options = ["help","all","graph","maxprice=","url="]

usage = ("\nUsage: python3 anaylyze.py --url <url>\n\n" +
         "Options/Arguments:\n\n" + "-u/--url: url of a moment (required)\n" +
         "-m/--maxprice: enter a maximum price you are willing to " +
         "spend\n-a/--all: show every listing, ignoring value\n" +
         "-g/--graph: display graph\n" +
         "-h/--help: display usage information\n")

try:
  args, _ = getopt.getopt(argv, short_options, long_options)
except getopt.error as err:
  print('\n'+str(err))
  print(usage)
  sys.exit(2)

for arg, val in args:
  if arg in ("-h", "--help"):
    print(usage)
    sys.exit(2)
  elif arg in ("-u", "--url"):
    url = val
  elif arg in ("-m", "--maxprice"):
    try:
      max_price = int(val)
    except:
      print("\nMax price entered incorrectly")
      print(usage)
      sys.exit(2)
  elif arg in ("-a", "--all"):
    all_listings = True
  elif arg in ("-g", "--graph"):
    graph = True

if url == '':
  print("\nURL entered incorrectly")
  print(usage)
  sys.exit(2)

time_func("analyze the listing", analyze__and_display_listing, url, max_price, all_listings, listings)

if graph:
    time_func("graph the listing", graph_listing, listings)



