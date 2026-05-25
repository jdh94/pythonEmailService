# -*- coding: utf-8 -*-

# スタンドアロン（単体）Redis サーバーへの接続クライアント。
# RedisCluster ではなく通常の redis.Redis を使う（Connection Type: Standalone）。
import redis
from redis.exceptions import ConnectionError as RedisConnectionError
import time
import datetime
import LoggerFactory

logger = LoggerFactory.loggerFactory()


# Redis に接続できない場合（ローカル開発環境など）に使うメモリ代替ストア。
# { key: (value, expire_datetime) } の辞書で管理する。
class _InMemoryStore:
    def __init__(self):
        self._store: dict = {}

    def set(self, key, value, expire_time):
        # expire_time は datetime.timedelta を想定する。
        expires_at = datetime.datetime.now() + expire_time
        self._store[key] = (value, expires_at)
        return True

    def get(self, key):
        entry = self._store.get(key)
        if entry is None:
            return None
        value, expires_at = entry
        # 有効期限切れの場合は削除して None を返す。
        if datetime.datetime.now() > expires_at:
            del self._store[key]
            return None
        return value

    def delete(self, key):
        self._store.pop(key, None)
        return True


class RedisClient():
    def __init__(self):
        self.redisClient = None
        self._fallback = None  # Redis 接続失敗時のメモリ代替ストア
        self.connect_to_redis()

    def connect_to_redis(self):
        for i in range(2):  # 試行回数を2回に減らして起動を速くする
            try:
                self.redisClient = redis.Redis(
                    host='homejdh.iptime.org',
                    port=9003,
                    password='fldeldehdgn1!',
                    decode_responses=True,
                    socket_connect_timeout=2,
                    socket_timeout=2,
                )
                # ping() で実際に接続確認する。
                self.redisClient.ping()
                logger.info("REDIS STANDALONE CONNECT SUCCESS")
                self._fallback = None
                return self.redisClient
            except RedisConnectionError as ex:
                logger.error("Failed to connect to Redis server. Retrying in 2 seconds...")
                logger.error(ex)
                time.sleep(2)
            except Exception as ex:
                logger.error("REDIS CONNECTION ERROR : {e}".format(e=ex))
                time.sleep(2)

        # 2回試してもつながらない場合はメモリストアで代替する。
        # 本番環境では Redis を必ず使うこと。ローカル開発用の措置。
        logger.error("Redis に接続できません。メモリストアで代替します（開発環境用）。")
        self._fallback = _InMemoryStore()

    def _use_fallback(self):
        return self._fallback is not None

    def setValue(self, key, value, expireTime):
        try:
            if self._use_fallback():
                self._fallback.set(key, value, expireTime)
                return "success"
            self.redisClient.set(key, value, expireTime)
            return "success"
        except RedisConnectionError as ex:
            logger.info('REDIS SET VALUE ERROR :: Reconnecting to Redis server...')
            logger.error(ex)
            self.connect_to_redis()
        except Exception as ex:
            logger.error("REDIS SET VALUE ERROR : {k}, {v}".format(k=key, v=value))
            logger.error(ex)
            return "fail"

    def getValue(self, key):
        try:
            if self._use_fallback():
                return self._fallback.get(key)
            result = self.redisClient.get(key)
            return result
        except RedisConnectionError as ex:
            logger.info('REDIS GET VALUE ERROR :: Reconnecting to Redis server...')
            logger.error(ex)
            self.connect_to_redis()
        except Exception as ex:
            logger.error("REDIS GET VALUE ERROR : {k}".format(k=key))
            logger.error(ex)
            return "fail"

    def delValue(self, key):
        try:
            if self._use_fallback():
                self._fallback.delete(key)
                return "success"
            self.redisClient.delete(key)
            return "success"
        except RedisConnectionError as ex:
            logger.info('REDIS DEL VALUE ERROR :: Reconnecting to Redis server...')
            logger.error(ex)
            self.connect_to_redis()
        except Exception as ex:
            logger.error("REDIS DEL VALUE ERROR : {k}".format(k=key))
            logger.error(ex)
            return "fail"
