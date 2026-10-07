# Day 1 Rehearsal Script — Run This Before Oct 14

Goal: verify every live demo works on **both** implementation routes, so nothing breaks live in front of 50+ students regardless of which one a team picks.

**Two tracks to test, identically:**
- **Colab track (code path):** Colab free tier, `all-MiniLM-L6-v2` for embeddings, your notebooks (Weeks 1–3 pattern) for RAG/Graph RAG
- **n8n track (no-code path):** n8n free-tier account, OpenAI node wired to your shared API key, same retrieval → generation → grounding-fix flow rebuilt as a workflow instead of code

Run the *entire* rehearsal once on each track. Note timing and any errors per step. This directly targets last time's split — some students followed the LangGraph/Python demo, others followed better via n8n — so Day 1 has to work equally well demoed either way.

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

**What to rehearse:** retrieval + generation, then the deliberate break — once in your Colab notebook, once as an n8n workflow (HTTP/embedding node → OpenAI node, same prompt).

Checklist — Colab:
- [ ] `.env`/API key loads correctly on a **fresh Colab runtime**
- [ ] Rehearse what happens if the API call is slow/rate-limited live — have a pre-run output ready to show if the live call hangs more than ~10 seconds

Checklist — n8n:
- [ ] Rebuild the same retrieval → prompt → OpenAI-node flow in a **fresh n8n free-tier account** (not your existing one, which already has saved credentials/history)
- [ ] Confirm the OpenAI node picks up the shared API key via n8n credentials, not hardcoded in a node field (so you can rotate/revoke centrally)
- [ ] Confirm the same conflated "stock replenishment" failure reproduces in n8n's output panel, not just in Colab — the lesson has to land the same way regardless of which tool a team is watching

---

## Segment 4 (1:15–1:45) — The fix: Graph RAG (Week 3 material)

**What to rehearse:** the Neo4j Aura connection + the `connected_order: None` proof — once from the Colab notebook, once from an n8n Neo4j/HTTP node hitting the same Aura instance.

Checklist:
- [ ] **Aura Free instance status** — confirm it's not paused (Aura Free auto-pauses after inactivity; verify it's "Running" the morning of, not the night before)
- [ ] Driver connection succeeds on a fresh Colab run (you already hit a `ServiceUnavailable` mid-session once — rehearse the fix: `driver.close()` + recreate, so if it happens live you're not debugging cold)
- [ ] Confirm the two-cluster graph visualization renders correctly in the Aura Console query view you'll be screen-sharing
- [ ] If demoing the n8n route for this segment too: confirm an n8n node can reach Aura (same URI/credentials pattern) from a fresh n8n account without a firewall/allowlist surprise

---

## Segment 5 (2:00–3:30) — Hands-on lab

This is the segment most likely to reveal Colab-vs-n8n divergence, since **students** will be running this, not you — some teams will build in notebooks, others in n8n, exactly like last time.

Checklist:
- [ ] Time how long the Colab starter notebook takes to run end-to-end from a cold start (no cached anything) — this is your realistic per-student setup time estimate for the code path
- [ ] Time how long importing and running the n8n starter template takes on a **brand-new, never-configured** n8n account (not yours, which already has history/config) — ask someone to test this on a fresh signup if possible
- [ ] If using a shared/pooled API key across both tracks: rehearse what happens under **concurrent load** — have a few people (or scripted parallel calls) hit the same key simultaneously across Colab and n8n at once, and confirm it doesn't rate-limit into failure
- [ ] Confirm both starter kits (Colab notebook link, n8n template) are labeled clearly enough that a team knows which one they picked and doesn't mix instructions from the other

---

## What to log after each rehearsal run

For every segment: timing (actual vs. planned), any error encountered, and whether the Colab track and the n8n track behaved differently. This log is what turns into your final go/no-go call the day before the event — send it to me and we'll adjust the schedule/checklist together.
