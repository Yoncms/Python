#### 爬取组网的题目
import requests
import urllib3
import re
class zujuan:
	mJson = {}
	mHead = {}
	s = ''
	i = 1
	def __init__ (self):
		self.mHead = {
			"Host":"www.zujuan.com",
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
			"Accept":"*/*",
			"Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
			"Accept-Encoding":"gzip, deflate",
			"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
			"X-Requested-With":"XMLHttpRequest",
			"Connection":"keep-alive",
		}

	def setData (self, Url):
		urllib3.disable_warnings() ## 防止报错
		res = requests.get(Url,headers=self.mHead, verify=False)
		res.encoding = 'utf-8'
		self.mJson = res.json()

	## 生成选择题的四个答案的函数
	def abcd (self, obj):
		## 选择题通常有四个答案供选择
		opt = ['A','B','C','D']
		for em in opt:
			## 防止有时候没有四个答案的情况，先做个判断
			if em in obj.keys():
				self.s += em + '.' + obj[em] + '<br />'

	def makeData (self):
		Json = self.mJson['data']['questions']
		for x in Json:
			text = x['question_text']
			if '</p>' not in text:
				text += '<br />' 
			self.s += '</p>' + str(self.i) + '.' + text
			## 判断对象里是否存在减值是list的元素，keys类似于php里的array_keys
			if 'list' in x.keys() and x['list'] != None:
				j = 1
				for em in x['list']:
					if 'question_text' in em.keys():
						## 填空的空格使用下划线
						sr = '('+str(j)+')'+em['question_text'].replace( '<span class="filling" ></span>', '_________' )
						self.s += sr + '<br />'
						j += 1
			self.i += 1
			## 如果有options答案表示选择题
			if x['options'] != None:
				self.abcd( x['options'] )

	def Run (self, Url, fn):
		self.setData( Url )
		self.makeData()
		## 打开文件时也要指定编码，防止写入文件时中文乱码
		with open( fn,'w',encoding="utf-8" ) as f:
			f.write( '<meta charset="utf-8" />'+self.s )
		f.close()		

	def csrf (self):
		U = 'https://passport.zujuan.com/login'
		## 避免https抓取时的警告
		urllib3.disable_warnings()
		res = requests.get(U,verify=False)
		return re.findall('<input type="hidden" name="_csrf" value="(.+?)">', res.text )[0]	

	def mLogin (self):
		Url = 'https://www.zujuan.com/api/question/list?xd=2&chid=11&categories=4583&question_channel_type=&difficult_index=&exam_type=&kid_num=&grade_id=&sort_field=time&filterquestion=0&content=&joinType=&year=2022&version_id=&terms=16&_=1656166696377&page=1'
		mHead = {
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
			"cookie":"xd=75519cb9f2bf90d001c0560f5c40520062a60ada9cb38350078f83e04ee38a31a%3A2%3A%7Bi%3A0%3Bs%3A2%3A%22xd%22%3Bi%3A1%3Bi%3A2%3B%7D; _csrf=7407f18cc704a65fe728db0bc1ca020c878a5d1abbae0b72aad792cbaa85e8e3a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22ZSojnGgvUUcntoLCyYllfwm6PBmY6iA9%22%3B%7D; Hm_lvt_6de0a5b2c05e49d1c850edca0c13051f=1656751615; Hm_lvt_7c883648bf8afa969f5d094927d16816=1656751615; 53gid2=11292608094011; 53gid0=11292608094011; 53gid1=11292608094011; 53revisit=1656751615312; 53kf_72203385_from_host=www.zujuan.com; kf_72203385_land_page_ok=1; 53kf_72203385_land_page=https%253A%252F%252Fwww.zujuan.com%252F; 53uvid=1; onliner_zdfq72203385=0; device=310bdaba05b30bb632f66fde9bf3e2b91ebc4d607c250c2e1a1d9e0dfb900f01a%3A2%3A%7Bi%3A0%3Bs%3A6%3A%22device%22%3Bi%3A1%3BN%3B%7D; jump_url=07a0dbb3786e280ecb03486a0bec9fa3a5d10229d85f5608a1be9aba0e91277aa%3A2%3A%7Bi%3A0%3Bs%3A8%3A%22jump_url%22%3Bi%3A1%3Bs%3A23%3A%22https%3A%2F%2Fwww.zujuan.com%2F%22%3B%7D; visitor_type=old; 53kf_72203385_keyword=https%3A%2F%2Fpassport.zujuan.com%2F; _sync_login_identity=3b81e26a92ac5e41ceaa6a2b4dc2351d7ff04c74d885b7d1e26f92ab9d8ffc1ca%3A2%3A%7Bi%3A0%3Bs%3A20%3A%22_sync_login_identity%22%3Bi%3A1%3Bs%3A50%3A%22%5B1839598%2C%22rS-lsXI7pWqA3OWvKAiZXh4w_1qqdZnS%22%2C86400%5D%22%3B%7D; _identity=b2bc3326f7f6620bb985359203df3d2c8eed22bcee1b59e2e902c5276bbe4dd9a%3A2%3A%7Bi%3A0%3Bs%3A9%3A%22_identity%22%3Bi%3A1%3Bs%3A50%3A%22%5B1839598%2C%224aa288c0a2792fb04dc0d9a8b6bc002f%22%2C86400%5D%22%3B%7D; global_xd_chid=%7B%22xd%22%3A%222%22%2C%22chid%22%3A%2211%22%7D; _ACTIVE_BASKET_OPTION=; PHPSESSID=mffug7q3jpok9sbsqdl3tirji1; chid=cafaf1cbed4501b7d0e92ec2938f9931b96d5755c316dee169a043deb23cf4fea%3A2%3A%7Bi%3A0%3Bs%3A4%3A%22chid%22%3Bi%3A1%3Bs%3A2%3A%2211%22%3B%7D; Hm_lpvt_7c883648bf8afa969f5d094927d16816=1656754196; Hm_lpvt_6de0a5b2c05e49d1c850edca0c13051f=1656754196"
		}
		r_session = requests.session()
		## 避免https抓取时的警告
		urllib3.disable_warnings()
		res = r_session.get( Url, headers=mHead, cookies=cookies, verify=False )
		print( res.text )

	def answer (self):
		U = 'https://m.zujuan.com/question/detail-52034140.shtml'
		header={
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
			'cookie':'visitor_type=old; xd=75519cb9f2bf90d001c0560f5c40520062a60ada9cb38350078f83e04ee38a31a%3A2%3A%7Bi%3A0%3Bs%3A2%3A%22xd%22%3Bi%3A1%3Bi%3A2%3B%7D; _ACTIVE_BASKET_OPTION=; Hm_lvt_7c883648bf8afa969f5d094927d16816=1656899175; Hm_lvt_6de0a5b2c05e49d1c850edca0c13051f=1656899175; 53gid2=11302678872011; 53gid0=11302678872011; 53gid1=11302678872011; 53revisit=1656899175353; 53kf_72203385_from_host=www.zujuan.com; kf_72203385_land_page_ok=1; 53kf_72203385_land_page=https%253A%252F%252Fwww.zujuan.com%252Fquestion%253Fxd%253D2%2526chid%253D11; 53uvid=1; onliner_zdfq72203385=0; visitor_type=old; _csrf=41b0941ea0e93b15a5d3108c0c30e9db22c430e5f9ed8daef748ba85e592968ba%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22EgYOx6XWTa51-vuL3WlazZPaaazHsw2p%22%3B%7D; device=310bdaba05b30bb632f66fde9bf3e2b91ebc4d607c250c2e1a1d9e0dfb900f01a%3A2%3A%7Bi%3A0%3Bs%3A6%3A%22device%22%3Bi%3A1%3BN%3B%7D; jump_url=2433c4f5e3a62d64a319ab3ec4006c2f97beaf54c0e33f9bb043cb3ff904a6b5a%3A2%3A%7Bi%3A0%3Bs%3A8%3A%22jump_url%22%3Bi%3A1%3Bs%3A64%3A%22https%3A%2F%2Fwww.zujuan.com%2Fquestion%3Ftree_type%3Dknowledge%26xd%3D2%26chid%3D11%22%3B%7D; _sync_login_identity=4a6d8a45e49d2ac35e3500c2ef03bf8fcbd57a819fb49f439645865162ae7a60a%3A2%3A%7Bi%3A0%3Bs%3A20%3A%22_sync_login_identity%22%3Bi%3A1%3Bs%3A50%3A%22%5B1839598%2C%22L7Te7EwScQrUoKFcd9S3xBRy_66rSM37%22%2C86400%5D%22%3B%7D; _identity=b2bc3326f7f6620bb985359203df3d2c8eed22bcee1b59e2e902c5276bbe4dd9a%3A2%3A%7Bi%3A0%3Bs%3A9%3A%22_identity%22%3Bi%3A1%3Bs%3A50%3A%22%5B1839598%2C%224aa288c0a2792fb04dc0d9a8b6bc002f%22%2C86400%5D%22%3B%7D; global_xd_chid=%7B%22xd%22%3A%222%22%2C%22chid%22%3A%2211%22%7D; 53kf_72203385_keyword=https%3A%2F%2Fpassport.zujuan.com%2F; PHPSESSID=9grrso9m8na3pm2p6tck0rrpp0; chid=cafaf1cbed4501b7d0e92ec2938f9931b96d5755c316dee169a043deb23cf4fea%3A2%3A%7Bi%3A0%3Bs%3A4%3A%22chid%22%3Bi%3A1%3Bs%3A2%3A%2211%22%3B%7D; Hm_lpvt_6de0a5b2c05e49d1c850edca0c13051f=1656900143; Hm_lpvt_7c883648bf8afa969f5d094927d16816=1656900143'
		}
		## 避免https抓取时的警告
		urllib3.disable_warnings()
		r_session = requests.session()
		res = r_session.get(U, headers=header, verify=False )
		with open('aw.htm','w',encoding='utf-8') as f:
			f.write( res.text )
		f.close()
