import sqlite3

def build_database(conn):
    conn.execute("PRAGMA foreign_keys = ON")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS Artist (
        artist_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        genre TEXT NOT NULL,
        origin_city TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS Track (
        track_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        duration_seconds INTEGER NOT NULL,
        artist_id INTEGER NOT NULL REFERENCES Artist(artist_id)
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS Playlist (
        playlist_id INTEGER PRIMARY KEY,
        playlist_name TEXT NOT NULL,
        owner_name TEXT NOT NULL
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS PlaylistTrack (
        playlist_id INTEGER NOT NULL REFERENCES Playlist(playlist_id),
        track_id INTEGER NOT NULL REFERENCES Track(track_id),
        position INTEGER NOT NULL,
        PRIMARY KEY (playlist_id, track_id)
    )
    """)

    conn.commit()


def seed_database(conn):
    artists = [
        (1, "Drake", "Hip-Hop", "Toronto"),
        (2, "Taylor Swift", "Pop", "Pennsylvania"),
        (3, "Bad Bunny", "Reggaeton", "San Juan"),
        (4, "SZA", "R&B", "St. Louis"),
        (5, "The Weeknd", "R&B", "Toronto"),
        (6, "Dua Lipa", "Pop", "London")
    ]

    tracks = [
        (1, "Gods Plan", 199, 1),
        (2, "Hotline Bling", 267, 1),
        (3, "One Dance", 173, 1),
        (4, "Anti Hero", 200, 2),
        (5, "Blank Space", 231, 2),
        (6, "Cruel Summer", 178, 2),
        (7, "Titi Me Pregunto", 244, 3),
        (8, "Ojitos Lindos", 258, 3),
        (9, "Moscow Mule", 245, 3),
        (10, "Kill Bill", 153, 4),
        (11, "Good Days", 279, 4),
        (12, "Snooze", 201, 4),
        (13, "Blinding Lights", 200, 5),
        (14, "Save Your Tears", 215, 5),
        (15, "The Hills", 242, 5),
        (16, "Levitating", 203, 6),
        (17, "New Rules", 209, 6),
        (18, "Dont Start Now", 183, 6)
    ]

    playlists = [
        (1, "Workout", "Alex"),
        (2, "Chill", "Maria"),
        (3, "Study", "Chris"),
        (4, "Party", "Jamie")
    ]

    playlist_tracks = [
        (1, 1, 1), (1, 3, 2), (1, 6, 3), (1, 13, 4), (1, 16, 5),
        (2, 2, 1), (2, 10, 2), (2, 11, 3), (2, 14, 4), (2, 18, 5),
        (3, 4, 1), (3, 5, 2), (3, 8, 3), (3, 12, 4), (3, 17, 5),
        (4, 1, 1), (4, 7, 2), (4, 9, 3), (4, 13, 4), (4, 16, 5)
    ]

    conn.executemany("INSERT OR IGNORE INTO Artist VALUES (?, ?, ?, ?)", artists)
    conn.executemany("INSERT OR IGNORE INTO Track VALUES (?, ?, ?, ?)", tracks)
    conn.executemany("INSERT OR IGNORE INTO Playlist VALUES (?, ?, ?)", playlists)
    conn.executemany("INSERT OR IGNORE INTO PlaylistTrack VALUES (?, ?, ?)", playlist_tracks)

    conn.commit()


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")

    build_database(conn)
    seed_database(conn)

    try:
        conn.execute("INSERT INTO Track VALUES (100, 'Fake Song', 200, 9999)")
    except sqlite3.IntegrityError as e:
        print("IntegrityError caught:", e)
        conn.rollback()

    file_conn = sqlite3.connect("music.db")
    conn.backup(file_conn)
    file_conn.close()

    conn.close()

    print("Database saved as music.db")
    