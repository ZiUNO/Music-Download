# -*- coding: utf-8 -*-
"""
* @Author: ziuno
* @Software: PyCharm
* @Time: 2018/10/17 8:48
"""
import os

from engines.Music import Music
from engines.QQMusic import QQMusic


def search_menu():
    global music
    music.music_name = ''
    while len(music.music_name) == 0:
        os.system("cls")
        print('请正确输入音乐名及歌手名（可省略）')
        print("Download one")
        print('（输入Q回车退出）')
        music.music_name = input('音乐名:')
        if music.music_name == 'Q':
            os.system("cls")
            return
    music.singer_name = input('歌手名（可省略）:')
    music.search()
    music.save_source()
    print('搜索完成')
    os.system("pause")
    os.system("cls")
    download_menu()


def download_menu():
    has_download = []
    while True:
        print("Download one")
        print("音乐列表:")
        music_list = music.music_list
        print('No.0  :（下载全部）')
        for music_name_index in range(len(music_list)):
            print('No.%-3d:%s' % (music_name_index + 1, music_list[music_name_index]))
        print('已下载:', ' '.join(has_download))
        print('（回车默认退出）')
        choice = input('请输入下载音乐标号(a [to b]):')
        if len(choice) == 0:
            os.system("cls")
            break
        choice = choice.split(' ')
        os.system("cls")
        if len(choice) == 1:
            if choice[0].isdigit():
                index = int(choice[0])
                if index < -1 or index > len(music_list) + 1:
                    print('范围错误，请重新输入')
                    continue
                elif index == 0:
                    for index in range(len(music_list)):
                        Music.download(music_list[index])
                        has_download.append(music_list[index])
                    os.system("pause")
                    os.system("cls")
                    break
                else:
                    Music.download(music_list[index - 1])
                    has_download.append(music_list[index - 1])
        elif len(choice) == 3:
            if choice[1] != 'to' or not (choice[0].isdigit() and choice[2].isdigit()):
                print('语法错误，请重新输入')
                continue
            start = int(choice[0])
            end = int(choice[2])
            if start == 0:
                for index in range(len(music_list)):
                    Music.download(music_list[index])
                    has_download.append(music_list[index])
                print('已全部下载')
                os.system("pause")
                os.system("cls")
                break
            elif start < -1 or start > len(music_list) + 1 or end < -1 or end > len(music_list) + 1 or start > end:
                print('范围错误，请重新输入')
            else:
                for index in range(start, end + 1):
                    Music.download(music_list[index - 1])
                    has_download.append(music_list[index - 1])
                print('下载成功')
        os.system("cls")


def main_menu():
    while True:
        print("Download one")
        print("1.音乐搜索")
        print("2.下载全部历史")
        print("3.清除历史")
        print("0.退出")
        choice = input()
        os.system("cls")
        if choice not in ['1', '2', '3', '0']:
            print('命令错误，请重新输入')
        elif choice == '1':
            search_menu()
        elif choice == '2':
            Music.download_all()
            os.system("cls")
            print('全部下载完毕')
        elif choice == '3':
            is_clear = Music.clear_history()
            os.system("cls")
            if is_clear:
                print('已清除搜索历史')
        else:
            break


music = QQMusic()

if __name__ == '__main__':
    main_menu()
    del music
