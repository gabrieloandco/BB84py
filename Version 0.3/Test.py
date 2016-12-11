from AliceClass import *
from BobGen import *
Al = Alice(10)
Bo = BobGen(10)
Re =  Al.Measure(Bo)
print Re
con = Re.Coincidences()
print con
llave= Re.Key(con)
print llave
