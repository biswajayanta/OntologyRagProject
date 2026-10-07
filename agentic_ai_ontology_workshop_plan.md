# IEEE-CIS Amrita — Agentic AI + Knowledge Grounding Workshop
**Draft for review — Oct 14–15, 2026**
**Confirmed timings: Day 1, 8:30 AM–1:30 PM (5 hrs) · Day 2, 2:00–3:30 PM (90 min)**
**Expected attendance: 40–50 students**

---

## Design constraints (from what actually happened last time)

- **LangGraph + weather/AirNow demo:** followed by students who'd completed pre-reqs; others fell behind.
- **n8n + OpenAI redo:** more students could follow — lower setup friction than raw Python.
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
| 10:30–12:30 | **Hands-on lab** | Students build a minimal grounded agent from a pre-built template — Colab (code) track or n8n (no-code) track | Guided, most plumbing done — students customize, not build from scratch |
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
4. **A shared n8n workflow template (import-only)** for teams who prefer low-code, matching what worked better last time.
5. **No individual LLM API key sign-up requirement** — see mitigation checklist below.
6. **One added step for this edition: each team creates a free Neo4j Aura account** before Day 2's build window opens. Day 1's grounding fix (notebook 3) is Neo4j-based, and Day 2 requires teams to build their own grounding mechanism the same way — this is the one piece of individual account setup that can't be pooled like the LLM key, so flag it clearly at the Day 1 problem-statement release, not buried in a pre-read.

Total pre-read time target: **under 15 minutes**, one link to click, one cell to run, one video to watch — plus the one Neo4j Aura signup, done once between Day 1 and Day 2.

---

## Environment/failure mitigation checklist

Directly targeting last time's hiccups:

- [ ] **Provide a shared, pre-funded LLM API key** (or a small pool of keys) with a usage cap — removes "I couldn't get an API key in time" as a failure mode entirely.
- [ ] **Default to Colab, not local Python** — zero install, works identically on any student's laptop/OS.
- [ ] **Offer n8n as the low-code alternative**, matching what demonstrably worked better last time for less code-comfortable students.
- [ ] **Pre-test both paths 48 hours before the event** end-to-end, on a fresh account, exactly as a student would.
- [ ] **Pre-load/cache any datasets or models** referenced in the lab — no live downloads competing for venue Wi-Fi during the session.
- [ ] **1–2 roaming mentors per 4–5 teams** during the hands-on lab, specifically hunting for setup issues rather than teaching content.
- [ ] **Confirm every team has a working Neo4j Aura Free account before they leave Day 1** — this is the one piece of setup that's per-team, not pooled; a team that only discovers Aura signup friction during the build window loses build time, not lab time.

---

## Day 2 — Problem statement

**Working title:** *"Build an agent that tells the truth about what it doesn't know."*

**The scenario (given to teams):** a deliberately *different domain* from the Day 1 demo — campus operations and student services, not the enterprise customer/order data you demoed with. Records are scattered across departments that use overlapping, inconsistent language — the same underlying facts, described in ways that sound similar but aren't the same event (e.g., a hostel room allotment vs. a facilities maintenance fee — both mention "room," neither is the other). Most records are standalone, but some explicitly name a person or ticket ID (`Student S001`, `HMT-58`) — where that ID genuinely repeats across two records, it IS the same event, so the task isn't "always say unrelated," it's "tell the two cases apart." See `day2_dataset_generator.py` for the full 14-category, 172-record dataset, the held-out adversarial test set (7 questions — four target vocabulary-overlap pairs, two go further and test whether the agent invents a *causal* link across categories that don't share vocabulary at all, and one tests whether the agent links on an incidental descriptive field, like a room number, instead of a genuine per-event identifier), and 3 positive-control questions (correct answer: "yes, connected"). Using a new domain, rather than reusing the demo dataset, means teams are tested on whether they understood the *pattern*, not on how well they memorized your walkthrough.

**The task:** build an agent (any framework — Colab/Python or n8n) that answers natural-language questions using this dataset — **never asserting a relationship between two records that don't actually reference the same event, and correctly affirming one when the data genuinely supports it.** **The grounding mechanism itself should be Neo4j-based**, matching Day 1's notebook 3 — teams each create a free Aura account for this — so what's taught and what's judged stay consistent. A lesser structural check (e.g. a lookup table) still earns partial credit on Grounding Mechanism below; prompting alone earns none.

**Why this is unambiguous and objectively gradable:** every record in the dataset carries a hidden ground-truth category label, invisible to teams but known to judges. This lets every part of the rubric below be checked mechanically against a fixed answer key, not judged by feel.

**Submission deadline: 2 hours before the Day 2 session** (e.g., 12:00 PM if the session starts at 2:00 PM). This is announced at the Day 1 problem-statement release (12:45–1:15 PM) so every team knows it before they leave the room. The deadline exists so batch scoring (below) can run *before* the 90-minute live slot, not compete with it.

### Evaluation rubric

| Criterion | Weight | How it's scored (objective) |
|---|---|---|
| **Retrieval correctness** | 25% | For a fixed, judge-held set of test questions, % of retrieved records matching the correct ground-truth category |
| **No fabricated connections** | 35% | A fixed panel of adversarial ambiguous questions (unseen by teams in advance) — binary pass/fail per question: did the agent state or imply a link between two records that don't share ground-truth category/entity? |
| **Grounding mechanism present** | 15% | Checklist-scored code review: full credit for a working Neo4j graph check (consistent with Day 1); partial credit for a lesser explicit structure (e.g. a lookup table); zero for prompting-only. Yes/no per sub-item, not a subjective quality judgment |
| **Runs end-to-end on judge's test set** | 15% | Binary: does it execute without crashing on a held-out question set at judging time |
| **Live demo clarity** | 10% | Fixed checklist (states the answer clearly, cites which record(s) it used, stays within time limit) — not open-ended presentation scoring |

**Key design choice:** the "no fabricated connections" test uses questions teams have never seen, scored against a known-correct answer (whether a connection genuinely exists) — this is what makes the criterion objective rather than a judge's subjective read of "did that sound plausible."

---

## Day 2 — Two-tier judging model (batch + live checkpoint)

With ~10–12 teams and only 90 minutes, a full live rubric interview per team doesn't fit. Judging splits into two tiers so the score stays consistent regardless of what order a team gets seen live:

**Tier 1 — Batch scoring (before 2:00 PM, no team present required):**
Covers 60% of the rubric (Retrieval correctness 25% + No fabricated connections 35%) plus most of Grounding mechanism (15%). Run every submitted agent against your fixed retrieval test questions and the hidden adversarial questions in `day2_dataset_generator.py`. This happens in the gap between the submission deadline and the live session — you're not scoring under time pressure with the team watching.

**Tier 2 — Live checkpoint (2:10–~3:00 PM, ~3 min/team):**
Covers what genuinely needs a live moment: Runs end-to-end (15%) and Live demo clarity (10%). Each team runs their agent once, and if their batch results flagged something borderline (e.g., they failed one hidden question), you ask them to explain it live rather than re-testing everything from scratch.

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
3. `day2_dataset_generator.py`, `judges_evaluation_question_bank.md`, and `day2_judging_scorecard.xlsx` are ready — flag if you want the retrieval test questions (5 suggested in the scorecard) drafted for you as well, since those aren't in the dataset file yet.
