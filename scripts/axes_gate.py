#!/usr/bin/env python3
"""diversity-axes-gate. usage: axes_gate.py candidate.json --vocab vocab.json --registry registry.json
[--primary AXIS] [--max-share 0.6] [--min-n 4]   exit 0 ok | 1 violation | 2 bad input"""
import argparse, collections, json, sys
ap = argparse.ArgumentParser(); ap.add_argument("candidate"); ap.add_argument("--vocab", required=True); ap.add_argument("--registry", required=True)
ap.add_argument("--primary"); ap.add_argument("--max-share", type=float, default=0.6); ap.add_argument("--min-n", type=int, default=4)
a = ap.parse_args()
try:
    cand = json.load(open(a.candidate)); vocab = json.load(open(a.vocab)); reg = json.load(open(a.registry))
except Exception as e:
    print(f"bad input: {e}"); sys.exit(2)
if not isinstance(vocab, dict) or not vocab: print("empty or malformed vocabulary (need {axis: [values]}): nothing is measured"); sys.exit(2)
if not isinstance(cand, dict) or not isinstance(reg, list) or not all(isinstance(r, dict) for r in reg) or not all(isinstance(v, list) for v in vocab.values()):
    print("bad input shape: candidate must be an object, registry a list of objects, vocabulary {axis: [values]}"); sys.exit(2)
if any(isinstance(v, (list, dict)) for v in cand.values()) or any(isinstance(v, (list, dict)) for r in reg for v in r.values()):
    print("axis values must be plain strings"); sys.exit(2)
errs = []
for axis, allowed in vocab.items():
    if axis not in cand: errs.append(f"axis '{axis}' not declared"); continue
    if cand[axis] not in allowed: errs.append(f"axis '{axis}': '{cand[axis]}' is not in the vocabulary {allowed} (register new values first)")
if not errs:
    combo = tuple(cand[k] for k in vocab)
    for r in reg:
        if tuple(r.get(k) for k in vocab) == combo: errs.append(f"exact combination already shipped by '{r.get('name', '?')}'")
    if a.primary:
        for r in reg:
            if r.get(a.primary) == cand[a.primary]: errs.append(f"primary axis '{a.primary}' = '{cand[a.primary]}' already used by '{r.get('name', '?')}'")
    allr = reg + [cand]
    if len(allr) >= a.min_n:
        for axis in vocab:
            val, n = collections.Counter(r.get(axis) for r in allr).most_common(1)[0]
            if n / len(allr) > a.max_share and cand[axis] == val:
                errs.append(f"monoculture: '{val}' would cover {n}/{len(allr)} on axis '{axis}' (max {a.max_share:.0%}); pick a less-used value")
    usage = {ax: collections.Counter(r.get(ax) for r in reg) for ax in vocab}
    hint = {ax: [v for v in vocab[ax] if usage[ax][v] == 0][:3] for ax in vocab}
    print("unused values (prefer these next): " + json.dumps(hint))
print("\n".join(errs) if errs else "ok: candidate adds diversity"); sys.exit(1 if errs else 0)
