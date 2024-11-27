# HAR Based Bilibili Comment Downloader

使用基于HAR文件提取与解析的方法，提取B站评论数据

## 使用方法

- 确保已安装并配置好chrome浏览器、chromedriver和browsermob-proxy
- 在脚本`download_bilibili_comments.py`中的第21行：`BROWSERMOB_PATH = 'E:/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat'`输入自己browsermob-proxy的安装路径
- 运行该脚本，控制台会提示：“Please input the link of the video: ”。输入视频链接后，在程序调用的chrome浏览器页面中登陆B站账号
- 运行完毕后，该目录下会保存`comments.csv`文件

使用到的Python非标准库包括：

- `pandas`
- `browsermobproxy`
- `selenium`
