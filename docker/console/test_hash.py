"""
 Contact me:
   e-mail:   enrique@enriquecatala.com 
   Linkedin: https://www.linkedin.com/in/enriquecatala/
   Web:      https://enriquecatala.com
   Twitter:  https://twitter.com/enriquecatala
   Support:  https://github.com/sponsors/enriquecatala
   Youtube:  https://www.youtube.com/enriquecatala   
"""

#%% start
import hashlib

texto = u"ñañaña"

hashlib.md5(texto.encode("utf-8"))

# md5 - 128 bits
hashlib.md5(texto.encode("utf-8")).hexdigest()

#%% sha1 - 160 bits
o = hashlib.sha1(texto.encode("utf-8"))
print (o.hexdigest())