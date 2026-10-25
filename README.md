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

This simulation is a **content-based recommender only**. It has no data about other users and no skip or like history, so it prioritizes how closely each song's *attributes* match one user's *stated preferences*. Each song gets a score from 0 to 4.0 based on **genre**, **mood**, and **energy**. The songs are then sorted to return the top K with an explanation for each.

### Data flow

```
INPUT                    PROCESS (the loop)                        OUTPUT
user_prefs               load_songs("data/songs.csv")
{genre, mood, energy} ─► for each song in the CSV:             ─► sort by score (desc)
                           score_song(user_prefs, song)            take the first K
                           -> (score, reasons)                     -> Top K (song, score, explanation)
```

### Song features

| Feature | Type | Role in scoring |
|---|---|---|
| `id`, `title`, `artist` | int / str | Identification and display only, not scored |
| `genre` | categorical | Match bonus against `favorite_genre` |
| `mood` | categorical | Match bonus against `favorite_mood` |
| `energy` | float 0-1 | Closeness to `target_energy` |
| `valence`, `acousticness`, `tempo_bpm`, `danceability` | float | Loaded but **not scored yet** (possible future refinements) |

### UserProfile features

| Feature | Type | Compared against |
|---|---|---|
| `favorite_genre` | str | `Song.genre` (exact match) |
| `favorite_mood` | str | `Song.mood` (exact match) |
| `target_energy` | float 0-1 | `Song.energy` (closeness) |
| `likes_acoustic` | bool | Stored on the profile but **not used in scoring yet** |

### Scoring rule (one song)

Each song is judged on its own against the user's preferences. Categorical features (genre, mood) are all-or-nothing: a match earns its points and a miss earns none. Energy, the only numeric feature scored, rewards **closeness to the user's target**, not higher or lower values: `similarity = 1 - |song_energy - target_energy|`. The final score is the sum of these parts, with genre weighted highest (2.0), then mood (1.0), then energy (up to 1.0). The recipe below gives the exact points.

### Algorithm Recipe (max score 4.0)

| Rule | Points |
|---|---|
| Genre matches `favorite_genre` (exact) | **+2.0** |
| Mood matches `favorite_mood` (exact) | **+1.0** |
| Energy similarity: `1 - abs(song.energy - target_energy)`, floored at 0 | **+0.0 to +1.0** |

`score_song` also returns a plain-language reason for each part that contributed.

### Ranking rule (whole list)

A single song's score says nothing on its own, so the system scores **every** song in the catalog, sorts by score in descending order, and returns the top K, each with the reasons behind its score. Ties keep CSV order, because Python's sort is stable.

### Expected biases

- **Genre over-prioritization.** A genre match is worth 2.0, which is half the maximum score. A same-genre song with the wrong mood and a poor energy fit (about 2.0 to 2.5) can still beat an off-genre song that matches the mood and energy exactly (at most 2.0). Great songs from adjacent genres can be buried.
- **Exact-match brittleness.** `rock` vs `metal`, or `chill` vs `relaxed`, count as total misses. There is no notion of similar genres or moods.
- **Energy is the only graded signal.** Songs that tie on genre and mood are separated only by energy. Valence, acousticness, tempo, and danceability are ignored, so two songs with very different feel can score the same.
- **Small, uneven catalog.** Genres with only one or two songs will fill the top K with near-misses from other genres, and users with a rare favorite genre get weaker results.
- **Filter bubble.** Scoring rewards similarity to stated tastes, so the system never surfaces anything unfamiliar and cannot help a user discover new genres.

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

Output of `python -m src.main` for a pop / happy listener with a target energy of 0.80:

```
Loaded songs: 18

============================================================
                   TOP 5 RECOMMENDATIONS
             profile: pop / happy / energy 0.80
============================================================

#1  Sunrise City by Neon Echo
    Score: 3.98 / 4.00
    Why:
      - genre match: pop (+2.0)
      - mood match: happy (+1.0)
      - energy 0.82 vs target 0.80 (+0.98)

#2  Gym Hero by Max Pulse
    Score: 2.87 / 4.00
    Why:
      - genre match: pop (+2.0)
      - energy 0.93 vs target 0.80 (+0.87)

#3  Rooftop Lights by Indigo Parade
    Score: 1.96 / 4.00
    Why:
      - mood match: happy (+1.0)
      - energy 0.76 vs target 0.80 (+0.96)

#4  Bass Cathedral by Kilo Verse
    Score: 1.00 / 4.00
    Why:
      - energy 0.80 vs target 0.80 (+1.00)

#5  Night Drive Loop by Neon Echo
    Score: 0.95 / 4.00
    Why:
      - energy 0.75 vs target 0.80 (+0.95)

============================================================
```

