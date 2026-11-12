"""Prepare a bounded, cached review pool from public MUSINSA user outfit posts.

Run with the project's Python 3.11 environment. Original images and raw responses
stay under outputs/v3 and are never included in the public source release.
The site allows ChatGPT-User on its public pages as checked on 2026-11-12.
"""
from pathlib import Path
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import json
import time
import logging
import os
from scrapling.fetchers import Fetcher

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/v3'
PROXY = os.environ.get('OUTFIT_PROXY')  # Optional existing network proxy; never rotate identities.
logging.getLogger('scrapling').setLevel(logging.ERROR)

def fetch(url):
    response = Fetcher.get(url, proxy=PROXY, headers={'User-Agent': 'ChatGPT-User'},
                           stealthy_headers=False, timeout=20, retries=0)
    if response.status != 200:
        raise RuntimeError(f'Stopping collection: HTTP {response.status} at {urlparse(url).hostname}')
    return response

def main():
    OUT.mkdir(exist_ok=True)
    pool = {}
    page = json.loads((OUT / 'content-page1.json').read_text())
    for n in range(10):
        for section in page['data']['list']:
            for item in section.get('contents', []):
                if item.get('contentType') == 'USER_SNAP' and item.get('formatType') == 'POST':
                    pool[item['id']] = item
        print('candidate posts', len(pool), flush=True)
        next_url = page['data']['list'][0].get('links', {}).get('next')
        if not next_url or n == 9:
            break
        if urlparse(next_url).hostname != 'content.musinsa.com':
            raise RuntimeError('Unexpected pagination host')
        cache = OUT / f'content-page{n + 2}.json'
        if not cache.exists():
            time.sleep(1)
            cache.write_bytes(fetch(next_url).body)
        page = json.loads(cache.read_text())
    candidates = list(pool.values())
    for n, item in enumerate(candidates):
        item['reviewIndex'] = n + 1
        item['previewFile'] = f'outputs/v3/previews/{n + 1:03d}.jpg'
    (OUT / 'candidate-pool.json').write_text(json.dumps(candidates, ensure_ascii=False, indent=2))
    (OUT / 'previews').mkdir(exist_ok=True)
    def preview(item):
        dest = ROOT / item['previewFile']
        if not dest.exists():
            dest.write_bytes(fetch(item['thumbnailUrl']).body)
        return item['reviewIndex']
    with ThreadPoolExecutor(max_workers=3) as executor:
        list(executor.map(preview, candidates))
    print('Downloaded previews', len(candidates), flush=True)

if __name__ == '__main__':
    main()
