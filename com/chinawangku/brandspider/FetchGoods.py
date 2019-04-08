#!/usr/bin/env python3
#-*-coding:UTF-8-*-
import re

import MySQLdb
import requests
import random
import datetime
from lxml import etree
from imp import reload
import sys

reload(sys)
sys.setdefaultencoding('utf8')


# 程序进行前准备：
# 1.要先创建个数据库将1688database名字的数据库，然后创建好urltable表，用sqlyong工具将店铺网址都放到urltable表里面去
# 2.将urltable表的url店铺地址存储到url_list列表中
#   url的格式：https://shop1470760677060.1688.com/page/offerlist.htm?spm=a261y.7663282.0.0.Su0VBS

def get_url_list():
	url_list = []
	get_url_sql = 'SELECT url FROM urltable;'
	count = cur.execute(get_url_sql)
	print
	u' 有  %s 个店铺地址  ' % count
	urlresults = cur.fetchall()
	result = list(urlresults)
	for url in result:
		print
		url[0]
		url_list.append(url[0])
	return url_list


def get_all_goods_url(page):
	begin = datetime.datetime.now()

	# 如果出现异常，尝试次数5次，还是错误，则判断，页码超出范围，停止采集。
	page = page
	print
	u'.................第%s页...........' % page
	count = 0
	conut_net = 0

	DD = True
	while DD:
		print
		'conut_net-->', conut_net
		try:
			proxyHost = "proxy.abuyun.com"
			proxyPort = "9020"
			proxyUser = "H4073W6H9EJ29Z4D"
			proxyPass = "32D3D1294745B2B2"
			proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
				"host": proxyHost,
				"port": proxyPort,
				"user": proxyUser,
				"pass": proxyPass,
			}
			proxies = {
				"http": proxyMeta,
				"https": proxyMeta,
			}
			headers = {
				# ':authority':'bertoys.1688.com',
				# ':method':'GET',
				# ':path':'/page/offerlist.htm?spm=a2615.7691456.0.0.0MNLge&tradenumFilter=false&sampleFilter=false&mixFilter=false&privateFilter=false&mobileOfferFilter=%24mobileOfferFilter&groupFilter=false&sortType=tradenumdown&pageNum=6',
				# ':scheme':'https',
				'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				'accept-encoding': 'gzip, deflate, sdch, br',
				'accept-language': 'zh-CN,zh;q=0.8',
				'referer': url,
				'upgrade-insecure-requests': '1',
				'user-agent': useragent,
			}

			shop_url = url.split('?')[0]
			spm = url.split('?')[1]

			parameter = {
				'spm': spm,
				'tradenumFilter': 'false',
				'sampleFilter': 'false',
				'mixFilter': 'false',
				'privateFilter': 'false',
				'mobileOfferFilter': '$mobileOfferFilter',
				'groupFilter': 'false',
				'sortType': 'tradenumdown',
				'pageNum': str(page),
			}

			# 测试ip地址是否更换
			#             targetUrl = "http://www.ip.cn/"
			#             resp = requests.get(targetUrl, proxies=proxies)
			#             print resp.status_code
			#             #print resp.text
			#             regex =  '<code>(.*?)</code>'
			#             address_ip  = re.findall(regex, resp.text)[0]
			#             print address_ip
			#

			htm = requests.get(url, params=parameter, headers=headers, proxies=proxies)
			html = htm.text
			selecor = etree.HTML(html)
			goodlist = selecor.xpath('//*[@id="wp-all-offer-tab"]/div/div[2]/div/div/div/ul/li')
			# time.sleep(5)
			# print goodlist
			for good in goodlist:
				try:
					good_name = good.xpath('div[3]/a/text()')[0]
				except:
					print
					u'>>>>>>>>>>>>>>>>>>>>警告：没有找到商品名字，请检查程序！<<<<<<<<<<<<<<<<<<<<<<<<'
					good_name = ''
				# print 'good_name----------->  ',good_name
				try:
					good_url = good.xpath('div[3]/a/@href')[0]

				except:
					print
					u'>>>>>>>>>>>>>>>>>>>>警告：没有找到商品网址，请检查程序！<<<<<<<<<<<<<<<<<<<<<<<<'
					good_url = ''
				# print 'good_url----------->  ',good_url
				# //*[@id="wp-all-offer-tab"]/div/div[2]/div/div/div/ul/li/div[3]/a
				try:
					good_cover = good.xpath('div[1]/a/img/@data-lazy-load-src')[0]
					good_cover = 'https:' + good_cover
				except:
					good_cover = ''
					print
					u'>>>>>>>>>>>>>>>>>>>>警告：没有找到封面，请检查程序！<<<<<<<<<<<<<<<<<<<<<<<<'
				# print 'good_cover----------->  ',good_cover
				# //*[@id="wp-all-offer-tab"]/div/div[2]/div/div/div/ul/li/div[2]/div[1]/em

				try:
					good_price = good.xpath('div/em/text()')[0]
				except:
					try:
						good_price = good.xpath('div[2]/div[1]/em/text()')[0]
					except:
						good_price = 0
				# good_price = 0
				# print '>>>>>>>>>>>>>>>>>>>>警告：没有找到价格，请检查程序！<<<<<<<<<<<<<<<<<<<<<<<<'
				# print 'good_price----------->  ',good_price
				# //*[@id="wp-all-offer-tab"]/div/div[2]/div/div/div/ul/li/div[2]/div[2]/span
				# //*[@id="wp-all-offer-tab"]/div/div[2]/div/div/div/ul/li/div[2]/div[2]/span
				try:
					# buy_num =  good.xpath('div[2]/div[2]/span/text()')[0]
					buy_num = good.xpath('div/span/text()')[1]
				except:
					try:
						buy_num = good.xpath('div[2]/div[2]/span/text()')[0]

					except:
						buy_num = '0'
					# print '>>>>>>>>>>>>>>>>>>>>警告：没有找到交易量，请检查程序或网页是否有交易量！<<<<<<<<<<<<<<<<<<<<<<<<'
				# print 'buy_num----------->  ',buy_num

				try:
					insert_good_sql = "insert into  goodstable(shop_name,good_name,good_url,good_cover,buy_num,good_price) values ( '%s','%s','%s','%s','%s','%s')" % (
					shop_name, good_name, good_url, good_cover, buy_num, good_price)
					cur.execute(insert_good_sql)
					conn.commit()
				# print insert_good_sql
				except Exception as e:
					print
					e
					print
					u'数据库已经存在数据'

			if len(goodlist) == 0:
				if conut_net > 2:
					DD = False

					return 0
				else:
					conut_net += 1
					print
					u'conut_net出现异常，再次采集%s次' % conut_net
				continue
			else:
				DD = False
				return len(goodlist)

		except Exception as e:
			print
			e
			count += 1
			if count < 3:
				print
				'count出现异常，再次采集%s次' % count
				continue

			else:
				return 0


