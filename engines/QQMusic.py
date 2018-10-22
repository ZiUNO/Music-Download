# -*- coding: utf-8 -*-
"""
* @Author: ziuno
* @Software: PyCharm
* @Time: 2018/10/17 21:22
"""
import re
from random import randint
from time import sleep

import requests

from engines.Music import Music


class QQMusic(Music):

    def __init__(self):
        super().__init__()

    def search(self):
        if self._music_name is None:
            raise RuntimeError('未设定音乐名')
        else:
            encode_name = str(self._music_name.encode(encoding='utf-8')).upper()[1:]
            music_name_encoded = str('%'.join(encode_name.split('\\X')))[1:-1]
            print('Searching...')
            url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace' \
                  '=txt.yqq.song&searchid=62681517279281672&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20' \
                  '&w=%s&g_tk=5381&jsonpCallback=MusicJsonCallback24009799704592139&loginUin=0&hostUin=0&format=jsonp' \
                  '&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0' % music_name_encoded
            page = requests.get(url).text
            media_ids = re.findall('media_mid":"(.*?)","size_128"', page, re.S)
            albummids = []
            sleep_time = randint(3, 20)
            print('Sleep %s second(s)...' % sleep_time)
            sleep(sleep_time)
            print('Getting albummids...')
            for media_id in media_ids:
                url = 'https://y.qq.com/n/yqq/song/%s.html' % media_id
                page = requests.get(url).text
                albummid = re.findall('<a href="//y.qq.com/n/yqq/album/(.*?).html" itemprop="inAlbum"', page, re.S)
                if len(albummid) == 0:
                    continue
                else:
                    albummids.append(albummid[0])
                    sleep(randint(1, 3))
            sleep_time = randint(3, 20)
            print('Sleep %s second(s)...' % sleep_time)
            sleep(sleep_time)
            print('Getting songmid')
            for albummid in albummids:
                url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_album_info_cp.fcg?albummid=%s&g_tk=5381&jsonpCallback' \
                      '=albuminfoCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0' \
                      '&platform=yqq&needNewCode=0' % albummid
                page = requests.get(url).text
                songmids = re.findall('"songmid":"(.*?)",', page, re.S)
                names = re.findall('"songname":"(.*?)",', page, re.S)
                singer_name = re.findall('"singername":"(.*?)",', page, re.S)[0]
                print('Getting purl of %s' % albummid)
                for songmid_index in range(len(songmids)):
                    if str(self._music_name).lower() not in str(names[songmid_index]).lower():
                        continue
                    url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?callback=getplaysongvkey7337371457506539&g_tk=5381' \
                          '&jsonpCallback=getplaysongvkey7337371457506539&loginUin=0&hostUin=0&format=jsonp&inCharset' \
                          '=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data=%7B%22req%22%3A%7B' \
                          '%22module%22%3A%22CDN.SrfCdnDispatchServer%22%2C%22method%22%3A%22GetCdnDispatch%22%2C' \
                          '%22param%22%3A%7B%22guid%22%3A%222998688000%22%2C%22calltype%22%3A0%2C%22userip%22%3A%22' \
                          '%22%7D%7D%2C%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A' \
                          '%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%222998688000%22%2C%22songmid%22%3A%5B%22' \
                          '' + \
                          songmids[
                              songmid_index] + '%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%220%22%2C' \
                                               '%22loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A' \
                                               '%7B%22uin%22%3A0%2C%22format%22%3A%22json%22%2C%22ct%22%3A20%2C%22cv' \
                                               '%22%3A0%7D%7D '
                    page = requests.get(url).text
                    purl = re.findall('"purl":"(.*?)"', page, re.S)[0]
                    if len(purl) == 0:
                        continue
                    url = 'http://isure.stream.qqmusic.qq.com/' + purl
                    print('Get link of (%s, %s, %s)' % (names[songmid_index], singer_name, url))
                    self._data.append([names[songmid_index], singer_name, url])
                    sleep(randint(1, 3))
            print('Searching completed.')
