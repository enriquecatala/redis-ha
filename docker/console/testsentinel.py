#from redis import StrictRedis

from redis.sentinel import Sentinel

sentinel = Sentinel([('redis-sentinel', 26379),
                     ('redis-sentine2', 26380),
                     ('redis-sentine3', 26381)],
                     socket_timeout=None,
                     password="str0ng_passw0rd", 
                     sentinel_kwargs={"password": "str0ng_passw0rd"})

r = sentinel.discover_master('mymaster')
print(f"master: {r}")

master = sentinel.master_for('mymaster',socket_timeout=0.1)
slave = sentinel.slave_for('mymaster',socket_timeout=0.1)

# set a value
master.set('foo', 'bar')

# get the value
slave.get('foo')
