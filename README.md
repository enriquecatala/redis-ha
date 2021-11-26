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
sudo chown -R 1001:1001 redis-data/
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
sudo apt install redis-tools

# connect to redis node
#redis-cli -h 127.0.0.1 -p 26379 -a str0ng_passw0rd
redis-cli -h redis-sentinel -p 26379 -a str0ng_passw0rd

# get info
info
# get masters
sentinel masters
sentinel master mymaster
```

### Connect to master

```bash
#redis-cli -h 127.0.0.1 -p 6379 -a str0ng_passw0rd
redis-cli -h redis-sentinel -p 6379 -a str0ng_passw0rd

```


# Examples

```bash
# get databases
info keyspace

# list all keys
keys *

# list keys with pattern
keys *pattern*

# clean database0
select 0
flushdb
```

## Mass insert

The data must be created in the form:
```txt
SET key1 value1
SET key2 value2
...
```
where each row must be separated by <mark>CRLF</mark>

To mass insert data into redis:
```bash
# use PIPE 
#cat data/data.txt | redis-cli -h 127.0.0.1 -p 6379 -a str0ng_passw0rd --pipe
cat data/data.txt | redis-cli -h redis-sentinel -p 6379 -a str0ng_passw0rd --pipe
```

>NOTE: For more info https://redis.io/topics/mass-insert
## add values
```bash
import hashlib
texto = u"ñañaña"

hashlib.md5(texto.encode("utf-8"))

hashlib.md5(texto.encode("utf-8")).hexdigest()
```