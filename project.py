from lastfm_api import get_similar_artists
from musicbrainz_api import get_artist_data
from interface import create_gui

def main():
    '''
    artist_name = input("Enter an artist: ")
    # Last FM API
    similar_artists = get_similar_artists(artist_name)

    for name, match in similar_artists:   # for name, match because both are used
        print(f"{name} / {match:.1f}% similarity")
        
    # MusicBrainz API
    albums = get_artist_data(artist_name)

    if albums is None:
        print("Artist not found.")
        return

    print(f"\nFound {len(albums)} albums by {artist_name}:\n")

    for album in albums:
        print(f"{album[0]} ({album[2]})")
        print(f"Tags: {', '.join(album[3])}")
        print(f"MBID: {album[4]}")
        print(f"Artwork: {album[5]}\n")
    '''
    create_gui()
        
    print("Similar artist recommendations and similarity scores are provided by Last.fm. Album metadata is provided by MusicBrainz. Information may be incomplete or inaccurate. Please keep that in mind when using this tool.")


if __name__ == "__main__":
    main()