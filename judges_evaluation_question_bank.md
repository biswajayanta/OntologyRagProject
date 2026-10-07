# Judges' Evaluation Question Bank — Day 2 Competition

**Use this with `day2_judging_scorecard.xlsx`, not instead of it.** With ~10–12 teams and a 90-minute live slot (2:00–3:30 PM), there isn't time for a full interview per team — scoring runs in two tiers:

- **Tier 1 (batch, before 2:00 PM, submissions due 2 hrs ahead):** run the hidden test set on every team's submission with nobody present. This produces the numbers for Retrieval correctness (25%) and No fabricated connections (35%) — fill these into the `Batch Test Results` tab of the scorecard.
- **Tier 2 (live, ~3 min/team during the session):** covers Runs end-to-end (15%) and Live demo clarity (10%), plus Grounding mechanism (15%) if you didn't finish that in the code-review pass beforehand. The question bank below is for this tier — short, targeted, and using the batch results to decide *which* question is worth asking a given team, rather than running the full bank on everyone.

If you have co-judges, score independently in your own copy of the scorecard and reconcile only at the 3:00–3:20 PM deliberation slot — don't compare live-checkpoint scores with them while you're still scoring.

---

## Before the live session: run the hidden test set (Tier 1)

Do this identically for every team's submission, with nobody present:

