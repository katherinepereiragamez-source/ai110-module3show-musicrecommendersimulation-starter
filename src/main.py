"""
Command line runner for the Music Recommender Simulation.
Run with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs

DIVIDER     = "─" * 68
W_RANK      =  3
W_TITLE     = 24
W_ARTIST    = 18
W_SCORE     =  6


def _bar(score: float, max_score: float = 10.0, width: int = 16) -> str:
    """Compact ASCII bar representing score out of max_score."""
    filled = round(width * score / max_score)
    return "█" * filled + "░" * (width - filled)


def main() -> None:
    songs = load_songs("data/songs.csv")

    # ── user profile (keys must match score_song expectations) ──────────────
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood":  "happy",
        "target_energy":  0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # ── header ───────────────────────────────────────────────────────────────
    print(f"\n  {'MUSIC RECOMMENDER':^{W_TITLE + W_ARTIST + 30}}")
    print(f"  {DIVIDER}")
    print(f"  Profile  →  genre: {user_prefs['favorite_genre']}"
          f"  |  mood: {user_prefs['favorite_mood']}"
          f"  |  energy: {user_prefs['target_energy']}"
          f"  |  acoustic: {user_prefs['likes_acoustic']}")
    print(f"  Catalog  →  {len(songs)} songs loaded\n")

    # ── table header ─────────────────────────────────────────────────────────
    print(f"  {'#':<{W_RANK}}  {'Title':<{W_TITLE}}  {'Artist':<{W_ARTIST}}  "
          f"{'Score':>{W_SCORE}}  Bar")
    print(f"  {DIVIDER}")

    # ── rows ─────────────────────────────────────────────────────────────────
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        title  = song['title'][:W_TITLE]
        artist = song['artist'][:W_ARTIST]
        bar    = _bar(score)

        print(f"  {rank:<{W_RANK}}  {title:<{W_TITLE}}  {artist:<{W_ARTIST}}  "
              f"{score:>{W_SCORE}.2f}  {bar}")

        # parse the reason tokens out of the explanation string
        # explanation format: '"Title" by Artist — reason1; reason2 (total: X)'
        if "—" in explanation:
            reasons_part = explanation.split("—", 1)[1]
            # strip trailing (total: …)
            if "(total:" in reasons_part:
                reasons_part = reasons_part[:reasons_part.rfind("(total:")].strip()
            for reason in reasons_part.split(";"):
                reason = reason.strip().rstrip(".")
                if reason:
                    print(f"  {'':{W_RANK}}  {'':>{W_TITLE}}  {'':>{W_ARTIST}}    ↳  {reason}")
        print()

    print(f"  {DIVIDER}")
    print(f"  Scores are out of 10.0  "
          f"(genre +2 · mood +2 · energy +3 · acousticness +3)\n")


if __name__ == "__main__":
    main()
