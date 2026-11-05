import os
import requests
import musicbrainzngs

def main():
    from interface import create_gui
    create_gui() 
    print("Similar artist recommendations and similarity scores are provided by Last.fm. Album metadata is provided by MusicBrainz. Information may be incomplete or inaccurate. Please keep that in mind when using this tool.")

# LAST FM API //
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
    if "error" in data:
        print("Error:", data["message"])
        return []

    similar_artists = []
    for artist in data["similarartists"]["artist"]: # scouts for the similar artists.
        name = artist["name"]
        match = float(artist["match"]) * 100        # percentage 
        similar_artists.append((name, match)) 

    return similar_artists

# MUSICBRAINZ API // 
musicbrainzngs.set_useragent("OnTheNeedle", "0.1", "fstover25@gmail.com")


def get_artist_data(artist_name):
    result = musicbrainzngs.search_artists(artist=artist_name, limit=5)
    artists = result["artist-list"]
    artist = None

    for a in artists:
        if a["name"].lower() == artist_name.lower():
            artist = a
            break

    if artist is None:
        return None, None

    artist_id = artist["id"]
    artist_name = artist["name"]

    def get_releases(release_type):
        releases = []

        result = musicbrainzngs.browse_release_groups(
            artist=artist_id,
            release_type=[release_type],
            includes=["tags"],
            limit=100)

        for group in result["release-group-list"]:
            title = group["title"]
            release_date = group.get("first-release-date", "Unknown")
            mbid = group["id"]
            tags = []
            for tag in group.get("tag-list", []):
                tags.append(tag["name"])

            artwork_url = f"https://coverartarchive.org/release-group/{mbid}/front-500"
            release = [title, artist_name, release_date, tags[:5], mbid, artwork_url]
            releases.append(release)
        return releases

    albums = get_releases("album")
    singles = get_releases("single")
    return albums, singles

# formatting function
def format_album_info(album):
    title = album[0]
    release_date = album[2]
    tags = ", ".join(album[3])

    return f"{title}\n{release_date}  /  {tags}"


if __name__ == "__main__":
    main()