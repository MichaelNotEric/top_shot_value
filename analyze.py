import csv
import json
import sys
import getopt
import requests
from bs4 import BeautifulSoup

import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np

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
         "spend\n-a/--all: show every listing\n" +
         "-g/--graph: display graph\n" +
         "-h/--help: display usage information\n")

try:
  args, vals = getopt.getopt(argv, short_options, long_options)
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

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
script = soup.find('script', id='__NEXT_DATA__')
json_object = json.loads(script.contents[0])
moment = json_object['props']['pageProps']['moment']
play = moment['play']

moments = moment['momentListings']

# add each listing at or below max price if it was passed in
for m in moments:
  serial = int(float(m['moment']['flowSerialNumber']))
  price = int(float(m['moment']['price']))
  if not max_price:
    listings.insert(0,(serial, price))
  elif price <= max_price:
    listings.insert(0,(serial, price))

if not all_listings:
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

print("\n" + play['stats']['playerName'] + " " +
      play['stats']['playCategory'] + " - " +
      moment['set']['flowName'] + " " +
      str(moment['set']['flowSeriesNumber']))

print(str(moment['circulationCount']) + " copies exist")

print(str(moment['momentListingCount']) +
      " copies are listed for sale between $" +
      str(int(float(moment['priceRange']['min']))) +
      " and $" + str(int(float(moment['priceRange']['max']))))

if max_price:
  print("\nMax Price set to $" + str(max_price) + "\n")
else:
  print("\nNo Max Price was set\n")

jersey_listing = None
i = 0
while i < len(listings):
  if listings[i][0] == int(play['stats']['jerseyNumber']):
    jersey_listing = "#" + str(listings[i][0]) + " - $" + str(listings[i][1])
    jersey_listing = (listings[i][0],listings[i][1])
    listings.pop(i)
    i = i - 1

  i = i + 1

with open('out.csv','w') as f:
  writer = csv.writer(f, delimiter=',')
  if jersey_listing:
    print("#" + str(jersey_listing[0]) + " - $" +
          str(jersey_listing[1]) + " (Jersey Number)\n")

    writer.writerow([jersey_listing[0], jersey_listing[1]])

  for l in listings:
    print("#" + str(l[0]) + " - $" + str(l[1]))
    writer.writerow([l[0], l[1]])

print("\nCheck out.csv for results in an excel-friendly format!\n")

if graph:
  first = lambda x:x[0]
  second = lambda x:x[1]
  serials = map(first, listings)
  prices = map(second, listings)
  x = np.fromiter(prices, dtype=np.int)
  y = np.fromiter(serials, dtype=np.int)

  area = (10 * np.ones(len(x),dtype=np.int))  # 0 to 15 point radii

  plt.scatter(x, y, s=area, alpha=0.5)
  plt.show()
