#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File: download_bilibili_comments.py
@Time: 2024/11/27 09:25:24
@Author: lvlh2
"""


import json
import os
import re
import time
from pathlib import Path

import pandas as pd
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BROWSERMOB_PATH = 'E:/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat'


def download_har_file() -> None:
    """Downloads the har file."""
    server = Server(BROWSERMOB_PATH)
    server.start()
    proxy = server.create_proxy()

    options = Options()
    options.add_argument(f'--proxy-server={proxy.proxy}')
    options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Chrome(options=options)

    proxy.new_har('network', options={'captureContent': True})

    # url = 'https://www.bilibili.com/video/BV18M4m1y7Zy/'
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


def extract_comments() -> pd.Series:
    """Extracts the comments from the har file.

    Returns:
        pd.Series: The comments.
    """
    with open('network.har', 'r', encoding='utf-8') as f:
        har = json.load(f)

    pat = re.compile(r'https://api.bilibili.com/x/v2/reply/wbi/main')

    comments_all = []
    for entry in har['log']['entries']:
        if pat.search(entry['request']['url']):
            data = json.loads(entry['response']['content']['text'])['data']

            comments = [
                {
                    (
                        reply['member']['uname'],
                        reply['member']['sex'],
                        reply['content']['message'],
                        reply['like'],
                    ): [
                        sub_reply['content']['message']
                        for sub_reply in reply['replies']
                    ]
                }
                for reply in data['replies']
            ]
            comments_all.extend(comments)

    comments_all = (
        pd.concat(map(pd.Series, comments_all), axis=0)
        .explode()
        .rename_axis(['User Name', 'Sex', 'Comments', 'Likes'])
        .rename('Replies')
    )
    return comments_all


def main():
    path = Path(__file__).parent
    os.chdir(path)

    download_har_file()

    comments = extract_comments()
    comments.to_csv('comments.csv')


if __name__ == '__main__':
    main()
