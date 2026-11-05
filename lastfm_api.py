# LAST FM API // SEE PROJECT.PY
import os
import requests

api_key = os.getenv("LASTFM_API_KEY")
url = "https://ws.audioscrobbler.com/2.0/"

def get_similar_artists(artist_name):               # finds similar artist names, based on input
    params = {
        "method": "artist.getSimilar",
        "artist": artist_name,
        "api_key": api_key,
        "format": "json",
        "limit": 10
    }
    response = requests.get(url, params=params)
    
    data = response.json()                          # returns a json file
    if "error" in data:                             # basic error message, just in case
        print("Error:", data["message"])
        return []

    similar_artists = []
    for artist in data["similarartists"]["artist"]: # scouts for the similar artists.
        name = artist["name"]
        match = float(artist["match"]) * 100        # percentage 
        similar_artists.append((name, match))       # expand list for every artist

    return similar_artists
