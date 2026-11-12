from scrapling.fetchers import Fetcher
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.robotparser import RobotFileParser
import re,json,time
R=Path(__file__).resolve().parents[1];rows=json.loads((R/'outputs/candidates.json').read_text());out=[]
BASE='https://en.jogunshop.com';rp=RobotFileParser();rp.parse(Fetcher.get(BASE+'/robots.txt',timeout=20).body.decode().splitlines())
selected=[0,1,2,3,4,5,6,7,8,9,10,11,13,15,17,18,19,20,21,22,23,25,26,27,29,30,33,34,35]
def details(pair):
 n,r=pair
 if not rp.can_fetch('*',r['source']):return []
 time.sleep(1)
 try:
  p=Fetcher.get(r['source'],timeout=25);s='\n'.join(p.css('script::text').getall());m=re.search(r'"common_detail_img":("(?:\\.|[^"\\])*")',s)
  if not m:return []
  paths=[v for v in json.loads(m[1]).strip('{}').split('|') if v.endswith(('.jpg','.jpeg','.png'))][:4]
  return [{**r,'candidate':n+1,'slot':j+1,'image':BASE+'/storage/jogunshopU0/www/'+path} for j,path in enumerate(paths)]
 except Exception as e:print('detail failed',n+1,type(e).__name__);return []
with ThreadPoolExecutor(max_workers=2) as ex:
 for result in ex.map(details,[(n,rows[n]) for n in selected]):out.extend(result)
(R/'outputs/static-candidates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));dest=R/'outputs/static';dest.mkdir(exist_ok=True)
def download(pair):
 n,r=pair;time.sleep(.5)
 try:
  res=Fetcher.get(r['image'],timeout=20)
  if res.status==200:(dest/f'{n+1:03}.jpg').write_bytes(res.body)
 except Exception as e:print('image failed',n+1,type(e).__name__)
with ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(download,enumerate(out)))
print('Static candidates:',len(out))
