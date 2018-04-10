# -*- coding:utf-8 -*-
import sys
import requests
from bs4 import BeautifulSoup

from config import HEADERS
from constants import BASE_URL, BASE_FILE_PATH, MUSIC_DOWN_FILE_PATH

reload(sys)
sys.setdefaultencoding('utf8')

class FiveSingSpider(object):

    def __init__(self, artist_id_or_name, song_type='yc'):
        self.artist_id_or_name = artist_id_or_name
        self.song_type = song_type
        self.page = page
        self.url = BASE_URL + '/%s/%s/%s.html' % \
                    (self.artist_id_or_name, self.song_type, 1)
        self.req = self.get_req(self.url, error_file_name='%s_error' % self.song_type)
        self.soup = BeautifulSoup(self.req.content, 'lxml')

    def get_req(self, url, error_file_name, params=None):
        while 1:
            try:
                req = requests.get(url, headers=HEADERS, params=params)
                break
            except Exception, e:
                error_file = os.path.join(BASE_FILE_PATH, error_file_name +'.txt')
                with open(error_file, 'a+') as error_f:
                    error_f.write(url+'\n')
                print url, e

        if req.status_code == 200:
            return req

    def get_song_base_info(self, song_name_item):
        down_info = {}
        song_a = song_name_item.a
        song_name = song_a.text
        song_url = song_a['href']
        song_value = song_url.split('/')
        song_type = song_value[-2] 
        song_id = song_value[-1].split('.')[0]
        down_info = {
            'song_name':song_name,
            'song_id':song_id,
            'song_type':song_type,
            'song_url':song_url,
            'artist_name':self.get_artist_name()
        }
        return down_info

    def get_artist_name(self):
        '''歌手的名字，和网址里包含的有些不一样
        '''
        artist_name = self.soup.title.text.split(u'的')[0]
        return artist_name

    def get_next_page_url(self, soup):
        '''音乐人界面的下一页的链接
        '''
        page_next = soup.find('a',{'class':'page_next'})
        if page_next:
            next_url = BASE_URL + page_next['href']
        else:
            next_url = None
        return next_url

    def get_total_page_count(self, soup):
        '''新页面的总页数
        '''
        noFlush_load_link = soup.find_all('a',{'class':'noFlush_load_link'})[-1]
        total_page_count = noFlush_load_link['href'].split('/')[-1].split('.')[0]
        return total_page_count

    def download(self, soup):
        # artist_name = self.get_artist_name()
        song_name_item = self.soup.find('div',{'class':'song_name'})
        if song_name_item:
            song_name, song_id, song_type, song_url = self.get_song_base_info(song_name_item)
            next_url = self.get_next_page_url(self.soup)
            if next_url:
                next_req = self.get_req(next_url, error_file_name='%s_error' % self.song_type)
                next_soup = BeautifulSoup(next_req.content, 'lxml') 
                self.download(next_soup)
            else:
                return 0
        else:
            pass

    def new_down(self):
        down_infos = []
        song_name_item = self.soup.find('strong',{'class':'list_name'})
        # song_name, song_id, song_type, song_url = self.get_song_info(song_name_item)
        down_info = self.get_song_base_info(song_name_item)
        page_count = self.get_total_page_count(self.soup)
        page_count = int(page_count)
        down_info.update({'page_count':page_count})
        down_infos.append(down_info)
        if page_count > 1:
            for page in xrange(2, page_count+1):
                url = BASE_URL + '/%s/%s/%s.html' % (self.artist_id_or_name, self.song_type, page)
                new_req = self.get_req(new_url, error_file_name='%s_error' % self.song_type)
                new_soup = BeautifulSoup(new_req.content, 'lxml')
                song_name_item = soup.find('strong',{'class':'list_name'})
                down_info = self.get_song_base_info(song_name_item)
                down_info.update({'page_count':page_count})
                down_infos.append(down_info)
        return down_infos

if __name__ == '__main__':

    old_spider = FiveSingSpider('marblue')
    # new_spider = FiveSingSpider('midaho')