# top_shot_value

This script is meant to show NBA Top Shot listings that should be considered to have good value.

Usage: 



```
pip install -r requirements.txt

python3 analyze.py --url <URL of moment listing>
```

optional:

`--maxprice (maximum price you are willing to spend) - don't include listings over your max price`

`--all - include all listings`

`--help - shows usage information`



Example:



`python3 analyze.py --url https://www.nbatopshot.com/listings/p2p/208ae30a-a4fe-42d4-9e51-e6fd1ad2a7a9+e6e2647d-ee43-442d-95f7-38c6cfd43171 --maxprice 500`
