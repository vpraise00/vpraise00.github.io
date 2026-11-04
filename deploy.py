#!/usr/bin/env python3
"""One-command bootstrap of https://vpraise00.github.io from a local .env.

Only use on a trusted local computer. Token is never printed or committed.
The script creates a PUBLIC username.github.io repository, uploads the site and
GitHub Actions workflow with one Git commit, and enables branch-based Pages.
"""
from __future__ import annotations
import argparse
import base64
import concurrent.futures
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
API='https://api.github.com'
EXCLUDE_DIRS={'.git','__pycache__','.venv','venv','.pytest_cache','.idea','.vscode','node_modules'}
EXCLUDE_FILES={'deploy.log','.env','Thumbs.db','.DS_Store'}

class GithubError(Exception):pass


def dotenv(path: Path) -> dict[str,str]:
    values={}
    if path.exists() and path.is_file():
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            line=line.strip()
            if not line or line.startswith('#'): continue
            if line.startswith('export '):line=line[7:].strip()
            if '=' not in line:continue
            k,v=line.split('=',1)
            k=k.strip().upper();v=v.strip()
            if len(v)>=2 and v[0]==v[-1] and v[0] in ('"',"'"):v=v[1:-1]
            values[k]=v
    return values


def git_token(values: dict[str,str]) -> str:
    for key in ('GITHUB_TOKEN','GH_TOKEN','GITHUB_PAT','GITHUB_ACCESS_TOKEN','GITHUB_PERSONAL_ACCESS_TOKEN','GIT_TOKEN','PERSONAL_ACCESS_TOKEN'):
        t=os.environ.get(key) or values.get(key)
        if t and t not in ('replace-with-your-github-token','your-token-here'):
            return t.strip()
    for k,v in values.items():
        if ('GITHUB' in k or k.startswith('GH_')) and ('TOKEN' in k or 'PAT' in k) and v.strip():return v.strip()
    return ''


def api_request(token: str, method: str, path: str, payload: dict | None = None) -> dict:
    data=json.dumps(payload).encode('utf-8') if payload is not None else None
    req=urllib.request.Request(API+path,data=data,method=method,headers={
        'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json',
        'X-GitHub-Api-Version':'2022-11-28','User-Agent':'EmbodiedResearchRadar-Pages-deployer/1.0',
        **({'Content-Type':'application/json'} if data is not None else {})})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            body=resp.read()
            return json.loads(body.decode('utf-8')) if body else {}
    except urllib.error.HTTPError as e:
        response=e.read(1100).decode('utf-8','replace')
        try:msg=json.loads(response).get('message',response)
        except ValueError:msg=response[:230]
        raise GithubError(f'GitHub HTTP {e.code} {method} {path}: {msg}') from None
    except urllib.error.URLError as e:
        raise GithubError(f'GitHub connection failed while accessing {path}: {type(e.reason).__name__}') from None


def collect_files() -> list[tuple[str,bytes]]:
    output=[]
    for f in ROOT.rglob('*'):
        if not f.is_file():continue
        rel=f.relative_to(ROOT)
        if any(x in EXCLUDE_DIRS for x in rel.parts):continue
        if f.name in EXCLUDE_FILES or f.name.endswith(('.pyc','.swp','.tmp','.log')):continue
        if f.name.startswith('.env'):continue
        if f.is_symlink():continue
        if f.stat().st_size>3_000_000:raise ValueError(f'Unexpected large file: {rel}')
        content=f.read_bytes()
        if b'\0' in content:raise ValueError(f'Unexpected binary file: {rel}')
        output.append((rel.as_posix(),content))
    return sorted(output)


def set_secret(token: str, repo: str, name: str, secret: str) -> bool:
    if not secret or secret.lower().startswith(('replace','your-key')):return False
    try:
        from nacl import encoding,public
    except ImportError:
        print('[INFO] PyNaCl not installed; optional OPENAI_API_KEY secret was not set.')
        print('       Run: py -m pip install pynacl  / or add the secret in GitHub Settings → Secrets and variables → Actions')
        return False
    details=api_request(token,'GET',f'/repos/{repo}/actions/secrets/public-key')
    pubkey=public.PublicKey(details['key'].encode('utf-8'),encoder=encoding.Base64Encoder())
    encrypted=public.SealedBox(pubkey).encrypt(secret.encode('utf-8'))
    ciphertext=base64.b64encode(encrypted).decode('ascii')
    api_request(token,'PUT',f'/repos/{repo}/actions/secrets/{name}',{
        'encrypted_value':ciphertext,'key_id':details['key_id']})
    return True


