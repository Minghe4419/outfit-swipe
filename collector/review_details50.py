"""Read provenance and optional full outfit angles for the bounded review pool."""
from collect_review50 import ROOT, OUT, fetch
from concurrent.futures import ThreadPoolExecutor
import json
import time

SELECTED = [1,4,7,9,10,12,14,15,16,17,18,19,20,21,22,23,24,25,26,30,31,32,33,35,36,37,40,41,42,43,44,45,47,48,51,53,55,56,57,59,60,62,63,66,68,72,75,78,81,84]
ALTERNATE = [3,5,6,28,39,58,64,70,74,77,88]

def main():
    pool = json.loads((OUT / 'candidate-pool.json').read_text())
    (OUT / 'details').mkdir(exist_ok=True)
    def detail(index):
        item = pool[index-1]
        path = OUT / 'details' / f'{index:03d}.json'
        if not path.exists():
            response = fetch(item['linkUrl'])
            data = json.loads(response.css('script#__NEXT_DATA__::text').get())
            queries = data['props']['pageProps']['dehydratedState']['queries']
            snap = next(q['state']['data']['data'] for q in queries if q['queryKey'][0] == 'contentAPI.getApi2SnapSnapsByIdV1')
            profiles = next((q['state']['data']['data']['list'] for q in queries if q['queryKey'][0] == 'contentAPI.getApi2SnapProfilesV1'), [])
            author = next((p['nickname'] for p in profiles if p['id'] == snap['createdBy']['id']), '用户穿搭')
            path.write_text(json.dumps({'reviewIndex':index, 'author':author, 'snap':snap},ensure_ascii=False,indent=2))
            time.sleep(.7)
        return json.loads(path.read_text())
    with ThreadPoolExecutor(max_workers=2) as executor:
        for item in executor.map(detail, SELECTED+ALTERNATE):
            print('Verified post',item['reviewIndex'],item['author'],item['snap']['aggregations']['likeCount'],flush=True)
    for index in ALTERNATE:
        d=json.loads((OUT/'details'/f'{index:03d}.json').read_text())
        for j,media in enumerate(d['snap']['medias'][:4]):
            if media['type'] != 'IMAGE': continue
            path=OUT/'previews'/f'alt-{index:03d}-{j}.jpg'
            if not path.exists(): path.write_bytes(fetch(media['path']).body)
    print('Provenance verified; alternate angles ready',flush=True)

if __name__ == '__main__': main()
