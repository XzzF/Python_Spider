import pandas as pd
import matplotlib.pyplot as plt 


# csv_cols = ['name', 'stars', 'score', 'time', 'area']
# csv 文件中已经有列名了, 不用再指定了; 再指定就会将原有列名读作一行数据
# df = pd.read_csv('猫眼电影Top100.csv', encoding = 'utf-8', names = csv_cols)
df = pd.read_csv('猫眼电影Top100.csv', encoding = 'utf-8')


# plt 显示中文
font_name = "STKaiti"
plt.rcParams['font.family'] = font_name
plt.rcParams['axes.unicode_minus'] = False # in case minus sign is shown as box

# 使用 ggplot style
plt.style.use('ggplot')


# 分析评分最高的 10 部电影
def Analysis_film() :
	# 先按评分排序
	top_films = df.sort_values('score', ascending = False)

	# 取出电影名称及对应的评分
	names = list(top_films.name[:10])
	scores = list(top_films.score[:10])

	# 画图的时候不支持字符串, 所以转化为 float
	for i, v in enumerate(scores) :
		scores[i] = float(v)

	# print (names)
	# print (type(scores[0]))

	x_pos = [i for i, _ in enumerate(scores)]
	width = 0.75
	# 柱状图
	plt.bar(x_pos, scores, width, color = '#FF5A00')

	plt.xlabel("电影名称")
	plt.ylabel("评分")
	plt.title("猫眼评分最高的10部电影")

	plt.ylim( (9.0, 9.7) )  # 设置 y 轴的范围

	# 给柱条上写上对应的评分
	for i, v in enumerate(scores) :
		# plt.text(x, y, text, ...) x,y 坐标, text 文本
		plt.text(i, v + 0.02, str(v), ha = 'center', color = 'blue')

	plt.xticks(x_pos, names, rotation = -45)
	plt.tight_layout() #自动控制空白边缘, 以全部显示x轴名称
	# plt.savefig('./imgs/top10_film.png', dpi = 700)  # dpi 表示分辨率
	plt.show()

# 分析各国家/地区的电影数量
def Analysis_area() :
	# 按地区分组, 统计数量后排序
	area_count = df.groupby('area').area.count().sort_values(ascending = True)
	# print (area_count.index)

	y_pos = [i for i, _ in enumerate(area_count.values)]
	width = 0.70
	# 水平的柱状图
	plt.barh(y_pos, area_count.values, width, align = 'center', color = 'red')

	for i, v in enumerate(area_count.values) :
		plt.text(v + 0.7, i - 0.1, str(v), ha = 'center', color = 'green')

	plt.yticks(y_pos, area_count.index)
	plt.title(u'各国家/地区电影数量')
	plt.ylabel(u'国家/地区')
	plt.xlabel(u'数量(部)')

	plt.tight_layout()
	plt.savefig('./imgs/area.png', dpi = 700)
	# plt.show()

# 分析各年份的电影数量
def Analysis_year() :
	# method one
	# lambda 表达式, 不是很懂, 但是很简单
	# df['year'] = df['time'].map(lambda x: x.split('-')[0])

	# method two
	df['year'] = df['time'].copy()
	# loc[i, 'year'] 表示第 i 行 year 列的单元值
	for i, v in enumerate( df['year'] ) :
		df.loc[i, 'year'] = v.split('-')[0]

	# 指定图形的宽度, 高度 和分辨率
	plt.figure(figsize = (13.195, 5.841), dpi = 700)

	year_count = df.groupby(by = 'year').year.count()

	x_pos = [i for i, _ in enumerate(year_count.values)]

	# 折线图
	plt.plot(year_count.index, year_count.values, linewidth = 2, color = 'green')

	# 在对应位置写上文本
	for i, v in enumerate(year_count.values) :
		plt.text(i, v + 0.2, str(v), ha = 'center', color = 'blue')

	plt.title(u'各年份上映的电影数量')
	plt.xlabel(u'年份(年)')
	plt.ylabel(u'数量(部)')

	plt.tight_layout()
	plt.savefig('./imgs/year.png', dpi = 700)
	# plt.show()


def Analysis_actor() :
	# print (df['stars'].values)
	star_doc = []
	for s in df['stars'].values :
		for x in s.split(',') :
			star_doc.append(x)
	# set 去重
	uniq_star = set(star_doc)
	# print (uniq_star)

	# 构建演员及其参演电影数量的字典
	dict_star = {}
	for i in uniq_star :
		if (star_doc.count(i) > 1) :
			dict_star[i] = star_doc.count(i)

	# 二维排序: 先按参演数量排序, 再按名字排序
	dict_star = sorted(dict_star.items(), key = lambda x: (x[1], x[0]), reverse = True)
	# 排序之后是元组形式
	dict_star = dict(dict_star[:10])
	# print (dict_star)

	x_pos = [i for i, _ in enumerate(dict_star.keys())]

	x = list(dict_star.keys())
	y = list(dict_star.values())

	plt.bar(x_pos, y)

	for i, v in enumerate(y) :
		plt.text(i, v + 0.2, str(v), ha = 'center', color = 'blue')

	# 名字逆时针旋转 45 度, 避免拥挤
	plt.xticks(x_pos, x, rotation = 45)
	plt.title(u'各演员参演的电影数量')
	plt.xlabel(u'演员')
	plt.ylabel(u'数量(部)')

	plt.tight_layout()
	plt.savefig('./imgs/actor.png', dpi = 700)
	# plt.show()

if __name__ == '__main__':
	'''
	Import Tips : 一定要分为 4 次分别运行 !
		写的时候偷懒了, 没有新建 plt
	'''
	# Analysis_film()
	# Analysis_area()
	# Analysis_year()
	Analysis_actor()