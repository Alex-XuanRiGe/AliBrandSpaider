#!/usr/bin/env python3
#-*- coding:UTF-8 -*-

import  requests
from requests import RequestException


def get_catg1_html(url):
	response = requests.get(url)
	if response.status_code == 200:
		html = response.content
		html_doc = html.decode("utf-8", "ignore") ##解决获取到的源码中-中文字符乱码问题
		print('-----------------Requestrian Successfullly!----------------------------------')
		return html_doc
	else:
		return "Response Erro!" + response.status_code

def parse_catg1():
	return ""



def main():
	url = 'https://www.1688.com/?spm=a261b.2187593.alibar.d5.6780633f1Ujldj'
	# useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'

	# headers = {
	# 	# ':authority':'bertoys.1688.com',
	# 	# ':method':'GET',
	# 	# ':path':'/page/offerlist.htm?spm=a2615.7691456.0.0.0MNLge&tradenumFilter=false&sampleFilter=false&mixFilter=false&privateFilter=false&mobileOfferFilter=%24mobileOfferFilter&groupFilter=false&sortType=tradenumdown&pageNum=6',
	# 	# ':scheme':'https',
	# 	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	# 	'accept-encoding': 'gzip, deflate, sdch, br',
	# 	'accept-language': 'zh-CN,zh;q=0.8',
	# 	'referer': url,
	# 	'upgrade-insecure-requests': '1',
	# 	'user-agent': useragent,
	# }

	content = get_catg1_html(url)
	print(content)

if __name__== '__main__':
	main()