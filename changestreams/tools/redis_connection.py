import redis

redis_instances = {"service_name": "mymaster",
                   "master_host": "redis-master",
                   "master_port": 26379,
                   "sentinel_1_host": "sentinel-1",
                   "sentinel_1_port": 26379,
                   "sentinel_2_host": "sentinel-2",
                   "sentinel_2_port": 26379,
                   "sentinel_3_host": "sentinel-3",
                   "sentinel_3_port": 26379, }

try:
    redis_service = redis_instances["service_name"]
    redis_connection = redis.sentinel.Sentinel(
        [(redis_instances["master_host"], redis_instances["master_port"]),
         (redis_instances["sentinel_1_host"], redis_instances["sentinel_1_port"]),
         (redis_instances["sentinel_2_host"], redis_instances["sentinel_2_port"]),
         (redis_instances["sentinel_3_host"], redis_instances["sentinel_3_port"])],
        min_other_sentinels=2,
        encoding="utf-8",
        decode_responses=True)
    master = redis_connection.master_for(redis_service)
except redis.RedisError as err:
    print(err, flush=True)
