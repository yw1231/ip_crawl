import pymongo
import json

with open('mongo_conf.json', 'r', encoding='utf8') as fp:
    mongo_conf = json.load(fp)

client = pymongo.MongoClient(
    host=mongo_conf['host'],
    port=mongo_conf['port'],
    username=mongo_conf['username'],
    password=mongo_conf['password'],
    authSource=mongo_conf['db']
)
db = client[mongo_conf['db']]
ip_pool = db.ip_pool


class MongoService:

    @classmethod
    def query_all(cls):
        '''
        查询集合中所有数据
        '''
        data = ip_pool.find({}, {'_id':0})
        return data

    @classmethod
    def query(cls, cond: dict):
        '''
        根据条件查询集合中数据
        cond:mongodb查询条件
        '''
        data = ip_pool.find(cond, {'_id':0})
        return data

    @classmethod
    def insert_one(cls, data: dict):
        ip_pool.insert_one(data)

    @classmethod
    def insert_many(cls, data: list):
        ip_pool.insert_many(data)

    @classmethod
    def update_one(cls, query_cond: dict, update_cond: dict):
        '''
        更新一个文档
        query_cond:dict  查询条件 
        update_cond:dict  更新条件
        '''
        ip_pool.update_one(query_cond, update_cond, upsert=True)

    @classmethod
    def update_many(cls, query_cond: dict, update_cond: dict):
        '''
        批量更新文档
        query_cond:dict  查询条件 
        update_cond:dict  更新条件
        '''
        ip_pool.update_many(query_cond, update_cond, upsert=True)

    @classmethod
    def del_one(cls, cond: dict):
        '''
        删除一个文档
        '''
        ip_pool.delete_one(cond)

    @classmethod
    def del_many(cls, cond: dict):
        '''
        删除一个文档
        '''
        ip_pool.delete_many(cond)
        
    @classmethod
    def query_limit(cls, x:int=1, num:int=5):
        '''
        取出最x的num条数据
        x:1升序 -1降序
        '''
        data = ip_pool.find({}, {'_id':0}).sort("last_check", x).limit(num)
        return data
    
if __name__ == '__main__':
    data = MongoService.query_limit(1, 10)
    print(list(data))
    
