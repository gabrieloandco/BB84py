# Copyright (c) 2016 Gabriel Oliveri (<gabrieloandco@gmail.com>)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from Matrix import Matrix
import random
from XorEncrypt import *
from math import sqrt

ket0=Matrix.fromList([[1.0],[0.0]])
ket1=Matrix.fromList([[0.0],[1.0]])
ketsum=Matrix.fromList([[round(1/sqrt(2),1)],[round(1/sqrt(2),1)]])
ketmin=Matrix.fromList([[round(1/sqrt(2),1)],[round(-1/sqrt(2),1)]])

class Alice(Matrix):

	def __init__(self,blocks,null=0):
		self.blocks=blocks
		self.realid=id(self)
		self.null=null
		Alices=[]
		if null==0:
			for i in range(0,blocks):
				c = random.choice([1,2,3,4])
				if c==1:
					Alices.append(ket0)
				if c==2:
					Alices.append(ket1)
				if c==3:
					Alices.append(ketsum)
				if c==4:
					Alices.append(ketmin)
			self.bases=Alices
		else:
			for i in range(0,blocks):
				Alices.append(0)
			self.bases=Alices

	def __str__(self):
		a=[]
		for base in self.bases:
			a.append(str(base))
		stren = XorEncrypt(str(a),self.realid)
		strde = XorDecrypt(stren,id(self))
		return strde
	
	def __repr__(self):
		string=str(self)
		i=2
		d=[]
		for base in range(0,self.blocks):
			a=float(string[i:i+4])
			i+=6
			b=float(string[i:i+4])
			i+=10
			c=[a,b] #remove c for a simpler code
			if c == [1.0,0.0]:
				d.append(' ket0 ')
			elif c == [0.0,1.0]:
				d.append(' ket1 ')
			elif c == [round(1/sqrt(2),1), round(1/sqrt(2),1)]:
				d.append(' ketsum ')
			elif c == [round(1/sqrt(2),1), round(-1/sqrt(2),1)]:
				d.append(' ketmin ')
			else:
				d.append(' error ')

		return str(d)
 	
	def PrintBases(self):
		print repr(self)

	def Measure(self,Bob):
		Result=Alice(self.blocks,1)
		for i in range(0,self.blocks):
			Result.bases[i]= Bob[i]*self.bases[i]
		return Result
	
	def Coincidences(self):
		con=[]
		if self.realid == id(self):
			for i in range(self.blocks):
				mc=self.bases[i]
				test = round(sqrt((mc[0][0])**2+(mc[1][0])**2),1)
    				if test == 0.7:
        				con.append(0)
    				else:
        				con.append(1)

		else:
			print 'Not original computer'
		return con

	def Key(self,con):
		llave=[]
		if self.realid == id(self):
			for i in range(self.blocks):
				if con[i] == 1:
            				if str(self.bases[i]) == '+0.0\n+1.0\n':
                				llave.append(1)

            				elif str(self.bases[i]) == '+1.0\n+0.0\n':
                				llave.append(0)

            				elif str(self.bases[i]) == '+0.7\n-0.7\n':
                				llave.append(1)

            				elif str(self.bases[i]) == '+0.7\n+0.7\n':
                				llave.append(0)

		else:
			print 'Not original computer'	 	
		return llave		

		
def Main():
	Alices = Alice(10)

	print Alices

	Alices.PrintBases()
if __name__=='__main__':
	Main()
