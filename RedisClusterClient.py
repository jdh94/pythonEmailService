# -*- coding: utf-8 -*-

# what does this import mean? from and import
# from rediscluster import RedisCluster what does it mean?
# from rediscluster는 rediscluster 모듈에서 RedisCluster 클래스를 가져오는 것입니다.
# how can i search the rediscluster? because it is not in the standard library
# how to search the rediscluster?
# You can search for the rediscluster library on the Python Package Index (PyPI) or its official documentation.
# how to search the rediscluster in pypi?
# You can search for the rediscluster library on the Python Package Index (PyPI) by visiting https://pypi.org/ and entering "rediscluster" in the search bar.
# redis-py-cluster is a Python client for Redis that supports Redis Cluster.
# what is redis-py-cluster?
# redis-py-cluster는 Redis 클러스터를 지원하는 Python 클라이언트입니다.
# what is cluster?
# Redis Cluster는 Redis의 분산 데이터베이스 솔루션으로, 데이터를 여러 노드에 분산 저장하여 확장성과 가용성을 높입니다.
# what is distributed database?
# 분산 데이터베이스는 데이터를 여러 서버에 분산 저장하여 성능과 가용성을 높이는 데이터베이스 시스템입니다.
# then is oracle a distributed database?
# 오라클은 분산 데이터베이스를 지원하는 데이터베이스 관리 시스템입니다. 그러나 기본적으로는 단일 서버에서 실행됩니다.
from rediscluster import RedisCluster
from rediscluster.exceptions import RedisClusterException
import time
import LoggerFactory

logger = LoggerFactory.loggerFactory()

class RedisClient():
    def __init__(self):
        self.redisClient = None
        self.connect_to_redis()

    def connect_to_redis(self):
        # while True:  # 연결 될때까지 무한 반복
        for i in range(3):
            try:
                # Connect to Redis
                startup_nodes = [
                    {"host": "3.38.162.192", "port": "6379"}
#                    ,{"host": "3.38.162.192", "port": "6379"}
                ]
                self.redisClient = RedisCluster(startup_nodes=startup_nodes, decode_responses=True,
                                                password='fldeldehdgn1!')
                logger.info("REDIS CLUSTER CONNECT")
                return self.redisClient
            except RedisClusterException as ex:
                logger.error("Failed to connect to Redis server. Retrying in 5 seconds...")
                logger.error(ex)
                time.sleep(5)
            except Exception as ex:
                logger.error("REDIS CONNECTION ERROR : {e}".format(e=ex))
                time.sleep(5)

    def setValue(self, key, value, expireTime):
        # while True:
        try:
            self.redisClient.set(key, value, expireTime)
            return "success"
        except RedisClusterException as ex:
            logger.info('REDIS SET VALUE ERROR :: Reconnecting to Redis server...')
            logger.error(ex)
            self.connect_to_redis()
        except Exception as ex:
            logger.error("REDIS SET VALUE ERROR : {k}, {v}".format(k=key, v=value))
            logger.error(ex)
            return "fail"

    def getValue(self, key):
        #while True:
        try:
            result = self.redisClient.get(key)
            return result
        except RedisClusterException as ex:
            logger.info('REDIS GET VALUE ERROR :: Reconnecting to Redis server...')
            logger.error(ex)
            self.connect_to_redis()
        except Exception as ex:
            logger.error("REDIS GET VALUE ERROR : {k}".format(k=key))
            logger.error(ex)
            return "fail"

    def delValue(self, key):
        #while True:
        try:
            self.redisClient.delete(key)
            return "success"
        except RedisClusterException as ex:
            logger.info('REDIS DEL VALUE ERROR :: Reconnecting to Redis server...')
            logger.error(ex)
            self.connect_to_redis()
        except Exception as ex:
            logger.error("REDIS DEL VALUE ERROR : {k}".format(k=key))
            logger.error(ex)
            return "fail"