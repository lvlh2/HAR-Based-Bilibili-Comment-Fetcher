#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File: extract_har_file.py
@Time: 2024/08/23 18:42:26
@Author: lvlh2
"""


import json
import os
import time

from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def main():
    path = os.path.dirname(__file__)
    os.chdir(path)

    server = Server('E:/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat')
    server.start()
    proxy = server.create_proxy()

    options = Options()
    options.add_argument(f'--proxy-server={proxy.proxy}')
    options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Chrome(options=options)

    proxy.new_har('network', options={'captureContent': True})

    url = input('Please input the link of the video: ')
    driver.get(url)

    input()

    temp_height = 0
    while True:
        driver.execute_script('window.scrollBy(0,1000)')
        time.sleep(1)
        check_height = driver.execute_script(
            'return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;'
        )
        if check_height == temp_height:
            break
        temp_height = check_height

    time.sleep(5)

    har = proxy.har

    server.stop()
    driver.quit()

    with open('network.har', 'w', encoding='utf-8') as f:
        json.dump(har, f)


if __name__ == '__main__':
    main()
