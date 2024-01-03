from mindfulguard.classes.database.redis import Redis


def test_connection():
    redis = Redis().client()
    assert redis.connection.ping() == True, redis.connection.ping()

def test_insert():
    redis = Redis().client()
    key: str = 'Key'
    value: str = 'value'
    redis.connection.set(key, value)

    assert redis.connection.get(key) == value
