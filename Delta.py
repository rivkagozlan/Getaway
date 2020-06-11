from array import array

class Deltas:#Additions to original class
    def __init__(self):
        self.__indexesVec = array("h")
        self.__valuesVec = array("f")
        self.__maxDeltasNum = 100
        self.__deltasNum = 0
        
    def getMaxDeltasNum(self):
        return self.__maxDeltasNum
    
    def getdeltasNum(self):
        return self.__deltasNum 
    
    def addDelta(self, compressedIndexes, data):
        if(len(self.__valuesVec) >= self.__maxDeltasNum):
            print("You tried add deltas more than the max deltas in buffer number")
            return
        self.__indexesVec.append(compressedIndexes)
        self.__valuesVec.append(data)
        ##################################################################
        print("*********************************")
        print("------ You added a delta to the buffer ------")
        print("The length of the indexes value in bytes: ",self.__indexesVec.itemsize)
        print("The length in elements of the buffer: ",self.__indexesVec.buffer_info())
        print("The compressed indexes value: ",compressedIndexes)
        print("in bytes: ",self.__indexesVec.tobytes())
        print("*********************************\n")
        ##################################################################   
    
    def getAsString(self):
        deltas_str = ""
        for i in range(len(self.__indexesVec)):
            deltas_str += str(float(self.__indexesVec[i]))+","
            deltas_str += str("%.4f" % self.__valuesVec[i])+","
        deltas_str = deltas_str[:-1]
        return deltas_str
#d=Deltas()
#d.addDelta(257, 5.998878)
#d.addDelta(258, 6.788844)
#d.addDelta(259, 7.3444232)
#print(d.getAsString())


