import redis
import json

redis_instances = {"service_name": "mymaster",
                   "master_host": "redis-master",
                   "master_port": 26379,
                   "sentinel_1_host": "sentinel-1",
                   "sentinel_1_port": 26379,
                   "sentinel_2_host": "sentinel-2",
                   "sentinel_2_port": 26379,
                   "sentinel_3_host": "sentinel-3",
                   "sentinel_3_port": 26379, }


class Redis:
    def __init__(self):
        try:
            self.redis_service = redis_instances["service_name"]
            self.redis_connection = redis.sentinel.Sentinel(
                [(redis_instances["master_host"], redis_instances["master_port"]),
                 (redis_instances["sentinel_1_host"], redis_instances["sentinel_1_port"]),
                 (redis_instances["sentinel_2_host"], redis_instances["sentinel_2_port"]),
                 (redis_instances["sentinel_3_host"], redis_instances["sentinel_3_port"])],
                min_other_sentinels=2,
                encoding="utf-8",
                decode_responses=True)
        except redis.RedisError as err:
            print(err, flush=True)

    def set(self, key, value):
        try:
            master = self.redis_connection.master_for(self.redis_service)
            master.set(str(key), str(value))
            return {"success": True}
        except redis.RedisError as err:
            return {"success": False,
                    "error": err}

    def get(self, key):
        try:
            master = self.redis_connection.master_for(self.redis_service)
            value = master.get(str(key))
            if value:
                value = json.loads(value)
            return {"success": True, "value": value, "key": key}
        except redis.RedisError as err:
            return {"success": False,
                    "error": err}


RedisClient = Redis()
