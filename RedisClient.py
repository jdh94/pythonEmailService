# -*- coding: utf-8 -*-

import redis
import LoggerFactory
import time

logger = LoggerFactory.loggerFactory()

class RedisClient():
    # what is RedisClient?
    # RedisClient는 Redis 서버와 연결하고 데이터를 저장, 조회 및 삭제하는 기능을 제공하는 클래스입니다.
    # what is __init__?
    # __init__는 클래스의 생성자로, 객체가 생성될 때 자동으로 호출됩니다.
    # what is self.pool?
    # self.pool은 Redis 서버와의 연결을 관리하는 ConnectionPool 객체입니다.
    # what is parameter of __init__?
    # __init__의 매개변수는 없습니다. 객체가 생성될 때 자동으로 호출되며, Redis 서버와 연결을 설정합니다.
    # but it has parameter in __init__(self)?
    # __init__(self)에는 매개변수가 없지만, self는 클래스의 인스턴스를 참조하는 매개변수입니다.
    # what is parameter in redis.ConnectionPool? "db=0"?
    # redis.ConnectionPool의 매개변수 db는 Redis 데이터베이스의 인덱스를 지정합니다. 기본값은 0입니다.
    def __init__(self):
        self.pool = redis.ConnectionPool(host='3.38.162.196', port=6379, db=0)
        self.connect_to_redis()

    # does it cause infinite  loop?
    # Yes, the connect_to_redis method will cause an infinite loop if the Redis server is unreachable.
    # then how to fix it?
    # To fix the infinite loop, you can implement a retry limit or a timeout mechanism.
    # is this code run just once? or multiple times?
    # The connect_to_redis method is called once in the __init__ method, but it will retry indefinitely until a connection is established.
    def connect_to_redis(self):
        # is this for expession correct? and my sentence is correct?
        # Yes, the for loop is correct. It will attempt to connect to Redis 3 times before giving up.
        for i in range(3): # retry 횟수 지정
        # while True:  # 연결 될때까지 무한 반복
            try:
                # Connect to Redis
                self.redisClient = redis.Redis(connection_pool=self.pool)
                return self.redisClient
            except redis.ConnectionError as ex:
                logger.error("Failed to connect to Redis server. Retrying in 5 seconds...")
                logger.error(ex)
                # why does it has syntax error?
                # because it is not indented properly
                # what is indent? explain it in korean
                # indent는 코드 블록을 구분하기 위해 사용하는 공백 문자입니다. 파이썬에서는 들여쓰기가 문법적으로 중요합니다.
                # what is this code doing?
                # 이 코드는 Redis 서버에 연결할 수 없을 때 5초 후에 다시 시도하는 것입니다.
                time.sleep(5)
            except Exception as ex:
                logger.error(ex)

    def setValue(self, key, value, expireTime):
        # why does it have while True?
        # while True:  # 연결 될때까지 무한 반복
        # why should I use while True?
        # while True는 Redis 서버와 연결이 끊어졌을 때 재연결을 시도하기 위해 사용됩니다.
        try:
            self.redisClient.set(key, value, expireTime)
            return "success"
        except redis.ConnectionError as ex:
            logger.info('REDIS SET VALUE ERROR :: Reconnecting to Redis server...')
            logger.error(ex)
            self.connect_to_redis()
        except Exception as ex:
            logger.error("REDIS SET VALUE ERROR : {k}, {v}".format(k=key, v=value))
            logger.error(ex)
            return "fail"

    def getValue(self, key):
        try:
            result = self.redisClient.get(key)
            return result
        except redis.ConnectionError as ex:
            logger.info('REDIS GET VALUE ERROR :: Reconnecting to Redis server...')
            logger.error(ex)
            self.connect_to_redis()
        except Exception as ex:
            logger.error("REDIS GET VALUE ERROR : {k}".format(k=key))
            logger.error(ex)
            return "fail"

    def delValue(self, key):
        try:
            self.redisClient.delete(key)
            return "success"
        except redis.ConnectionError as ex:
            logger.info('REDIS DEL VALUE ERROR :: Reconnecting to Redis server...')
            logger.error(ex)
            self.connect_to_redis()
        except Exception as ex:
            logger.error("REDIS DEL VALUE ERROR : {k}".format(k=key))
            logger.error(ex)
            return "fail"