# Judges' Evaluation Question Bank: Day 2 Competition (v4, "Complete the grounding")

**Use this with `day2_judging_scorecard.xlsx`, not instead of it.** With ~10-12 teams and a 90-minute live slot (2:00-3:30 PM), scoring runs in two tiers:

- **Tier 1 (batch, before 2:00 PM, submissions due 2 hrs ahead):** read each team's pattern registry and run the hidden pack. Produces No fabricated connections (30%), Affirms real links (20%) and Pattern choices (20%).
- **Tier 2 (live, ~3 min/team):** Explaining outcomes (20%), Runs end-to-end (5%), Live demo clarity (5%). The questions below are for this tier. Use the batch results to decide *which* question is worth asking each team.

If you have co-judges, score independently in your own copy of the scorecard and reconcile only at the 3:00-3:20 PM deliberation.

**What teams were given:** a working pipeline with ONE regex (Student ID) in a pattern registry. They extended the registry, ran an 8+3 question public pack, and wrote an outcomes table plus one remaining failure. They never saw the hidden pack.

---

## Before the live session: Tier 1

For every team, with nobody present:

1. Open the notebook. Read the `PATTERNS` and `REJECTED_CANDIDATES` cells. Note the pattern names.
2. Count **Kind 1 added beyond Student** (Alumnus, Club, Ticket: 0-3) and **Kind 2 adopted** (Room, Block, Amount, Semester, or any other incidental field).
3. Save the registry as JSON (`[{"name": ..., "regex": ...}, ...]`) and run `python day2_offline_check.py team_registry.json`. Copy the 1/0 marks for **H1-H9** (hidden adversarial) and **HP1-HP4** (hidden positive) into the `Batch Test Results` tab.
4. For teams near a boundary, run their notebook live against the hidden pack (`day2_reference_solution.ipynb` section 8b shows how) and read the LLM's wording. The offline check does not simulate retrieval or the answer text.
5. Decide what to ask live:
   - A team with false links (adversarial failures): ask which pattern caused it.
   - A team with all adversarial passes but missed positives: ask what strings they did *not* check. That pattern usually means they linked on too little.
   - A team with both clean: ask the Kind 1 vs Kind 2 question below.

**What each hidden question tests**

| ID | Tests | A team fails it if it adopted... |
|---|---|---|
| H1-H6 | Vocabulary overlap and cross-category causal traps | (fails only if linking on very loose patterns) |
| H7 | Room 118 shared by two different students | a **Room** pattern |
| H8 | 46000 payment (S009) vs. an unrelated 46000 refund | an **Amount** pattern |
| H9 | "spring semester" shared by library and shuttle records | a **Semester** pattern |
| HP1 | HMT-58 ticket (needs a Ticket pattern) | missed **Ticket** |
| HP2 | Student S001 (works with the given Student pattern) | (removed Student) |
| HP3 | Club RC-1 (needs a Club pattern) | missed **Club** |
| HP4 | Alumnus A001 (needs an Alumnus pattern) | missed **Alumnus** |

---

## 1. Pattern choices and rationale (20%)

**Goal:** can the team tell an identifier from an incidental field, and defend it with the data?

Ask:
- "Which of your patterns are Kind 1 and which Kind 2? How do you tell?"
- "Pick a pattern you rejected. What in the data convinced you?" (Strong teams cite a specific record, e.g. Room 118 appearing for two different students.)
- "Pick a pattern you adopted. If I saw that same string in a record from last year, would it still be about the same event?"

**Strong answer:** Kind 1 = a string that is issued once per person, club or case and would still point to it anywhere. Kind 2 = a value reused across unrelated events (place, amount, time period). Uses specific records as evidence.
**Weak answer:** "more patterns means more links", or "it repeated, so it must matter." Treats every repeating string as an identifier.

**Score it in the `Pattern Score` tab:** coverage and restraint are automatic from the batch counts. You enter rationale quality (0-30): each adopted pattern has an example and a same-event argument (0-10), rejected lookalikes have data-based reasons (0-10), and the team can articulate Kind 1 vs. Kind 2 live (0-10).

---

## 2. No fabricated connections (30%) and Affirms real links (20%)

**Goal:** these are scored from the hidden pack, not from how well the team talks. Use the interview to catch a team that got lucky vs. one that understands.

Ask:
- "Here is a question you haven't seen: [one hidden adversarial question]. What does your system say, and why?"
- "Does your agent ever say two things ARE connected, or does it only ever say 'unrelated'?" (a fast way to spot a system that just learned to hedge)
- "If I added 500 new records tomorrow, what would break and what would keep working?"

**Strong answer:** explains the verdict by naming the shared entity (or the absence of one). Understands that the registry, not the prompt, decides what gets linked.
**Weak answer:** "we told the LLM to be careful", or blames the LLM for a link that their own pattern created.

**Scoring note:** a team that passes everything adversarial but fails several positives gets full marks on one criterion and lost marks on the other. That is intended: both failure modes matter.

---

## 3. Explaining outcomes (20%)

**Goal:** can the team trace each result to its cause?

Ask (pick one row from their outcomes table, ideally a failure):
- "Why did this one come out this way?"
- "Where did the baseline fabricate and your graph didn't? What did your graph know that the baseline didn't?"
- "You said your remaining failure is [X]. How would you find out whether it happens on a real question?"

**Strong answer:** attributes causes correctly (a pattern linked the records; retrieval did not return both; the link is written without an ID). The remaining failure is specific, plausible and testable.
**Weak answer:** blames the LLM without checking which pattern created the link; vague remaining failure ("sometimes it's wrong"); the outcomes table is incomplete or copied.

**Watch for:** a table where every row says "correct" with no remaining failure. Real systems have a limit; a team that cannot name one has not looked.

---

## 4. Runs end-to-end (5%)

Mostly binary. Ask only if it broke:
- "Is that a one-off (API, network, a paused Aura instance) or would it fail every time?"

**Strong:** knows why it failed, and shows it working from a backup run.
**Weak:** surprised by the failure, or it is a repeatable bug.

---

## 5. Live demo clarity (5%)

Fixed checklist, yes/no each:
- [ ] States the answer to your question directly
- [ ] Cites the record IDs it used, or says "no recorded link" when that is right
- [ ] Stays within ~3 minutes
- [ ] More than one team member can explain one row of the outcomes table

---

## Rendering the final judgment

`day2_judging_scorecard.xlsx` computes this for you. Weights: No fabrication 30% | Positives 20% | Pattern score 20% | Explaining outcomes 20% | Runs 5% | Demo 5%.

When two teams are close, break the tie on **pattern rationale**. It is the clearest sign of understanding: a team that knows why a room number is not an identifier will handle the next dataset too.

Log a one-line note per team in "Judge notes" right after their checkpoint. You will not remember 10-12 teams' specifics at the end of the day.
