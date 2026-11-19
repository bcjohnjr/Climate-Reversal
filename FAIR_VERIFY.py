#!/usr/bin/env python3
"""FaIR 56-case independent archived-output verifier and pinned-source reproducer.

No fabricated data; no dependence on the existing Climate-Reversal folder layout.
All uploaded files are flat at the repository root. Structured subdirectories
are restored locally from two content-addressed, SHA-256-checked ZIP archives.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, math, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
RESULTS='FAIR_56_CASE_OUTPUTS.zip'
CODE='FAIR_REPRODUCTION_CODE_V6.zip'
MANIFEST='FAIR_UPLOAD_SHA256SUMS.txt'


def sha256_file(p:Path)->str:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()


def validate_root_hashes():
 lines=(ROOT/MANIFEST).read_text(encoding='ascii').strip().splitlines()
 entries={}
 for line in lines:
  digest,name=line.split('  ',1)
  if not (len(digest)==64 and all(c in '0123456789abcdef' for c in digest)):
   raise RuntimeError('Malformed SHA-256 entry: '+line)
  if '/' in name or '\\' in name or name in entries:raise RuntimeError('Unsafe/duplicate manifest name')
  entries[name]=digest
 available={p.name for p in ROOT.iterdir() if p.is_file() and p.name!=MANIFEST}
 missing=set(entries)-available
 if missing:
  raise RuntimeError('Missing flat-upload files: '+str(sorted(missing)))
 # The destination is an EXISTING research repository containing README.md,
 # data.zip, and other research files. Extra files are intentionally permitted.
 for name,digest in entries.items():
  actual=sha256_file(ROOT/name)
  if actual!=digest:raise RuntimeError('SHA-256 mismatch: '+name)
 print('PASS: SHA-256 verified for all',len(entries),'outer upload files',flush=True)


def safe_extract(archive:Path,target:Path):
 target=target.resolve();target.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(archive) as z:
  if z.testzip() is not None:raise RuntimeError('Corrupt ZIP archive '+archive.name)
  names=z.namelist()
  if len(names)!=len(set(names)):raise RuntimeError('Duplicate ZIP paths '+archive.name)
  for i in z.infolist():
   rel=Path(i.filename)
   if rel.is_absolute() or '..' in rel.parts or '\\' in i.filename or i.filename.startswith('/'):
    raise RuntimeError('Unsafe ZIP path: '+i.filename)
   dest=(target/rel).resolve()
   if not dest.is_relative_to(target):raise RuntimeError('ZIP traversal blocked '+i.filename)
  z.extractall(target)


def verify_inner_hashes():
 rows=list(csv.DictReader((ROOT/'FAIR_RESULTS_SHA256.csv').open(newline='',encoding='utf-8')))
 assert len(rows)==56*11,('Expected 616 result files',len(rows))
 pathset={row['path'] for row in rows}
 if len(pathset)!=len(rows):raise RuntimeError('Duplicate result manifest path')
 with zipfile.ZipFile(ROOT/RESULTS) as z:
  actual=set(z.namelist())
  if actual!=pathset:raise RuntimeError('Results ZIP and file manifest have different file lists')
  cases=set()
  for row in rows:
   p=row['path'];parts=Path(p).parts
   if len(parts)!=3 or parts[0]!='results':raise RuntimeError('Malformed results path '+p)
   cases.add(parts[1]); b=z.read(p)
   if len(b)!=int(row['size_bytes']) or hashlib.sha256(b).hexdigest()!=row['sha256']:
    raise RuntimeError('Corrupted original result bytes: '+p)
 if len(cases)!=56:raise RuntimeError('Expected 56 distinct case directories')
 print('PASS: exact archived-byte SHA-256 for',len(rows),'files across',len(cases),'cases',flush=True)


def compare_audit_files(a:Path,b:Path):
 # An exact content equality check is appropriate: both comparison reports
 # are produced by the identical pinned comparator and unchanged case bytes.
 import csv
 with a.open(newline='',encoding='utf-8') as f:left=list(csv.DictReader(f))
 with b.open(newline='',encoding='utf-8') as f:right=list(csv.DictReader(f))
 if len(left)!=len(right)!=152:raise RuntimeError('Expected 152 comparisons')
 if len(left)!=152 or len(right)!=152:raise RuntimeError('Expected exactly 152 comparison rows')
 for ix,(x,y) in enumerate(zip(left,right)):
  if x!=y:raise RuntimeError(f'Comparison report diverged at row {ix+1}: {x} != {y}')
 print('PASS: newly calculated 152 comparisons match the submitted audit report',flush=True)


def verify_reproduction(work:Path):
 safe_extract(ROOT/CODE,work)
 safe_extract(ROOT/RESULTS,work)
 shutil.copy2(ROOT/'FAIR_EXPECTED_56.json',work/'expected_cases.json')
 proc=subprocess.run([sys.executable,str(work/'src/compare_results.py'),
   '--results',str(work/'results'),'--references',str(work/'references'),
   '--out',str(work/'verified_reports'),'--expected-cases',str(work/'expected_cases.json')],cwd=work)
 if proc.returncode:raise RuntimeError('Reproduced numerical comparator failed')
 status=json.loads((work/'verified_reports/status.json').read_text(encoding='utf-8'))
 if (status.get('status')!='FULL_56_NUMERICALLY_REPRODUCED' or status.get('valid_cases')!=56
     or status.get('published_comparisons')!=152 or status.get('comparisons_passed')!=152
     or status.get('comparisons_failed')!=0):
  raise RuntimeError('Required 56/56 + 152/152 evidence not reproduced')
 compare_audit_files(work/'verified_reports/comparison.csv',ROOT/'FAIR_152_COMPARISONS.csv')
 subprocess.run([sys.executable,str(work/'src/test_s4_timebound_regression.py'),'--results',str(work/'results')],check=True,cwd=work)
 print('PASS: independently rechecked the complete 56-case archive; 152/152 published numerical comparisons',flush=True)


def main():
 ap=argparse.ArgumentParser()
 g=ap.add_mutually_exclusive_group(required=True)
 g.add_argument('--verify',action='store_true',help='Verify preserved outputs and 152 numerical comparisons')
 g.add_argument('--extract-code',action='store_true',help='Unpack source code to a chosen workspace')
 g.add_argument('--rerun',action='store_true',help='Execute 56 FaIR cases from scratch with pinned sources (Git/network required)')
 ap.add_argument('--workspace',default=None,help='Where to unpack; default for rerun/extract: FAIR_RERUN_WORKSPACE')
 ap.add_argument('--keep-work',action='store_true',help='Keep temporary verification files at FAIR_LOCAL_VERIFIED')
 args=ap.parse_args()
 validate_root_hashes()
 if args.verify:
  verify_inner_hashes()
  if args.keep_work:
   work=Path(args.workspace or ROOT/'FAIR_LOCAL_VERIFIED').resolve()
   if work.exists():raise RuntimeError('Workspace exists; choose a new --workspace to prevent overwriting')
   work.mkdir(parents=True)
   verify_reproduction(work)
   print('Verification reports saved under',work/'verified_reports')
  else:
   with tempfile.TemporaryDirectory(prefix='fair_56_verify_') as tmp:
    verify_reproduction(Path(tmp))
 elif args.extract_code:
  w=Path(args.workspace or ROOT/'FAIR_RERUN_WORKSPACE').resolve()
  if w.exists() and any(w.iterdir()):
   # GitHub Actions uses an existing checkout directory; do not silently
   # clobber a pre-existing reproduction source file in it.
   for name in ('src','references','inputs','archived'):
    if (w/name).exists():raise RuntimeError(f'Workspace already contains {name}; refusing to overwrite')
  safe_extract(ROOT/CODE,w)
  print('Pinned-source FaIR reproduction source prepared at',w)
 else:
  w=Path(args.workspace or ROOT/'FAIR_RERUN_WORKSPACE').resolve()
  if w.exists():raise RuntimeError('Rerun directory already exists; select a new --workspace')
  safe_extract(ROOT/CODE,w)
  print('Rerunning 56 pinned FaIR configurations. No previous result is implied.')
  subprocess.run([sys.executable,str(w/'src/execute.py'),'--scope','full','--compare'],cwd=w,check=True)

if __name__=='__main__':
 try:main()
 except Exception as exc:
  print('AUDIT FAILED:',type(exc).__name__,exc,file=sys.stderr)
  sys.exit(1)
