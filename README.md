## 前言

​		这是本人结合网络上的教程做的爬取免费代理IP的小工具，水平有限写的比较随意莫怪。

​		分别爬取了开心代理，快代理，89ip三个网站的免费代理IP。由于每个网站更新免费代理的速度并不快，也为了避免给这些网站造成压力，该程序对每个网站的爬取是同步的，但是三个任务之间是异步进行的，爬取到的IP会存入Mongodb数据库。同时会有一个任务会实时去数据库校验库里的ip是否依然存活，并记录存活时间。

​		使用者只需要将自己的mongodb配置写入mongo_conf.json文件即可使用该程序

## 环境

python3.7及以上

## 使用方法

1. 安装相关依赖 

   > pip install -r requirements.txt

2. 将自己的mongodb配置写入mongo_conf.json文件

3. 运行

   > python main.py