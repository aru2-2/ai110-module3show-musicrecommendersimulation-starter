# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Think of the recommender as a judge giving every song in the catalog a score out of 4 points, based on how well it fits what the listener says they like. Then it lines the songs up from highest score to lowest and shows the top five.

**What the listener tells us:** a favorite genre (like pop), a favorite mood (like happy), and how energetic they want the music to feel, on a scale from 0 (very calm) to 1 (very intense).

**How a song earns points:**

- **Genre: up to 2 points.** If the song's genre is exactly the listener's favorite, it gets 2 points. If not, it gets none.
- **Mood: up to 1 point.** Same idea. An exact mood match earns 1 point, otherwise none.
- **Energy: up to 1 point.** This one is graded, not all-or-nothing. A song whose energy is exactly what the listener wants gets the full point, and the further away it is, the fewer points it earns. A song that is a little too mellow or a little too intense still gets most of the point.

The three parts are added together. Genre counts the most because it is the strongest sign of taste, and the others help break ties between songs of the same genre.

**Why it can explain itself:** every time a song earns points, the system writes down why, for example "genre match: pop (+2.0)". The final list shows each song's score next to those reasons, so the listener can see exactly why it was recommended.

**What it ignores:** tempo, how danceable or acoustic a song is, and how positive it sounds are all in the data but are not used in scoring. The system also only knows exact matches, so "rock" and "metal" are treated as completely different, and "chill" and "relaxed" are too.

**Changes from the starter:** the starter code had no scoring at all. I added the point system above, the step that ranks every song and keeps the top few, and the plain-language reasons shown with each result.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The biggest weakness I found is that the genre bonus (2 points) is worth more than the whole energy score (at most 1 point, and even the worst energy match still earns about 0.3), so energy can only break ties. In my tests, a rock fan who asked for calm music (energy 0.30) was still given the loud Storm Runner (energy 0.91) at #1 with a score of 3.39, while Porch Light Lullaby, a perfect energy match, scored only 1.00. The same thing happened to a classical fan who wanted high energy: the quiet Nocturne in Grey (energy 0.22) ranked first, and the next four songs were an unrelated mix of high-energy tracks. Because 13 of the 15 genres in the catalog have only one song, a listener gets one genre match and then four slots filled almost entirely by energy, which feels random. This means the system favors people whose taste fits neatly into one genre label and underserves anyone who cares more about the feel of the music than its category.

---

## 7. Evaluation  

