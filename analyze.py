import json
import sys
import getopt
import requests
from bs4 import BeautifulSoup

listings = []

url = ''
max_price = None

argv = sys.argv[1:]

short_options = "hm:u:"
long_options = ["help","maxprice=","url="]

usage = ("\nUsage: python3 anaylyze.py --url <url>\n\nOptions:\n\n"
        + "-m/--maxprice: enter a maximum price you are willing to "
        + "spend\n-h/--help: display usage information\n")

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

# remove listings of equal or higher price but higher serial number
i = 0
while i < len(listings):
  for l in listings:
    if len(listings) == 0:
      print("Something went wrong, please try again")
      sys.exit(2)
    if (listings[i][1] >= l[1] and listings[i][0] > l[0] and
        listings[i][0] != int(play['stats']['jerseyNumber'])):
      listings.pop(i)
      i = i - 1

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

with open('out.txt','w') as f:
  if jersey_listing:
    print("#" + str(jersey_listing[0]) + " - $" +
          str(jersey_listing[1]) + " (Jersey Number)\n")

    f.write(str(jersey_listing[0]) + "," + str(jersey_listing[1]) +
            " (Jersey Number)\n\n")

  for l in listings:
    print("#" + str(l[0]) + " - $" + str(l[1]))
    f.write(str(l[0]) + ',' + str(l[1]) + '\n')

print("\nCheck out.txt for results!\n")
