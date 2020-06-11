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
                if(j != self.__numColumns - 1):
                    self.__mat[i][j] = random.uniform(thresholdVal[j][0], thresholdVal[j][1]) 
                else:
                    self.__mat[i][j] = -1 # In the initialiesing the indexes value will be -1

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







#thresholdVal = [[15.1,35.1],[14.8,16.1],[40.1,60.9],[1.0,4.0],[5.0,8.0],[6.0,8],[77.0,99.0],[55.0,66.3],[77.7,100.0],[12.0,67.0]]
#deviationVal = [[10,40],[14,20],[33,70.9],[0.5,5],[3,9.1],[5,9],[66,100],[33,77],[68.7,200],[11,68]]
#extremeVal = [[5,45],[13,24],[22,80.9],[0,6.666],[2,11],[3,10],[55,102],[11,88],[54.7,300],[10,69]]

#up=Mat(None, 1000, 10, thresholdVal)
#print(up.getMat())

#ref=Mat(up)
#print(ref.getMat())






#add to server  
#import Vec
#        self.__deltaVec = deltaVec #A vector for the values that need to be updated in the matrix, which is sent to the server

##Comparison-Something like that
# if temperature < __deviationVal[0][0] or temperature > __deviationVal[0][1]:
                # self.__deltaVecec.vecAppend(0,temperature);


                #  v=Vec.Vec()#if we did import- check the code
                #  v.vecAppend(1,2)
                #  v.vecAppend(7,2)
                #  print(v.getVec())
