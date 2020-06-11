import socket
import struct
import ctypes
from Mat import Mat
from Delta import Deltas

class Getaway:#Additions to original class
    def __init__(self, deviationVal, extremeVal):
        self.__numSensors = 1000 # maybe get it from 1 group?
        self.__numIndices = 10 # maybe get it from 1 group?
        
        self.__thresholdVal = []
        self.__deviationVal = deviationVal
        self.__extremeVal = extremeVal         
        
        self.__upMat = None
        self.__refMat = None
        self.__numDeltasSent = 0 # The number of the deltas we sent so far
        self.__numDeltaToSend = 30 # After sending this number of deltas, a full frame should be sent to the cloud
        self.__deltasVec = Deltas() 
    
    # The function initializes the thresholdVal array and the two matrices
    def __thresholdVal_Mats_init(self, thresholdVal_str):
        vec = thresholdVal_str[0:len(thresholdVal_str)].split(",")             
        k=0
        for i in range (self.__numIndices):
            self.__thresholdVal.append([])
            for j in range (2):
                self.__thresholdVal[i].append([])
                self.__thresholdVal[i][j] = float(vec[k])
                k = k+1
        self.__upMat = Mat(None, self.__numSensors, self.__numIndices + 1, self.__thresholdVal)
        self.__refMat = Mat(self.__upMat)        
        
    def getThresholdVal(self):
        return self.__thresholdVal
    
    def setThresholdVal(self, thresholdVal):
        self.__thresholdVal = [row[:] for row in thresholdVal]    
    
    def getDeviationVal(self):
        return self.__deviationVal
    
    def setDeviationVal(self, deviationVal):
        self.__deviationVal = [row[:] for row in deviationVal]            
    
    def getExtremeVal(self):
        return self.__extremeVal    
        
    def setExtremeVal(self, extremeVal):
        self.__extremeVal = [row[:] for row in extremeVal] 
    
    # The function compress two integer numbers to one short variable
    def __compressIndexes(self, indexX, indexY):
        compressedVal = ctypes.c_ushort((indexX << 8) | indexY)
        return compressedVal;
    
    def __handlesData(self, sensorData):
        tempVec = sensorData[0:len(sensorData)].split(",")
        row = []
        i = 0
        for i in range (self.__numIndices):
            row.append(float(tempVec[i]))
        row.append(self.__compressIndexes(int(tempVec[i+1]), int(tempVec[i+2])))         
        rowIndex = int(tempVec[i+3])
        self.__upMat.setRow(rowIndex, row)
    
    def __matsCompare(self):
        if(self.__refMat.getMat()[11][10] != -1):
            self.__deltasVec.addDelta(self.__upMat.getMat()[11][self.__numIndices].value, self.__refMat.getMat()[11][0])
        else:
            self.__deltasVec.addDelta(self.__upMat.getMat()[0][self.__numIndices].value, self.__refMat.getMat()[0][0]) 
        
    def run_server(self):
        server_socket = socket.socket() # Creating a new socket object
        port = 65531
        server_socket.bind(('127.0.0.1', port)) # Binding the socket to a specific address and port
        server_socket.listen(5) # Configure the socket backlog to 5
        print('Waiting for connection...')
        conn, addr = server_socket.accept()
        print ("Socket Up and running with a connection from",addr)
        
        #receiving the threshold values as string
        thresholdVal_str = conn.recv(1024).decode()
        self.__thresholdVal_Mats_init(thresholdVal_str)
        
        while True: # Receiving updates from sensors
            sensorData = conn.recv(1024).decode()
            print ("***** The message received:",sensorData," *****")
            self.__handlesData(sensorData)
            ###########################################################
            print("\n************************************")
            print("line 0: ",self.__upMat.getRow(0),"\n")
            print("line 1: ",self.__upMat.getRow(1),"\n")
            print("line 11: ",self.__upMat.getRow(11))
            print("************************************\n")
            self.__matsCompare()
            ###########################################################

        conn.close()
        
        #python Getaway.py
        #python client.py
        #10.1010,11.1111,20.2020,21.2121,30.3030,31.3131,40.4040,41.4141,50.5050,51.5151,60.6060,61.6161,70.7070,71.7171,80.8080,81.8181,90.9090,91.9191,100.1001,101.1011
        #1.1111,2.2222,3.3333,4.4444,5.5555,6.6666,7.7777,8.8888,9.9999,10.1010,1,1,0










    #if __name__ == '__main__':
    
thresholdVal = [[15.1,35.1],[14.8,16.1],[40.1,60.9],[1.0,4.0],[5.0,8.0],[6.0,8],[77.0,99.0],[55.0,66.3],[77.7,100.0],[12.0,67.0]]
deviationVal = [[10,40],[14,20],[33,70.9],[0.5,5],[3,9.1],[5,9],[66,100],[33,77],[68.7,200],[11,68]]
extremeVal = [[5,45],[13,24],[22,80.9],[0,6.666],[2,11],[3,10],[55,102],[11,88],[54.7,300],[10,69]]
s = Getaway(deviationVal, extremeVal)
s.run_server()



##In these arrays - lower value in index 0, upper value in index 1
#self.__thresholdVal = []
#self.__deviationVal = []
#self.__extremeVal = []          

#self.init2DArr(self.__thresholdVal, self.__numIndices, 2)        
#self.init2DArr(self.__deviationVal, self.__numIndices, 2)
#self.init2DArr(self.__extremeVal, self.__numIndices, 2)