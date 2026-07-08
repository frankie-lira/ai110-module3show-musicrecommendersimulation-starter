import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Stores the catalog of songs this recommender will rank."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs for the given user profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation of why a song was recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Reads songs from a CSV file into a list of dicts, converting numeric fields to floats."""
    numeric_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = dict(row)
            for field in numeric_fields:
                song[field] = float(song[field])
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song against user prefs, returning (total_score, reasons) per the Phase 2 recipe."""
    reasons: List[str] = []

    acoustic_pts = 30 * (1 - abs(song["acousticness"] - user_prefs["target_acousticness"]))
    reasons.append(f"Acousticness match: +{acoustic_pts:.1f}")

    energy_pts = 20 * (1 - abs(song["energy"] - user_prefs["target_energy"]))
    reasons.append(f"Energy match: +{energy_pts:.1f}")

    valence_pts = 5 * (1 - abs(song["valence"] - user_prefs["target_valence"]))
    reasons.append(f"Valence match: +{valence_pts:.1f}")

    genre_pts = 15 if song["genre"] == user_prefs["favorite_genre"] else 0
    if genre_pts:
        reasons.append(f"Genre match ({song['genre']}): +{genre_pts}")

    mood_pts = 10 if song["mood"] == user_prefs["favorite_mood"] else 0
    if mood_pts:
        reasons.append(f"Mood match ({song['mood']}): +{mood_pts}")

    total_score = acoustic_pts + energy_pts + valence_pts + genre_pts + mood_pts
    return total_score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song and returns the top k as (song, score, reasons) tuples, highest score first."""
    # Score each song, pairing it with its total and reasons.
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))

    # sorted() builds a NEW sorted list and leaves `scored` untouched; .sort() would
    # mutate `scored` in place and return None. We use sorted() so the caller's data
    # is never reordered as a side effect. key picks the score (index 1); reverse=True
    # ranks highest-first.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    return ranked[:k]
