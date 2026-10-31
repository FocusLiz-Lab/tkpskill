#!/usr/bin/env python3
"""Search bundled evidence with standard-library Python only."""
import argparse, json
from pathlib import Path
parser=argparse.ArgumentParser()
parser.add_argument('query')
parser.add_argument('--topic', default='')
parser.add_argument('--limit', type=int, default=8)
args=parser.parse_args()
tokens=args.query.lower().split()
found=[]
for line in (Path(__file__).resolve().parents[1]/'知识库/原子库/atoms.jsonl').open(encoding='utf-8'):
    row=json.loads(line)
    if args.topic and args.topic not in row.get('topics',[]): continue
    text=' '.join(str(row.get(key,'')) for key in ('knowledge','original','source_title')).lower()
    score=sum(text.count(token) for token in tokens)
    if score: found.append((score,row))
for _,row in sorted(found,key=lambda item:(-item[0],item[1]['id']))[:max(1,min(args.limit,30))]:
    print(json.dumps(row,ensure_ascii=False))