def main():
    parser=argparse.ArgumentParser(description='Deploy Embodied Research Radar to username.github.io using a local GitHub token.')
    parser.add_argument('--env',default=r'D:\vpraise\.env' if os.name=='nt' else '.env',help='Path to your existing .env (default on Windows: D:\\vpraise\\.env)')
    parser.add_argument('--owner',default='vpraise00',help='GitHub account owner (default vpraise00)')
    parser.add_argument('--dry-run',action='store_true',help='Validate and print file counts; never call GitHub')
    args=parser.parse_args()
    owner=args.owner.strip()
    if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?',owner):
        parser.error('Invalid GitHub owner name.')
    repository=f'{owner}/{owner}.github.io'
    files=collect_files()
    if not files:raise SystemExit('No site files found. Please extract the entire ZIP first.')
    if args.dry_run:
        print(f'[DRY RUN] {repository}: {len(files)} safe text files, {sum(len(c) for _,c in files)//1024} KiB; no secrets read or uploaded.')
        print('[DRY RUN] Found required site files:', all(x in dict(files) for x in ('index.html','config/topics.json','data/papers.json','.github/workflows/daily-research.yml')))
        return
    path=Path(os.path.expandvars(args.env)).expanduser()
    values=dotenv(path)
    token=git_token(values)
    if not token:
        print(f'[ERROR] Could not find GitHub token in local .env: {path} or the process environment.',file=sys.stderr)
        print('Supported keys: GITHUB_TOKEN, GH_TOKEN, GITHUB_PAT, GITHUB_ACCESS_TOKEN, GITHUB_PERSONAL_ACCESS_TOKEN.',file=sys.stderr)
        raise SystemExit(2)
    print(f'[INFO] Authenticating GitHub account; source path={ROOT}')
    user=api_request(token,'GET','/user')
    if user.get('login','').lower()!=owner.lower():
        raise GithubError(f'Authenticated GitHub account does not match owner={owner}. No changes made.')
    try:
        repo=api_request(token,'GET',f'/repos/{repository}')
        print(f'[INFO] Existing repository found: {repository} (updating requested site files only).')
    except GithubError as ex:
        if 'HTTP 404' not in str(ex):raise
        print(f'[INFO] Creating PUBLIC GitHub Pages repository: {repository}')
        repo=api_request(token,'POST','/user/repos',{'name':f'{owner}.github.io','description':'VLA · WAM · Robotics research radar, updated daily','private':False,'auto_init':True,'has_issues':True,'has_wiki':False})
    if repo.get('private',False):
        raise GithubError('Repository is private; expected a public Pages repo. Change visibility to public manually before proceeding.')
    branch=repo.get('default_branch') or 'main'
    base=api_request(token,'GET',f'/repos/{repository}/git/ref/heads/{urllib.parse.quote(branch,safe="")}')['object']['sha']
    commit=api_request(token,'GET',f'/repos/{repository}/git/commits/{base}')
    base_tree=commit['tree']['sha']
    print(f'[INFO] Uploading {len(files)} text files to {branch} as a single commit...')
    def blob(item):
        rel,content=item
        value=content.decode('utf-8-sig')
        obj=api_request(token,'POST',f'/repos/{repository}/git/blobs',{'content':value,'encoding':'utf-8'})
        return {'path':rel,'mode':'100644','type':'blob','sha':obj['sha']}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        entries=list(executor.map(blob,files))
    tree=api_request(token,'POST',f'/repos/{repository}/git/trees',{'base_tree':base_tree,'tree':entries})
    if tree['sha'] != base_tree:
        new_commit=api_request(token,'POST',f'/repos/{repository}/git/commits',{
            'message':'feat: publish Embodied Research Radar and daily updates','tree':tree['sha'],'parents':[base]})
        api_request(token,'PATCH',f'/repos/{repository}/git/refs/heads/{urllib.parse.quote(branch,safe="")}',{'sha':new_commit['sha'],'force':False})
        print(f'[OK] Committed {len(files)} files to {repository}@{branch}')
    else:print('[INFO] Files already match; no new commit needed.')
    try:
        pages=api_request(token,'GET',f'/repos/{repository}/pages')
        print('[OK] GitHub Pages is already enabled:', pages.get('html_url',f'https://{owner}.github.io/'))
    except GithubError as ex:
        if 'HTTP 404' in str(ex):
            try:
                pages=api_request(token,'POST',f'/repos/{repository}/pages',{'source':{'branch':branch,'path':'/'}})
                print('[OK] GitHub Pages publishing source enabled from repository branch.')
            except GithubError as setup_error:
                print(f'[WARN] Automatic Pages setup failed: {setup_error}')
                print(f'       Open: https://github.com/{repository}/settings/pages and select Deploy from a branch → {branch} → /(root).')
        else:print(f'[WARN] Could not check Pages state: {ex}')
    openai=values.get('OPENAI_API_KEY') or os.environ.get('OPENAI_API_KEY','')
    if openai:
        try:
            if set_secret(token,repository,'OPENAI_API_KEY',openai):
                print('[OK] Optional OpenAI API key securely encrypted into GitHub Actions secrets. The key was not committed.')
        except GithubError as ex:
            print(f'[WARN] Could not register OpenAI secret; set it in the repository Actions settings: {ex}')
    else:
        print('[INFO] OPENAI_API_KEY absent; daily new papers will publish as abstract-only previews.')
    print('\n===== SETUP RESULT =====')
    print(f'Site URL: https://{owner}.github.io/')
    print(f'Repository: https://github.com/{repository}')
    print(f'Daily runs: https://github.com/{repository}/actions/workflows/daily-research.yml')
    print('Schedule: approximately 09:15 KST, GitHub Actions schedule (delays possible).')
    print('Note: Pages may take time to publish after repository creation; check Actions / Settings → Pages if not yet live.')

if __name__=='__main__':
    try:main()
    except GithubError as ex:
        print(f'[ERROR] {ex}',file=sys.stderr)
        raise SystemExit(1)
