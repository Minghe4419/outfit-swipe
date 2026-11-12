"""Manual curation after viewing outputs/static-N.png; never guesses image labels."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
# preview number, Chinese title, style, palette, silhouette, layering, season
SELECTION=[
(3,'藏蓝衬衫 × 米色长裤',['简约','通勤'],['蓝色系','大地色'],['利落'],['叠穿'],['春秋']),
(4,'橄榄绿与白色的轻通勤',['简约','通勤'],['大地色','浅色系'],['利落'],['简洁单层'],['春秋']),
(5,'深色牛仔衬衫，配白裤',['休闲','简约'],['黑白灰'],['宽松'],['叠穿'],['春秋']),
(9,'红格纹叠穿浅色牛仔',['休闲','复古'],['蓝色系','亮色点缀'],['宽松'],['叠穿'],['春秋']),
(12,'灰格纹与棕色长裤',['复古','休闲'],['大地色'],['宽松'],['叠穿'],['春秋']),
(13,'深色衬衫与直筒牛仔',['简约','通勤'],['蓝色系'],['利落'],['简洁单层'],['春秋']),
(17,'黑白格纹，红鞋点睛',['复古','休闲'],['蓝色系','亮色点缀'],['宽松'],['叠穿'],['春秋']),
(19,'棕格纹与黑色长裤',['复古','休闲'],['大地色'],['宽松'],['叠穿'],['春秋']),
(26,'浅蓝衬衫与黑色短裤',['简约','休闲'],['蓝色系','浅色系'],['宽松'],['叠穿'],['夏季']),
(28,'短袖格纹 × 米色长裤',['休闲','复古'],['蓝色系','大地色'],['宽松'],['叠穿'],['夏季']),
(31,'浅桃色衬衫与浅蓝牛仔',['休闲','简约'],['浅色系','蓝色系'],['宽松'],['叠穿'],['夏季']),
(34,'白衬衫与米色短裤',['简约','休闲'],['浅色系','大地色'],['利落'],['叠穿'],['夏季']),
(35,'黑色衬衫的夏日叠穿',['休闲'],['黑白灰'],['宽松'],['叠穿'],['夏季']),
(41,'藏蓝短袖与浅色短裤',['简约','休闲'],['蓝色系','浅色系'],['利落'],['简洁单层'],['夏季']),
(21,'浅格纹衬衫与黑色阔腿裤',['休闲','简约'],['浅色系','黑白灰'],['宽松'],['叠穿'],['春秋']),
(43,'牛仔短袖与黑色长裤',['简约','休闲'],['蓝色系','黑白灰'],['利落'],['简洁单层'],['夏季']),
(50,'浅粉针织与黑色长裤',['简约','通勤'],['浅色系'],['利落'],['简洁单层'],['春秋','秋冬']),
(52,'深色夹克的低调叠穿',['简约','通勤'],['黑白灰','蓝色系'],['宽松'],['叠穿'],['春秋','秋冬']),
(53,'灰色针织，红鞋点睛',['简约','休闲'],['黑白灰','亮色点缀'],['宽松'],['简洁单层'],['春秋']),
(55,'橄榄绿夹克与红色内搭',['休闲','复古'],['大地色','亮色点缀'],['宽松'],['叠穿'],['春秋']),
]
def curate():
 rows=json.loads((R/'outputs/static-candidates.json').read_text());result=[]
 for order,(index,title,style,palette,silhouette,layering,season) in enumerate(SELECTION):
  row=rows[index-1]
  if not (R/'outputs/static'/f'{index:03}.jpg').exists():raise RuntimeError(f'Missing preview {index}')
  result.append({'id':f'look-{index:03}','order':order,'title':title,'image':row['image'],'source':row['source'],'sourceName':'JOGUNSHOP','facets':dict(style=style,palette=palette,silhouette=silhouette,layering=layering,season=season),'previewIndex':index,'tagMethod':'manual-visual-review','capturedDate':'2026-11-12'})
 (R/'app/looks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print('Curated',len(result))
if __name__=='__main__':curate()
