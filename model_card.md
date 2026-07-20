# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

This recommender is designed for classroom exploration of how content-based 
recommendation systems work, not for real-world deployment. Given a user's stated 
music taste preferences (favorite genre, favorite mood, and target energy/valence/
acousticness values), it scores every song in a small catalog and returns the top-K 
matches with plain-language explanations for each score.

It assumes the user can articulate their preferences as explicit numeric/categorical 
values rather than inferring taste from listening behavior. It is a simulation meant 
to demonstrate and evaluate the mechanics of content-based scoring, not a production 
recommender for real listeners.

---

## 3. How the Model Works  

Every song has five key traits: genre, mood, energy, valence, and acousticness. A 
user describes their taste using the same traits — a favorite genre, a favorite mood, 
and target values for energy, valence, and acousticness.

To score a song, the system checks how close the song's energy, valence, and 
acousticness are to what the user asked for, and gives partial credit the closer they 
are — a perfect match earns full points, and the points shrink the further off the 
song is. On top of that, the song gets a bonus if its genre matches the user's 
favorite genre, and another bonus if its mood matches the user's favorite mood. All 
of these points get added together into one final score, and the system does this for 
every song in the catalog, then sorts them from highest score to lowest to produce the 
final recommendation list.

Acousticness carries the most weight (30 of 80 possible points), followed by energy 
(20 points), then the genre and mood bonuses (15 and 10 points), with valence 
carrying the least weight (5 points). This is different from an early draft of the 
scoring logic, which weighted energy and valence roughly equally — the final weights 
were chosen after analyzing which features actually vary enough across the catalog to 
tell songs apart.

---

## 4. Data  

The catalog contains **18 songs**. The original starter file had 10 songs across 7 
genres (pop, lofi, rock, ambient, jazz, synthwave, indie pop); 8 more songs were added 
covering genres not previously represented (hip-hop, classical, r&b, folk, electronic, 
metal, country, reggae), bringing the total to 15 genres across 18 songs and roughly 
14 distinct moods.

No data was removed. Because genres and moods are spread so thin across only 18 
songs (most genres appear only once or twice), the dataset likely does not capture 
the full range of real musical taste — subgenres, regional styles, instrumental vs. 
vocal preference, and lyrical content are entirely missing from the catalog.

---

## 5. Strengths  

The system gives sensible, explainable results for users whose stated preferences 
line up cleanly with a genre/mood in the catalog. For example, a "Deep Intense Rock" 
profile (rock genre, intense mood, high energy, low acousticness) correctly surfaced 
"Storm Runner" as the clear top pick with the highest score seen in any test (79.40) — 
matching genre, mood, energy, and acousticness all at once.

Comparing opposite profiles also confirmed the system responds sensibly to different 
tastes: a "Chill Lofi" profile favored calm, high-acousticness songs (Library Rain, 
Midnight Coding), while "Deep Intense Rock" favored high-energy, low-acousticness 
songs (Storm Runner, Iron Verdict) — showing the scoring logic correctly separates 
opposite ends of the taste spectrum.

The system is also transparent: every recommendation comes with a plain-language 
breakdown of exactly why it scored the way it did, rather than a black-box number.

---

## 6. Limitations and Bias 

The scoring formula weights acousticness (30 pts) more heavily than energy (20 pts). 
This means a user who wants high-energy music but also indicates any acoustic 
preference will have their energy preference overridden — the "Acoustic Headbanger" 
test profile (energy=1.0, acousticness=1.0) returned the catalog's calmest, most 
acoustic songs as its top picks, not the most energetic ones, even though the user 
explicitly asked for maximum energy. The system has no way to detect or flag 
contradictory input; it silently averages the terms into a "compromise" that doesn't 
actually satisfy either stated preference.

Because genre and mood values are so sparse across only 18 songs, most user profiles 
will only get their genre/mood bonus applied to a handful of songs (sometimes just 
one), meaning the numeric features (acousticness, energy, valence) end up doing most 
of the real work in ranking — genre/mood act more like light tie-breakers than 
meaningful preferences. Valence in particular is nearly useless as a discriminator, 
since most songs in the catalog cluster tightly in the same valence range (0.48–0.84).

The system might also unintentionally favor whichever genre/mood happens to be best 
represented in the catalog (pop and happy, in this case), since users whose taste 
matches an underrepresented genre have fewer songs available to ever score well.

---

## 7. Evaluation  

I tested four user profiles: Starter (Pop Happy), High-Energy Pop, Chill Lofi, and 
Deep Intense Rock, plus one adversarial profile designed to break the system.

Each of the four "normal" profiles produced results that matched my musical intuition — 
happy/pop preferences surfaced upbeat pop songs, chill/lofi preferences surfaced calm 
acoustic songs, and intense/rock preferences surfaced high-energy rock songs. The 
biggest surprise came from comparing High-Energy Pop against the Starter profile: 
even with energy pushed up to 0.9, the ranking barely changed, because acousticness 
was doing more of the work than energy in the scoring formula.

The adversarial test — "The Acoustic Headbanger" (energy=1.0, acousticness=1.0, 
mood="angry", genre="k-pop," none of which exist in the catalog) — was the most 
revealing. I expected the system to either surface the catalog's most energetic songs 
or produce an obviously bad/low-confidence result. Instead, it confidently returned 
the calmest, most acoustic songs in the catalog as its "top" recommendation, with no 
indication that the user's preferences were contradictory or unmatchable. This 
confirmed that acousticness's higher weight silently overrides energy whenever the 
two pull in opposite directions.

---

## 8. Future Work  

- Add a way to detect contradictory preferences (e.g., very high energy + very high 
  acousticness) and either flag low confidence or ask the user to clarify, instead of 
  silently averaging into a compromise no real song matches.
- Rebalance or dynamically adjust feature weights based on how much each feature 
  actually varies in a given catalog, rather than using one fixed set of weights.
- Add more songs per genre/mood so genre and mood bonuses can play a more meaningful 
  role instead of acting as light tie-breakers.
- Add diversity logic to the ranking step so the top-K results aren't dominated by 
  near-duplicate songs (e.g. multiple songs from the same artist or nearly identical 
  attribute profiles).
- Consider additional features like instrumentalness or a context/activity tag 
  (workout, study, party) to capture dimensions of taste the current numeric features 
  can't reach.

---

## 9. Personal Reflection  

Building this project showed me how much of a recommender's "intelligence" actually 
comes down to arithmetic and weight choices rather than anything resembling real 
understanding of music. The system doesn't know what a song sounds like — it's just 
comparing numbers and adding up points, and the weights I chose for those numbers 
completely determine what the system considers a "good" recommendation.

The most interesting discovery was building an adversarial test case on purpose. I 
expected requesting maximum energy and maximum acousticness at the same time to 
either break the system or get flagged as invalid, but instead it just quietly 
returned a result that satisfied neither preference the user actually cared about. 
This changed how I think about real recommendation apps — a confident-looking "Top 
Pick" doesn't necessarily mean the system actually understood what you wanted; it 
might just mean one feature in the formula happened to win out over another, without 
anyone — including the user — ever being told that trade-off happened.

Using Claude Code sped up implementation significantly — it correctly translated my 
Phase 2 scoring recipe into working code on the first try, and independently verified 
its own work by running test cases before reporting back. However, I had to double-
check its "adversarial profile" suggestion by actually reading the score breakdown 
myself to confirm the acousticness-over-energy bug was real and not just a fluke — AI 
tools were fast at generating and testing code, but I still needed to verify the 
*reasoning* behind the results made sense before trusting them.