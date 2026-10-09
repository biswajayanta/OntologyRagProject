"""
Day 2 offline structural checker -- JUDGES' TOOL (no Neo4j, no OpenAI, no internet).

Given a team's PATTERN REGISTRY (the list of regexes they adopted), this rebuilds the same
entity graph the starter notebook builds in Neo4j and answers, for every question in the
hidden and public packs: "would the grounding check call these two records CONNECTED?"

  adversarial question  -> PASS if the two trap records are NOT connected
  positive control      -> PASS if the two shared records ARE connected

This is the STRUCTURAL verdict. The starter's grounded_answer() is fixed (given to every team,
temperature 0), so the final answer follows this verdict when retrieval returns the two records.
Retrieval itself is not simulated here -- spot-check borderline teams by actually running them.

Usage:
    python day2_offline_check.py                     # runs the built-in sample registries
    python day2_offline_check.py team_registry.json  # JSON list of {"name":..., "regex":...}
"""
import re, sys, json, runpy, os
from collections import defaultdict, deque

HERE = os.path.dirname(os.path.abspath(__file__))
G = runpy.run_path(os.path.join(HERE, "day2_dataset_generator.py"))
TEXTS = G["campus_texts"]
K1, K2 = G["KIND1_PATTERNS"], G["KIND2_PATTERNS"]
MAX_HOPS = 6   # matches shortestPath((a)-[*..6]-(b)) in the notebooks


def build_graph(patterns):
    """patterns: list of {"name": str, "regex": str}. Returns adjacency over Event/Entity nodes."""
    adj = defaultdict(set)
    for i, text in enumerate(TEXTS):
        ev = ("Event", i)
        adj[ev]
        for p in patterns:
            for m in re.finditer(p["regex"], text):
                ent = (p["name"], m.group(1))
                adj[ev].add(ent)
                adj[ent].add(ev)
    return adj


def hops(adj, a, b):
    if a == b:
        return 0
    seen, q = {a}, deque([(a, 0)])
    while q:
        node, d = q.popleft()
        if d >= MAX_HOPS:
            continue
        for nb in adj[node]:
            if nb == b:
                return d + 1
            if nb not in seen:
                seen.add(nb)
                q.append((nb, d + 1))
    return None


def connected(adj, text_a, text_b):
    return hops(adj, ("Event", TEXTS.index(text_a)), ("Event", TEXTS.index(text_b))) is not None


def evaluate(patterns, pack, records_key):
    adj = build_graph(patterns)
    rows = []
    for t in pack:
        a, b = t[records_key]
        conn = connected(adj, a, b)
        passed = conn if t["expect_connected"] else (not conn)
        rows.append({"id": t["id"], "connected": conn, "pass": passed, "kind2": t.get("kind2_trap") or t.get("kind", "")})
    return rows


def pct(rows):
    return round(100 * sum(r["pass"] for r in rows) / len(rows)) if rows else 0


def report(name, patterns):
    ha = evaluate(patterns, G["HIDDEN_ADVERSARIAL"], "trap_records")
    hp = evaluate(patterns, G["HIDDEN_POSITIVE"], "shared_records")
    pa = evaluate(patterns, G["PUBLIC_ADVERSARIAL"], "trap_records")
    pp = evaluate(patterns, G["PUBLIC_POSITIVE"], "shared_records")
    names = {p["name"] for p in patterns}
    k1_cov = sorted(n for n in K1 if n in names)
    k2_used = sorted(n for n in K2 if n in names)
    print(f"\n=== {name} ===")
    print(f" patterns adopted: {sorted(names)}")
    print(f" Kind 1 covered ({len(k1_cov)}/4): {k1_cov} | Kind 2 adopted: {k2_used or 'none'}")
    for label, rows in (("HIDDEN adversarial", ha), ("HIDDEN positive", hp), ("PUBLIC adversarial", pa), ("PUBLIC positive", pp)):
        marks = " ".join(f"{r['id']}:{'1' if r['pass'] else '0'}" for r in rows)
        print(f" {label:19s} {pct(rows):3d}%  {marks}")
        for r in rows:
            if not r["pass"]:
                what = "falsely CONNECTED" if not r["connected"] is False and not r["pass"] and r["connected"] else "NOT connected (missed link)"
                print(f"     fail {r['id']}: {what}  [{r['kind2']}]")
    return {"hidden_adv": ha, "hidden_pos": hp, "public_adv": pa, "public_pos": pp,
            "k1_cov": k1_cov, "k2_used": k2_used}


SAMPLE_REGISTRIES = {
    "Starter as shipped (Student only)": [{"name": "Student", "regex": K1["Student"]}],
    "Ananya  (Student + Alumnus + Club + Ticket)": [{"name": n, "regex": K1[n]} for n in ("Student", "Alumnus", "Club", "Ticket")],
    "Rahul   (Student + Ticket + Room + Amount + Block + Semester)": [{"name": n, "regex": r} for n, r in
        [("Student", K1["Student"]), ("Ticket", K1["Ticket"])] + [(k, K2[k]) for k in ("Room", "Amount", "Block", "Semester")]],
    "Priya   (Student + Alumnus)": [{"name": n, "regex": K1[n]} for n in ("Student", "Alumnus")],
}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        reg = json.load(open(sys.argv[1]))
        report(os.path.basename(sys.argv[1]), reg)
    else:
        for name, reg in SAMPLE_REGISTRIES.items():
            report(name, reg)
