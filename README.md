# HAR-Based-Bilibili-Comment-Fetcher

使用基于HAR文件提取与解析的方法，获取B站评论接口链接，并爬取评论数据

## 使用方法

- 确保已安装并配置好chromedriver和browsermob-proxy
- 在脚本`extract_har_file.py`中的第23行：`server = Server('E:/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat')`的`Server`中输入自己browsermob-proxy的安装路径
- 运行该脚本后，在**脚本所在目录**会保存`network.har`文件
- 然后在`fetch_comments.py`开头的`HEADERS`变量中配置Cookie
- 运行`fetch_comments.py`（确保`fetch_comments.py`和`network.har`位于同一目录下），爬取评论信息
- 运行完毕后，该目录下会保存`comments.csv`文件
