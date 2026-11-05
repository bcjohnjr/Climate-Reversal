# For a NEW, EMPTY github.com/bcjohnjr/Climate-Reversal repository.
# Run from PowerShell after extracting the supplied ZIP to a local folder.
$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
if (!(Get-Command git -ErrorAction SilentlyContinue)) { throw 'Install Git for Windows first.' }
if (!(Get-Command python -ErrorAction SilentlyContinue)) { throw 'Install Python 3 first.' }
if (Test-Path '.git') { throw 'A .git folder already exists. Stop to avoid overwriting existing history.' }
python scripts/fetch_pinned_sources.py
if ($LASTEXITCODE -ne 0) { throw 'Failed to recover source code; nothing uploaded.' }
python scripts/verify_archive.py
if ($LASTEXITCODE -ne 0) { throw 'Failed data verification; nothing uploaded.' }
git init -b main
if ($LASTEXITCODE -ne 0) { throw 'git init failed.' }
git remote add origin 'https://github.com/bcjohnjr/Climate-Reversal.git'
git add -A
git commit -m 'Archive pinned climate model code, original V67 results, figures and published supplementary tables'
if ($LASTEXITCODE -ne 0) { throw 'git commit failed; configure your Git name/email.' }
git push -u origin main
if ($LASTEXITCODE -ne 0) { throw 'GitHub push failed. Confirm authentication and that the target repository is empty.' }
Write-Host 'Published to https://github.com/bcjohnjr/Climate-Reversal'
Write-Host 'DO NOT create the final Zenodo DOI until sensitivity-data gaps have been resolved.'
