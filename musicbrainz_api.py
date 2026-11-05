# MUSICBRAINZ API // SEE PROJECT.PY
import musicbrainzngs
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
