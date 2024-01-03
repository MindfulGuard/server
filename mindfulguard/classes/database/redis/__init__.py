from mindfulguard.database.redis.connection import RedisConnection

class Redis:
    def __init__(self):
        self.CACHE_NAME_SETTINGS: str = 'settings'
        self.PATH_SAFE_ALL_ITEM: str = '/v1/safe/all/item' 

    def client(self):
        return RedisConnection()