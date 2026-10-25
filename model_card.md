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

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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
