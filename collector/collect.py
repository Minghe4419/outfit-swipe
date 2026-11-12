"""Public JOGUNSHOP outfit candidates. Does not crawl /Search or member pages."""
from pathlib import Path
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser
from scrapling.fetchers import Fetcher
import json,time,argparse
ROOT=Path(__file__).resolve().parents[1]
BASE='https://en.jogunshop.com'
CATEGORIES={'衬衫叠穿':1698,'日常休闲':870,'针织基础':869}
def collect(limit=36):
    robots=Fetcher.get(BASE+'/robots.txt',timeout=25)
    if robots.status!=200: raise RuntimeError('Cannot verify robots.txt')
    rp=RobotFileParser();rp.parse(robots.body.decode().splitlines())
    rows=[];seen=set()
    for label,cid in CATEGORIES.items():
        url=f'{BASE}/Product/Category/list/cid/{cid}'
        if not rp.can_fetch('*',url): continue
        time.sleep(1.5)
        page=Fetcher.get(url,timeout=30)
        if page.status!=200: continue
        for img in page.css('a[href*="/Product/Detail/"] img'):
            src=img.attrib.get('src','');href=img.parent.attrib.get('href','')
            if 'product.' not in src or not href or href in seen: continue
            seen.add(href)
            rows.append({'id':f'look-{len(rows)+1:02}', 'image':urljoin(url,src).replace('http://jogunshop.img','https://jogunshop.img'), 'source':urljoin(url,href),'sourceName':'JOGUNSHOP','seed':label})
            if sum(r['seed']==label for r in rows)>=limit//len(CATEGORIES):break
    dest=ROOT/'outputs/candidates.json';dest.write_text(json.dumps(rows,ensure_ascii=False,indent=2))
    print(f'Extracted {len(rows)} unique candidates to {dest}')
    return rows
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--download-preview',action='store_true');args=p.parse_args();rows=collect()
    if args.download_preview:
        dest=ROOT/'outputs/previews';dest.mkdir(exist_ok=True)
        for n,r in enumerate(rows):
            try:
                time.sleep(.5);res=Fetcher.get(r['image'],timeout=25)
                if res.status==200:(dest/f'{n+1:02}.gif').write_bytes(res.body)
            except Exception as exc:print(type(exc).__name__,n+1)
