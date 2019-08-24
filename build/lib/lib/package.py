#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
import re
import lib.Utils as U
import platform

# 判断系统类型，windows使用findstr，linux使用grep
system = platform.system()
if system is "Windows":
    find_util = "findstr"
else:
    find_util = "grep"

class Package:
    def __init__(self, apk_path):
        self.apk_path = apk_path
        self.name = ""
        self.launchactivity = ""
        self.version_code = ""

    def get_package(self):
        # 判断是否有apk，如果没有则说明下载异常返回false
        if self.apk_path.endswith("apk") and os.path.exists(self.apk_path):
            if self.__set_pkg_info():
                return True
            else:
                return False
        else:
            return False


    def __set_pkg_info(self):
        # 获取文件名
        self.apk_name = os.path.basename(self.apk_path)

        # 获取包名
        cmd = "aapt dump badging '{}' | %s package".format(self.apk_path, find_util)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1,
                         close_fds=True)
        stdout, stderr = process.communicate()
        stdout, stderr = str(stdout, encoding='utf-8'), str(stderr, encoding='utf-8')
        if stdout is None:
            U.Logging.error("[pkg_info] time out: {}".format(cmd))
        elif "ERROR" in stderr:
            U.Logging.error("[pkg_info] cannot execute: {}".format(cmd))
            U.Logging.error("[pkg_info] result: {}".format(stderr))
        else:
            try:
                package_name = re.findall(r"name='([a-zA-Z0-9.*]+)'", stdout)
                self.name = package_name[0]
                self.version_code = re.findall(r"versionCode='([0-9]+)'", stdout)[0]
            except Exception as e:
                U.Logging.error("[pkg_info] failed to regex package name from {}. {}".format(stdout, e))
        # 获取启动Activity
        cmd = "aapt dump badging '{}' | %s launchable-activity".format(self.apk_path,find_util)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1,
                                   close_fds=True)
        stdout, stderr = process.communicate()
        stdout, stderr = str(stdout, encoding='utf-8'), str(stderr, encoding='utf-8')
        if stdout is None:
            U.Logging.error("[pkg_info] time out: {}".format(cmd))
        elif "ERROR" in stderr:
            U.Logging.error("[pkg_info] cannot execute: {}".format(cmd))
            U.Logging.error("[pkg_info] result: {}".format(stderr))
        else:
            try:
                activity_list = re.findall(r"name='(.+?)'", stdout)
                main_activity = ""
                for activity in activity_list:
                    if not activity.startswith("com.squareup") and not activity.startswith("com.github"):
                        main_activity = activity
                        break
                self.activity = main_activity
            except Exception as e:
                U.Logging.error("[pkg_info] failed to regex main activity from {}. {}".format(stdout, e))

        if self.name and self.activity:
            return True

        return False





