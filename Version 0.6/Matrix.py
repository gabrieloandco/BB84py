import random
import operator
import sys
import unittest


class MatrixError(Exception):
    """ An exception class for Matrix """
    pass

class Matrix(object):
    
    def __init__(self, m, n, init=True):
        self.realid = id(self)
        if init:
            self.rows = [[0]*n for x in range(m)]
        else:
            self.rows = []
        self.m = m
        self.n = n
        
    def __getitem__(self, idx):
        if self.realid ==id(self): 
            return self.rows[idx]
        else:
            raise MatrixError, "Not original Computer"

    def __setitem__(self, idx, item):
        self.rows[idx] = item
        
    def __str__(self):
        if self.realid ==id(self):
            s='\n'.join([' '.join([("+"+ str(item)) if item>=0 else (""+str(item)) for item in row]) for row in self.rows])
            return s + '\n'
        else:
            raise MatrixError, "Not original Computer"

    def __repr__(self):
        if self.realid ==id(self):
    	    s=str(self.rows)
            rank = str(self.getRank())
            rep="M: %s " % (s)
            return rep
        else:
            raise MatrixError, "Not original Computer"
    
    def reset(self):
        """ Reset the matrix data """
        self.rows = [[] for x in range(self.m)]
                     


    def __eq__(self, mat):
        """ Test equality """

        return (mat.rows == self.rows)
        

    def __mul__(self, mat):
        """ Multiple a matrix with this matrix and
        return the new matrix. Doesn't modify
        the current matrix """
        
        matm, matn = mat.getRank()
        
        if (self.n != matm):
            raise MatrixError, "Matrices cannot be multipled!"
        
        mat_t = mat.getTranspose()
        mulmat = Matrix(self.m, matn)
        
        for x in range(self.m):
            for y in range(mat_t.m):
                mulmat[x][y] = sum([item[0]*item[1] for item in zip(self.rows[x], mat_t[y])])

        return mulmat

    def getRank(self):
        return (self.m, self.n)

    def transpose(self):
        """ Transpose the matrix. Changes the current matrix """
        
        self.m, self.n = self.n, self.m
        self.rows = [list(item) for item in zip(*self.rows)]

    def getTranspose(self):
        """ Return a transpose of the matrix without
        modifying the matrix itself """
        
        m, n = self.n, self.m
        mat = Matrix(m, n)
        mat.rows =  [list(item) for item in zip(*self.rows)]
        
        return mat


    def save(self, filename):
        open(filename, 'w').write(str(self))
        
    @classmethod
    def _makeMatrix(cls, rows):

        m = len(rows)
        n = len(rows[0])
        # Validity check
        if any([len(row) != n for row in rows[1:]]):
            raise MatrixError, "inconsistent row length"
        mat = Matrix(m,n, init=False)
        mat.rows = rows

        return mat
        
    @classmethod
    def makeRandom(cls, m, n, low=0, high=10):
        """ Make a random matrix with elements in range (low-high) """
        
        obj = Matrix(m, n, init=False)
        for x in range(m):
            obj.rows.append([random.randrange(low, high) for i in range(obj.n)])

        return obj


        return cls._makeMatrix(rows)

    @classmethod
    def fromList(cls, listoflists):
        """ Create a matrix by directly passing a list
        of lists """

        # E.g: Matrix.fromList([[1 2 3], [4,5,6], [7,8,9]])

        rows = listoflists[:]
        return cls._makeMatrix(rows)
        

class MatrixTests(unittest.TestCase):


    def testMul(self):
        m1 = Matrix.fromList([[1, 2, 3], [4, 5, 6]])
        m2 = Matrix.fromList([[7, 8], [10, 11], [12, 13]])
        self.assertTrue(m1 * m2 == Matrix.fromList([[63, 69], [150, 165]]))
        self.assertTrue(m2*m1 == Matrix.fromList([[39, 54, 69], [54, 75, 96], [64, 89, 114]]))



if __name__ == "__main__":
    unittest.main()
