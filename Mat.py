import random
#import numpy as np

class Mat:
    #for update matrix: Mat(None, numRows, numColumns, thresholdVal)
    #for reference matrix: Mat(otherMat)
    def __init__(self, otherMat = None, numRows = None, numColumns = None, thresholdVal = None):

        self.__mat = []  #The mat: rows= the sensors, columns= indices.  

        if(otherMat is None): #for initialize the update matrix
            self.__numRows = numRows
            self.__numColumns = numColumns
            self.init2DArr(self.__mat, self.__numRows, self.__numColumns)                    
            self.initMat(thresholdVal)            
        else: #for initialize the reference matrix
            self.__numRows = otherMat.getNumRows()
            self.__numColumns = otherMat.getNumColumns()
            self.setMat(otherMat.getMat())


    #The function create a range1-by-range2-size matrix        
    def init2DArr(self, mat, range1, range2):
        for i in range (range1):
            mat.append([])
            for j in range (range2):
                mat[i].append([])

    #The function initialize the mat attribute in random numbers by the threshold values  
    def initMat(self, thresholdVal):
        for i in range (self.__numRows):
            for j in range (self.__numColumns):
                self.__mat[i][j] = random.uniform(thresholdVal[j][0], thresholdVal[j][1])
                
                #if(j != self.__numColumns - 1):
                    #self.__mat[i][j] = random.uniform(thresholdVal[j][0], thresholdVal[j][1]) 
                #else:
                    #self.__mat[i][j] = -1 # In the initialiesing the indexes value will be -1

    def getRow(self, index):
        return self.__mat[index]

    #The function sets row in the mat
    def setRow(self, index, indicesArr):
        self.__mat[index] = indicesArr.copy()

    def getMat(self):
        return self.__mat

    def setMat(self, mat):
        self.__mat = [row[:] for row in mat]  #copy the arrays    

    def getNumRows(self):
        return self.__numRows

    def getNumColumns(self):
        return self.__numColumns
    
    def getMatAsStr(self):
        s=""
        i=0
        while i < self.__numRows:         
            for x in self.__mat[i]:#number of cols
                s+=str("%.4f" % x)
            i += 1
        s+=str("%.4f" % 0)
        return s
    
            