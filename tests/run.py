import json, os, subprocess, sys, tempfile
G = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "axes_gate.py"); d = tempfile.mkdtemp(); ok = True
vocab = {"oracle": ["constraint", "dataset", "measurement"], "session": ["stage-journey", "daily-set", "run-attempt"], "surface": ["grid", "canvas", "side-stage"], "rule_family": ["pack", "route", "sort", "slide", "timing"]}
reg = [{"name": f"g{i}", "oracle": "constraint", "session": "stage-journey", "surface": "grid", "rule_family": r} for i, r in enumerate(["pack", "route", "sort", "slide"])]
def w(n, o): p = os.path.join(d, n); json.dump(o, open(p, "w")); return p
V, R = w("v.json", vocab), w("r.json", reg)
def run(c, *x): return subprocess.run([sys.executable, G, w("c.json", c), "--vocab", V, "--registry", R, *x], capture_output=True, text=True)
def expect(n, p, rc, text=None):
    global ok; g = p.returncode == rc and (text is None or text in p.stdout); ok &= g; print(("ok   " if g else "FAIL ") + f"{n}" + ("" if g else f"\n     {p.stdout}"))
new = {"name": "n", "oracle": "measurement", "session": "daily-set", "surface": "canvas", "rule_family": "timing"}
expect("diverse candidate passes", run(new, "--primary", "rule_family"), 0)
expect("missing axis rejected", run({k: v for k, v in new.items() if k != "surface"}), 1, "not declared")
expect("word outside vocabulary rejected", run(dict(new, surface="grid-ish")), 1, "not in the vocabulary")
expect("old single-axis rule: repeated rule_family", run(dict(new, rule_family="pack"), "--primary", "rule_family"), 1, "already used")
expect("monoculture on oracle/session/surface is caught even with a new rule", run(dict(new, oracle="constraint", session="stage-journey", surface="grid", rule_family="timing")), 1, "monoculture")
expect("exact combination blocked", run(dict(reg[0], name="dup")), 1, "exact combination")
bad = subprocess.run([sys.executable, G, w("c.json", new), "--vocab", w("e.json", {}), "--registry", R], capture_output=True, text=True)
expect("empty vocabulary measures nothing => refuse", bad, 2)
bad2 = subprocess.run([sys.executable, G, w("c.json", new), "--vocab", V, "--registry", w("r2.json", {"not": "a list"})], capture_output=True, text=True)
expect("registry of the wrong shape is exit 2, not a traceback", bad2, 2)
sys.exit(0 if ok else 1)
