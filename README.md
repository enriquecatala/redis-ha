<div>
    <a href="https://github.com/sponsors/enriquecatala"><img src="https://img.shields.io/badge/GitHub_Sponsors--_.svg?style=flat-square&logo=github&logoColor=EA4AAA" alt="GitHub Sponsors"></a>
    <a href="https://enriquecatala.com"><img src="https://img.shields.io/website?down_color=red&down_message=down&label=enriquecatala.com&up_color=46C018&url=https%3A%2F%2Fenriquecatala.com&style=flat-square" alt="Data Engineering with Enrique Catalá"></a>
    <a href="https://www.linkedin.com/in/enriquecatala"><img src="https://img.shields.io/badge/LinkedIn--_.svg?style=flat-square&logo=linkedin" alt="LinkedIn Enrique Catalá Bañuls"></a>
    <a href="https://twitter.com/enriquecatala"><img src="https://img.shields.io/twitter/follow/enriquecatala?color=blue&label=twitter&style=flat-square" alt="Twitter @enriquecatala"></a>
    <a href="https://youtube.com/enriquecatala"><img src="https://raw.githubusercontent.com/enriquecatala/enriquecatala/master/img/youtube.png" alt="Data Engineering: Canal youtube de Enrique Catalá" height=20></a>
</div>

<a href="https://mvp.microsoft.com/es-es/PublicProfile/5000312?fullName=Enrique%20Catala"><img src="https://raw.githubusercontent.com/enriquecatala/enriquecatala/master/img/MVP_Logo_horizontal.png" alt="Microsoft DataPlatform MVP Enrique Catalá"></a>

- [redis-ha](#redis-ha)
  - [Set permission on data directory](#set-permission-on-data-directory)
- [Start up the cluster](#start-up-the-cluster)
  - [Test from docker container](#test-from-docker-container)
  - [Redis client](#redis-client)
    - [Connect to master](#connect-to-master)
- [Examples](#examples)
  - [Mass insert](#mass-insert)
  - [add values](#add-values)
- [Credits](#credits)
# redis-ha
Redis High Availability deploiment for docker and kubernetes

## Set permission on data directory

If you are running this in a local docker environment, please make sure you have set the permission on the data directory.

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

**IMPORTANT:** redis-data directory is in the .gitignore file, so data will not be saved.
# Start up the cluster

```bash
docker compose up --build
```
## Test from docker container

If you uncommented from the docker-compose file the console container, you will be able to connect to docker-console application to test it.

```bash
docker exec -it docker-console-1  python testsentinel.py 
```

After executing the last command, if you connect to the redis-master, this is what you should get: 

## Redis client

From the redis client:

```bash
#install 
sudo apt install redis-tools

# connect to redis node
#redis-cli -h redis-sentinel -p 26379 -a str0ng_passw0rd
redis-cli -h 127.0.0.1 -p 26379 -a str0ng_passw0rd


# get info
info
# get masters
sentinel masters
sentinel master mymaster
```

### Connect to master

```bash
#redis-cli -h redis-master -p 6379 -a str0ng_passw0rd
redis-cli -h 127.0.0.1 -p 6379 -a str0ng_passw0rd


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
#cat data/data.txt | redis-cli -h redis-master -p 6379 -a str0ng_passw0rd --pipe
cat "D:\prepared_blacklist_for_redis\part-00000-tid-8877533473703218517-d3e24d59-c5ee-4a52-9c37-9b89a217b070-263-1-c000.csv" | redis-cli -h 127.0.0.1 -p 6379 -a somesecretpassword --pipe
```

>NOTE: For more info https://redis.io/topics/mass-insert
## add values
```bash
import hashlib
texto = u"ñañaña"

hashlib.md5(texto.encode("utf-8"))

hashlib.md5(texto.encode("utf-8")).hexdigest()
```

# Credits

https://github.com/tarosky/k8s-redis-ha
https://hub.docker.com/r/bitnami/redis-sentinel/
https://docs.bitnami.com/tutorials/deploy-redis-sentinel-production-cluster/

