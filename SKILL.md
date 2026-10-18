---
name: diversity-axes-gate
description: Stop a production line (apps, games, articles, designs) from converging on one shape. Use when every output looks the same (same lobby, same layout, same oracle, same session shape), when a gate blocks only one axis of repetition, or when you need closed vocabularies, a registry of what has been made, and a check that blocks reused combinations and axis monoculture. A gate that doesn't measure an axis guarantees that axis homogenises.
---

# diversity-axes-gate

Real case: four released games had different *rules* (the only axis the registry blocked) but every one had
home -> stage select -> uniform grid, and all four used the same proof type, though the constitution allowed four.
The user said "the lobby, stage select and board are too consistent". It wasn't sloppy execution - **the pipeline
mandated it** (a gate required a stage-select screen; another assumed everything is a grid).

## Method

1. **Name every axis along which outputs can differ**, each with a **closed vocabulary** in a file
   (`vocab.json`). Free text lets the same thing hide behind a new word. New values must be registered *first*.
2. Every candidate **declares all axes** in a JSON file before work starts (`candidate.json`).
3. A `registry.json` lists what has already shipped (its declared axes).
4. The gate (`scripts/axes_gate.py`) fails when:
   - an axis is missing, or its value is outside the vocabulary (typos, invented words);
   - the **exact combination** already exists in the registry;
   - after adding this candidate, **one value covers more than `--max-share` of an axis** among >= `--min-n` entries
     (monoculture), unless the candidate uses a value that is not yet dominant;
   - the candidate repeats the value of the blocked "primary" axis (e.g. rule family) - the old single-axis rule.
5. **Audit the pipeline's own mandates**: grep your gates for "must", "always", "every" and ask which axis each one
   quietly forces. Mandates that fix a screen flow, a layout, or an assumption belong behind a vocabulary value, not in a gate.
6. When picking the *next* thing to build, choose the axis value with the lowest usage count first.
7. Define the discriminating criterion for easily mislabeled axes (e.g. input verb: split by *what decides the outcome* -
   the release moment or the traced path - not by finger shape).

```bash
python3 scripts/axes_gate.py candidate.json --vocab vocab.json --registry registry.json --primary rule_family
python3 tests/run.py
```
Exit 0 ok | 1 violation | 2 bad input. The gate that doesn't measure an axis will not stop it from collapsing;
if a new kind of sameness shows up, add the axis, don't scold the process.
