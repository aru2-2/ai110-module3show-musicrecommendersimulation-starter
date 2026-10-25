# 🎵 Music Recommender Simulation

## Project Summary

My version, **VibeMatch 1.0**, is a small content-based recommender. It reads a catalog of 18 songs from `data/songs.csv`. A listener gives a favorite genre, a favorite mood and a target energy. Every song gets a score out of 4.0: up to 2.0 for genre, 1.0 for mood and 1.0 for how close its energy is to the target. The top 5 songs are shown, each with plain-language reasons for its score. I tested it on three realistic listeners and ten tricky edge cases to see where the rules work and where they break.

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

A single song's score says nothing on its own, so the system scores **every** song in the catalog, sorts by score in descending order, and returns the top K, each with the reasons behind its score. Ties keep CSV order, because Python's sort is stable. The top K is then picked with the diversity penalty described below.

### Diversity and fairness

Ranking purely by score lets one artist or genre fill the whole top K (the filter-bubble bias below). The recommender counters this with a **diversity penalty** applied while the list is built:

1. Pick the highest-scoring song first, with no penalty.
2. Before each following pick, every remaining song loses points for each already-picked song it repeats:

| Repeat | Penalty (per already-picked song) |
|---|---|
| Same artist | **-0.75** |
| Same genre | **-0.25** |

3. Pick the best adjusted score, update the counts, and repeat until K songs are chosen.

Penalties stack, so a third song by the same artist loses 1.5. The penalty shows up in each song's reasons (for example `genre repeat: pop (-0.25)`), and the displayed score is the adjusted one, so a song's score can drop below what its genre, mood and energy matches alone would give.

**Why this is fairer:**
- **Artists:** a single prolific artist can't crowd out others whose songs score almost as well, so smaller artists get exposure.
- **Listeners:** the top K covers more than one artist or genre, which gives the user some variety instead of five near-copies.

