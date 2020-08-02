# -*-coding:utf-8-*-
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time
import os
import sys
import json
from multiprocessing import Process, freeze_support
from androidDevice import androidDevice


class androidXXQG(androidDevice):
    # 按钮配置
    def config_device(self):
        config_filename = '.\\{}.json'.format(self.device)
        if not os.path.exists(config_filename):
            config = {'学习page':{'学习but':None, '推荐but':None, '要闻but':None, '浙江but':None, '播放新闻but':None},
                      '播放新闻page':{'新闻返回but':None},
                      '电视台page':{'电视台but':None, '学习视频but':None, '联播频道but':None},
                      '学习视频page':{'学习新视界but':None, '奋斗新时代but':None, '强军之路but':None, '绿水青山but':None,'播放短视频but':None},
                      '播放短视频page':{'继续播放but':None,'拖到末尾but':None,'视频返回but':None},
                      '联播频道page':{'播放联播but':None},
                      '播放联播page':{'继续播放but':None, '视频返回but':None}
                      }
            def onClickWrapper(event):
                androidDevice.onClick(event, config, page)
            for page in config.keys():
                input("请手机调整至：{}".format(page))
                self.pull_screenshot()  # 截屏
                fig = plt.figure(self.device)
                ax = plt.subplot()
                plt.title(self.device)
                ax.imshow(np.array(Image.open('autojump-{0}.png'.format(self.device))))  # im = 绘制图像（数组名、动画=打开）
                fig.canvas.mpl_connect('button_press_event', onClickWrapper)
                buttons = list(config[page].keys())
                print('请电脑依次点击：{}'.format(str(buttons)))
                #plt.ion()
                plt.show()
            with open(config_filename, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False)

        with open(config_filename, encoding="utf-8") as f:
            config = json.load(f)
        return config

    # xxqg自动
    def play_device(self):
        # 看文章
        print('新闻开始')
        sys.stdout.flush()
        loc = self.config['学习page']['学习but']
        self.tap(loc[0], loc[1])
        time.sleep(1)
        print('6篇轮播文章')
        loc = self.config['学习page']['推荐but']
        self.tap(loc[0], loc[1])
        time.sleep(1)
        for i in range(6):
            loc = self.config['学习page']['播放新闻but']
            self.tap(loc[0], loc[1])
            time.sleep(1)
            # 拖到底部
            for j in range(20):
                self.swipe([540,1500], [540,408])
                # time.sleep(1)
            # 停留1分钟
            time.sleep(40)
            loc = self.config['播放新闻page']['新闻返回but']
            self.tap(loc[0], loc[1])
            time.sleep(1)

        print('6篇要闻')
        loc = self.config['学习page']['要闻but']
        self.tap(loc[0], loc[1])
        time.sleep(1)
        for i in range(6):
            loc = self.config['学习page']['播放新闻but']
            self.tap(loc[0], loc[1])
            time.sleep(1)
            for j in range(20):
                self.swipe([540,1500], [540,408])
                # time.sleep(1)
            # 停留1分钟
            time.sleep(40)
            loc = self.config['播放新闻page']['新闻返回but']
            self.tap(loc[0], loc[1])
            time.sleep(1)
            self.swipe([540, 1500], [540, 1100])
            time.sleep(1)
        # print('6篇浙江')
        # loc = self.config['学习page']['浙江but']
        # self.tap(loc[0], loc[1])
        # time.sleep(1)
        # for i in range(6):
        #     self.swipe([540, 1500], [540, 1100])
        #     time.sleep(1)
        #     loc = self.config['学习page']['播放新闻but']
        #     self.tap(loc[0], loc[1])
        #     time.sleep(1)
        #     for j in range(20):
        #         self.swipe([540, 1500], [540, 408])
        #         # time.sleep(1)
        #     # 停留1分钟
        #     time.sleep(40)
        #     loc = self.config['播放新闻page']['新闻返回but']
        #     self.tap(loc[0], loc[1])
        #     time.sleep(1)
        # 短视频
        print('短视频开始')
        sys.stdout.flush()
        loc = self.config['电视台page']['电视台but']
        self.tap(loc[0], loc[1])
        time.sleep(1)
        loc = self.config['电视台page']['学习视频but']
        self.tap(loc[0], loc[1])
        time.sleep(1)
        self.swipe([540, 408], [540, 1500])
        time.sleep(1)
        for name in ['学习新视界but', '奋斗新时代but', '强军之路but', '绿水青山but']:
            loc = self.config['学习视频page'][name]
            self.tap(loc[0], loc[1])
            time.sleep(1)
            # 每个专题看2个视频
            for i in range(2):
                loc = self.config['学习视频page']['播放短视频but']
                self.tap(loc[0], loc[1])
                time.sleep(2)
                loc = self.config['播放短视频page']['继续播放but']
                self.tap(loc[0], loc[1])
                # time.sleep(1)
                loc = self.config['播放短视频page']['拖到末尾but']
                self.tap(loc[0], loc[1])
                # 播放至结束
                time.sleep(15)
                loc = self.config['播放短视频page']['视频返回but']
                self.tap(loc[0], loc[1])
                time.sleep(1)
                self.swipe([540, 1500], [540, 1100])
            self.swipe([540, 408], [540, 1500])
            time.sleep(1)
        # 联播
        print('联播开始')
        sys.stdout.flush()
        loc = self.config['电视台page']['联播频道but']
        self.tap(loc[0], loc[1])
        time.sleep(1)
        loc = self.config['联播频道page']['播放联播but']
        self.tap(loc[0], loc[1])
        time.sleep(1)
        loc = self.config['播放联播page']['继续播放but']
        self.tap(loc[0], loc[1])
        # 播放18分钟
        time.sleep(1080)
        loc = self.config['播放联播page']['继续播放but']
        loc = self.config['播放联播page']['视频返回but']
        self.tap(loc[0], loc[1])
        time.sleep(1)
        print('联播结束')
        sys.stdout.flush()


if __name__ == '__main__':
    def run(device=None):
        phone = androidXXQG(device)
        phone.play_device()
    # 单进程
    # device_list = androidDevice.conn_device()
    # run(device_list[0])

    # 多进程
    freeze_support()
    device_list = androidDevice.conn_device()
    process_pool = []
    for device in device_list:
        process = Process(target=run, args=(device, ))
        process_pool.append(process)
        process.start()
    for process in process_pool:
        process.join()
