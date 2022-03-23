"""
 Contact me:
   e-mail:   enrique@enriquecatala.com 
   Linkedin: https://www.linkedin.com/in/enriquecatala/
   Web:      https://enriquecatala.com
   Twitter:  https://twitter.com/enriquecatala
   Support:  https://github.com/sponsors/enriquecatala
   Youtube:  https://www.youtube.com/enriquecatala   
"""

from redis.sentinel import Sentinel
import os

print("Defining sentinel connection...")
sentinel = Sentinel([(os.environ.get("SENTINEL1"), os.environ.get("SENTINEL1_PORT")),
                     (os.environ.get("SENTINEL2"), os.environ.get("SENTINEL2_PORT")),
                     (os.environ.get("SENTINEL3"), os.environ.get("SENTINEL3_PORT"))],
                     socket_timeout=None,
                     password=os.environ.get("REDIS_PASSWORD"), 
                     sentinel_kwargs={"password": os.environ.get("REDIS_PASSWORD")})


r = sentinel.discover_master('mymaster')
print(f"Master connection retrieved from sentinel: {r}")

master = sentinel.master_for('mymaster',socket_timeout=0.1)
slave = sentinel.slave_for('mymaster',socket_timeout=0.1)

print("1) Setting key 'test_key_from_testsentinel.py' in master: ")
# set a value
master.set('test_key_from_testsentinel.py', 'test from testsentinel.py success')

# get the value
value_from_slave = slave.get('test_key_from_testsentinel.py')
print(f"2) Value retrieved from slave: {value_from_slave}")
