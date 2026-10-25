"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import textwrap

try:
    from src.recommender import load_songs, recommend_songs  # python -m src.main
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs  # python src/main.py


# Distinct taste profiles. Categorical keys score 1 on exact match, else 0;
# numeric keys are scored by closeness, 1 - |song_value - target|.
# likes_acoustic matches the UserProfile field; False means a low-acousticness target.
PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.90,
        "target_valence": 0.85,
        "target_acousticness": 0.15,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.30,
        "target_valence": 0.55,
        "target_acousticness": 0.75,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "target_valence": 0.35,
        "target_acousticness": 0.10,
        "likes_acoustic": False,
    },
}

# Adversarial profiles: each probes a suspected weakness in score_song.
EDGE_CASE_PROFILES = {
    # genre bonus (2.0) outweighs the whole energy range
    "Conflicting: classical / sad / high energy": {
        "genre": "classical", "mood": "sad", "energy": 0.90,
    },
    # wrong genre but quiet songs should still beat perfect mood + energy matches
    "Genre trap: lofi / intense / 0.95": {
        "genre": "lofi", "mood": "intense", "energy": 0.95,
    },
    # "sad" is not a mood label in the catalog (melancholic, wistful, ...)
    "Unknown mood label: sad": {
        "genre": "none", "mood": "sad", "energy": 0.25,
    },
    # genre absent from the catalog; max score is 2.0
    "Unknown genre: k-pop": {
        "genre": "k-pop", "mood": "happy", "energy": 0.80,
    },
    # exact string matching: case and whitespace break the genre match
    "Case/whitespace: 'Pop '": {
        "genre": "Pop ", "mood": "happy", "energy": 0.80,
    },
    # energy target outside 0-1 zeroes every energy score
    "Out-of-range energy: 5.0": {
        "genre": "pop", "mood": "happy", "energy": 5.0,
    },
    # nothing matches, so ties are broken by CSV order
    "Flat scores: no matches / 0.5": {
        "genre": "none", "mood": "none", "energy": 0.50,
    },
    # likes_acoustic is never read by score_song
    "Ignored field: acoustic metal": {
        "genre": "metal", "mood": "angry", "energy": 0.97,
        "likes_acoustic": True, "target_acousticness": 0.95,
    },
    # no usable preference is rejected with a ValueError
    "Missing keys: empty profile": {},
    # non-numeric energy is rejected with a ValueError
    "Wrong type: energy 'high'": {
        "genre": "pop", "mood": "happy", "energy": "high",
    },
}


def format_table(headers: list, rows: list, max_widths: list) -> str:
    """Render rows as an ASCII grid; cells wrap to max_widths and may hold newlines."""
    def wrap(cell: str, w: int) -> list:
        lines = []
        for line in cell.split("\n"):
            # hanging indent keeps wrapped bullet text aligned under its "- "
            indent = "  " if line.startswith("- ") else ""
            lines += textwrap.wrap(line, w, subsequent_indent=indent) or [""]
        return lines

    wrapped = [[wrap(c, w) for c, w in zip(row, max_widths)] for row in rows]
    widths = [
        max([len(h)] + [len(l) for r in wrapped for l in r[i]])
        for i, h in enumerate(headers)
    ]
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def line(cells: list) -> str:
        return "| " + " | ".join(c.ljust(w) for c, w in zip(cells, widths)) + " |"

    out = [sep, line(headers), sep]
    for r in wrapped:
        height = max(len(c) for c in r)
        for n in range(height):
            out.append(line([c[n] if n < len(c) else "" for c in r]))
        out.append(sep)
    return "\n".join(out)


def print_recommendations(name: str, user_prefs: dict, songs: list, width: int = 60) -> None:
    print()
    print("=" * width)
    print(name.upper().center(width))
    print(f"prefs: {user_prefs}".center(width) if len(str(user_prefs)) < width else f"prefs: {user_prefs}")
    print("=" * width)

    try:
        recommendations = recommend_songs(user_prefs, songs, k=5)
    except ValueError as exc:
        print(f"\nREJECTED: {exc}")
        print("\n" + "=" * width)
        return

    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        rows.append([
            str(rank),
            f"{song['title']}\nby {song['artist']}",
            f"{score:.2f}",
            "\n".join(f"- {reason}" for reason in explanation.split("; ")),
        ])
    print()
    print(format_table(["#", "Song", "Score/4", "Reasons"], rows, max_widths=[3, 24, 7, 44]))

    print("\n" + "=" * width)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, songs)

    print("\n\n" + " EDGE CASES ".center(60, "#"))
    for name, user_prefs in EDGE_CASE_PROFILES.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
