#!/usr/bin/env python3
"""Single-purpose cleanup for bcjohnjr/Climate-Reversal. Never pushes without YES."""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import sys
import tempfile

EXPECTED='https://github.com/bcjohnjr/Climate-Reversal'
REMOVE=('OPEN_ISSUES_FOR_AGU.md','REPOSITORY_UPDATE_INSTRUCTIONS.md')

def git(repo,*args,check=True):
    p=subprocess.run(['git','-C',str(repo),*args],text=True,capture_output=True)
    if check and p.returncode:
        raise RuntimeError(f"git {args}: {p.stderr.strip()} {p.stdout.strip()}")
    return p.stdout.strip()

def main():
    ap=argparse.ArgumentParser(description='Cleanup obsolete review notes from public research archive')
    ap.add_argument('--repo',help='Existing checked-out Climate-Reversal git clone. If absent, clone it in a new temporary folder.')
    ap.add_argument('--prepare-only',action='store_true',help='Stage edits but do not commit or push')
    args=ap.parse_args()
    patch=Path(__file__).resolve().parent
    assert (patch/'README.md').is_file(), 'Missing replacement README.md next to this script'
    if args.repo:
        repo=Path(args.repo).expanduser().resolve()
        assert repo.is_dir(),f'No such clone: {repo}'
    else:
        repo=Path(tempfile.mkdtemp(prefix='climate-reversal-cleanup-'))/'Climate-Reversal'
        print('Cloning into',repo,flush=True)
        p=subprocess.run(['git','clone',EXPECTED+'.git',str(repo)],text=True)
        if p.returncode:raise SystemExit('Git clone failed; check network and credentials')
    remote=git(repo,'remote','get-url','origin')
    valid={'https://github.com/bcjohnjr/Climate-Reversal.git',EXPECTED,'git@github.com:bcjohnjr/Climate-Reversal.git'}
    assert remote in valid, f'Unexpected git origin: {remote}'
    assert git(repo,'branch','--show-current')=='main','Expected main branch; switch to main first'
    assert not git(repo,'status','--porcelain'), 'Working tree has existing changes; refusing to alter or stage them'
    old=(repo/'README.md').read_text(encoding='utf-8')
    assert 'not associated with an active journal submission' in old, 'Outdated text is already absent; no change needed'
    for name in REMOVE:
        assert (repo/name).is_file(),f'{name} is already absent; do not apply partial patch blindly'
    (repo/'README.md').write_bytes((patch/'README.md').read_bytes())
    git(repo,'add','--','README.md')
    git(repo,'rm','--',*REMOVE)
    paths=git(repo,'diff','--cached','--name-only').splitlines()
    assert set(paths)==set(('README.md',*REMOVE)),f'Unexpected staged paths: {paths}'
    print('Staged changes:\n'+git(repo,'diff','--cached','--stat'))
    print('Git repository:',repo)
    if args.prepare_only:
        print('PREPARE ONLY: Nothing has been committed or pushed')
        return
    answer=input('Type YES to commit exactly these three paths and push to GitHub main: ').strip()
    if answer!='YES':
        print('No push made. Staged changes remain in',repo)
        return
    git(repo,'commit','-m','Remove outdated editorial notes and use journal-neutral archive description')
    print('Local commit:',git(repo,'rev-parse','HEAD'))
    print('Pushing...')
    p=subprocess.run(['git','-C',str(repo),'push','origin','HEAD:main'],text=True)
    if p.returncode:raise SystemExit('Push failed: local commit is preserved in '+str(repo))
    print('SUCCESS: repository housekeeping pushed. No research outputs changed.')

if __name__=='__main__':
    try:main()
    except Exception as e:
        print('ERROR:',e,file=sys.stderr)
        sys.exit(1)
