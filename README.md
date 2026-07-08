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
- `genre` (categorical) — e.g. pop, lofi, rock, ambient, jazz, synthwave, indie pop
- `mood` (categorical) — e.g. happy, chill, intense, relaxed, moody, focused
- `energy` (numerical, 0–1) — how intense/energetic the song feels
- `valence` (numerical, 0–1) — how positive/upbeat vs. dark the song feels
- `acousticness` (numerical, 0–1) — acoustic/organic vs. synthetic/produced
- `tempo_bpm` (numerical, ~60–160) — the song's tempo

**UserProfile features:**
- `preferred_genre`
- `preferred_energy` (0–1)
- `preferred_valence` (0–1)
- `preferred_acousticness` (0–1)

**How the Recommender scores a song:**
Each numerical feature is compared using normalized similarity: 
`similarity = 1 - |user_pref - song_value|` (with tempo_bpm min-max normalized first, 
since it isn't already on a 0–1 scale like the others). Genre is scored as an exact 
match (1) or non-match (0), with room to upgrade to graded "genre family" matching 
later (e.g. lofi/ambient/jazz treated as related). The final score combines these with 
weights: `score = 0.30·sim(energy) + 0.25·sim(valence) + 0.20·sim(acousticness) + 0.25·genre_score`.

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



