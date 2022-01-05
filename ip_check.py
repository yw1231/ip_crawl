import asyncio
import logging
from mongo_service import MongoService
import httpx
import time
from fake_useragent import UserAgent

class IpCheck:

    def __init__(self):
        # 每次取出5个数据
        self.limit = 5
        # ip校验url
        self.check_url: str = 'http://www.whatismyip.com.tw'
        self.headers = {'User-Agent': UserAgent(verify_ssl=False).random}
    
    async def main(self):
        while True:
            try:
                data = MongoService.query_limit(1, self.limit)
                await asyncio.gather(*[self.check(item) for item in data])
                await asyncio.sleep(2)
            except:
                await asyncio.sleep(3)
            
    async def check(self, data):
        is_useful = await self.test_proxy(data['ip'])
        if is_useful:
            now_time = int(time.time())
            data["last_check"] = now_time
            data["live_time"] = now_time-data['get_time']
            MongoService.update_one({'ip': data["ip"]}, {"$set":data})
        else:
            MongoService.del_one(data)
            logging.info(f"{data['ip']}已过期...")
    
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
                if res.status_code == 200:
                    return True
                else:
                    return False
        except:
            return False
            
            
if __name__ == '__main__':
    ip_check = IpCheck()
    asyncio.run(ip_check.main())
    
