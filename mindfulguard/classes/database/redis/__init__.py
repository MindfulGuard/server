from mindfulguard.database.redis.connection import RedisConnection

class Redis:
    def __init__(self):
        self.CACHE_NAME_SETTINGS = 'settings'

    def client(self):
        return RedisConnection()