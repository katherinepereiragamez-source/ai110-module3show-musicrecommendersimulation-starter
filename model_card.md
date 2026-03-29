1. Model Name
Vibe Analyzeer 1.0

2. Intended Use
VibeFinder is designed to suggest songs from a small catalog that match a listener's current mood and taste preferences. It is built for classroom exploration — not for production use — and is meant to demonstrate how a basic recommendation algorithm works under the hood.
The system assumes the user can describe their preferences clearly: a favourite genre, a preferred mood, a target energy level, and whether they like acoustic or electronic sounds. It works best for users with a consistent, well-defined taste rather than someone whose preferences shift from song to song.
This is not intended to replace a real streaming service. It has no play history, no social signals, and a catalog of only 20 songs.

3. How the Model Works
Every song in the catalog gets a score from 0 to 10. The score is built from four questions:

Does the genre match? If the song's genre matches the user's favourite, it earns 2 points.
Does the mood match? Same idea — an exact mood match earns another 2 points.
How close is the energy? Songs are rated 0 to 1 for intensity. The closer a song's energy is to the user's target, the more points it earns — up to 3 points for a perfect match.
Does the acoustic feel fit? If the user likes acoustic, organic-sounding music, songs with high acousticness score higher. If they prefer electronic or produced sounds, it's the opposite. This is worth up to 3 points.

Once every song has a score, they are sorted from highest to lowest and the top five are returned along with a plain-English breakdown explaining exactly why each song scored the way it did.
The main change from the starter logic was replacing a simple weighted average with a transparent point system, and combining the score and explanation into a single function so the output is always consistent.

4. Data
The catalog contains 20 songs, all fictional. They were created specifically for this simulation.
Genres represented include pop, lofi, rock, ambient, synthwave, jazz, indie pop, country, electronic, R&B, metal, folk, classical, hip-hop, and EDM. Moods covered include happy, chill, intense, relaxed, moody, focused, nostalgic, energetic, romantic, angry, sad, peaceful, confident, euphoric, and uplifting.
Ten songs came with the starter project and ten were added to improve diversity. No songs were removed.
What is missing: the dataset has no real listener data, no play counts, no skips, and no ratings. It also has only one or two songs per genre in some cases, which means niche listeners may not get great matches. Real musical taste — things like preferred key, tempo feel, or lyrical themes — is not captured at all.

5. Strengths
The system works well for users with clear, mainstream preferences. A pop/happy/high-energy listener gets Sunrise City and Gym Hero at the top, which matches intuition immediately.
The point breakdown also works well as a teaching tool. Because every recommendation comes with a reason — "genre match (+2.0)", "energy score (+2.9)" — it is easy to see exactly why one song ranked above another. There are no black-box surprises.
The energy and acousticness scores handle continuous values gracefully. A song that is close but not perfect on energy still earns partial credit rather than getting a zero, which makes the rankings feel more natural than strict binary matching would.

6. Limitations and Bias
Genre dominance. Genre is a binary match worth 2 points. A song in a slightly different but very similar genre (like indie pop vs. pop) scores the same as a song in a completely unrelated genre. This penalises songs that might actually suit the user.
Mood is too coarse. "Relaxed" and "chill" are close in meaning but treated as completely different. A chill-seeking user will never see Coffee Shop Stories (jazz, relaxed) ranked highly even if it would be a perfect fit.
Underrepresented genres. Classical, metal, and country each appear only twice. Users whose favourite genre is one of these will at best get 2 matching songs and 3 partial matches.
No history or novelty. The system will recommend the same five songs every single time. It has no way to say "you've already heard this one" or "here's something new you might not have tried."
Acoustic preference is all-or-nothing. The likes_acoustic field is a boolean. There is no middle ground for a user who enjoys a mix of both styles.

7. Evaluation
Three user profiles were tested manually:

Pop/happy/high-energy — Sunrise City and Gym Hero appeared at the top as expected. Both are pop songs with high energy and happy moods.
Lofi/chill/low-energy/acoustic — Library Rain and Midnight Coding ranked first and second. Both are lofi and chill, with high acousticness and low energy.
Metal/angry/high-energy — Iron Cathedral was the only exact genre+mood match and ranked first. The remaining four slots were filled by high-energy songs from other genres, which was reasonable but showed the catalog depth problem clearly.

One surprise: Rooftop Lights (indie pop, happy) consistently appeared in top-5 results for pop/happy profiles despite not being tagged as pop. This revealed that energy and acousticness similarity can partially compensate for a genre mismatch — which is actually a realistic behaviour.

8. Future Work
Add more songs per genre. The most immediate improvement would be expanding the catalog to at least 5 songs per genre so niche listeners get meaningful choices.
Soften the genre and mood matching. Instead of binary matches, similar genres and moods could be grouped (e.g., "lofi" and "ambient" share a chill cluster) so related songs earn partial credit rather than zero.
Add a listening history filter. Even a simple list of already-heard song IDs would prevent the system from recommending the same tracks on every run and would make the simulation feel much more realistic.
Introduce a diversity nudge. Currently the top 5 results can all be from the same genre. A small penalty for consecutive same-genre picks would make the list more interesting.

9. Personal Reflection

This project taught me how to dive deep into all cases and edge cases. The AI was useful in brainstorming and handling the score algorithms. However, it was up to me to decide how certain songs were categorized. This project does come with a lot of bias, my analysis of songs may differ from someone elses. These are small details that neither the AI or myself can truly account for. I am not fully content with the visualization of my program. A future extension of this program would primarily be on the UI and not the backend.
