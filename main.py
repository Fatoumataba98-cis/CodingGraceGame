import sqlite3
from schema_data import build_database, seed_database
from queries import *

def main():
    conn = sqlite3.connect("music.db")

    while True:
        print("\nMenu:")
        print("1. Show playlist tracks")
        print("2. Show tracks not in any playlist")
        print("3. Show most added track")
        print("4. Show playlist durations")
        print("0. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            name = input("Enter playlist name: ")
            rows = get_playlist_tracks(conn, name)
            for r in rows:
                print(r)

        elif choice == "2":
            rows = get_tracks_on_no_playlist(conn)
            for r in rows:
                print(r)

        elif choice == "3":
            rows = get_most_added_track(conn)
            for r in rows:
                print(r)

        elif choice == "4":
            rows = get_playlist_durations(conn)
            for r in rows:
                print(r)

        elif choice == "0":
            break

        else:
            print("Invalid option")

    conn.close()


if __name__ == "__main__":
    main()