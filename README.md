# redis-ha
Redis High Availability deploiment for docker and kubernetes

https://github.com/tarosky/k8s-redis-ha
https://hub.docker.com/r/bitnami/redis-sentinel/
https://docs.bitnami.com/tutorials/deploy-redis-sentinel-production-cluster/


## Set permission on data directory

```bash
# create folders
mkdir redis-data
mkdir redis-data/redis
mkdir redis-data/redis/data
mkdir redis-data/redis/conf
mkdir redis-data/redis-slave
mkdir redis-data/redis-slave/data
mkdir redis-data/redis-slave/conf
mkdir redis-data/redis-sentinel
mkdir redis-data/redis-sentinel/data
mkdir redis-data/redis-sentinel/conf

# setup permissions on the redis-data 
sudo chown -R 1001:1001 redis-data/
```


