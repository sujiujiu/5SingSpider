class FiveSingCrawl(BaseSeleniumClass):

    def login(self, username=None, pwd=None, is_third=True, 
                    third_part='QQ', third_usname=None, third_pwd=None):
        '''默认为第三方登录，分为QQ/weibo/kugou,则不需要输入账户密码
        友情提示：属性的名称不能有空格
        
        [description]
        
        Keyword Arguments:
            username {[type]} -- 用户名（通行证/邮箱/手机号码） (default: {None})
            pwd {[type]} -- 密码 (default: {None})
            is_third {bool} -- 是否为第三方登录 (default: {True})
            third_part {[type]} -- 第三方登录默认选择QQ (default: 'QQ')
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
                    third_name = self.driver.find_element_by_id("u")
                    third_pwd = self.driver.find_element_by_id("p")
                    third_name.send_keys(third_usname)
                    self.driver.implicitly_wait(5)
                    third_pwd.send_keys(third_pwd)
                    self.driver.implicitly_wait(5)
                    # 点击登录
                    self.driver.find_element_by_id("login_button").click()
                    self.driver.current_window_handle
                else:
                    # 头像登录
                    img_out_focus = self.driver.find_element_by_class_name("img_out_focus")
                    if img_out_focus：
                        img_out_focus.click()
                        self.driver.current_window_handle


            elif third_part == 'weibo':
                self.driver.find_element_by_class_name("weibo").click()
                self.driver.implicitly_wait(10)
                # 切换页面
                self.driver.current_window_handle
                third_name = self.driver.find_element_by_id("userId")
                third_pwd = self.driver.find_element_by_id("passwd")
                third_name.send_keys(third_usname)
                self.driver.implicitly_wait(5)
                third_pwd.send_keys(third_pwd)
                self.driver.implicitly_wait(5)
                # 点击登录
                self.driver.find_element_by_class_name("btnP").click()
                self.driver.current_window_handle
            else:
                self.driver.find_element_by_class_name("kugou").click()
        else:
            # 使用账号密码登录
            # 获取账户和密码的输入框
            us_name = self.driver.find_element_by_class_name("us_name")
            us_pwd = self.driver.find_element_by_class_name("us_pwd")
            # us_name = self.driver.find_element_by_id("txtUserName")
            # us_pwd = self.driver.find_element_by_id("txtPassword")
            # 将账户和密码分别输入两个框，每次操作间隔5秒
            us_name.send_keys(username)
            self.driver.implicitly_wait(5)
            us_pwd.send_keys(pwd)
            self.driver.implicitly_wait(5)
            # 勾选记住我
            self.driver.find_element_by_class_name("IsSave").click()
            # 点击登录
            self.driver.find_element_by_class_name("lo_bnt").click()
            self.driver.current_window_handle


    def get_download(self, url):
        artist_name = url.split('/')[3]
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        action_downs = self.driver.find_elements_by_class_name("action_down")
        for action_down in action_downs:
            self.driver.implicitly_wait(5)
            action_down.click()
            self.driver.current_window_handle
            music_btn = self.driver.find_element_by_class_name("btn")
            music_btn.click()
            music_href = music_btn.get_attribute('href')
            with open()

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