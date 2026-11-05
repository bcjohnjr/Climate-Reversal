#!/usr/bin/env python3
"""Materialize historical repositories exactly at the pinned commits used by the paper.

Requires git and network access. Never silently substitutes a current branch tip.
"""
from pathlib import Path
import json, subprocess, shutil, sys

root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'provenance/archive_manifest.json').read_text(encoding='utf-8'))
for x in manifest['source_repositories']:
    repo=x['repository']; dest=root/x['destination']; sha=x['commit']
    if dest.exists() and any(dest.iterdir()):
        raise SystemExit(f'{dest} already exists and is nonempty; refusing to overwrite pinned sources')
    dest.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['git','clone','--quiet','https://github.com/'+repo+'.git',str(dest)],check=True)
    subprocess.run(['git','-C',str(dest),'checkout','--detach','--quiet',sha],check=True)
    actual=subprocess.check_output(['git','-C',str(dest),'rev-parse','HEAD'],text=True).strip()
    if actual != sha: raise SystemExit(f'Commit mismatch for {repo}: {actual} != {sha}')
    shutil.rmtree(dest/'.git')
    print('Imported',repo,sha,'to',dest.relative_to(root))
print('All three pinned upstream repositories imported successfully.')
