# Day 1 Rehearsal Script — Run This Before Oct 14

Goal: verify every live demo works end to end on a fresh Colab runtime, so nothing breaks live in front of 50+ students.

**Track to test:** Colab free tier, `all-MiniLM-L6-v2` for embeddings, your notebooks (Weeks 1-3 pattern) for RAG/Graph RAG, and the Day 2 starter for the hands-on lab.

Run the *entire* rehearsal once from a cold start. Note timing and any errors per step.

---

## Segment 1 (0:00–0:15) — Opening hook: the false-narrative demo

**What to rehearse:** your Week 2 "stock replenishment" failure case, live, cold-started (i.e., run it as if you've never run it before — this is exactly how it'll feel live on Oct 14).

Checklist:
- [ ] Colab notebook opens and runs top-to-bottom with zero manual fixes
- [ ] The exact conflated answer ("...shipped to the customer's warehouse yesterday...") reproduces — LLM outputs aren't always identical run-to-run, so if you get a different (but still wrong-in-spirit) answer, that's fine; if it suddenly answers *correctly*, you need a backup failure example ready (see below)
- [ ] Time yourself: this should take under 3 minutes end-to-end including narration

**Backup plan if the LLM "accidentally" gets it right this time:** LLM outputs aren't deterministic. Have a **second pre-recorded example** ready (screenshot or short video of a previous run) so the hook never depends on live reproducibility. Rehearse pulling this up smoothly, not scrambling for it.

---

## Segment 2 (0:15–0:45) — Embeddings & similarity (Week 1 material)

**What to rehearse:** the cosine similarity demo + the `[7]`/`[8]` misranking finding from your own Day 1.

Checklist:
- [ ] `sentence-transformers` model download completes within a reasonable time on fresh Colab (first run downloads ~90MB — test on venue Wi-Fi speed if possible, or pre-download and cache in the notebook you'll share)
- [ ] The misranking example reproduces clearly enough to explain in under 2 minutes without over-explaining the math

**Simplify for a room, not a 1:1 tutorial:** you don't need the full cosine-similarity-by-hand walkthrough here — one clean example (correct match) and one clean counter-example (near-miss) is enough. Rehearse the *shortened* version, not the full Week 1 depth.

---

## Segment 3 (0:45–1:15) — RAG pipeline + the break (Week 2 material)

**What to rehearse:** retrieval + generation, then the deliberate break — in your Colab notebook.

Checklist:
- [ ] `.env`/API key loads correctly on a **fresh Colab runtime**
- [ ] Rehearse what happens if the API call is slow/rate-limited live — have a pre-run output ready to show if the live call hangs more than ~10 seconds


---

## Segment 4 (1:15–1:45) — The fix: Graph RAG (Week 3 material)

**What to rehearse:** the Neo4j Aura connection + the `connected_order: None` proof — from the Colab notebook.

Checklist:
- [ ] **Aura Free instance status** — confirm it's not paused (Aura Free auto-pauses after inactivity; verify it's "Running" the morning of, not the night before)
- [ ] Driver connection succeeds on a fresh Colab run (you already hit a `ServiceUnavailable` mid-session once — rehearse the fix: `driver.close()` + recreate, so if it happens live you're not debugging cold)
- [ ] Confirm the two-cluster graph visualization renders correctly in the Aura Console query view you'll be screen-sharing

---

## Segment 5 (2:00-3:30) - Hands-on lab

Students open `day2_starter_notebook.ipynb`, run it, and do one guided step: add the Alumnus pattern and see the public positive control PP3 flip to "connected".

Checklist:
- [ ] Time the starter notebook from a cold start on a fresh Colab runtime (no cached anything). This is your realistic per-student setup time.
- [ ] With a **fresh Aura Free account**, confirm the graph-building cell finishes and prints per-pattern link counts
- [ ] Before the guided step, PP3 shows "NOT connected" in `run_pack(PUBLIC_POSITIVE)`; after adding the Alumnus pattern and re-running the graph cell, it shows "CONNECTED via Alumnus A002"
- [ ] If using a shared/pooled API key: have a few people (or scripted parallel calls) hit the same key at once and confirm it does not rate-limit into failure
- [ ] **Pilot the baseline:** run the public and hidden packs through `baseline_rag_answer` and note how often it actually fabricates. Do the same in the reference solution. This tells you how strongly to frame "baseline fails, graph works" on Day 1.

---

## What to log after each rehearsal run

For every segment: timing (actual vs. planned), any error encountered, and anything that behaved differently from the plan. This log is what turns into your final go/no-go call the day before the event — send it to me and we'll adjust the schedule/checklist together.
