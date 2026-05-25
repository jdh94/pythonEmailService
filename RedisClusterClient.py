# -*- coding: utf-8 -*-
import time
import redis
import LoggerFactory

logger = LoggerFactory.loggerFactory()

class RedisClient():
    def __init__(self):
        self.redisClient = None
        self.connect_to_redis()

    def connect_to_redis(self):
        for i in range(3):
            try:
                self.redisClient = redis.Redis(
                    host='127.0.0.1',
                    port=6379,
                    decode_responses=True
                )
                self.redisClient.ping()
                logger.info("REDIS CONNECT")
                return self.redisClient
            except Exception as ex:
                logger.error("REDIS CONNECTION ERROR : {e}".format(e=ex))
                time.sleep(5)

    def setValue(self, key, value, expireTime):
        try:
            self.redisClient.set(key, value, ex=expireTime)
            return "success"
        except Exception as ex:
            logger.error("REDIS SET VALUE ERROR : {k}, {v}".format(k=key, v=value))
            logger.error(ex)
            return "fail"

    def getValue(self, key):
        try:
            return self.redisClient.get(key)
        except Exception as ex:
            logger.error("REDIS GET VALUE ERROR : {k}".format(k=key))
            logger.error(ex)
            return "fail"

    def delValue(self, key):
        try:
            self.redisClient.delete(key)
            return "success"
        except Exception as ex:
            logger.error("REDIS DEL VALUE ERROR : {k}".format(k=key))
            logger.error(ex)
            return "fail"