**Trade-offs:**
- The genre penalty is deliberately small (0.25) next to the 2.0 genre match, so it only reorders close calls. A user who wants only their favorite genre still gets it.
- A relevant song can be pushed down in favor of a slightly weaker one from a different artist. Raise or lower `ARTIST_PENALTY` and `GENRE_PENALTY` in `src/recommender.py` to change how strict this is.
- It does not fix the small catalog or the exact-match brittleness. It only changes how the top K is assembled from the scores.

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
   ```

2. Install dependencies:

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

## Recommendations for Multiple Profiles

`python -m src.main` prints the top 5 for each taste profile as a table. The Reasons column shows exactly how each score was built, including diversity penalties (`artist repeat`, `genre repeat`):

### High-Energy Pop

```
+---+------------------+---------+--------------------------------------+
| # | Song             | Score/4 | Reasons                              |
+---+------------------+---------+--------------------------------------+
| 1 | Sunrise City     | 3.92    | - genre match: pop (+2.0)            |
|   | by Neon Echo     |         | - mood match: happy (+1.0)           |
|   |                  |         | - energy 0.82 vs target 0.90 (+0.92) |
+---+------------------+---------+--------------------------------------+
| 2 | Gym Hero         | 2.72    | - genre match: pop (+2.0)            |
|   | by Max Pulse     |         | - energy 0.93 vs target 0.90 (+0.97) |
|   |                  |         | - genre repeat: pop (-0.25)          |
+---+------------------+---------+--------------------------------------+
| 3 | Rooftop Lights   | 1.86    | - mood match: happy (+1.0)           |
|   | by Indigo Parade |         | - energy 0.76 vs target 0.90 (+0.86) |
+---+------------------+---------+--------------------------------------+
| 4 | Storm Runner     | 0.99    | - energy 0.91 vs target 0.90 (+0.99) |
|   | by Voltline      |         |                                      |
+---+------------------+---------+--------------------------------------+
| 5 | Solar Parade     | 0.98    | - energy 0.88 vs target 0.90 (+0.98) |
|   | by Calle Sol     |         |                                      |
+---+------------------+---------+--------------------------------------+
```

### Chill Lofi

```
+---+---------------------+---------+--------------------------------------+
| # | Song                | Score/4 | Reasons                              |
+---+---------------------+---------+--------------------------------------+
| 1 | Library Rain        | 3.95    | - genre match: lofi (+2.0)           |
|   | by Paper Lanterns   |         | - mood match: chill (+1.0)           |
|   |                     |         | - energy 0.35 vs target 0.30 (+0.95) |
+---+---------------------+---------+--------------------------------------+
| 2 | Midnight Coding     | 3.63    | - genre match: lofi (+2.0)           |
|   | by LoRoom           |         | - mood match: chill (+1.0)           |
|   |                     |         | - energy 0.42 vs target 0.30 (+0.88) |
|   |                     |         | - genre repeat: lofi (-0.25)         |
+---+---------------------+---------+--------------------------------------+
| 3 | Spacewalk Thoughts  | 1.98    | - mood match: chill (+1.0)           |
|   | by Orbit Bloom      |         | - energy 0.28 vs target 0.30 (+0.98) |
+---+---------------------+---------+--------------------------------------+
| 4 | Focus Flow          | 1.65    | - genre match: lofi (+2.0)           |
|   | by LoRoom           |         | - energy 0.40 vs target 0.30 (+0.90) |
|   |                     |         | - artist repeat: LoRoom (-0.75)      |
|   |                     |         | - genre repeat: lofi (-0.50)         |
+---+---------------------+---------+--------------------------------------+
| 5 | Porch Light Lullaby | 1.00    | - energy 0.30 vs target 0.30 (+1.00) |
|   | by Wren and Willow  |         |                                      |
+---+---------------------+---------+--------------------------------------+
```

### Deep Intense Rock

```
+---+------------------+---------+--------------------------------------+
| # | Song             | Score/4 | Reasons                              |
+---+------------------+---------+--------------------------------------+
| 1 | Storm Runner     | 3.99    | - genre match: rock (+2.0)           |
|   | by Voltline      |         | - mood match: intense (+1.0)         |
|   |                  |         | - energy 0.91 vs target 0.92 (+0.99) |
+---+------------------+---------+--------------------------------------+
| 2 | Gym Hero         | 1.99    | - mood match: intense (+1.0)         |
|   | by Max Pulse     |         | - energy 0.93 vs target 0.92 (+0.99) |
+---+------------------+---------+--------------------------------------+
| 3 | Pulse Garden     | 0.97    | - energy 0.95 vs target 0.92 (+0.97) |
|   | by Fractal Bloom |         |                                      |
+---+------------------+---------+--------------------------------------+
| 4 | Solar Parade     | 0.96    | - energy 0.88 vs target 0.92 (+0.96) |
|   | by Calle Sol     |         |                                      |
+---+------------------+---------+--------------------------------------+
| 5 | Iron Requiem     | 0.95    | - energy 0.97 vs target 0.92 (+0.95) |
|   | by Grave Signal  |         |                                      |
+---+------------------+---------+--------------------------------------+
```

---

## Experiments You Tried

### 1. Different types of users

I ran the three profiles above plus ten edge cases from `src/main.py`. The three realistic listeners got sensible lists with no songs shared between Chill Lofi and Deep Intense Rock. The edge cases showed the weak spots:

- **Classical fan who wants high energy.** The quiet *Nocturne in Grey* ranked #1 (2.32). The other four songs were loud songs from unrelated genres.
- **Lofi fan who asks for "intense" at 0.95.** Two quiet lofi songs (2.47 and 2.15) beat two loud intense songs that matched mood and energy almost perfectly (1.98 and 1.96). The third lofi song fell to #5 (1.20) because of the diversity penalties.
- **k-pop fan.** The genre is not in the catalog, so the best possible score was 2.0.
- **"Pop " with a capital letter and a space.** Same list as "pop", so the typo cleanup works.
- **Energy of 5.0 (a typo).** Every song got 0 energy points. No error was shown.
- **Acoustic metal fan.** Same list as a plain metal fan. The `likes_acoustic` setting is never read.
- **Empty profile and energy `"high"`.** Both were rejected with a clear message.

### 2. Lowering the genre weight from 2.0 to 0.5

I changed `GENRE_POINTS` for one run, without saving the change. Results:

- **High-Energy Pop:** *Gym Hero* fell from #2 to #3. *Rooftop Lights* (happy, but indie pop) rose from #3 to #2. That is closer to what a "happy pop" fan expects.
- **Chill Lofi:** *Focus Flow* (lofi, but not chill, and a repeat artist) dropped out of the top 5. *Porch Light Lullaby* moved up to #4 and *Coffee Shop Stories* entered at #5.
- **Deep Intense Rock:** the same top 5 as before.
- **Classical fan who wants 0.90:** *Nocturne in Grey* fell out of the top 5. The list became all loud songs. That fits the request for high energy, but the listener's favorite genre vanished.
- **Calm rock fan (energy 0.30):** *Storm Runner* still ranked #1 at 1.89, because the rock and intense matches still outweighed the energy gap.

### 3. Lowering genre to 0.5 and doubling energy to 2.0

I ran this as a second one-off test. Now energy is worth more than the genre and mood bonuses combined (2.0 vs 1.5). Results:

- **Calm rock fan:** *Storm Runner* still ranked #1 (2.28). *Porch Light Lullaby*, a perfect energy match, jumped to #2 (2.00). The list now has a real mix of loud and quiet songs.
- **Pop, lofi and rock listeners:** the #1 songs stayed the same. Only the lower ranks shuffled.

### What I learned from these tests

Changing one weight changes who the system serves well. A high genre weight helps people with a single clear genre. A lower genre weight helps people who care more about the feel of the music. Neither setting is "correct". It depends on who the listener is.

I did not test adding tempo or valence to the score. The scorer does not use them yet. That is the next experiment I would try.

---

## Limitations and Risks

- **Tiny catalog.** There are only 18 songs. Lofi has 3 and pop has 2. The other 13 genres have one song each, so most listeners get one good match and four filler songs.
- **Genre is too loud.** A genre match (2.0) outweighs the whole energy score (at most 1.0). A calm rock fan still gets a loud rock song at #1.
- **Exact matches only.** "pop" and "indie pop" count as different genres. "chill" and "relaxed" count as different moods.
- **Unused data.** Valence, tempo, danceability and acousticness are loaded but ignored. The `likes_acoustic` setting does nothing.
- **Quiet failures.** Unknown genres or moods, and energy outside 0 to 1, still return a confident-looking list with no warning.
- **Only a light diversity fix.** The diversity penalty (see above) discourages repeats, but it is small. With a tiny catalog, the top 5 can still repeat an artist or genre when nothing else scores well.
- **No lyrics, language or listening history.** The system only sees a few labels and numbers. It cannot learn from what a listener plays or skips.
- **Filter bubble.** It only rewards what the listener already said they like, so it will not help them find something new.

See [model_card.md](model_card.md) for more detail.

---

## Reflection

[**Model Card**](model_card.md)

I learned that a recommender turns data into predictions by comparing numbers and labels. Here, each song gets points for matching a listener's genre, mood and energy. Then the points are sorted. The "prediction" is only as good as the choices behind it: which features count, how much each one is worth, and what the catalog contains. One choice, making genre worth 2 points, shaped almost every list. When I lowered it to 0.5, different songs rose to the top. Even the song that looked like a bug, *Gym Hero* for "Happy Pop" fans, was correct under my rules. Thus, my biggest learning moment during this project was recognizing how much the rules mattered and fixing them when they became problematic.

Additionally, I learned that bias shows up in small, quiet ways. Listeners with a common genre like lofi get full lists. Listeners with a rare genre get one match and four fillers. Listeners who care about feel more than genre get ignored. Nothing in the output warns them. The scoring also only rewards what a person already said they like, so it never helps them discover anything new. Real apps face the same problems at a much larger scale. They need more data, more signals and checks for fairness, not just a good score.