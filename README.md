# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This project implements a content-based music recommender. Instead of using other 
users' listening behavior (collaborative filtering), it scores each song by comparing 
its own attributes — genre, mood, energy, valence, and acousticness — against a user's 
stated preferences. It then ranks the full song list to produce recommendations.

---

## How The System Works

Real-world recommenders like Spotify and YouTube generally use two approaches: 
collaborative filtering, which predicts what a user will like based on patterns across 
many users' behavior (plays, skips, saves), and content-based filtering, which predicts 
based on an item's own attributes (genre, tempo, energy). This simulation implements a 
content-based recommender.

**Song features:**
- `genre` (categorical) — e.g. pop, lofi, rock, ambient, jazz, synthwave, indie pop, and others added in Phase 2 (hip-hop, classical, r&b, folk, electronic, metal, country, reggae)
- `mood` (categorical) — e.g. happy, chill, intense, relaxed, moody, focused
- `energy` (numerical, 0–1) — how intense/energetic the song feels
- `valence` (numerical, 0–1) — how positive/upbeat vs. dark the song feels
- `acousticness` (numerical, 0–1) — acoustic/organic vs. synthetic/produced
- `tempo_bpm` (numerical, ~60–160) — the song's tempo (tracked but not currently used in scoring — a candidate feature for future iterations)

**UserProfile features:**
- `favorite_genre`
- `favorite_mood`
- `target_energy` (0–1)
- `target_valence` (0–1)
- `target_acousticness` (0–1)

**How songs are chosen:**
Scoring a song is a *local* operation — it only tells you how well one song matches 
a user, not how it compares to everything else. The Recommender separately runs a 
ranking step across the full song list: sorting by score, breaking ties (e.g. by song 
id), and cutting the list down to a top-N recommendation set. This separation matters 
because a good score is only meaningful relative to other songs' scores, and because 
list-level rules — like avoiding near-duplicate recommendations or excluding songs 
already played — can't be handled by scoring a single song in isolation.

This design prioritizes explainability and handles brand-new songs immediately (no 
cold-start problem), at the tradeoff of being less able to surface unexpected, 
serendipitous recommendations the way collaborative filtering can.

**Algorithm Recipe (finalized):**

```
score(song) = 30 × (1 - |acousticness - target_acousticness|)   # strongest discriminator
            + 20 × (1 - |energy - target_energy|)                # strong
            + 5  × (1 - |valence - target_valence|)               # weak, kept small
            + 15 if genre == favorite_genre else 0                # soft bonus
            + 10 if mood == favorite_mood else 0                  # soft bonus
```

Maximum possible score: 80 points.

Weights were chosen based on analyzing the actual spread of values in the dataset: 
acousticness is nearly bimodal (produced songs cluster low, acoustic songs cluster 
high) making it the strongest discriminator, energy has a wide, well-distributed 
range, and valence is weakly discriminating since most songs cluster tightly between 
0.48–0.84. Genre and mood are treated as additive soft bonuses rather than filters, 
since genre/mood values are sparse (many appear only once or twice across 18 songs) — 
treating them as hard filters would return almost no results for most user profiles. 
The bonuses are deliberately capped below the acousticness swing (25 combined vs. 30) 
so a genre/mood match can influence ranking but can't override a strong acoustic 
mismatch.

This recipe replaced an earlier draft formula (a simple weighted-average of energy, 
valence, acousticness, and a flat genre score) after Phase 2 data analysis showed 
acousticness and energy are strong discriminators in this dataset while valence 
barely separates songs at all.

**Potential biases to watch:**

- The system may over-favor whichever mood/genre happens to be best-represented in 
  the catalog, since sparse categories rarely get their bonus triggered at all.
- Heavier weighting on acousticness and energy means the recommender could 
  systematically underrate songs that are a great "vibe" match but differ on 
  production style (e.g. an acoustic cover of an electronic song).
- With only 18 songs, the numeric ranges (especially valence) are not statistically 
  robust — a larger catalog could shift what counts as a "strong" vs. "weak" 
  discriminator entirely.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

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