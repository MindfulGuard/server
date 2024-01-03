import redis
from mindfulguard.classes.database.redis.connection_base import RedisConnectionBase


class RedisConnection(RedisConnectionBase):
    def __init__(self):
        super().__init__()
        self.connection = redis.Redis(
            host = self._host,
            port = self._port,
            username = self._username,
            password = self._password,
            decode_responses = True,
            db=self._ld
        )