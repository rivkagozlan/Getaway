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
        
        self.__msgRcvNum = 0 #Summarize the number of messages received up to the total number of sensors
    
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
        rowIndex = int(tempVec[i+3])
        self.__upMat.setRow(rowIndex, row)
     
    def __matsCompare(self):
        __numOfChanges = 0
        __maxChanges = 6000
        __exVal = False 
        
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
                if (__exVal == False and self.__extremeVal[j][0]<=self.__upMat.getMat()[i][j]-self.__refMat.getMat()[i][j]) or (self.__extremeVal[j][1]<=self.__refMat.getMat()[i][j]-self.__upMat.getMat()[i][j]):
                    print("we found extreme value")
                    __exVal = True
                    
                #Checking deviation values
                if (self.__deviationVal[j][0]<=self.__upMat.getMat()[i][j]-self.__refMat.getMat()[i][j]) or (self.__deviationVal[j][1]<=self.__refMat.getMat()[i][j]-self.__upMat.getMat()[i][j]):
                    print("------ Delta added for index: ",i,",",j," change from ",self.__refMat.getMat()[i][j]," to ",self.__upMat.getMat()[i][j]," ------")
                    self.__refMat.getMat()[i][j] = self.__upMat.getMat()[i][j] #update the reference matrix
                    if(self.__deltasVec.addDelta(self.__compressIndexes(i,j).value,self.__refMat.getMat()[i][j]) == False):
                        #send delta
                        print("sent:  "+self.__deltasVec.getAsString()+"\n")
                        self.__sendToCloud(self.__deltasVec.getAsString(), True)
                        self.__deltasVec.addDelta(self.__compressIndexes(i,j).value,self.__refMat.getMat()[i][j])
                        
        #If we found extreme value- we send delta anyway       
        if(__exVal == True):
            print("sent:  "+self.__deltasVec.getAsString()+"\n")
            self.__sendToCloud(self.__deltasVec.getAsString(), True)
                        
    def __sendToCloud(self, msg, clearDeltas):
        self.__client_socket.send(msg.encode())
        if(clearDeltas):
            self.__deltasVec.clearDeltas()    
        print("*********************************************sent")
        
    
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
        print("******************************************")
        print ("Received:",thresholdVal_str)        
        self.__thresholdVal_Mats_init(thresholdVal_str)
        
        self.__run_client()
        #Sending the initial matrix to the cloud
        self.__sendToCloud(self.__refMat.getMatAsStr(), False)
        
        while True: # Receiving updates from sensors
            sensorData = conn.recv(1024).decode()
            self.__msgRcvNum += 1
            print("******************************************")
            print ("Received:",sensorData)
            self.__handlesData(sensorData)
            
            #Comparing the matrices after receiving messages as the number of sensors
            #if(self.__msgRcvNum == self.__numSensors):
            if(self.__msgRcvNum == 20):
                self.__matsCompare()
                self.__msgRcvNum = 0
            

        conn.close()
        
              