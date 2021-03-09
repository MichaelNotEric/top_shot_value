import csv

from listings import get_all_listings_from_url

def analyze_and_display_listing(url, max_price, all_listings):

    if not str.startswith(url, "https://www.nbatopshot.com/listings/p2p/"):
        raise ValueError("User passed malformed URL")
    if max_price and max_price < 0:
        raise ValueError("User passed invalid maxprice")

    listings = []
    moment = get_all_listings_from_url(url)
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
          moment['set']['flowName'] + " (" +
          str(moment['set']['flowSeriesNumber']) + ")")

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
	
    return listings
