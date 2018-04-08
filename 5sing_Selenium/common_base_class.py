# -*- coding:utf-8 -*-
from config import HEADERS
from constants import CHROME_DRIVER
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.action_chains import ActionChains


class BaseSeleniumClass(object):

    def __init__(self, down_dir):
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent='%s'" % HEADERS['User-Agent'])
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': down_dir}
        options.add_experimental_option('prefs', prefs)
        chromedriver = CHROME_DRIVER
        self.driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
        self.driver.maximize_window()  
        self.driver.implicitly_wait(10)      

    def close_tab(self):
        # 关闭标签
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()
        self.driver.refresh()

    def tearDown(self):
        # 关闭浏览器
        self.driver.implicitly_wait(5)
        self.driver.quit()

