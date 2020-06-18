import socket
import struct
import ctypes
from Mat import Mat
from Delta import Deltas

class Getaway:#Additions to original class
    def __init__(self, deviationVal, extremeVal):
        self.__numSensors = 1000
        self.__numIndices = 10
        
        # In these arrays - lower value in index 0, upper value in index 1
        self.__thresholdVal = []
        self.__deviationVal = deviationVal
        self.__extremeVal = extremeVal         
        
        self.__upMat = None
        self.__refMat = None
        self.__deltasVec = Deltas() 
        
        self.__client_socket = None
        
        self.__msgRcvNum = 0
    
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
        #self.__upMat = Mat(None, self.__numSensors, self.__numIndices + 1, self.__thresholdVal)
        self.__upMat = Mat(None, self.__numSensors, self.__numIndices, self.__thresholdVal)        
        self.__refMat = Mat(self.__upMat)
        

    # The function compress two integer numbers to one short variable
    def __compressIndexes(self, indexX, indexY):
        compressedVal = ctypes.c_ushort((indexX << 8) | indexY)
        return compressedVal;
    
    # The function receives the sensor message in the string, and updates the appropriate row in the update matrix
    def __handlesData(self, sensorData):
        tempVec = sensorData[0:len(sensorData)].split(",")
        row = []
        i = 0
        for i in range (self.__numIndices):
            row.append(float(tempVec[i]))
        #row.append(self.__compressIndexes(int(tempVec[i+1]), int(tempVec[i+2])))         
        rowIndex = int(tempVec[i+3])
        self.__upMat.setRow(rowIndex, row)
    
    
    def __matsCompare(self):
        __numOfChanges = 0
        __maxChanges = 6000
       # __maxChanges = 1
        
        #chcking if need to send all the matrix
        for i in range(self.__numSensors):
            for j in range(self.__numIndices):
                if (self.__deviationVal[j][0] <= self.__upMat.getMat()[i][j] - self.__refMat.getMat()[i][j]) or (self.__deviationVal[j][1] <= self.__refMat.getMat()[i][j] - self.__upMat.getMat()[i][j]):
                    __numOfChanges += 1
                    if (__numOfChanges>=__maxChanges):
                        self.__refMat.setMat(self.__upMat.getMat())
                        #send mat
                        self.__sendToCloud(self.__refMat.getMatAsStr(), False)
    
        for i in range(self.__numSensors):
            for j in range(self.__numIndices):
                #Testing the Critical Values
                if (self.__extremeVal[j][0]<=self.__upMat.getMat()[i][j]-self.__refMat.getMat()[i][j]) or (self.__extremeVal[j][1]<=self.__refMat.getMat()[i][j]-self.__upMat.getMat()[i][j]):
                    print("we found extreme value")
                    self.__refMat.getMat()[i][j] = self.__upMat.getMat()[i][j] #update the reference matrix
                    if(self.__deltasVec.addDelta(self.__compressIndexes(i,j).value,self.__refMat.getMat()[i][j]) == False):
                        #send delta
                        self.__sendToCloud(self.__deltasVec.getAsString(), True)
                        self.__deltasVec.addDelta(self.__compressIndexes(i,j).value,self.__refMat.getMat()[i][j])
                    #send delta anyway
                    self.__sendToCloud(self.__deltasVec.getAsString(), True)
                    
                #Checking deviation values
                elif (self.__deviationVal[j][0]<=self.__upMat.getMat()[i][j]-self.__refMat.getMat()[i][j]) or (self.__deviationVal[j][1]<=self.__refMat.getMat()[i][j]-self.__upMat.getMat()[i][j]):
                    print("i: "+str(i)+" ,j: "+str(j))
                    self.__refMat.getMat()[i][j] = self.__upMat.getMat()[i][j] #update the reference matrix
                    if(self.__deltasVec.addDelta(self.__compressIndexes(i,j).value,self.__refMat.getMat()[i][j]) == False):
                        #send delta
                        self.__sendToCloud(self.__deltasVec.getAsString(), True)
                        self.__deltasVec.addDelta(self.__compressIndexes(i,j).value,self.__refMat.getMat()[i][j])
                        
    def __sendToCloud(self, msg, clearDeltas):
        self.__client_socket.send(msg.encode())#maby delete encode
        if(clearDeltas):
            self.__deltasVec.clearDeltas()        
    
    def __run_client(self):
        self.__client_socket = socket.socket()
        self.__client_socket.connect(('127.0.0.1',65521))
        
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
        
        self.__run_client()
        #in the begining, need we send something to the cloud?
        #self.__client_socket.send(str.encode());
        #self.__client_socket.close()                    
        
        while True: # Receiving updates from sensors
            sensorData = conn.recv(1024).decode()
            print ("***** The message received:",sensorData," *****")
            self.__handlesData(sensorData)
            ###########################################################
            print("\n************************************")
            print("line 0: ",self.__upMat.getRow(0),"\n")
            print("ref line 0: ",self.__refMat.getRow(0),"\n")            
            self.__matsCompare()
            ###########################################################

        conn.close()
        
              