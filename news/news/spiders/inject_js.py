#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# created by heqingpan

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

_init_js="""
(function (){
if (window.__e)
{ return;
}
var e=document.createElement('div');
e.setAttribute("id","__s_msg");
e.style.display="none";
document.body.appendChild(e);
window.__e=e;
})();
window.__s_set_msg=function(a){
    window.__e.setAttribute("msg",a.toString()||"");
}
"""
_loadJsFmt="""
var script = document.createElement('script');
script.src = "{0}";
document.body.appendChild(script);
"""
_jquery_cdn="http://lib.sinaapp.com/js/jquery/1.7.2/jquery.min.js"
_warpjsfmt="__s_set_msg({0})"

class ExeJs(object):
    def __init__(self,driver,trytimes=10):
        from time import sleep
        self.driver=driver
        driver.execute_script(_init_js)
        while trytimes >0:
            try:
                self.msgNode=driver.find_element_by_id('__s_msg')
                break
            except Exception:
                sleep(1)
                trytimes -= 1
        if self.msgNode is None:
            raise Exception()
    def exeWrap(self,jsstr):
        """ jsstr 执行后有返回值，返回值通过self.getMsg()获取 """
        self.driver.execute_script(_warpjsfmt.format(jsstr))
    def loadJs(self,path):
        self.execute(_loadJsFmt.format(path))
    def loadJquery(self,path=_jquery_cdn):
        self.loadJs(path)
    def execute(self,jsstr):
        self.driver.execute_script(jsstr)
    def getMsg(self):
        return self.msgNode.get_attribute('msg')


if __name__ == "__main__":
	desired = DesiredCapabilities.CHROME
	desired ['loggingPrefs'] = { 'browser':'ALL' }
	display = Display(visible=0, size=(800, 600))
	#self.display.start()
	chrome_options = Options()
	# 使用headless无界面浏览器模式
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.binary_location = "/usr/bin/chromium-browser"
	# 启动浏览器，获取网页源代码
	browser = webdriver.Chrome(executable_path="/usr/local/chromedriver-Linux64",chrome_options = chrome_options,desired_capabilities=desired)
	#browser.get("http://www.zjhrss.gov.cn/col/col1389544/index.html?uid=4451525&pageNum=1")
	browser.get("http://www.zjhrss.gov.cn/col/col1389544/index.html?uid=4451525&pageNum=143")
	
	exeJs = ExeJs(browser)
	exeJs.exeWrap('$("a.default_pgBtn.default_pgNext.default_pgNextDisabled").length')
	print exeJs.getMsg()
