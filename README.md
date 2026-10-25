# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world platforms like Spotify and YouTube combine two signals. **Collaborative filtering** learns from millions of users' behavior (likes, skips, replays, playlist adds) to find songs that people with similar taste enjoyed. **Content-based filtering** compares a song's attributes, such as tempo, energy, and mood, to a listener's profile. Production systems blend both, add context like time of day, and use a second ranking stage to balance relevance, freshness, and variety.

This simulation is a **content-based recommender only**. It has no data about other users and no skip or like history, so it prioritizes how closely each song's *attributes* match one user's *stated preferences*. **Energy** counts most, because it is the strongest separator in the catalog, followed by **mood** and **genre** matches, with **valence** and **acousticness** as secondary refinements. Each song gets a weighted score from 0 to 1, and the songs are then sorted to return the top K with an explanation for each.

### Song features

| Feature | Type | Role in scoring |
|---|---|---|
| `id`, `title`, `artist` | int / str | Identification and display only, not scored |
| `genre` | categorical | Match bonus against `favorite_genre` |
| `mood` | categorical | Match bonus against `favorite_mood` |
| `energy` | float 0-1 | Closeness to `target_energy` (highest weight) |
| `valence` | float 0-1 | Closeness to the user's preferred positivity |
| `acousticness` | float 0-1 | Closeness to the user's acoustic preference |
| `tempo_bpm` | float | Optional, and only after normalizing (it overlaps with energy) |
| `danceability` | float 0-1 | Optional, low priority |

### UserProfile features

| Feature | Type | Compared against |
|---|---|---|
| `favorite_genre` | str | `Song.genre` (exact match) |
| `favorite_mood` | str | `Song.mood` (exact match) |
| `target_energy` | float 0-1 | `Song.energy` (closeness) |
| `likes_acoustic` | bool | `Song.acousticness` (`True` targets high acousticness, `False` targets low) |

### Scoring rule (one song)

Numeric features reward **closeness to the user's target**, not higher or lower values: `similarity = 1 - |song_value - target|`. Categorical features score 1 for a match and 0 otherwise. The final score is a weighted sum of these similarities, with weights that sum to 1. Mood is weighted above genre, because mood describes how a song feels and genre is sparse in a small catalog.

### Ranking rule (whole list)

Every song in the catalog is scored, then the songs are sorted by score in descending order and the top K are returned, each with the reasons behind its score.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



