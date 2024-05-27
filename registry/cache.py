import redis


class RedisCacher:
    """
    RedisCacher - is a class, which realises logic for storing binary data in redis
    """
    _client: redis.client.Redis

    def __init__(self, host: str, port: int) -> None:
        self._client = redis.Redis(host, port)

    def set(self, key: str, value: bytes) -> None:
        self._client.set(key, value)

    def get(self, key: str) -> bytes:
        return self._client.get(key)
