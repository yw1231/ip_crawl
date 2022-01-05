import asyncio
import httpx
from fake_useragent import UserAgent
from lxml import etree
import logging
import time
import random
from mongo_service import MongoService
import re


class CrawlKaixin:
    def __init__(self):
        self.headers = {'User-Agent': UserAgent(verify_ssl=False).random}
        # ip校验url
        self.check_url: str = 'http://www.whatismyip.com.tw'

    def refresh_headers(self):
        """
        刷新请求头
        """
        self.headers = {'User-Agent': UserAgent(verify_ssl=False).random}

    async def test_proxy(self, proxy):
        """
        测试代理IP是否可用
        """
        proxies = {
            'http://': 'http://{}'.format(proxy),
            'https://': 'https://{}'.format(proxy),
        }
        try:
            async with httpx.AsyncClient(proxies=proxies) as client:
                res = await client.get(url=self.check_url, headers=self.headers, timeout=3)
                # res = await client.get(url=self.check_url, timeout=3)
                if res.status_code == 200:
                    return True
                else:
                    return False
        except:
            return False

    async def crawl(self):
        logging.info('开心代理 开始获取代理ip。。。')
        async with httpx.AsyncClient() as client:
            while True:
                try:
                    page = random.randint(1, 11)
                    url = f'http://www.kxdaili.com/dailiip/1/{page}.html'
                    res = await client.get(url)
                    res.encoding = 'utf8'
                    obj = etree.HTML(res.text)
                    items = obj.xpath('//table[@class="active"]/tbody/tr')
                    for item in items:
                        # ip地址
                        ip = item.xpath('td[1]/text()')[0].strip()
                        # 端口
                        port = item.xpath('td[2]/text()')[0].strip()
                        # 匿名度
                        anonymity = item.xpath('td[3]/text()')[0].strip()[:2]
                        # 类型
                        ip_type = item.xpath('td[4]/text()')[0].strip()
                        # 位置
                        location = item.xpath('td[6]/text()')[0].strip()
                        try:
                            location = location[:re.search(r"市", location).end()]
                        except:
                            pass
                        proxy = f'{ip}:{port}'
                        is_useful = await self.test_proxy(proxy)
                        if is_useful:
                            logging.info(f'数据源:开心代理 成功获取一条ip')
                            now_time = int(time.time())
                            data = {'ip': proxy, 'anonymity': anonymity, 'ip_type': ip_type, 'location': location,
                                    'market': '开心代理', 'get_time': now_time, 'last_check': now_time, 'live_time': 0}
                            MongoService.update_one({'ip': proxy}, {'$set': data})
                except:
                    await asyncio.sleep(1)

    async def main(self):
        start = time.time()
        await self.crawl()
        end = time.time()
        logging.info(f'耗时{end-start}s')


if __name__ == '__main__':
    crawl_kaixin = CrawlKaixin()
    asyncio.run(crawl_kaixin.main())