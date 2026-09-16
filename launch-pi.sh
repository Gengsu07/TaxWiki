#!/usr/bin/env bash
# launch-pi.sh — Launch pi with the project knowledge base attached.
#
# Sets PI_KNOWLEDGE_DIR so pi-knowledge uses ./.knowledge (the repo's local
# gitignored index, see TAXWIKIDESIGN.md §6) instead of the global default.
# Without this, pi-knowledge tools (knowledge_search etc.) can't see the
# "Indonesian Tax Wiki" KB already built from raw/.

set -euo pipefail

# Work from the repo root regardless of where the script is invoked from.
cd "$(dirname "$0")"

export PI_KNOWLEDGE_DIR="$(pwd)/.knowledge"
echo "PI_KNOWLEDGE_DIR=$PI_KNOWLEDGE_DIR"

# Ensure the pi-knowledge tooling is installed (one-time; safe to re-run).
# pi install -l npm:pi-knowledge

exec pi "$@"