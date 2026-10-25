"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs  # python -m src.main
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs  # python src/main.py


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Taste profile: an upbeat pop listener who likes produced, positive music
    user_prefs = {
        # categorical: exact match scores 1, otherwise 0
        "genre": "pop",
        "mood": "happy",

        # numeric: scored by closeness, 1 - |song_value - target|
        "energy": 0.80,
        "target_valence": 0.80,
        "target_acousticness": 0.20,

        # matches the UserProfile field; False means a low-acousticness target
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    width = 60
    print()
    print("=" * width)
    print(f"TOP {len(recommendations)} RECOMMENDATIONS".center(width))
    print(
        f"profile: {user_prefs['genre']} / {user_prefs['mood']} / "
        f"energy {user_prefs['energy']:.2f}".center(width)
    )
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} by {song['artist']}")
        print(f"    Score: {score:.2f} / 4.00")
        print("    Why:")
        for reason in explanation.split("; "):
            print(f"      - {reason}")

    print("\n" + "=" * width)


if __name__ == "__main__":
    main()
