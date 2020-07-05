from array import array
import ctypes

class Deltas:#Additions to original class
    def __init__(self):
        self.__indexesVec = array("f")
        self.__valuesVec = array("f")
        
        self.__maxDeltasNum = 500
        
    def getMaxDeltasNum(self):
        return self.__maxDeltasNum
    
    #The function adds a delta if there is a space and returns True, otherwise - False
    def addDelta(self, compressedIndexes, data):
        if(len(self.__valuesVec) >= self.__maxDeltasNum):
            return False
        self.__indexesVec.append(compressedIndexes)
        self.__valuesVec.append(data)
        return True
    
    #The function returns the deltas vector as float array in string, in format: <indexes,data, ...>
    def getAsString(self):
        deltas_str = ""
        for i in range(len(self.__indexesVec)):
            deltas_str += str("%.4f" % float(self.__indexesVec[i]))
            deltas_str += str("%.4f" % self.__valuesVec[i])
        deltas_str += str("%.4f" % 0)
        deltas_str += "*"
        return deltas_str
    
    def clearDeltas(self):
        self.__indexesVec = array("f")
        self.__valuesVec = array("f")
        self.__deltasNum = 0