1. Feed their running system the **7 hidden adversarial questions** (see `day2_dataset_generator.py` → `hidden_adversarial_tests`), the **3 positive-control questions** (`hidden_positive_control_tests` — correct answer is "yes, connected," not "unrelated"), and a fixed set of retrieval test questions (5 suggested — draft these against the specific dataset once it's finalized). All are unseen by teams.
2. Record, per question: did it retrieve the right records? For the adversarial set, did it fabricate a connection, or correctly say "unrelated"? For the positive-control set, did it correctly affirm the connection, or did it also default to "unrelated" — which would mean it isn't really checking anything?
3. Enter results into the `Batch Test Results` tab — Retrieval %, Fabrication %, and the separate Positive Control column.
4. Use these results going into the live checkpoint to decide what's worth asking: a team that failed a hidden question is worth a direct question about it live; a team that aced the adversarial set but failed every positive control is worth asking about directly too — that pattern usually means "always say unrelated," not a real check.

---

## 1. Retrieval correctness (25%)

**Goal:** confirm retrieval is finding the right category of record, not just "something similar-sounding."

Ask:
- "Walk me through what happens between me typing a question and your system finding a record — what does it actually search over?"
- "Show me a question where your system retrieved the *wrong* record. Why do you think that happened?" (A team that can't produce one either hasn't tested edge cases, or is being unconvincing — probe further.)
- "If I doubled your dataset size, what in your system would need to change?"

**Strong answer:** names the embedding model, explains similarity search in their own words, can point to at least one real failure case they found themselves.
**Weak answer:** can't explain what "similar" means in their system, treats retrieval as a black box they copy-pasted, has never tried an adversarial question themselves.

---

## 2. No fabricated connections (35%) — the core criterion

**Goal:** this is the whole point of the exercise. Spend the most interview time here.

Ask, using 2–3 questions from your hidden set that they haven't seen:
- "Here's a question I haven't shown you before: [ask one hidden adversarial question live]." Watch what it says — does it confidently merge two records, or does it correctly flag "these don't appear related in the data"?
- "How does your system know when it *shouldn't* connect two records?" — this is the key design question. Listen for: an explicit schema/graph/entity check, vs. "the LLM is just prompted to be careful" (weaker — prompting alone doesn't reliably fix this, and they should know that from Day 1's demo).
- "Show me the actual mechanism in your code/workflow that prevents this — not the prompt text, the logic."
- If they used n8n: "Which node or step is doing the connection-checking — is it explicit logic, or are you trusting the LLM node to self-police?"

**Strong answer:** can point to a specific structural check — ideally a Neo4j graph traversal (`shortestPath` / `connected_order`-style), the same mechanism taught on Day 1 — that would catch a fabricated link even if the LLM's phrasing tried to imply one. A lesser structural check (entity-ID match, a lookup table) still counts as real, just weaker. Understands *why* prompting alone (e.g., "don't make things up") is insufficient — ties back to the Day 1 lesson.
**Weak answer:** relies entirely on prompt instructions ("I told it to only use the context"), cannot explain what actually stops a false merge, or — worst case — the live hidden-question test just showed it fabricating a connection in front of you.

**Scoring note:** this criterion is graded primarily off the hidden test set results you already recorded, not off how well the team talks about it. Use the interview to catch a team that got lucky on the hidden set but has no real mechanism (talks like the weak-answer pattern) vs. a team that got one hidden question wrong despite a sound mechanism (partial credit, not zero).

---

## 3. Grounding mechanism present (15%)

**Goal:** did they build something beyond raw vector similarity, or is it retrieval + LLM and nothing else?

Ask:
- "If I asked you to draw your data model on a whiteboard right now, what would it look like — a flat list, or something with structure?"
- "Is there anywhere in your system where a relationship between two records is checked as a hard fact, rather than inferred from text similarity?"
- "What would you add next if you had one more day?" (A team with real grounding usually names the *next* structural improvement — e.g., "add disjointness rules," "handle transitive relationships." A team with no grounding usually says "better prompts" or "bigger model.")

**Strong answer:** a working Neo4j graph with an actual path/connectivity check — full credit, and what was taught on Day 1. A simple lookup table of valid category pairs is a real step beyond raw similarity too, and earns partial credit, but isn't the target mechanism this year.
**Weak answer:** the entire system is "embed everything, retrieve top-k, ask the LLM" with no explicit structure anywhere.

---

## 4. Runs end-to-end on judge's test set (15%)

**Goal:** this is mostly binary and mechanical — you're confirming what you already saw.

Ask (only if it broke):
- "What just failed — is that a live-demo hiccup, or would it fail the same way every time?"
- "If it's an API/rate-limit issue: is that a fundamental design gap, or bad luck on timing?"

**Strong answer:** if something breaks, the team immediately knows why (and it's plausibly an infra hiccup, not a design flaw) and can show it working via a backup/recording.
**Weak answer:** the team is surprised by the failure and can't explain it, or the failure is a repeatable design bug (e.g., crashes on any question containing a certain word).

---

## 5. Live demo clarity (10%)

**Goal:** fixed checklist, minimal subjectivity — walk through it in order.

- [ ] States the final answer to the judge's question clearly and directly (not buried in a paragraph)
- [ ] States which record(s) it used to answer, or explicitly says "insufficient information" when that's correct
- [ ] Stays within the ~3-minute checkpoint window
- [ ] If asked "why did it answer that," someone on the team — not just one person — can explain the mechanism

Score each box yes/no per team; this criterion should need almost no judgment call.

---

## Rendering the final judgment

Don't hand-calculate this — `day2_judging_scorecard.xlsx`'s "My Independent Scoring" tab pulls in the batch results and computes the weighted total and rank automatically as you fill in the three live-checkpoint scores per team. For each team, you'll have entered:
1. Hidden test set results (pulled in automatically — retrieval %, fabrication %)
2. Grounding mechanism score (from your code-review pass, done before or alongside the live checkpoint)
3. Runs end-to-end + Live demo clarity (filled live, from the checkpoint above)

When two teams are close, let the **"No fabricated connections"** criterion break the tie — it's weighted highest (35%) because it's the actual lesson of the two days; a team that nails retrieval but occasionally still fabricates a link has learned less than a team that's slightly slower but never does.

Log a one-line note per team in the scorecard's "Judge notes" column right after their checkpoint — you'll want it later if anyone asks how the judging worked, and you won't remember 10–12 teams' specifics by the end of the day, especially if reconciling scores with co-judges afterward.
