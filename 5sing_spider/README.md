# 5sing_spider

没使用抓包工具，使用F12不能在5sing页面本身找到XHR数据，但是找到一个解析网站的API，可以通过输入歌曲id和song_type，重定向后的url直接获得MP3的下载链接。

song_type:

    1. yc - 原唱
  
    2. fc - 翻唱
  
    3. bz - 伴奏

格式：http://music.nb-fk.com/music.php?5sing={song_type}/{song_id}

eg:http://music.nb-fk.com/music.php?5sing=yc/3423557

这个API只能获取单首歌，我写的代码也只针对于5sing的音乐空间和音乐人空间的两个用的比较多的模板，从歌手页抓取所有歌曲的链接，然后使用urllib.urlretrieve进行下载