**What I tested.** I ran 13 listener profiles through the recommender and read the top 5 songs and the "why" reasons for each. Three were realistic listeners: **High-Energy Pop** (pop, happy, energy 0.90), **Chill Lofi** (lofi, chill, energy 0.30) and **Deep Intense Rock** (rock, intense, energy 0.92). The other ten were deliberately awkward cases meant to break the scoring, such as a classical fan who wants high energy, a k-pop fan (a genre the catalog doesn't have), and a profile typed as "Pop " with a stray space. For each one I checked two things. Did the songs match what I would expect a person with that taste to want? And did the "why" reasons add up to the score shown?

### The three main profiles, compared in pairs

**High-Energy Pop vs. Chill Lofi.** These two get almost completely different lists, which is what I wanted to see. Pop gets Sunrise City, Gym Hero and Rooftop Lights, all loud and bright (energy 0.76 to 0.93). Lofi gets Library Rain, Midnight Coding and Focus Flow, all quiet (energy 0.35 to 0.42). The two lists share no songs. This makes sense because the biggest point source, genre, points at completely different songs, and the energy score then pulls each list toward its own end of the loud-to-quiet scale.

**High-Energy Pop vs. Deep Intense Rock.** The lists are different, but they overlap in one song: **Gym Hero** is #2 for both. Both listeners want very high energy (0.90 and 0.92), and both lists then fill out with the same loud songs (Storm Runner, Solar Parade). What separates them is the top spot. Pop's #1 is Sunrise City (pop + happy), and Rock's #1 is Storm Runner (rock + intense) with a near-perfect 3.99. This makes sense, because when two listeners want the same loudness, only genre and mood can tell them apart.

**Chill Lofi vs. Deep Intense Rock.** These are the opposite ends of the energy scale (0.30 vs 0.92) and they behave that way: not a single song is shared. The lofi list is all quiet, acoustic songs and the rock list is all loud, electric ones. One difference in *shape*: Lofi has three lofi songs in its top 3 and so gets three genre bonuses, while Rock has only one rock song in the whole catalog, so its list drops from 3.99 at #1 to 1.99 at #2. The scoring can only reward a genre as many times as the catalog has songs in it, so the rock fan gets a thinner list than the lofi fan.

### Why does "Gym Hero" keep showing up for people who just want "Happy Pop"?

Gym Hero is a pop song, and pop is worth 2 points, the biggest prize in the system. Gym Hero's mood is "intense", not "happy", so it misses the 1-point mood bonus. But it still collects the full 2 genre points, plus about 0.97 for being very close in energy to a high-energy listener. That totals 2.97, which is enough to beat every song that is *not* pop, and there are only two pop songs in the whole catalog. The best non-pop "happy" song, Rooftop Lights, gets 1.86. The system treats "pop" as a label and doesn't know that a workout anthem and a sunny pop tune feel different. The same song also appears for the rock fan, because Gym Hero's mood is "intense" and it earns a mood point there. So Gym Hero isn't wrong for either listener, but it only shows up for "Happy Pop" fans because the catalog has so few pop songs to choose from.

### Edge-case pairs, compared

**Classical / high energy vs. Lofi / "intense" / 0.95.** These two were built the same way: a listener whose favorite genre only has quiet songs but who asks for loud music. In both cases genre won. The classical fan got the quiet Nocturne in Grey at #1 (2.32) even though the other four songs were all loud. The lofi fan got three quiet lofi songs at the top (about 2.4 each) *above* two loud "intense" songs that were perfect matches on mood and energy (about 1.97). This surprised me. I expected a listener asking for "intense, 0.95" to get intense songs, but the quiet songs won because a genre match (2 points) is worth more than a perfect mood plus energy match (about 2 points).

**Pop (clean) vs. "Pop " (extra space and capital letter).** These two return the same top 5, with the same scores. This tells me the cleanup step, which ignores capitals and extra spaces, is doing its job, so a small typing slip doesn't lock a listener out of their favorite genre.

**k-pop vs. "Pop ".** Same mood (happy) and about the same energy (0.80), but the k-pop listener's best score is only 1.98, while the pop listener's is 3.98. The system has no k-pop songs, so it can't give the 2-point genre bonus and falls back on "happy" and "close in energy". It does the sensible thing, since the top two are the happy pop and indie pop songs, but the k-pop fan is quietly worse off. They get lower scores and no hint that their genre isn't in the catalog.

**"Sad" mood vs. the "no matches at all / 0.5" profile.** Neither profile matches anything in the catalog by label, so both are ranked purely by energy. The "sad" listener (energy 0.25) gets the quiet songs (Spacewalk Thoughts, Nocturne in Grey, Porch Light Lullaby), which *feels* right for sad music. That's lucky, because "sad" is not one of the mood labels in the catalog (the real ones are "melancholic" and "wistful"), so the system never understood the request. The 0.5 profile gets the songs closest to the middle, with scores bunched between 0.87 and 0.98, so the order is nearly arbitrary.

**Pop (energy 0.90) vs. Pop with energy 5.0 (a typo).** With a sensible energy, the pop list is ranked from the top by genre, mood and energy. With 5.0, every song earns zero energy points, so the list is ranked on genre and mood alone. Sunrise City and Gym Hero still come out on top, but #4 and #5 are songs with a score of 0.00, picked by their order in the file. The system didn't crash or warn; it just quietly stopped paying attention to energy.

**Metal with "likes acoustic" turned on vs. a plain metal fan.** I asked for an acoustic metal fan and got Iron Requiem first at 4.00, then only loud, non-acoustic songs (Pulse Garden, Gym Hero, Storm Runner). The scorer never reads the "likes acoustic" setting, so a plain metal fan gets exactly the same list.

### What surprised me

1. **Genre is louder than I thought.** I knew genre was worth the most, but I didn't expect it to beat a perfect mood and energy match, or to put a quiet song first for someone who asked for loud music.
2. **The catalog size matters as much as the scoring rules.** Lofi has 3 songs and gets a full top 3. Metal, rock, jazz and folk have one song each, so those fans get one good match and four filler songs.
3. **The system fails silently.** It accepted "sad", "k-pop", an energy of 5.0 and an "acoustic" setting without any warning, and produced a confident-looking list each time. Only an empty profile or a non-number for energy was rejected.
4. **Some of my profile settings did nothing.** The realistic profiles also include target valence and target acousticness, but the scorer never reads them. The lists would be identical without them.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
