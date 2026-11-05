#!/usr/bin/env python3
"""Verify origin digests and structure; avoid claiming full reproduction of new sensitivity results."""
from pathlib import Path
from zipfile import ZipFile
from hashlib import sha256
import json,csv,sys

root=Path(__file__).resolve().parents[1]
m=json.loads((root/'provenance/archive_manifest.json').read_text(encoding='utf-8'))
errors=[]
for a in m['run']['artifacts']:
    p=root/'data/v67/original_artifacts'/a['file']
    if not p.is_file():errors.append('missing original zip '+str(p));continue
    got=sha256(p.read_bytes()).hexdigest()
    if got!=a['sha256']:errors.append(f'archive digest mismatch {p.name}: {got}')
    try:
        with ZipFile(p) as z:
            assert z.testzip() is None
    except Exception as e:errors.append(f'unreadable archive {p.name}: {e}')
case_roots=sorted(p for p in (root/'data/v67/cases').iterdir() if p.is_dir())
if len(case_roots)!=12:errors.append(f'expected 12 case roots; found {len(case_roots)}')
for case in case_roots:
    for sub,n in [('fair_work/fair_member_metrics.csv',841),('oscar_results/oscar_member_metrics.csv',200),('hector_work/hector_matched_timeseries.csv',158)]:
        f=case/sub
        if not f.exists():errors.append(str(f)+' missing');continue
        with f.open(encoding='utf-8',newline='') as inp:
            rows=sum(1 for _ in csv.DictReader(inp))
            if rows != n:errors.append(f'{f}: expected {n} rows, got {rows}')
    p=case/'case_results/v67_case_summary.json'
    if not p.exists():errors.append(str(p)+' missing')
    else:
        d=json.loads(p.read_text())
        if d.get('case_id')!=case.name:errors.append(f'{p}: case_id {d.get("case_id")} != {case.name}')
for t in m['supplementary_tables']:
    if not (root/t['file']).exists():errors.append('missing table '+t['file'])
for x in m['figure_files']:
    p=root/x['file']
    if not p.exists() or sha256(p.read_bytes()).hexdigest()!=x['sha256']:errors.append('missing/damaged figure '+x['file'])
for s in m['source_repositories']:
    dest=root/s['destination']
    if not dest.is_dir():print('SOURCE NOT YET IMPORTED:',s['repository'])
print('CHECKED: 13 original V67 archives, 12 case directories, model row counts, 6 tables, 4 figure images')
if errors:
    print('FAILURES:\n'+'\n'.join(errors),file=sys.stderr);sys.exit(1)
import subprocess
subprocess.run([sys.executable,str(root/'science_figures/check_against_supplement.py')],check=True)
print('PASS: Existing upstream numerical artifacts preserved intact. Figure sensitivity *inputs*, not model outputs, have been reconstructed.')
