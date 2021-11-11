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

# setup permissions on the data 
sudo chown -R 1001:1001 data/
```
# Test

```bash
docker compose up 
```
## Docker call

```bash
docker exec -it docker-console-1  python testsentinel.py 
```

## Redis client

From the redis client:

```bash
#install 
sudo apt install redis-client

# connect to redis node
redis-cli -h redis-sentinel -p 26379 -a str0ng_passw0rd
# get info
info
# get masters
sentinel masters
sentinel master mymaster
```

## add values
```bash
import hashlib
texto = u"ñañaña"

hashlib.md5(texto.encode("utf-8"))

hashlib.md5(texto.encode("utf-8")).hexdigest()
```