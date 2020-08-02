# -*-coding:utf-8-*-
import matplotlib.pyplot as plt
import os
import subprocess
import re
import sys
import wmi
import hashlib
import shutil
from abc import abstractmethod


class androidDevice():
    def __init__(self, device=None):
        """
        :param phone:adb 操作手机所需要的端口信息
        """
        self.device = device
        if self.device is None:
            self.device = androidDevice.conn_device()[0]
        self.config = self.config_device()

    # 截屏上传
    def pull_screenshot(self):
        os.system('adb -s {0} shell screencap -p /sdcard/autojump.png'.format(self.device))  # 发送 截屏命令 到手机
        os.system('adb -s {0} pull /sdcard/autojump.png ./autojump-{1}.png'.format(self.device, self.device))  # 发送 拉取图片到电脑 命令

    # 点击
    def tap(self, x, y):
        cmd = r'adb -s {0} shell input tap {1} {2}'.format(self.device, x, y)
        pi = os.popen(cmd)
        res = pi.read()
        # print(res)

    # 滑动
    def swipe(self, start, end):
        cmd = r'adb -s {0} shell input swipe {1} {2} {3} {4}'.format(self.device, int(start[0]), int(start[1]), int(end[0]),
                                                                     int(end[1]))
        pi = os.popen(cmd)
        res = pi.read()
        # print(res)

    # pyplot事件响应
    @staticmethod
    def onClick(event, config, page):  # 定义 鼠标点击 处理函数
        ix, iy = event.xdata, event.ydata
        now = (ix, iy)
        print('now click:', now)
        sys.stdout.flush()

        for key, value in config[page].items():
            if value is None:
                print('刚才点的是:', key)
                config[page][key] = now
                break

        if None not in config[page].values():
            plt.close()  # 关闭传入的 figure 对象

    # 算号
    @staticmethod
    def get_disk_Serial():
        c = wmi.WMI()
        disks = []
        for disk in c.Win32_DiskDrive():
            disks.append(disk.SerialNumber.strip())
        return disks

    # 连接设备
    @staticmethod
    def conn_device():
        serial = input("input 本机注册码:").strip()
        disks=androidDevice.get_disk_Serial()
        flag=0
        for disk in disks:
            h1=hashlib.md5()
            h1.update(bytes(disk+'migu',encoding='utf-8'))
            if h1.hexdigest()[0:16]== serial:
                flag=1
                break
        # if flag==0:
        #     sys.exit("\n\n注册码错误！")

        adb_path = 'C:\\Windows\\'
        adb_files = ['adb.exe', 'AdbWinApi.dll', 'AdbWinUsbApi.dll']
        for file in adb_files:
            if not os.path.exists(adb_path + file):
                shutil.copyfile('.\\adb\\' + file, adb_path + file)

        cmd = r'adb devices'
        pi = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        res = str(pi.stdout.read(), encoding='utf-8')
        # pi = os.popen(cmd)
        # res = pi.read()
        print(res)
        device_list = re.findall(r'^[A-Z0-9]+\b', res, re.M)
        return device_list

    @staticmethod
    def conn_device():
        adb_path = 'C:\\Windows\\'
        adb_files = ['adb.exe', 'AdbWinApi.dll', 'AdbWinUsbApi.dll']
        for file in adb_files:
            if not os.path.exists(adb_path + file):
                shutil.copyfile('.\\adb\\' + file, adb_path + file)

        cmd = r'adb devices'
        pi = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        res = str(pi.stdout.read(), encoding='utf-8')
        print(res)
        device_list = re.findall(r'^[A-Z0-9]+\b', res, re.M)
        return device_list

    # 按钮配置
    @abstractmethod
    def config_device(self):
        pass

    # xxqg自动
    @abstractmethod
    def play_device(self):
        pass