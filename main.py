import asyncio
import logging
from spiders.crawl_89ip import Crawl89IP
from spiders.crawl_kuaidaili import CrawlKuai
from spiders.crawl_kaixin import CrawlKaixin
from ip_check import IpCheck

logging.basicConfig(format='%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)

tasks = []
crawl_89ip = Crawl89IP()
crawl_kuai = CrawlKuai()
crawl_kaixin = CrawlKaixin()
ip_check = IpCheck()
task1 = crawl_89ip.main()
task2 = crawl_kuai.main()
task3 = crawl_kaixin.main()
task_check = ip_check.main()
tasks.append(task1)
tasks.append(task2)
tasks.append(task3)
tasks.append(task_check)


async def run():
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(run())
