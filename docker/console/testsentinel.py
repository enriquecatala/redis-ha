
# NOT WORKING
#
from redis import StrictRedis

from redis.sentinel import Sentinel

#password="REDIS_PASS", sentinel_kwargs={"password": "SENTINEL_PASS"}
sentinel = Sentinel([
            ('redis-sentinel', 26379)
            #('redis-sentinel2', 26379)            
        ], socket_timeout=0.1,
        password="str0ng_passw0rd", sentinel_kwargs={"password": "str0ng_passw0rd"}
    )

master = sentinel.master_for(
        'mymaster',
        password='str0ng_passw0rd',
        socket_timeout=0.1
    )

slave = sentinel.slave_for(
        'redis-slave',
        password='str0ng_passw0rd',
        socket_timeout=0.1
    )

# set a value
master.set('foo', 'bar')

# get the value
slave.get('foo')

