# generative-output-diversity-gate

**Stop a generator pipeline from shipping the same thing over and over: measure variety on several declared axes, not just one.**

[![test](https://github.com/Kein-chronicle/generative-output-diversity-gate/actions/workflows/test.yml/badge.svg)](https://github.com/Kein-chronicle/generative-output-diversity-gate/actions/workflows/test.yml) ![license](https://img.shields.io/badge/license-MIT-blue.svg) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)

## Why

Anything a gate does not measure converges. When a game factory deduplicated only on `rule_family`, every new game still shared the same lobby, session shape and screen layout. This gate takes a vocabulary of axes, a registry of what already shipped, and a candidate, and rejects monocultures.

## Install

**As a Claude Code skill** (Claude uses it when the task matches the skill description):

```sh
git clone https://github.com/Kein-chronicle/generative-output-diversity-gate.git ~/.claude/skills/diversity-axes-gate
```

For a single project, clone into `<project>/.claude/skills/diversity-axes-gate` instead, then start a new Claude Code session.

**As plain scripts:**

```sh
git clone https://github.com/Kein-chronicle/generative-output-diversity-gate.git
cd generative-output-diversity-gate
```

**Requires:** Python 3.10+.

## Quick start

Run it against a registry of four near-identical items:

```console
$ bash examples/demo.sh
# The registry already has four items that differ only in rule_family.
# A candidate with a fresh rule but the same shape is a monoculture:
$ python3 scripts/axes_gate.py examples/candidate-monoculture.json --vocab examples/vocab.json --registry examples/registry.json --primary rule_family
unused values (prefer these next): {"oracle": ["dataset", "measurement"], "session": ["daily-set", "run-attempt"], "surface": ["canvas", "side-stage"], "rule_family": ["timing"]}
monoculture: 'constraint' would cover 5/5 on axis 'oracle' (max 60%); pick a less-used value
monoculture: 'stage-journey' would cover 5/5 on axis 'session' (max 60%); pick a less-used value
monoculture: 'grid' would cover 5/5 on axis 'surface' (max 60%); pick a less-used value
[exit 1]

# A candidate that differs on the other axes passes:
$ python3 scripts/axes_gate.py examples/candidate-diverse.json --vocab examples/vocab.json --registry examples/registry.json --primary rule_family
unused values (prefer these next): {"oracle": ["dataset", "measurement"], "session": ["daily-set", "run-attempt"], "surface": ["canvas", "side-stage"], "rule_family": ["timing"]}
ok: candidate adds diversity
[exit 0]
```

The output above is real: it is produced by the files in `examples/`.

## Use it on your own files

```sh
python3 scripts/axes_gate.py candidate.json --vocab vocab.json --registry registry.json --primary rule_family
```

Sample inputs for every file format are in `examples/` and `tests/`; the details are in [SKILL.md](SKILL.md).

## What it checks

- Every axis value must be declared and from the vocabulary (a typo is not a new value).
- An exact combination already shipped is blocked.
- A candidate that would cover more than `--max-share` of the registry on any axis is a monoculture, even if its primary axis is new.
- Prints unused values to prefer next. An empty vocabulary or input of the wrong shape is refused (exit 2).

## Limits

- It measures what you declare; undeclared axes can still collapse.

## More from the same collection

Small, tested tools that grew out of running AI agents and game/app pipelines for months:

- [**llm-verdict-gate**](https://github.com/Kein-chronicle/llm-verdict-gate): Make AI and human review gates impossible to pass by silence: machine-parsed PASS/FAIL, missing verdict = FAIL.
- [**ci-gate-forgery-test**](https://github.com/Kein-chronicle/ci-gate-forgery-test): Prove your CI gates can actually fail: feed each gate forged-bad, empty and missing input and flag the ones that stay green.
- [**stale-verdict-guard**](https://github.com/Kein-chronicle/stale-verdict-guard): Bind a pass/fail verdict to a fingerprint of the source it judged, so an edit after review makes the verdict stale.

## Development

```sh
python3 tests/run.py
```

The tests include inputs that are supposed to be rejected, so a green run also shows the checks can fail. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).

If this saved you a debugging session, a star helps other people find it. Bug reports and failing test cases are even better.

<sub>Keywords: generative-ai, quality-gates, diversity, ai-agents, claude-code, claude-skills, agent-skills, pipeline</sub>
