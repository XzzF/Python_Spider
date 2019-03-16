import requests
import os
import csv
from bs4 import BeautifulSoup


URL = 'https://maoyan.com/board/4?offset='

# 请求头部
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
}

information = []

# 把上映时间和上映地区分开
def getRelease(info) :
	'''
	:param info: 上映信息的字符串 "YY-MM-DD(Area)"
	'''

	l = info.split('(')
	try :
		time = l[0][5:]
	except : time = 'Unknow'
	try :
		area = l[1][:-1]
	except : area = 'Unknow'
	return time, area


def parseThisPage(url) :
	'''
	:param url: 爬取的网页
	'''

	# 获得网页的 html 文本
	html = requests.get(url, headers = headers).text
	# print (html)
	# 构造解析器
	soup = BeautifulSoup(html, 'lxml')
	
	# 找到 <dl class='board-wrapper'> 中的所有 <dd> 标签
	# 是一个 list 
	lists = soup.find('dl', {'class': 'board-wrapper'}).find_all('dd')

	for item in lists :
	
		# 找 class='name' 的 <p> 标签, 其 <a> 子标签的文本就是电影名称
		name = item.find('p', {'class': 'name'}).a.text
		# class='star' 的文本就是主演 (并把前面 "主演：" 去掉)
		star = item.find('p', {'class': 'star'}).text.strip()[3:]

		# 电影评分 整数和小数分开的, 爬下来之后合起来就行
		score_info = item.find('p', {'class': 'score'}).find_all('i')
		score = score_info[0].text + score_info[1].text
		
		# 先爬取上映信息
		release_info = item.find('p', {'class': 'releasetime'}).text
		# 获得对应的时间和地区
		time = getRelease(release_info)[0]
		area = getRelease(release_info)[1]

		# 合成一个字典
		info  = {'name': name, 'stars': star, 'score': score, 'time': time, 'area': area}

		information.append(info)


def WriteDictToCSV(csv_file, csv_cols, dict_data) :
	'''
	:param csv_file: csv 文件的路径
	:param csv_cols: csv 文件的列名
	:param dict_data: 元素为字典的 list 数据
	'''

	# 指定编码方式为 utf-8 (newline 参数不这样指定的话, 会有多的空行)
	with open(csv_file, 'w', newline = '', encoding = 'utf-8-sig') as csvfile :

		# 传递列名给相应的参数
		writer = csv.DictWriter(csvfile, fieldnames = csv_cols)
		writer.writeheader()

		for data in dict_data :
			writer.writerow(data)

def save_data() :
	# 获取当前路径 并指定文件名
	csv_file = os.getcwd() + '\\猫眼电影Top100.csv'
	# 指定列名
	csv_cols = ['name', 'stars', 'score', 'time', 'area']
	WriteDictToCSV(csv_file, csv_cols, information)

if __name__ == '__main__':
	for i in range(10) :
		url = URL + str(i * 10)
		parseThisPage(url)

	save_data()