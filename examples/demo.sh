#!/usr/bin/env bash
cd "$(dirname "$0")/.."
run() { printf '$ %s\n' "$*"; "$@"; printf '[exit %s]\n\n' "$?"; }
echo "# The registry already has four items that differ only in rule_family."
echo "# A candidate with a fresh rule but the same shape is a monoculture:"
run python3 scripts/axes_gate.py examples/candidate-monoculture.json --vocab examples/vocab.json --registry examples/registry.json --primary rule_family
echo "# A candidate that differs on the other axes passes:"
run python3 scripts/axes_gate.py examples/candidate-diverse.json --vocab examples/vocab.json --registry examples/registry.json --primary rule_family
