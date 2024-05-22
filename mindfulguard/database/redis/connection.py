import redis
from loguru import logger
from mindfulguard.classes.database.redis.connection_base import RedisConnectionBase

class RedisConnection(RedisConnectionBase):
    def __init__(self):
        super().__init__()
        self.connection = redis.Redis(
            host=self._host,
            port=self._port,
            username=self._username,
            password=self._password,
            decode_responses=True,
            db=self._ld
        )
        logger.debug("Connection to Redis database opened. Host: {}, Port: {}, Username: {}, Database: {}", self._host, self._port, self._username, self._ld)
