import requests
import bs4
import os
import re
import multiprocessing

Domain = 'https://www.thepaper.cn/'

# 爬取的动态页面
URL = 'https://www.thepaper.cn/list_25635'

# 请求头部
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
}

# 获取当前 url 的 html 文本
def get_html(url) :
	response = requests.get(url, headers = headers)
	if (response.status_code == 200) :
		return response.text
	else : return None

# 解析当前的 html 文本
def ParseThisPage(html) :
	soup = bs4.BeautifulSoup(html, 'lxml')

	lts = soup.find_all('h2')
	for s in lts :
		# yield 会返回一个可迭代的 生成器 (generator), 
		# 只能一次性迭代
		yield {
		'title': s.a.text, 
		# 详情页面的链接 (只有后缀)
		'href': s.a['href']
		}

# 获取当前 html 文本中的图片链接
def get_pic_urls(html) :
	soup = bs4.BeautifulSoup(html, 'lxml')

	if(soup.h1) :
		# 取出 <h1>, 标题
		title = soup.h1.text
		# width 给出的是一个 list, 可以找到所有 width = "100%" 或 width = "600" 的 <img> 标签
		lts = soup.find_all(name = 'img', width = ['100%', '600'])

		for i in range(len(lts)) :
			pic_url = lts[i].attrs['src']
			# num 用来计数
			yield {
			'title': title,
			'pic_url': pic_url,
			'num': i
			}

# 保存图片
def save_pics(pic) :
	'''
	:pic: 一个字典, 包括 {'title': 标题, 'pic_url': 图片链接, 'num': 编号}
	'''

	title = pic['title']
	url = pic['pic_url']
	num = pic['num']
	# 用来去除一些文件名中不允许的字符
	# 文章标题中有好多半角字符的 ｜
	title = re.sub(r'[ \/:*?"<>|｜]', '', title).strip()
	# print (title)

	# 为当前这篇文章新建一个文件夹
	if not os.path.exists(title) :
		os.mkdir(title)

	response = requests.get(url, headers = headers)
	try:
		if (response.status_code == 200) :
			# 保存图片
			file = '{0}/{1}.jpg'.format(title, num)
			if not os.path.exists(file) :
				with open(file, 'wb') as f :
					f.write(response.content)
					print('文章"{0}"的第{1}张图片下载完成'.format(title,num))
	except Exception as e:
		print ('Picture download failed')
		return None


def Job(i) :
	# 构造 AJAX 的请求 url
	cur_url = Domain + 'load_index.jsp?nodeids=25635&topCids=&pageidx=' + str(i)
	html = get_html(cur_url)
	suffixs = ParseThisPage(html)

	for item in suffixs :
		# 解析详情页面
		html = get_html(Domain + item['href'])
		# 获取图片的 urls
		pic_urls = get_pic_urls(html)
		# 保存图片
		for pic in pic_urls :
			save_pics(pic)

'''
# 单进程, 耗时 1165.7s
if __name__ == '__main__' :
	# 新建一个文件夹
	if not os.path.exists('pengpai_pictures') :
		os.mkdir('pengpai_pictures')
	# 切换到那个文件夹下
	os.chdir('./pengpai_pictures')

	for i in range(1, 26) :
		Job(i)
'''

# 多进程, 耗时 343.8s
if __name__ == '__main__' :
	if not os.path.exists('pengpai_pictures') :
		os.mkdir('pengpai_pictures')
	os.chdir('./pengpai_pictures')

	pl = multiprocessing.Pool()
	pl.map(Job, [i for i in range(1, 26)])
	pl.close()
	pl.join()