---

## Recommendations for Multiple Profiles

Output of `python -m src.main` for the three taste profiles (top 5 each):

### High-Energy Pop

```
============================================================
                      HIGH-ENERGY POP                       
prefs: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9, 'target_valence': 0.85, 'target_acousticness': 0.15, 'likes_acoustic': False}
============================================================

#1  Sunrise City by Neon Echo
    Score: 3.92 / 4.00
    Why:
      - genre match: pop (+2.0)
      - mood match: happy (+1.0)
      - energy 0.82 vs target 0.90 (+0.92)

#2  Gym Hero by Max Pulse
    Score: 2.97 / 4.00
    Why:
      - genre match: pop (+2.0)
      - energy 0.93 vs target 0.90 (+0.97)

#3  Rooftop Lights by Indigo Parade
    Score: 1.86 / 4.00
    Why:
      - mood match: happy (+1.0)
      - energy 0.76 vs target 0.90 (+0.86)

#4  Storm Runner by Voltline
    Score: 0.99 / 4.00
    Why:
      - energy 0.91 vs target 0.90 (+0.99)

#5  Solar Parade by Calle Sol
    Score: 0.98 / 4.00
    Why:
      - energy 0.88 vs target 0.90 (+0.98)

============================================================
```

### Chill Lofi

```
============================================================
                         CHILL LOFI                         
prefs: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.3, 'target_valence': 0.55, 'target_acousticness': 0.75, 'likes_acoustic': True}
============================================================

#1  Library Rain by Paper Lanterns
    Score: 3.95 / 4.00
    Why:
      - genre match: lofi (+2.0)
      - mood match: chill (+1.0)
      - energy 0.35 vs target 0.30 (+0.95)

#2  Midnight Coding by LoRoom
    Score: 3.88 / 4.00
    Why:
      - genre match: lofi (+2.0)
      - mood match: chill (+1.0)
      - energy 0.42 vs target 0.30 (+0.88)

#3  Focus Flow by LoRoom
    Score: 2.90 / 4.00
    Why:
      - genre match: lofi (+2.0)
      - energy 0.40 vs target 0.30 (+0.90)

#4  Spacewalk Thoughts by Orbit Bloom
    Score: 1.98 / 4.00
    Why:
      - mood match: chill (+1.0)
      - energy 0.28 vs target 0.30 (+0.98)

#5  Porch Light Lullaby by Wren and Willow
    Score: 1.00 / 4.00
    Why:
      - energy 0.30 vs target 0.30 (+1.00)

============================================================
```

### Deep Intense Rock

```
============================================================
                     DEEP INTENSE ROCK                      
prefs: {'genre': 'rock', 'mood': 'intense', 'energy': 0.92, 'target_valence': 0.35, 'target_acousticness': 0.1, 'likes_acoustic': False}
============================================================

#1  Storm Runner by Voltline
    Score: 3.99 / 4.00
    Why:
      - genre match: rock (+2.0)
      - mood match: intense (+1.0)
      - energy 0.91 vs target 0.92 (+0.99)

#2  Gym Hero by Max Pulse
    Score: 1.99 / 4.00
    Why:
      - mood match: intense (+1.0)
      - energy 0.93 vs target 0.92 (+0.99)

#3  Pulse Garden by Fractal Bloom
    Score: 0.97 / 4.00
    Why:
      - energy 0.95 vs target 0.92 (+0.97)

#4  Solar Parade by Calle Sol
    Score: 0.96 / 4.00
    Why:
      - energy 0.88 vs target 0.92 (+0.96)

#5  Iron Requiem by Grave Signal
    Score: 0.95 / 4.00
    Why:
      - energy 0.97 vs target 0.92 (+0.95)

============================================================
```

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



