# -*- coding: utf-8 -*-
"""
* @Author: ziuno
* @Software: PyCharm
* @Time: 2018/10/17 21:25
"""

import abc
import os
from time import sleep
from random import randint
import openpyxl
import requests
import xlrd


class Music(object):

    def __del__(self):
        self._data.clear()
        self._music_name = None

    def __init__(self):
        self._music_name = None
        self._data = []

    @abc.abstractmethod
    def search(self):
        pass

    @property
    def music_name(self):
        return self._music_name

    @music_name.setter
    def music_name(self, name):
        self._music_name = name

    def save_source(self):
        if len(self._data) == 0:
            raise NotImplementedError('暂无数据')
        else:
            print('Saving source...')
            wb = openpyxl.load_workbook('data\\source.xlsx')
            ws = wb['music']
            for row_index in range(len(self._data)):
                ws.append(self._data[row_index])
            wb.save('data\\source.xlsx')
            wb.close()
            print('Source saved.')

    @staticmethod
    def __handle_name(name):
        name = list(name)
        illegal_characters = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
        for index in range(len(name)):
            if name[index] in illegal_characters:
                name[index] = '_'
        return ''.join(name)

    @staticmethod
    def download_all(path='data\\source.xlsx'):
        print('Begin to download...')
        wb = xlrd.open_workbook(path)
        ws = wb.sheet_by_name('music')
        sleep_count = randint(5, 10)
        for row_index in range(1, ws.nrows):
            row = ws.row(row_index)
            name = '%s-%s' % (row[0].value, row[1].value)
            name = Music.__handle_name(name)
            url = row[2].value
            if os.path.exists('Downloads\\%s.m4a' % name):
                print('%s.m4a already exists.' % name)
                continue
            print('Downloading %s...' % name, end='')
            while True:
                try:
                    music = requests.get(url, timeout=10)
                    print("successful")
                    break
                except:
                    print('failed, please wait a minute...')
                    sleep(randint(30, 50))
                    print('Downloading %s again...' % name, end='')
            file = open('Downloads\\%s.m4a' % name, 'wb')
            file.write(music.content)
            sleep(randint(1, 3))
            file.close()
            sleep_count -= 1
            if sleep_count == 0:
                sleep_time = randint(10, 50)
                print('Sleep %d seconds...' % sleep_time)
                sleep(sleep_time)
                print('Begin to download again...')
                sleep_count = randint(5, 10)
        print('Download complete')
