# -*- coding:utf-8 -*-
import sys
import requests
from lxml import etree
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.action_chains import ActionChains

from config import HEADERS
from constants import BASE_URL, SING_INDEX_URL, SING_LOGIN_URL
from common_base_class import BaseSeleniumClass

reload(sys)
sys.setdefaultencoding('utf8')


class FiveSingCrawl2(BaseSeleniumClass):

    def account_pwd_login(self, usname, uspwd, login_btn_name, login_type):
        # 使用账号密码登录
        # 获取账户和密码的输入框
        us_name = self.driver.find_element_by_id(usname)
        us_pwd = self.driver.find_element_by_id(uspwd)
        # 将账户和密码分别输入两个框，每次操作间隔5秒
        us_name.send_keys(username)
        self.driver.implicitly_wait(5)
        us_pwd.send_keys(pwd)
        self.driver.implicitly_wait(5)
        # 勾选记住我
        # self.driver.find_element_by_class_name("IsSave").click()
        # 点击登录
        if login_type == 'class':
            login_btn = self.driver.find_element_by_class_name(login_btn_name)
        elif login_type == 'id':
            login_btn = self.driver.find_element_by_id(login_btn_name)
        else:
            login_btn = self.driver.find_element_by_xpath(login_btn_name)

        login_btn.click()
        self.driver.current_window_handle

    def login(self, username=None, pwd=None, is_third=True, third_part='QQ', third_usname=None, third_pwd=None):
        '''默认为第三方登录，分为QQ/weibo/kugou,则不需要输入账户密码。
            第三方登录页可以通过账号密码的方式
            友情提示：属性的名称不能有空格
           
        Keyword Arguments:
            username {[type]} -- 用户名（通行证/邮箱/手机号码） (default: {None})
            pwd {[type]} -- 密码 (default: {None})
            is_third {bool} -- 是否为第三方登录 (default: {True})
            third_part {[type]} -- 第三方登录默认选择QQ (default: 'QQ')
            third_usname {[type]} -- 第三方登录的账号 (default: {None})
            third_pwd {[type]} -- 第三方登录的密码 (default: {None})
        '''
        self.driver.get(SING_LOGIN_URL)
        self.driver.implicitly_wait(10)
        if is_third:
            if third_part == 'QQ' or 'qq':
                self.driver.find_element_by_class_name("qq").click()
                self.driver.implicitly_wait(10)
                # 切换页面
                self.driver.current_window_handle
                self.driver.implicitly_wait(10)
                # 获取登录所需信息所在iframe框
                self.driver.switch_to_frame("ptlogin_iframe")
                self.driver.implicitly_wait(10)
                # 如果第三方登录的账号密码存在，则使用账号密码登录
                # 否则本地登录了QQ，可以点击头像，前提是必须本地登录
                if third_usname and third_pwd:
                    self.driver.find_element_by_id("switcher_plogin").click()
                    self.driver.current_window_handle
                    self.account_pwd_login(usname='u', uspwd='p', login_btn_name='login_button', login_type='id')
                else:
                    # 头像登录
                    img_out_focus = self.driver.find_element_by_class_name("img_out_focus")
                    img_out_focus.click()
                    self.driver.current_window_handle


            elif third_part == 'weibo':
                self.driver.find_element_by_class_name("weibo").click()
                self.driver.implicitly_wait(10)
                # 切换页面
                self.driver.current_window_handle
                self.account_pwd_login(usname='userId', uspwd='passwd', login_btn_name='btnP', login_type='class')
            else:
                # 酷狗的第三方入口，也是QQ、微博之类的，有点重复，其他的如微信也不想再写
                self.driver.find_element_by_class_name("kugou").click()
                self.driver.implicitly_wait(10)
                # 切换页面
                self.driver.current_window_handle
                self.account_pwd_login(usname='UserName', uspwd='UserPwd', login_btn_name='//*[@id="submit"]/span/input', login_type='xpath')
        else:
            # 账号密码登录
            self.account_pwd_login(usname='us_name', uspwd='us_pwd', login_btn_name='lo_bnt', login_type='class')
            # us_name = self.driver.find_element_by_id("txtUserName")
            # us_pwd = self.driver.find_element_by_id("txtPassword")

    def get_download(self, url, page_type):
        '''根据传入的是歌曲页面还是歌手的主页进行下载，
        如果是artist，则下载歌手的所有音乐，如果是song，则下单首（推荐）
        
        Arguments:
            url {[type]} -- 下载的url
            page_type {[type]} -- 分为artist和song（推荐）
        '''
        # artist_name = url.split('/')[3]
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        if page_type == 'song':
            music_down = self.driver.find_element_by_class_name("action_down")
            music_down.click()
            self.driver.current_window_handle
            music_btn = self.driver.find_element_by_class_name("btn")
            music_btn.click()
        else:
            music_downs = self.driver.find_elements_by_class_name("action_down")
            # music_downs = self.driver.find_elements_by_xpath("/html/body/div[3]/div[2]/div[3]/ul/li/div[2]/a[2]")
            # selenium不支持重命名，需要右键另存为需要依赖其他插件
            # music_names = self.driver.find_elements_by_xpath("/html/body/div[3]/div[2]/div[3]/ul/li/div[1]/a")
            # for music_name, music_down in zip(music_names, music_downs):
                # music_name = music_name.text
            for music_down in music_downs:
                self.driver.implicitly_wait(5)
                music_down.click()
                self.driver.current_window_handle
                music_btn = self.driver.find_element_by_class_name("btn")
                music_btn.click()
                # music_href = music_btn.get_attribute('href')

            page_end = self.driver.find_element_by_class_name("page_next1")
            if page_end:
                return None
            else:
                # 音乐人空间的下一页
                page_next = self.driver.find_element_by_class_name("page_next")
                # 新页面的下一页
                # noFlush_load_link = self.driver.find_elements_by_class_name("noFlush_load_link")
                # noFlush_load_link[-2].click()
                if page_next:
                    self.driver.implicitly_wait(5)
                    page_href = page_next.get_attribute("href")
                    page_next.click()
                    self.driver.implicitly_wait(10)
                    self.driver.current_window_handle
                    new_href = BASE_URL + page_href
                    # self.driver.get(new_href)
                    self.get_download(new_href)
            

        


if __name__ == '__main__':
    down_dir = 'd:\\'
    five_sing = FiveSingCrawl2(down_dir)
    five_sing.login()
    # url = BASE_URL + '/%s/%s/%s.html' % (artist_id_or_name, song_type, page)
    # 歌手
    # url = 'http://5sing.kugou.com/marblue/yc/1.html'
    # five_sing.get_download(url, page_type='artist')
    # 歌曲
    song_url = 'http://5sing.kugou.com/fc/16004239.html'
    five_sing.get_download(song_url, page_type='song')
    five_sing.close_tab()
    five_sing.tearDown()



