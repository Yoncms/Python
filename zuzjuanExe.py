#### 执行爬取
import time
import random
from zujuan import zujuan

zj = zujuan()

#zj.answer()
#
#exit()

Url = 'https://www.zujuan.com/api/question/list?xd=2&chid=11&categories=&question_channel_type=&difficult_index=&exam_type=&kid_num=&grade_id=&sort_field=time&filterquestion=0&content=&year=2022&tree_type=knowledge&version_id=&terms=&knowledges%5B%5D='
## 地址通过fiddler抓取
## 主题2
#Url += 'xd=2&chid=11&categories=&knowledges%5B%5D=1709&question_channel_type=&difficult_index=&exam_type=&kid_num=&grade_id=&sort_field=time&filterquestion=0&content=&year=2022&tree_type=knowledge&version_id=&terms=&_='
## 主题3
#Url += 'xd=2&chid=11&categories=&knowledges%5B%5D=1719&question_channel_type=&difficult_index=&exam_type=&kid_num=&grade_id=&sort_field=time&filterquestion=0&content=&tree_type=knowledge&joinType=&version_id=&terms=&_='
## 主题4
#Url += '1733&_='
## 主题5
Url += '1751&_='
for n in range(1,10):
	ts = str(time.time())[0:10]+'000'+'&page='+str( n )
	Url += ts
	zj.Run(Url,'oo.htm')
	print(str(n) + '>>>>正在运行，请稍等......')
	time.sleep( random.randint(3, 6) )
print( '>>>>程序结束<<<<' )
