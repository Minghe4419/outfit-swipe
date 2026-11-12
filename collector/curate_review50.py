"""Publish only the fifty visually reviewed whole outfits, never raw candidates."""
from pathlib import Path
from collections import Counter
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/v3'
# Each row is an explicit GPT visual review, not a caption keyword inference.
# index | title | thickness | style | palette | silhouette | layering
REVIEWS = '''
1|黑色长大衣与垂坠宽裤|厚暖|简约|黑白灰|宽松|叠穿
4|湖蓝短棉服与浅灰工装裤|厚暖|休闲|亮色点缀|宽松|叠穿
7|橄榄短夹克与黑色围巾|厚暖|休闲|大地色|宽松|叠穿
9|深灰长大衣与同色西裤|厚暖|通勤|黑白灰|宽松|叠穿
10|灰色短外套与黑色垂坠裤|适中|简约|黑白灰|宽松|叠穿
12|深色短夹克与直筒牛仔裤|适中|简约|蓝色系|利落|叠穿
14|棕色西装与卡其打褶裤|适中|复古|大地色|宽松|叠穿
15|黑色外套与宽腿长裤|适中|休闲|黑白灰|宽松|叠穿
16|橄榄针织与棕色休闲裤|适中|复古|大地色|宽松|简洁单层
39|黑色绒感外套与浅灰卫裤|厚暖|休闲|黑白灰|宽松|叠穿
18|焦糖格纹针织与黑色牛仔|适中|复古|大地色|宽松|简洁单层
19|深棕短夹克与黑色宽裤|适中|简约|大地色|宽松|叠穿
20|棕色针织与深色直筒裤|适中|复古|大地色|宽松|叠穿
21|酒红针织开衫与奶油长裤|适中|休闲|亮色点缀|宽松|叠穿
22|黑色工装夹克与卡其宽裤|适中|复古|大地色|宽松|叠穿
23|黑色皮夹克与酒红内搭|适中|复古|亮色点缀|利落|叠穿
24|燕麦色拉链针织与深色宽裤|适中|简约|浅色系|宽松|叠穿
58|深色短棉服与灰色长裤|厚暖|简约|黑白灰|利落|叠穿
26|黑色皮夹克与炭灰长裤|适中|简约|黑白灰|利落|叠穿
30|灰色夹克与浅蓝宽牛仔|适中|休闲|蓝色系|宽松|叠穿
28|深棕翻领针织与卡其宽裤|适中|复古|大地色|宽松|叠穿
32|红色翻领针织与灰色西裤|适中|复古|亮色点缀|宽松|叠穿
33|深色条纹针织与灰色长裤|适中|简约|黑白灰|利落|简洁单层
35|橄榄夹克与浅蓝牛仔裤|适中|休闲|大地色|宽松|叠穿
36|浅色图案外套与黑色长裤|适中|休闲|浅色系|宽松|叠穿
70|浅灰短棉服与米色宽裤|厚暖|简约|浅色系|宽松|叠穿
40|黑色短棉服与宽腿牛仔|厚暖|休闲|蓝色系|宽松|叠穿
41|深棕长大衣与棕色长裤|厚暖|通勤|大地色|利落|叠穿
42|全黑短夹克与直筒长裤|适中|简约|黑白灰|利落|叠穿
43|驼色短外套与浅灰长裤|适中|通勤|大地色|利落|叠穿
44|深色绒面夹克与橄榄长裤|厚暖|复古|大地色|利落|叠穿
45|黑色连帽卫衣与棕色宽裤|适中|休闲|大地色|宽松|简洁单层
47|皮夹克与浅蓝牛仔、黑靴|适中|复古|蓝色系|宽松|叠穿
48|深蓝运动上衣与同色长裤|适中|休闲|蓝色系|宽松|简洁单层
51|灰褐短棉服与炭色长裤|厚暖|休闲|大地色|宽松|叠穿
53|深棕针织与蓝色宽牛仔|适中|休闲|蓝色系|宽松|简洁单层
55|棕色牛角扣大衣与灰褐宽裤|厚暖|复古|大地色|宽松|叠穿
56|黑色短棉服与浅灰宽裤|厚暖|休闲|黑白灰|宽松|叠穿
57|浅灰纹理针织与黑色宽裤|适中|简约|黑白灰|宽松|简洁单层
59|黑色高领针织与黑色长裤|适中|简约|黑白灰|利落|简洁单层
60|黑色西装与灰褐宽腿长裤|适中|通勤|黑白灰|宽松|叠穿
62|深色拉链针织与运动鞋|适中|休闲|黑白灰|利落|叠穿
63|黑色短大衣与灰色西裤|厚暖|通勤|黑白灰|宽松|叠穿
66|深蓝翻领卫衣与浅灰卫裤|适中|休闲|蓝色系|宽松|简洁单层
68|焦糖灯芯绒西装与黑色长裤|适中|复古|大地色|利落|叠穿
72|黑色衬衫与棕色打褶长裤|适中|通勤|大地色|宽松|简洁单层
75|深棕针织与蓝色直筒牛仔|适中|简约|蓝色系|利落|简洁单层
78|炭灰短夹克与深蓝宽牛仔|适中|简约|蓝色系|宽松|叠穿
81|红色菱格针织与奶白长裤|适中|复古|亮色点缀|利落|叠穿
84|橄榄长款绗缝外套与卡其裤|厚暖|休闲|大地色|宽松|叠穿
'''
ANGLES = {28:1, 39:2, 58:3, 70:2}