if __name__ == '__main__':
	print
	'KAISHI'
	begin = datetime.datetime.now()
	print
	'KAISHI'
	# 判断超出页码的范围，如果五次则结束循环
	page_conut = 0
	useragent_list = []
	useragent_handle = open('user-agent.txt')
	for useragent in useragent_handle:
		useragent_list.append(useragent)
	conn = MySQLdb.connect(host='localhost', db='1688database', user='root', passwd='1111', port=3306, charset='utf8')
	cur = conn.cursor()
	url_list = get_url_list()
	for url in url_list:
		# 判断超出页码的范围，如果五次则结束循环
		page_conut = 0
		regex = 'https://(.*?).1688.com'
		shop_name = re.findall(regex, url)[0]
		print
		shop_name
		# 以店铺域名创建数据库表

		# creat_table_sql = "CREATE TABLE shop_name;"
		useragent = random.choice(useragent_list).replace('\n', '')
		# print useragent
		# 页面范围设置
		for page in range(1, 200):
			len_link = get_all_goods_url(page)
			# 返回列表为空三次，推断已经超过页码了
			if len_link == 0:
				page_conut += 1
				print
				'page_conut---->', page_conut
				if page_conut >= 3:
					print
					u'已经超出页码范围，停止采集，进入下个店铺采集'
					break
	count_sql = 'SELECT * FROM goodstable;'
	all_num = cur.execute(count_sql)
	conn.close()  # 关闭数据库连接
	end = datetime.datetime.now()
	print
	u'一共采集%s条数据' % all_num
	print
	u'一共花了 %s时间' % (end - begin)
