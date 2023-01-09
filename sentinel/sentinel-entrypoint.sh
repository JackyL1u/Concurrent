#!/bin/sh

exec docker-entrypoint.sh redis-server /etc/redis/sentinel.conf --sentinel
