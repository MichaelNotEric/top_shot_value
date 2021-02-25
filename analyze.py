import json
import sys
import getopt
import requests
from bs4 import BeautifulSoup

listings = []
temp = []

url = ''
max_price = None

argv = sys.argv[1:]

short_options = "hm:u:"
long_options = ["help","maxprice=","url="]

try:
  args, vals = getopt.getopt(argv, short_options, long_options)
except getopt.error as err:
  print('\n'+str(err))
  print("\nUsage: python3 anaylyze.py --url <url>\n\nOptions:\n\n-m/--maxprice: enter a maximum price you are willing to spend\n-h/--help: display usage information\n")
  sys.exit(2)

for arg, val in args:
  if arg in ("-h", "--help"):
    print("\nUsage: python3 anaylyze.py --url <url>\n\nOptions:\n\n-m/--maxprice: enter a maximum price you are willing to spend\n-h/--help: display usage information\n")
    sys.exit(2)
  elif arg in ("-u", "--url"):
    url = val
  elif arg in ("-m", "--maxprice"):
    try:
      max_price = int(val)
    except:
      print("\nMax price entered incorrectly")
      print("\nUsage: python3 anaylyze.py --url <url>\n\nOptions:\n\n-m/--maxprice: enter a maximum price you are willing to spend\n-h/--help: display usage information\n")
      sys.exit(2)

if url == '':
  print("\nURL entered incorrectly")
  print("\nUsage: python3 anaylyze.py --url <url>\n\nOptions:\n\n-m/--maxprice: enter a maximum price you are willing to spend\n-h/--help: display usage information\n")
  sys.exit(2)


page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
script = soup.find('script', id='__NEXT_DATA__')
json_object = json.loads(script.contents[0])

moment_listings = (json_object['props']['pageProps']['moment']['momentListings'])

for moment in moment_listings:
  serial = int(float(moment['moment']['flowSerialNumber']))
  price = int(float(moment['moment']['price']))
  if not max_price:
    listings.insert(0,(serial, price))
  elif price <= max_price:
    listings.insert(0,(serial, price))

i = 0
while i < len(listings):
  for l in listings:
    if listings[i][1] == l[1] and listings[i][0] > l[0]:
      listings.pop(i)
      i = i - 1

  i = i + 1

i = 0
while i < len(listings):
  for l in listings:
    if listings[i][1] > l[1] and listings[i][0] > l[0]:
      listings.pop(i)
      i = i - 1

  i = i + 1

with open('out.txt','w') as f:
  for l in listings:
    f.write(str(l[0]) + ',' + str(l[1]) + '\n')
