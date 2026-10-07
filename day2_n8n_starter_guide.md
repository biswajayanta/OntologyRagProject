# Day 2 Starter Guide — n8n (No-Code Track)

This mirrors `day2_starter_notebook.ipynb` exactly — same dataset, same broken baseline, same task — rebuilt as an n8n workflow instead of Python. **Build and test this yourself first** (per your own request) before handing it to teams as a template; the steps below are a build guide, not a guaranteed-working export, since n8n workflows need to be wired up and run in your actual account to confirm they behave.

Prerequisite: run section 7 of the Colab notebook once to produce `campus_embeddings_export.json` (172 records with precomputed embeddings, across 14 categories) — this avoids needing an embeddings API call inside n8n for every record every time the workflow runs.

**Not everything in the dataset is unrelated.** Most overlapping-looking record pairs genuinely are separate events, but some records explicitly name a person or ticket ID (e.g. `Student S001`, `HMT-58`) — where that ID repeats across two records, it's a genuine connection. A grounding check that just defaults to "these are unrelated" for anything ambiguous will fail those cases — make sure the IF node's branching can go either way, not just toward "unrelated."

**Grounding mechanism: Neo4j, same as the Colab track.** Teams create their own free Neo4j Aura account either way, so the grounding check below should hit that graph — not a lookup table — to keep both tracks consistent with what Day 1 taught.

---

## Workflow structure

```
[Manual Trigger] → [Set: question] → [HTTP Request: OpenAI Embeddings]
                                            ↓
                    [Code: cosine similarity retrieval]
                                            ↓
                    [Code / IF: grounding check ← YOUR TASK]
                                            ↓
                    [OpenAI: Chat Completion]
                                            ↓
                                       [output]
```

## Step-by-step

**1. Manual Trigger node** — for testing during the build. Swap for a Webhook or Chat Trigger later if you want teams to expose it as a chat interface.

**2. Set node — `question`**
Add a string field `question` with a test value, e.g. `"Did the student who got a new hostel room also get billed for a repair?"` — matches the self-test questions in the notebook, so both tracks can be sanity-checked against the same cases.

**3. HTTP Request node — embed the question**
- Method: POST
- URL: `https://api.openai.com/v1/embeddings`
- Auth: use n8n's credential store for your OpenAI API key (not hardcoded in the node — this is what lets you rotate/revoke centrally, and what to check first if something breaks under shared-key load)
- Body (JSON): `{"model": "text-embedding-3-small", "input": "{{ $json.question }}"}`
- **Note:** the notebook uses `all-MiniLM-L6-v2` (local, free) for its embeddings, but n8n's HTTP Request node calling OpenAI's embeddings endpoint is the more reliable no-code path. This means `campus_embeddings_export.json` needs to be **re-generated with an OpenAI embedding model** if you want the two tracks numerically comparable — or just accept they use different embedding spaces, which doesn't affect judging (the rubric doesn't care which embedding model was used).

**4. Code node — load the dataset + compute cosine similarity**
Paste the contents of `campus_embeddings_export.json` as a static variable at the top of the Code node (n8n's Code node runs JavaScript), then:
```javascript
const data = /* paste the exported JSON here */;
const questionEmbedding = $input.first().json.data[0].embedding;

function cosineSim(a, b) {
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

const scored = data.texts.map((text, i) => ({
  text,
  label: data.labels[i],
  score: cosineSim(questionEmbedding, data.embeddings[i]),
}));

scored.sort((a, b) => b.score - a.score);
const topK = scored.slice(0, 3);

return topK.map(item => ({ json: item }));
```

**5. HTTP Request / Code node — grounding check against Neo4j (YOUR TASK, same as the notebook)**
This is the piece with no default implementation — same gap as the notebook's `grounded_answer`. Build it against your Neo4j Aura instance, the same tool the Colab track's notebook 3 and reference solution use, so both tracks are held to the same expected mechanism:
- An **HTTP Request node** hitting Neo4j Aura's query API (or n8n's dedicated Neo4j community node, if available in your instance) with a `shortestPath` Cypher query between the retrieved records' matched graph nodes — same check as notebook 3's `connected_order`.
- An **IF node** downstream that branches on the query result: if no path was found, force a "these appear unrelated" response instead of letting the OpenAI node improvise from wording alone.
- A **Code node** that formats the graph query's result into plain-text facts before handing them to the OpenAI node — same idea as the notebook's `facts_from_rows()`, so the LLM is told the graph's verdict explicitly rather than inferring it.

A lookup table or a plain "be careful" prompt instruction is not the target here — build the actual Neo4j check, since every team has an Aura account either way.

**6. OpenAI node — Chat Completion**
- Model: `gpt-4o-mini` (or whichever matches your shared API budget)
- Prompt: aggregate the (corrected) context from the previous node into the same prompt template used in the notebook's `baseline_rag_answer` — keep this identical across both tracks so judging is consistent regardless of which track a team used.

---

## What to rehearse before trusting this as a team template

- [ ] Import this into a **brand-new n8n account** (not yours with existing credentials) and confirm each node connects and runs top-to-bottom
- [ ] Confirm the OpenAI credential is picked up via n8n's credential store, not a hardcoded key visible in the exported JSON (exported workflows can leak hardcoded credentials to every team — use the credential store precisely to avoid this)
- [ ] Run the same self-test questions from the notebook through this workflow and confirm the baseline (pre-grounding) version fails the same way the notebook's baseline does — if it doesn't fail the same way, the two tracks aren't actually equivalent challenges
- [ ] Once you've built your own grounding fix, confirm it actually blocks a fabricated connection in the n8n output panel, not just in theory

Report back what breaks and I'll help fix the specific step — this is exactly the kind of thing that looks right on paper and needs a real run to catch, same as the Aura connection issues from Week 3.
