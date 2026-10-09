# IEEE-CIS Amrita — Agentic AI + Knowledge Grounding Workshop
**Draft for review — Oct 14–15, 2026**
**Confirmed timings: Day 1, 8:30 AM–1:30 PM (5 hrs) · Day 2, 2:00–3:30 PM (90 min)**
**Expected attendance: 40–50 students**

---

## Design constraints (from what actually happened last time)

- **LangGraph + weather/AirNow demo:** followed by students who'd completed pre-reqs; others fell behind.
- **Lower-friction redo:** last time, students followed best where setup was lightest. This edition keeps to that: Colab only, a pre-built starter, and a shared key. (No n8n track this year.)
- **Recurring failure points:** Python environment setup, LLM API key availability, students not engaging with pre-read instructions.
- **Working assumption for this edition:** students will not read long pre-reads carefully. Every design choice below optimizes for *minimal setup, action over theory, and a working fallback at every step* — not for teaching completeness.
- **Timing constraint (new):** Day 2 is only 90 minutes — not enough time for teams to build *and* be judged. Day 2 is demo + judging only; all building happens in the gap between the two days, using the problem statement released at the end of Day 1.
- **Scale constraint (new):** 40–50 students means roughly 10–12 teams (at 4–5 students/team). That's too many for a full live rubric interview per team in 90 minutes — see the two-tier judging model below.

---

## Day 1 — Step-by-step schedule (8:30 AM–1:30 PM)

| Time | Activity | Format | Goal |
|---|---|---|---|
| 8:30–8:45 | **Opening hook:** live demo of an AI agent confidently stating a false fact by merging two unrelated records | You demo, no student action | Make the problem visceral before any theory — "watch it lie convincingly" |
| 8:45–9:15 | **Concept block 1 — Embeddings & similarity search** | Live demo only (your Week 1 notebook), light narration, no coding yet | Students see *why* retrieval finds "similar," not "correct" |
| 9:15–9:45 | **Concept block 2 — RAG pipeline + where it breaks** | Live demo (Week 2 notebook): show the exact conflated answer | Land the core lesson: fluent ≠ true |
| 9:45–10:15 | **Concept block 3 — Grounding the agent** | Live demo (Week 3 notebook): same query, graph-backed, now correct | Show the fix, motivate the hands-on lab |
| 10:15–10:30 | *Break* | | Also a buffer for late arrivals/setup |
| 10:30–12:30 | **Hands-on lab** | Students open `day2_starter_notebook.ipynb` in Colab, run it, and do **one guided step**: add the Alumnus pattern to the pattern registry and watch the public positive control PP3 flip from "no recorded link" to "connected". Everything else is left for the build window | Guided, plumbing is done. Students leave knowing how the registry works, and have run the starter once before Day 2 |
| 12:30–12:45 | *Buffer / mentor circulation* | Roaming TAs resolve individual blockers | Absorb the inevitable stragglers without derailing the group |
| 12:45–1:15 | **Problem statement release + team formation** | You present Day 2's problem statement live, walk through the rubric and the **submission deadline** | Teams leave Day 1 knowing exactly what "done" looks like and when it's due |
| 1:15–1:30 | **Wrap: build-window logistics, Q&A** | Confirm where/how to submit, office-hours availability if any | No team should be unsure how to submit before they leave the room |

**Why concepts come before any typing:** last time, students who skipped pre-reqs fell behind *during* the coding portion because they didn't yet have the concept to hang the code on. Front-loading three short, low-friction demos (no install required to watch) means everyone arrives at the hands-on lab with the same mental model, regardless of whether they did any pre-work.

---

## Pre-reads / resources — deliberately minimal

Given your read that students don't engage with lengthy instructions, cut pre-reads to the smallest thing that removes a Day 1 blocker — nothing else:

