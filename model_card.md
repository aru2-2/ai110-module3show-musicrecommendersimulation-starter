# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

A small, rule-based song recommender. It scores songs by genre, mood and energy.

---

## 2. Intended Use  

**What it does.** It suggests the top 5 songs from a small catalog. Each song comes with a score and a short reason.

**What it assumes about the listener.** It assumes people can name one favorite genre, one favorite mood and a target energy level. It also assumes taste stays the same from song to song. Real taste is messier than that.

**Who it is for.** This is a classroom project. It is meant for learning how recommenders work. It is not meant for real users or a real music app.

---

## 3. How the Model Works  

Think of the recommender as a judge giving every song in the catalog a score out of 4 points, based on how well it fits what the listener says they like. Then it lines the songs up from highest score to lowest and shows the top five.

**What the listener tells us:** a favorite genre (like pop), a favorite mood (like happy), and how energetic they want the music to feel, on a scale from 0 (very calm) to 1 (very intense).

**How a song earns points:**

- **Genre: up to 2 points.** If the song's genre is exactly the listener's favorite, it gets 2 points. If not, it gets none.
- **Mood: up to 1 point.** Same idea. An exact mood match earns 1 point, otherwise none.
- **Energy: up to 1 point.** This one is graded, not all-or-nothing. A song whose energy is exactly what the listener wants gets the full point, and the further away it is, the fewer points it earns. A song that is a little too mellow or a little too intense still gets most of the point.

The three parts are added together. Genre counts the most because it is the strongest sign of taste, and the others help break ties between songs of the same genre.

**Keeping the list varied:** the top five are picked one at a time. After each pick, every remaining song loses 0.75 points for each already-picked song by the same artist and 0.25 points for each one in the same genre. This keeps one artist or genre from filling the whole list. The first pick is never penalized, and the penalty is small next to the 2-point genre bonus, so it mostly reorders close calls.

**Why it can explain itself:** every time a song earns points, the system writes down why, for example "genre match: pop (+2.0)". The final list shows each song's score next to those reasons, so the listener can see exactly why it was recommended.

**What it ignores:** tempo, how danceable or acoustic a song is, and how positive it sounds are all in the data but are not used in scoring. The system also only knows exact matches, so "rock" and "metal" are treated as completely different, and "chill" and "relaxed" are too.

**Changes from the starter:** the starter code had no scoring at all. I added the point system above, the step that ranks every song and keeps the top few, the diversity penalty, and the plain-language reasons shown with each result.

---

## 4. Data  

**Size.** The catalog has 18 songs in `data/songs.csv`.

**What each song has.** Title, artist, genre, mood, energy, tempo, valence (how positive it sounds), danceability and acousticness. The scorer only uses genre, mood and energy.

**Genres.** There are 15 genres. Lofi has 3 songs and pop has 2. The other 13 have one song each. Examples are rock, jazz, metal, classical, folk, edm and reggaeton.

**Moods.** There are 14 moods. Chill has 3 songs, happy and intense have 2 each, and the rest have one each.

**What is missing.**
- Many genres, such as k-pop, blues and punk.
- Songs with middle energy. Only two songs fall between 0.45 and 0.70.
- Quiet songs that are not acoustic, and loud songs that are acoustic. Energy and acousticness move together in this data.
- Any songs in languages or styles outside a mostly Western mix.

---

## 5. Strengths  

**It works well for listeners with a clear, common taste.** Chill Lofi, High-Energy Pop and Deep Intense Rock all got lists that felt right. Their #1 songs scored 3.95, 3.92 and 3.99 out of 4.

**It separates opposite tastes.** The lofi list and the rock list share no songs. The quiet listener gets quiet songs. The loud listener gets loud songs.

**It explains itself.** Every result shows a score and the reasons, like "genre match: pop (+2.0)". You can check why a song was picked.

**It forgives small typos.** "Pop " with a capital letter and a space gives the same list as "pop".

**It rejects bad input.** An empty profile, or an energy like "high", is refused with a clear message.

**Its mistakes are easy to see.** Because the rules are simple, I could trace every odd result back to a rule. That made the problems easy to find.

---

## 6. Limitations and Bias 

