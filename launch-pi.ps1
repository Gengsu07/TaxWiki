# launch-pi.ps1 — Launch pi with the project knowledge base attached.
#
# Sets PI_KNOWLEDGE_DIR so pi-knowledge uses ./.knowledge (the repo's local
# gitignored index, see TAXWIKIDESIGN.md §6) instead of the global default.
# Without this, pi-knowledge tools (knowledge_search etc.) can't see the
# "Indonesian Tax Wiki" KB already built from raw/.

$ErrorActionPreference = 'Stop'

# Work from the repo root regardless of where the script is invoked from.
Set-Location $PSScriptRoot

$env:PI_KNOWLEDGE_DIR = (Join-Path $PSScriptRoot '.knowledge')
Write-Host "PI_KNOWLEDGE_DIR=$env:PI_KNOWLEDGE_DIR"

# Ensure the pi-knowledge tooling is installed (one-time; safe to re-run).
# pi install -l npm:pi-knowledge

& pi @args
exit $LASTEXITCODE