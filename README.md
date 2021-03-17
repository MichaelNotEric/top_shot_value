# top_shot_value

This script is meant to show NBA Top Shot listings that should be considered to have good value.

## Usage:

```
pip install -r requirements.txt
```

### To Analyze a Listing:

`python3 analyze.py --url <URL of moment listing>`

optional:

`--maxprice (maximum price you are willing to spend) - don't include listings over your max price`

`--all - include all listings, ignoring value`

`--graph - display results in a graph`

`--help - shows usage information`



Example:



`python3 analyze.py --url https://www.nbatopshot.com/listings/p2p/208ae30a-a4fe-42d4-9e51-e6fd1ad2a7a9+e6e2647d-ee43-442d-95f7-38c6cfd43171 --maxprice 500 --graph`


### To retrieve a list of lowest prices:

1. Add a file named input.txt to this directory.
2. In the file, add a url to a listing per line
3. Run `python3 prices.py`
4. Inspect output.txt. Each line will contain the lowest price for the corresponding line in input.txt

### To monitor a listing

`python3 wait_for_target.py --url <URL of moment listing> --target <target_price>`

When the moment's lowest price falls below the target price it will make a noise and open a tab for the listing.