The biggest weakness I found is that the genre bonus (2 points) is worth more than the whole energy score (at most 1 point, and even the worst energy match still earns about 0.3), so energy can only break ties. In my tests, a rock fan who asked for calm music (energy 0.30) was still given the loud Storm Runner (energy 0.91) at #1 with a score of 3.39, while Porch Light Lullaby, a perfect energy match, scored only 1.00. The same thing happened to a classical fan who wanted high energy: the quiet Nocturne in Grey (energy 0.22) ranked first, and the next four songs were an unrelated mix of high-energy tracks. Because 13 of the 15 genres in the catalog have only one song, a listener gets one genre match and then four slots filled almost entirely by energy, which feels random. This means the system favors people whose taste fits neatly into one genre label and underserves anyone who cares more about the feel of the music than its category.

---

## 7. Evaluation  

**What I tested.** I ran 13 listener profiles through the recommender and read the top 5 songs and the "why" reasons for each. Three were realistic listeners: **High-Energy Pop** (pop, happy, energy 0.90), **Chill Lofi** (lofi, chill, energy 0.30) and **Deep Intense Rock** (rock, intense, energy 0.92). The other ten were deliberately awkward cases meant to break the scoring, such as a classical fan who wants high energy, a k-pop fan (a genre the catalog doesn't have), and a profile typed as "Pop " with a stray space. For each one I checked two things. Did the songs match what I would expect a person with that taste to want? And did the "why" reasons add up to the score shown?

### The three main profiles, compared in pairs

**High-Energy Pop vs. Chill Lofi.** These two get almost completely different lists, which is what I wanted to see. Pop gets Sunrise City, Gym Hero and Rooftop Lights, all loud and bright (energy 0.76 to 0.93). Lofi gets Library Rain, Midnight Coding and Spacewalk Thoughts, all quiet (energy 0.28 to 0.42). The two lists share no songs. This makes sense because the biggest point source, genre, points at completely different songs, and the energy score then pulls each list toward its own end of the loud-to-quiet scale.

**High-Energy Pop vs. Deep Intense Rock.** The lists are different, but they overlap in one song: **Gym Hero** is #2 for both. Both listeners want very high energy (0.90 and 0.92), and both lists then fill out with the same loud songs (Storm Runner, Solar Parade). What separates them is the top spot. Pop's #1 is Sunrise City (pop + happy), and Rock's #1 is Storm Runner (rock + intense) with a near-perfect 3.99. This makes sense, because when two listeners want the same loudness, only genre and mood can tell them apart.

**Chill Lofi vs. Deep Intense Rock.** These are the opposite ends of the energy scale (0.30 vs 0.92) and they behave that way: not a single song is shared. The lofi list is all quiet, acoustic songs and the rock list is all loud, electric ones. One difference in *shape*: Lofi has three lofi songs in the catalog and gets genre bonuses for two of them in its top 2 (3.95 and 3.63), while Rock has only one rock song in the whole catalog, so its list drops from 3.99 at #1 to 1.99 at #2. The scoring can only reward a genre as many times as the catalog has songs in it, so the rock fan gets a thinner list than the lofi fan.

### Why does "Gym Hero" keep showing up for people who just want "Happy Pop"?

Gym Hero is a pop song, and pop is worth 2 points, the biggest prize in the system. Gym Hero's mood is "intense", not "happy", so it misses the 1-point mood bonus. But it still collects the full 2 genre points, plus about 0.97 for being very close in energy to a high-energy listener. That totals 2.97 before the small diversity penalty for repeating the genre (-0.25), so it displays as 2.72. Either way it beats every song that is *not* pop, and there are only two pop songs in the whole catalog. The best non-pop "happy" song, Rooftop Lights, gets 1.86. The system treats "pop" as a label and doesn't know that a workout anthem and a sunny pop tune feel different. The same song also appears for the rock fan, because Gym Hero's mood is "intense" and it earns a mood point there. So Gym Hero isn't wrong for either listener, but it only shows up for "Happy Pop" fans because the catalog has so few pop songs to choose from.

### Edge-case pairs, compared

**Classical / high energy vs. Lofi / "intense" / 0.95.** These two were built the same way: a listener whose favorite genre only has quiet songs but who asks for loud music. In both cases genre won. The classical fan got the quiet Nocturne in Grey at #1 (2.32) even though the other four songs were all loud. The lofi fan got two quiet lofi songs at the top (2.47 and 2.15) *above* two loud "intense" songs that were near-perfect matches on mood and energy (1.98 and 1.96). The third lofi song only fell to #5 (1.20) because of the diversity penalty. This surprised me. I expected a listener asking for "intense, 0.95" to get intense songs, but the quiet songs won because a genre match (2 points) is worth more than a perfect mood plus energy match (about 2 points).

**Pop (clean) vs. "Pop " (extra space and capital letter).** These two return the same top 5, with the same scores. This tells me the cleanup step, which ignores capitals and extra spaces, is doing its job, so a small typing slip doesn't lock a listener out of their favorite genre.

**k-pop vs. "Pop ".** Same mood (happy) and about the same energy (0.80), but the k-pop listener's best score is only 1.98, while the pop listener's is 3.98. The system has no k-pop songs, so it can't give the 2-point genre bonus and falls back on "happy" and "close in energy". It does the sensible thing, since the top two are the happy pop and indie pop songs, but the k-pop fan is quietly worse off. They get lower scores and no hint that their genre isn't in the catalog.

**"Sad" mood vs. the "no matches at all / 0.5" profile.** Neither profile matches anything in the catalog by label, so both are ranked purely by energy. The "sad" listener (energy 0.25) gets the quiet songs (Spacewalk Thoughts, Nocturne in Grey, Porch Light Lullaby), which *feels* right for sad music. That's lucky, because "sad" is not one of the mood labels in the catalog (the real ones are "melancholic" and "wistful"), so the system never understood the request. The 0.5 profile gets the songs closest to the middle, with scores bunched between 0.80 and 0.98, so the order is nearly arbitrary.

**Pop (energy 0.90) vs. Pop with energy 5.0 (a typo).** With a sensible energy, the pop list is ranked from the top by genre, mood and energy. With 5.0, every song earns zero energy points, so the list is ranked on genre and mood alone. Sunrise City and Gym Hero still come out on top, but #4 and #5 are songs with a score of 0.00, picked by their order in the file. The system didn't crash or warn; it just quietly stopped paying attention to energy.

**Metal with "likes acoustic" turned on vs. a plain metal fan.** I asked for an acoustic metal fan and got Iron Requiem first at 4.00, then only loud, non-acoustic songs (Pulse Garden, Gym Hero, Storm Runner). The scorer never reads the "likes acoustic" setting, so a plain metal fan gets exactly the same list.

### What surprised me

1. **Genre is louder than I thought.** I knew genre was worth the most, but I didn't expect it to beat a perfect mood and energy match, or to put a quiet song first for someone who asked for loud music.
2. **The catalog size matters as much as the scoring rules.** Lofi has 3 songs and gets a full top 3. Metal, rock, jazz and folk have one song each, so those fans get one good match and four filler songs.
3. **The system fails silently.** It accepted "sad", "k-pop", an energy of 5.0 and an "acoustic" setting without any warning, and produced a confident-looking list each time. Only an empty profile or a non-number for energy was rejected.
4. **Some of my profile settings did nothing.** The realistic profiles also include target valence and target acousticness, but the scorer never reads them. The lists would be identical without them.

---

## 8. Future Work  

**Use more of the data.** Score acousticness, valence and tempo too. Make the "likes acoustic" setting actually work.

**Give partial credit.** Let "pop" earn some points for "indie pop". Let "chill" earn some points for "relaxed". Right now close matches count as zero.

**Make energy matter more.** Raise its weight, or punish big gaps more. Then a calm listener would not get a loud song just because the genre matched.

**Mix up the top 5 more.** The diversity penalty already nudges lists away from repeats, but it is small. A hard cap on songs per genre or artist, or a smarter penalty, would do more. Without it, the Chill Lofi list still has two songs by LoRoom.

**Add more songs.** More songs per genre, more middle-energy songs and more genres.

**Be honest about gaps.** If the genre or mood is not in the catalog, say so. Do not quietly return a list.

**Handle mixed taste.** Let a listener pick two or three genres, or say "calm in the morning, loud at the gym".

**Explain better.** Say what was missing too, such as "no k-pop songs in the catalog".

---

## 9. Personal Reflection  

**What I learned.** A recommender is really a set of choices about what matters. In this music recommender simulation, I chose genre to be worth 2 points, and that one choice shaped almost every list. Clearly, I noticed that small weights have big effects.

**What surprised me.** A song that looked wrong, Gym Hero for "Happy Pop" fans, was actually correct under my rules. I realized that the rules were the problem, not a bug. I also learned that the data matters as much as the math. With one rock song in the catalog, a rock fan can only ever get one good match.

**How it changed my view.** When a music app shows me the same kind of song again and again, I now wonder what it is rewarding. It may be doing the same thing my scorer does. It might be sticking to my "favorite genre" and ignoring how I feel today. I also see why apps need lots of songs and lots of signals, not just a few labels, to provide more accurate recommendations for their users.
