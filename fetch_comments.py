#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File: fetch_comments.py
@Time: 2024/08/23 21:01:09
@Author: lvlh2
"""


import json
import os
import re
import time

import pandas as pd
import requests

HEADERS = {
    'cookie': "Your Cookie",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
}


class CookieError(Exception):

    def __init__(self, message: str) -> None:
        super().__init__(message)


def fetch_comments(comment_url: str) -> list[dict[str, list[str]]]:
    """Fetches the comments from the comment URL.

    Args:
        comment_url (str): The URL of the comment page.

    Returns:
        list: A list of dictionaries containing the comments.
    """
    response = requests.get(comment_url, headers=HEADERS)
    data = response.json()
    comments = [
        {
            (
                data['data']['replies'][i]['member']['uname'],
                data['data']['replies'][i]['member']['sex'],
                data['data']['replies'][i]['content']['message'],
                data['data']['replies'][i]['like'],
            ): [
                data['data']['replies'][i]['replies'][j]['content']['message']
                for j in range(len(data['data']['replies'][i]['replies']))
            ]
        }
        for i in range(len(data['data']['replies']))
    ]
    return comments


def main():
    path = os.path.dirname(__file__)
    os.chdir(path)

    with open('network.har', 'r') as f:
        har = json.load(f)

    pat = re.compile(r'https://api.bilibili.com/x/v2/reply/wbi/main')
    comment_urls = [
        har['log']['entries'][i]['request']['url']
        for i in range(len(har['log']['entries']))
        if pat.search(har['log']['entries'][i]['request']['url'])
    ]

    total_comments = []
    for i, url in enumerate(comment_urls, start=1):
        try:
            total_comments.extend(fetch_comments(url))
            print(f'Progress: {i}/{len(comment_urls)}', end='\r')
            time.sleep(0.1)
        except:
            raise CookieError('Cookie is invalid or expired, please reconfigure it.')

    total_comments = pd.concat(map(pd.Series, total_comments), axis=0)
    total_comments.explode().rename_axis(
        ['User Name', 'Sex', 'Comments', 'Likes']
    ).rename('Replies').to_csv('comments.csv')


if __name__ == '__main__':
    main()
