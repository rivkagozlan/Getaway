from Getaway import Getaway

class GWmanager:
    def __init__(self):
        self.__values = ["temperature","AmountOfRain","windSpeed","WindDirection","NearGroundTemperature","RelativeHumidity","TopGustSpeed","AtmosphericPressure","UpperWindDirection","GlobalRadiation"]
        self.deviationValues()
        self.extremeValues()

    def deviationValues(self):
        matUpperDeviation=[]
        matExtremeValues=[]
        
        defult = input("To fill the deviation values vector with defult values- press 0, If no- press 1")
        
        if(input == 0):
            matUpperDeviation = [[10,40],[14,20],[33,70.9],[0.5,5],[3,9.1],[5,9],[66,100],[33,77],[68.7,200],[11,68]]
            return
            
        for i in range (10):
            matUpperDeviation.append([])
            for j in range (2):
                matUpperDeviation[i].append([])
    
        for i in range (10):    
            for j in range (2):
                if j==0:
                    matUpperDeviation[i][j]=input("Please input an upper deviation values of " +self.__values[i])
                elif j==1:
                    matUpperDeviation[i][j]=input("Please input an lower deviation value of " +self.__values[i])                
    
    def extremeValues(self):
        defult = input("To fill the deviation values vector with defult values- press 0, If no- press 1")
        
        if(input == 1):
            matUpperDeviation = [[10,40],[14,20],[33,70.9],[0.5,5],[3,9.1],[5,9],[66,100],[33,77],[68.7,200],[11,68]]
            return
        
        for i in range (10):
            matExtremeValues.append([])
            for j in range (2):
                matExtremeValues[i].append([])
    
        for i in range (10):    
            for j in range (2):
                if j==0:
                    matUpperDeviation[i][j]=input("Please input an upper extreme values of " +self.__values[i])
                elif j==1:
                    matUpperDeviation[i][j]=input("Please input an lower Extreme value of " +self.__values[i])
    

#gwM = GWmanager()
