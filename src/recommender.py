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


# ---------------------------------------------------------------------------
# Sample user profile — used by main.py and as a scoring reference
# ---------------------------------------------------------------------------
SAMPLE_USER = UserProfile(
    favorite_genre="lofi",
    favorite_mood="chill",
    target_energy=0.40,   # prefers calm, low-intensity tracks
    likes_acoustic=True,  # gravitates toward acoustic/organic sound
)

# Critique addressed (see notes below):
# A profile of only genre + mood risks being too narrow — two lofi songs
# with identical genre/mood could score the same even if one is twice as
# energetic as the other.  Adding target_energy and likes_acoustic gives the
# scorer continuous signal so it can cleanly separate "intense rock" (high
# energy, low acousticness) from "chill lofi" (low energy, high acousticness)
# without relying solely on categorical matches.


# ---------------------------------------------------------------------------
# Scoring — returns (total_score, reasons) together
# ---------------------------------------------------------------------------

# Point values per feature (max possible total = 10.0)
POINTS = {
    "genre":       2.0,   # exact genre match
    "mood":        2.0,   # exact mood match
    "energy":      3.0,   # scaled by proximity to target (0.0–3.0)
    "acousticness":3.0,   # scaled by how well it fits likes_acoustic (0.0–3.0)
}


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Return a (score, reasons) tuple rating how well a song matches user preferences (0.0–10.0)."""
    total   = 0.0
    reasons = []

    # --- Genre (binary, +2.0) ---
    if song.get("genre") == user_prefs.get("favorite_genre"):
        pts = POINTS["genre"]
        total += pts
        reasons.append(f"genre match (+{pts:.1f})")

    # --- Mood (binary, +2.0) ---
    if song.get("mood") == user_prefs.get("favorite_mood"):
        pts = POINTS["mood"]
        total += pts
        reasons.append(f"mood match (+{pts:.1f})")

    # --- Energy proximity (continuous, 0.0–3.0) ---
    # Award full 3.0 when energy == target; scales linearly to 0.0 at distance ≥ 1.0
    target_energy = float(user_prefs.get("target_energy", 0.5))
    energy_diff   = abs(float(song.get("energy", 0.5)) - target_energy)
    energy_pts    = round(max(0.0, POINTS["energy"] * (1.0 - energy_diff)), 2)
    total += energy_pts
    reasons.append(f"energy score (+{energy_pts:.1f})")

    # --- Acousticness fit (continuous, 0.0–3.0) ---
    # likes_acoustic=True  → reward high acousticness
    # likes_acoustic=False → reward low acousticness
    likes_acoustic  = bool(user_prefs.get("likes_acoustic", False))
    acousticness    = float(song.get("acousticness", 0.5))
    raw_fit         = acousticness if likes_acoustic else (1.0 - acousticness)
    acoustic_pts    = round(POINTS["acousticness"] * raw_fit, 2)
    total += acoustic_pts
    reasons.append(f"acousticness fit (+{acoustic_pts:.1f})")

    return round(total, 2), reasons


# ---------------------------------------------------------------------------
# OOP interface
# ---------------------------------------------------------------------------

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top-k songs ranked by match score."""
        prefs = asdict(user)
        scored = sorted(
            self.songs,
            key=lambda s: score_song(prefs, asdict(s))[0],
            reverse=True,
        )
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a plain-English explanation for a single recommendation."""
        total, reasons = score_song(asdict(user), asdict(song))
        reason_str = "; ".join(reasons)
        return f'"{song.title}" by {song.artist} — {reason_str} (total: {total:.2f}/10.0).'


# ---------------------------------------------------------------------------
# Functional interface (used by src/main.py)
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file, casting numeric fields to float/int, and return a list of dicts."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"  Loaded {len(songs)} songs.")
    return songs


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
) -> List[Tuple[Dict, float, str]]:
    """Score every song against user_prefs, sort by score descending, and return the top-k (song, score, explanation) tuples."""
    results = []
    for d in songs:
        total, reasons = score_song(user_prefs, d)
        explanation = (
            f'"{d["title"]}" by {d["artist"]} — '
            + "; ".join(reasons)
            + f" (total: {total:.2f}/10.0)."
        )
        results.append((d, total, explanation))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:k]
