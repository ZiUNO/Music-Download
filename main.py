# -*- coding: utf-8 -*-
"""
* @Author: ziuno
* @Software: PyCharm
* @Time: 2018/10/17 8:48
"""
from engines.QQMusic import QQMusic

music = QQMusic()
music.name = input('音乐名：')
music.search()
music.save_source()
del music
# Music.download_all()
