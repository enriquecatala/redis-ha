
#%% start
import hashlib

texto = u"ñañaña"

hashlib.md5(texto.encode("utf-8"))

hashlib.md5(texto.encode("utf-8")).hexdigest()

#%% sha1
o = hashlib.sha1(texto.encode("utf-8"))
print (o.hexdigest())