from AliceGen import *
from BobGen import *
from QuantumConversion import *

blocks= int(raw_input("Security lvl: "))
Alice0 = AliceGen(blocks)
PrintAlice(Alice0)
AlStr=QuantumListToStr(Alice0)
AlList = QuantumStrToListAlice(AlStr,blocks)
Alice = QuantumListToBasesAlice(AlList)

print Alice0 == Alice

Bob= BobGen(blocks)

PrintBob(Bob)

Resultado = Medicion(Bob,Alice)

con = Con(Resultado)

print con

llavebob1 = LlaveBob(Alice,Bob,con)

print llavebob1

llavealice= LlaveAlice(Alice, con)

print llavealice

print "Intruso"

Eva = BobGen(blocks)

print "Bases de Eva"

PrintBob(Eva)

Colapso = Medicion(Eva,Alice)

print "Funcion Colapsada"

PrintAlice(Colapso)

Resultado = Medicion(Bob,Colapso)

print "Resultado"

PrintAlice(Resultado)

print "Coincidencias"

con = Con(Resultado)

print con

llavebob2 = LlaveBob(Alice,Bob,con)

print llavebob2

print llavebob1 == llavebob2



