import os
api_key = os.getenv("LASTFM_API_KEY")

if api_key:
    print("Last.fm API key successfully loaded")
else:
    print("API key not found")