1. **One-page primer** (bullet points, not prose, ~5 min read): "What is RAG, and why does it sometimes lie?" — just enough to recognize the Day 1 opening demo, not a tutorial.
2. **A short video walkthrough (3–5 min), not a written setup guide** — screen-recorded, showing exactly what "ready for Day 1" looks like. Video consistently gets watched where multi-step text instructions get skimmed or skipped.
3. **One pre-built, zero-install Colab notebook link** — students open it, run one cell that prints "Setup OK," and that's the entire pre-read task. No local Python, no venv, no pip installs before the event.
4. **No individual LLM API key sign-up requirement** — see mitigation checklist below.
5. **One added step for this edition: each team creates a free Neo4j Aura account** before Day 2's build window opens. Day 1's grounding fix (notebook 3) is Neo4j-based, and the Day 2 starter builds its graph in Neo4j the same way — this is the one piece of individual account setup that can't be pooled like the LLM key, so flag it clearly at the Day 1 problem-statement release, not buried in a pre-read.

Total pre-read time target: **under 15 minutes**, one link to click, one cell to run, one video to watch — plus the one Neo4j Aura signup, done once between Day 1 and Day 2.

---

## Environment/failure mitigation checklist

Directly targeting last time's hiccups:

- [ ] **Provide a shared, pre-funded LLM API key** (or a small pool of keys) with a usage cap — removes "I couldn't get an API key in time" as a failure mode entirely.
- [ ] **Default to Colab, not local Python** — zero install, works identically on any student's laptop/OS.
- [ ] **Pre-test the starter notebook 48 hours before the event** end-to-end, on a fresh Colab runtime and a fresh Aura account, exactly as a student would.
- [ ] **Pre-load/cache any datasets or models** referenced in the lab — no live downloads competing for venue Wi-Fi during the session.
- [ ] **1–2 roaming mentors per 4–5 teams** during the hands-on lab, specifically hunting for setup issues rather than teaching content.
- [ ] **Confirm every team has a working Neo4j Aura Free account before they leave Day 1** — this is the one piece of setup that's per-team, not pooled; a team that only discovers Aura signup friction during the build window loses build time, not lab time.

---

## Day 2 — Problem statement (v4: "Complete the grounding")

**Working title:** *"Build an agent that tells the truth about what it doesn't know."*

**Why this version.** Designing a grounding mechanism from scratch is too much for the build window. So teams receive a **complete, working pipeline** and one decision that matters: *which parts of a record identify a single event?*

**The scenario (given to teams):** campus operations and student services (a different domain from Day 1), 179 records across 14 categories. Departments describe different events in similar words (a hostel room allotment vs. a maintenance fee, both mention "room"). Most records stand alone; some name a person, club or ticket (`Student S001`, `Club RC-1`, `HMT-58`). Where such an ID repeats, it IS the same event, so the task is not "always say unrelated", it is "tell the two cases apart." See `day2_dataset_generator.py`.

**What teams receive (`day2_starter_notebook.ipynb`):** retrieval, the plain baseline RAG, Neo4j graph building driven by a **pattern registry**, and a grounded answer step (record IDs in the context, the checked verdict beside every pair, `temperature=0`). The registry contains **one** pattern: the Student ID regex.

**What teams do in the build window**
1. Explore the data and decide which other strings identify one event (**Kind 1**: person IDs, club codes, ticket numbers) and which are incidental fields reused across unrelated events (**Kind 2**: room, block, amount, semester).
2. Add their patterns to the registry, each with an example and a reason. List the lookalikes they *rejected* and why.
3. Run the **public pack** (8 adversarial + 3 positive-control questions) against baseline and grounded, and fill in an outcomes table: did the baseline fabricate, was grounded correct, and why, in terms of their patterns.
4. State **one failure they still have.**

**Why this teaches the lesson.** Add too little and real links are missed (positive controls fail). Add too much and unrelated records get linked (adversarial questions fail). The only way to score well is to understand what makes an identifier an identifier.

**What the judges run:** a **hidden pack** of the same shapes: 9 adversarial questions (including Kind 2 traps the public pack does not cover: Room 118, the 46000 payment/refund, the shared spring semester) and 4 positive controls (including ticket HMT-58 and Club RC-1, which need patterns the starter does not have).

**Submission deadline: 2 hours before the Day 2 session** (e.g., 12:00 PM for a 2:00 PM start), announced at the Day 1 problem-statement release. Deliverable: the notebook, run top to bottom on a fresh runtime, with the registry, outcomes table and remaining-failure note filled in.

