import tkinter as tk
import threading

from lastfm_api import get_similar_artists
from musicbrainz_api import get_artist_data


def create_gui():
    root = tk.Tk()
    root.title("On-the-Needle")
    root.geometry("960x670")
    root.minsize(600, 400)
    root.configure(bg="#3B3F42")

    # basic header
    header = tk.Frame(root, bg="#191B1D")
    header.pack(fill="x", padx=35, pady=30)

    tk.Label(
        header,
        text="On-the-Needle",
        font=("Arial", 23, "bold"),
        fg="white",
        bg="#191B1D"
    ).pack(anchor="w")

    tk.Label(
        header,
        text="Lil' music discovery tool based on Last.fm and MusicBrainz.",
        font=("Arial", 11),
        fg="#A4A9AE",
        bg="#191B1D"
    ).pack(anchor="w", pady=(5, 0))

    # search bar
    search_frame = tk.Frame(root, bg="#191B1D")
    search_frame.pack(fill="x", padx=35, pady=(0, 10))

    search_entry = tk.Entry(search_frame, font=("Arial", 13))
    search_entry.pack(side = "left", fill="x", expand=True, ipady=10)

    search_button = tk.Button(
        search_frame,
        text="Search",
        padx=20,
        pady=8
    )
    search_button.pack(side="left", padx=(12, 0))

    status_label = tk.Label(
        root,
        text="Enter an artist's name to get started.",
        font=("Arial", 10),
        fg="#A4A9AE",
        bg="#3B3F42"
    )
    status_label.pack(anchor="w", padx=35, pady=(0, 15))

    # contents (sub-frames)
    content = tk.Frame(root, bg="#191B1D")
    content.pack(fill="both", expand=True, padx=35, pady=(0, 30))

    artists_frame = tk.Frame(content, bg="#252A2D")
    artists_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

    albums_frame = tk.Frame(content, bg="#252A2D")
    albums_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))

    # scrollable results
    def create_scrollable_frame(parent):
        canvas = tk.Canvas(
            parent,
            bg="#252A2D",
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            parent,
            orient="vertical",
            command=canvas.yview
        )

        results_frame = tk.Frame(canvas, bg="#252A2D")
        results_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window(
            (0, 0),
            window=results_frame,
            anchor="nw",
            tags="results"
        )

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure("results", width=event.width)
        )

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def scroll_with_mouse(event):
            if event.delta > 0:
                canvas.yview_scroll(-1, "units")
            else:
                canvas.yview_scroll(1, "units")

        canvas.bind_all("<MouseWheel>", scroll_with_mouse)
        
        return results_frame

    # panel headings
    tk.Label(
        artists_frame,
        text="Similar artists",
        font=("Arial", 14, "bold"),
        fg="white",
        bg="#252A2D"
    ).pack(anchor="w", padx=20, pady=20)

    tk.Label(
        albums_frame,
        text="Albums",
        font=("Arial", 14, "bold"),
        fg="white",
        bg="#252A2D"
    ).pack(anchor="w", padx=20, pady=20)

    artists_results = create_scrollable_frame(artists_frame)
    albums_results = create_scrollable_frame(albums_frame)

    # initial messages
    tk.Label(
        artists_results,
        text="Similar artists will appear here.",
        fg="#A4A9AE",
        bg="#252A2D"
    ).pack(anchor="w", padx=20, pady=10)

    tk.Label(
        albums_results,
        text="Search for an artist to explore their albums.",
        fg="#A4A9AE",
        bg="#252A2D",
        wraplength=300,
        justify="left"
    ).pack(anchor="w", padx=20, pady=10)

    # search engine, using the imported functions
    def search_artist():
        artist_name = search_entry.get().strip()        # filter

        if not artist_name:
            status_label.config(text="Please enter an artist's name.")
            return

        # clear previous results
        for frame in (artists_results, albums_results):
            for widget in frame.winfo_children():
                widget.destroy()

        status_label.config(text=f"Searching for {artist_name}...")
        search_button.config(state="disabled")

        # fetch information in the background
        def fetch_data():
            try:
                similar_artists = get_similar_artists(artist_name)
                albums, singles = get_artist_data(artist_name)

                root.after(
                    0,
                    display_results,
                    artist_name,
                    similar_artists,
                    albums,
                    singles
                )

            except Exception as error:
                root.after(0, display_error, error)

        search_thread = threading.Thread(target=fetch_data, daemon=True)
        search_thread.start()

    # display search results
    def display_results(artist_name, similar_artists, albums, singles):
        search_button.config(state="normal")

        if similar_artists:
            for name, match in similar_artists:
                tk.Label(
                    artists_results,
                    text=f"{name}  /  {match:.1f}%",
                    font=("Arial", 12),
                    fg="white",
                    bg="#252A2D"
                ).pack(anchor="w", padx=20, pady=8)

        else:
            tk.Label(
                artists_results,
                text="No similar artists found.",
                fg="#A4A9AE",
                bg="#252A2D"
            ).pack(anchor="w", padx=20, pady=10)

        # check if artist exists in MusicBrainz
        if albums is None and singles is None:
            tk.Label(
                albums_results,
                text="Artist not found in MusicBrainz.",
                fg="#A4A9AE",
                bg="#252A2D"
            ).pack(anchor="w", padx=20)

            status_label.config(text="Search completed.")
            return

        # display albums
        if not albums:
            tk.Label(
                albums_results,
                text="No albums found.",
                fg="#A4A9AE",
                bg="#252A2D"
            ).pack(anchor="w", padx=20)

        else:
            for album in albums:
                title = album[0]
                release_date = album[2]
                tags = ", ".join(album[3])

                tk.Label(
                    albums_results,
                    text=f"{title}\n{release_date}  /  {tags}",
                    font=("Arial", 11),
                    fg="white",
                    bg="#252A2D",
                    justify="left",
                    wraplength=350
                ).pack(anchor="w", padx=20, pady=10)

        # singles
        tk.Label(
            albums_results,
            text="Singles",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#252A2D"
        ).pack(anchor="w", padx=20, pady=(25, 10))

        if not singles:
            tk.Label(
                albums_results,
                text="No singles found.",
                fg="#A4A9AE",
                bg="#252A2D"
            ).pack(anchor="w", padx=20)

        else:
            for single in singles:
                title = single[0]
                release_date = single[2]
                tags = ", ".join(single[3])

                tk.Label(
                    albums_results,
                    text=f"{title}\n{release_date}  /  {tags}",
                    font=("Arial", 11),
                    fg="white",
                    bg="#252A2D",
                    justify="left",
                    wraplength=350
                ).pack(anchor="w", padx=20, pady=10)

        status_label.config(text=f"Results for {artist_name}")

    # display errors
    def display_error(error):
        search_button.config(state="normal")
        status_label.config(text=f"Something went wrong: {error}")

    # connect search button and Enter key
    search_button.config(command=search_artist)
    search_entry.bind("<Return>", lambda event: search_artist())

    root.mainloop()

if __name__ == "__main__":
    create_gui()
