"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(label: str, user_prefs: dict, songs: list) -> None:
    """Runs recommend_songs for one profile and prints its top 5 with a header."""
    print("=" * 60)
    print(f"Profile: {label}")
    print("=" * 60)

    recommendations = recommend_songs(user_prefs, songs, k=5)
    for song, score, reasons in recommendations:
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {', '.join(reasons)}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Each profile uses the five keys the scoring recipe expects.
    profiles = {
        "Starter (Pop Happy)": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.8,
            "target_valence": 0.9,
            "target_acousticness": 0.1,
        },
        "High-Energy Pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.9,
            "target_valence": 0.85,
            "target_acousticness": 0.1,
        },
        "Chill Lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.2,
            "target_valence": 0.5,
            "target_acousticness": 0.85,
        },
        "Deep Intense Rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.9,
            "target_valence": 0.4,
            "target_acousticness": 0.1,
        },
    }

    for label, user_prefs in profiles.items():
        print_recommendations(label, user_prefs, songs)


if __name__ == "__main__":
    main()