def main():
    pool = json.loads((OUT/'candidate-pool.json').read_text())
    result=[]
    for order,row in enumerate(REVIEWS.strip().splitlines()):
        index,title,thickness,style,palette,silhouette,layering=row.split('|')
        index=int(index);candidate=pool[index-1]
        d=json.loads((OUT/'details'/f'{index:03d}.json').read_text());snap=d['snap']
        assert snap['model']['gender']=='MEN', (index,snap['model'])
        angle=ANGLES.get(index,0);image=snap['medias'][angle]['path']
        preview=f'outputs/v3/previews/alt-{index:03d}-{angle}.jpg' if index in ANGLES else candidate['previewFile']
        assert (ROOT/preview).exists()
        result.append({'id':'ms-'+snap['id'],'order':order,'title':title,'image':image,
          'source':candidate['linkUrl'],'sourceName':'MUSINSA · '+d['author'],
          'sourceAuthor':d['author'],'sourceLikes':snap['aggregations']['likeCount'],
          'sourcePublishedAt':snap['createdAt'], 'capturedDate':'2026-11-12',
          'selectionBasis':'男生用户冬季关键词热门列表候选；GPT逐张视觉筛选，非按点赞阈值保证高赞',
          'facets':{'thickness':[thickness],'style':[style],'palette':[palette],
                    'silhouette':[silhouette],'layering':[layering],
                    'season':['秋冬'] if thickness=='厚暖' else ['春秋']},
          'note':'厚度按画面粗分；冬季可能需要加外套' if thickness=='适中' else '韩系男生 · 整套灵感',
          'tagMethod':'gpt-visual-review','reviewIndex':index,'reviewedMediaIndex':angle,
          'previewFile':preview})
    assert len(result)==len({r['id'] for r in result})==len({r['image'] for r in result})==50
    authors=Counter(r['sourceAuthor'] for r in result)
    assert max(authors.values())<=3
    old=json.loads((OUT/'previous-looks.json').read_text())
    assert not ({r['image'] for r in old}&{r['image'] for r in result})
    (ROOT/'app/looks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    report={'candidatePosts':len(pool),'selectedPosts':50,'authorCount':len(authors),
            'thickness':dict(Counter(r['facets']['thickness'][0] for r in result)),
            'reviewMethod':'GPT contact-sheet visual review plus post provenance verification',
            'rejected':{'halfBodyOrIncomplete':[3,5,6,13,27,29,34,38,49,50,64,74,77,80,88,91],
                        'collageOrFlatlayOrText':[2,8,46,54,79,83],
                        'duplicateAngle':[65,71]},
            'alternateAngles':ANGLES,'allOldImagesRemoved':True,'noOnlineAICalls':True}
    (OUT/'review-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
