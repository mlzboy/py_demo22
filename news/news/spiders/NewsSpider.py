# -*- coding: utf-8 -*-
import datetime
import time
import scrapy
import codecs
import re
from news.items import *
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scrapy.http import HtmlResponse

class NewsspiderSpider(scrapy.Spider):
    name = 'NewsSpider'
    allowed_domains = ['zjhrss.gov.cn']
    start_urls = ['http://www.zjhrss.gov.cn/col/col1389544/index.html?uid=4451525&pageNum=140']

    def __init__(self):
	
	desired = DesiredCapabilities.CHROME
	desired ['loggingPrefs'] = { 'browser':'ALL' }
	self.display = Display(visible=0, size=(800, 600))
	self.display.start()
	chrome_options = Options()
	# 使用headless无界面浏览器模式
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.binary_location = "/usr/bin/chromium-browser"
	# 启动浏览器，获取网页源代码
	self.browser = webdriver.Chrome(executable_path="/usr/local/chromedriver-Linux64",chrome_options = chrome_options,desired_capabilities=desired)

    def parse(self, response):
	self.browser.get(response.url)
	self.log("url:%s"%(response.url,))
	#self.log(response.text)
	#time.sleep(10)
	#print "="*10,"first url loaded.."
	html = self.browser.page_source
	#f = codecs.open("./html.txt","w","utf-8")
	#f.write(html)
	#f.close()
        #self.log("="*10)
	for match in re.finditer(r'<li style[\s\S]*?<a[\s\S]*?href="(?P<href>[\s\S]*?)"[\s\S]*?>(?P<title>[\s\S]*?)</a>[\s\S]*?>(?P<date>[\s\S]*?)<', html):
	#for match in re.finditer(r"<a style[\s\S]*?href='(?P<href>[\s\S]*?)'[\s\S]*?>(?P<title>[\s\S]*?)</a>[\s\S]*?>(?P<date>[\s\S]*?)<", html):
		item = 	NewsItem()
		item['date'] = match.group("date")
		print "date:====>",item['date']
		#time.sleep(10000)
		item['href'] = match.group("href")
		item['title'] = match.group("title")
		print "title:====>",item['title']
		item['created_at'] = str(datetime.datetime.now())
		yield item
	#操作下一页
	#注意有return返回数值，否则返回None,在未发现此功能前还写了一个inject_js,多此一举，orz
	result = self.browser.execute_script('return $("a.default_pgBtn.default_pgNext.default_pgNextDisabled").length')
	print "result:====>",result,type(result)
	while result != 1:
		self.browser.execute_script('$("a.default_pgBtn.default_pgNext").click()')
		result = self.browser.execute_script('return $("a.default_pgBtn.default_pgNext.default_pgNextDisabled").length')
		print "result:====>",result,type(result)
		time.sleep(2)
		html = self.browser.page_source
		for match in re.finditer(r'<li style[\s\S]*?<a[\s\S]*?href="(?P<href>[\s\S]*?)"[\s\S]*?>(?P<title>[\s\S]*?)</a>[\s\S]*?>(?P<date>[\s\S]*?)<', html):
			item = 	NewsItem()
			item['date'] = match.group("date")
			item['href'] = match.group("href")
			item['title'] = match.group("title")
			print "title:====>",item['title']
			item['created_at'] = str(datetime.datetime.now())
			yield item
	

    def __del__(self):
	self.browser.quit()
	