**Why this is objectively gradable:** every question carries the two records it is about and whether they are truly connected. `day2_offline_check.py` reproduces the structural verdict from a team's registry alone, with no Neo4j or LLM, so batch scoring is fast and consistent.

### Evaluation rubric

| Criterion | Weight | How it's scored |
|---|---|---|
| **No fabricated connections** | 30% | Hidden adversarial pack (9 questions), pass/fail each: did the grounding link two records that are not connected? |
| **Affirms real links** | 20% | Hidden positive controls (4), pass/fail each: did it correctly say "connected"? Guards against a system that just says "unrelated" to everything |
| **Pattern choices and rationale** | 20% | Kind 1 coverage (40) + Kind 2 restraint (30) + rationale quality (30). Each adopted pattern needs an example and a same-event argument; rejected lookalikes need a data-based reason |
| **Explaining outcomes** | 20% | Outcomes table complete for the public pack, causes correctly attributed (pattern vs. retrieval), one specific and honest remaining failure |
| **Runs end-to-end** | 5% | Binary: runs on a fresh runtime at judging time |
| **Live demo clarity** | 5% | Fixed checklist: states the answer clearly, cites record IDs, can explain one row of their outcomes table, within time |

**Key design choice:** retrieval is given, so it is no longer scored. The scarce skill being judged is recognizing what identifies an event, and the cost of getting it wrong in either direction.

**Baseline caveat to pilot before the event:** the starter's baseline uses the plain Week 2 prompt. With a strict "use ONLY the context" prompt, the baseline can pass many adversarial questions (it did on the earlier hidden set). Run the public and hidden packs against the starter's baseline once and see how often it fabricates. If it rarely does, make the questions presuppose a link more strongly, or tell teams that the baseline-vs-grounded contrast is one of several things they explain, not the whole score.

---

## Day 2 — Two-tier judging model (batch + live checkpoint)

With ~10–12 teams and only 90 minutes, a full live rubric interview per team doesn't fit. Judging splits into two tiers:

**Tier 1 — Batch scoring (before 2:00 PM, no team present):**
Covers 70% of the rubric: No fabricated connections (30%), Affirms real links (20%) and Pattern choices (20%). Read each team's registry, save it as JSON, and run `day2_offline_check.py` to get the structural marks for the hidden pack. For teams near a decision boundary, also run their notebook live against the hidden pack, since the offline check does not simulate retrieval or the LLM's wording.

**Tier 2 — Live checkpoint (2:10–~3:00 PM, ~3 min/team):**
Covers Explaining outcomes (20%), Runs end-to-end (5%) and Live demo clarity (5%). Each team shows their registry and outcomes table and explains one row you choose. If batch results flagged something (a false link, a missed positive), ask about that row.

### Day 2 — Revised timing (2:00–3:30 PM)

| Time | Activity | Duration |
|---|---|---|
| 2:00–2:10 | Instructions, demo order, housekeeping | 10 min |
| 2:10–~3:00 | Live checkpoints, ~3 min/team across ~10–12 teams | ~50 min |
| 3:00–3:20 | Judges' deliberation | 20 min |
| 3:20–3:30 | Results + wrap | 10 min |

**Judging independence:** if co-judges are confirmed, each scores independently using their own copy of `day2_judging_scorecard.xlsx` (batch results tab shared as the common factual base, but the live-checkpoint scoring and notes stay private per judge until deliberation) — this avoids one judge's read anchoring another's before scores are compared.

---

## Open items for your review

1. Confirm whether there will be co-judges, so the deliberation step (3:00–3:20) can be planned as a reconciliation step across scorecards rather than just your own sign-off.
2. Confirm the submission mechanism (a shared drive folder, a form, email) so it's ready before Day 1 ends.
3. `day2_dataset_generator.py` (v4), `day2_offline_check.py`, `day2_starter_notebook.ipynb`, `day2_reference_solution.ipynb`, `judges_evaluation_question_bank.md` and `day2_judging_scorecard.xlsx` are updated for the new format.
4. **Pilot the starter and both question packs once, with a real OpenAI key and Aura instance.** The notebooks were checked against mock services only, so the live LLM wording and retrieval have not been exercised.
