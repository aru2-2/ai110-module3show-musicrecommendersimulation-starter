import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

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

# Algorithm Recipe (max score 4.0):
#   +2.0 genre match
#   +1.0 mood match
#   +0.0 to 1.0 energy similarity: 1 - |song energy - target energy|
GENRE_POINTS = 2.0
MOOD_POINTS = 1.0
ENERGY_POINTS = 1.0


def _normalize(label: str) -> str:
    """Lowercase a label and trim/collapse whitespace so 'Pop ' matches 'pop'."""
    return " ".join(str(label).lower().split())


def validate_prefs(user_prefs: Dict) -> None:
    """Raise ValueError if the profile has no usable preference or a non-numeric energy."""
    if not any(user_prefs.get(key) is not None for key in ("genre", "mood", "energy")):
        raise ValueError("profile needs at least one of 'genre', 'mood' or 'energy'")

    energy = user_prefs.get("energy")
    if energy is not None and (isinstance(energy, bool) or not isinstance(energy, (int, float))):
        raise ValueError(f"'energy' must be a number, got {energy!r}")


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song (max 4.0) and return it with a list of human-readable reasons.

    Genre, mood and energy are each optional in user_prefs; a missing one is skipped.
    """
    score = 0.0
    reasons: List[str] = []

    genre = user_prefs.get("genre")
    if genre is not None and _normalize(song["genre"]) == _normalize(genre):
        score += GENRE_POINTS
        reasons.append(f"genre match: {song['genre']} (+{GENRE_POINTS:.1f})")

    mood = user_prefs.get("mood")
    if mood is not None and _normalize(song["mood"]) == _normalize(mood):
        score += MOOD_POINTS
        reasons.append(f"mood match: {song['mood']} (+{MOOD_POINTS:.1f})")

    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        similarity = max(0.0, 1.0 - abs(float(song["energy"]) - target_energy))
        energy_score = ENERGY_POINTS * similarity
        score += energy_score
        reasons.append(
            f"energy {float(song['energy']):.2f} vs target {target_energy:.2f} "
            f"(+{energy_score:.2f})"
        )

    return score, reasons


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file, converting numeric columns to int/float."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            for key in ("energy", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            songs.append(row)
    return songs


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top k (song, score, reasons) tuples, sorted from highest to lowest score."""
    validate_prefs(user_prefs)
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked[:k]]


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Store the song catalog to recommend from."""
        self.songs = songs

    @staticmethod
    def _prefs(user: UserProfile) -> Dict:
        """Convert a UserProfile into the prefs dict that score_song expects."""
        return {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the k best-matching songs for the user, highest score first."""
        prefs = self._prefs(user)
        ranked = sorted(
            self.songs,
            key=lambda s: score_song(prefs, asdict(s))[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return the scoring reasons for a song as a single "; "-joined string."""
        _, reasons = score_song(self._prefs(user), asdict(song))
        return "; ".join(reasons)
