# -*- coding: utf-8 -*-
"""
* @Author: ziuno
* @Software: PyCharm
* @Time: 2018/10/17 8:48
"""
from engines.Music import Music
from engines.QQMusic import QQMusic

Music.clear_history()
music = QQMusic()
music.music_name = input('音乐名：')
music.singer_name = input('歌手名（可选）：')
music.search()
music.save_source()
music_list = music.music_list
print(music_list)
for name in music_list:
    download_it = input("下载%s？（回车下载）" % name)
    if download_it == '':
        Music.download(name)

del music
# Music.download_all()
