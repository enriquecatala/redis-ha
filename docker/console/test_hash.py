
#%% start
import hashlib

texto = u"ñañaña"

hashlib.md5(texto.encode("utf-8"))

# md5 - 128 bits
hashlib.md5(texto.encode("utf-8")).hexdigest()

#%% sha1 - 160 bits
o = hashlib.sha1(texto.encode("utf-8"))
print (o.hexdigest())