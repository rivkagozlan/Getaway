from Getaway import Getaway             
    
#The function fills the deviation or extreme values vector with the values that the user enters or with the default values of his choice.
def enterValues(valuesVec, values):
    for i in range (10):
        valuesVec.append([])
        for j in range (2):
            valuesVec[i].append([])
    
    for i in range (10):
        print("<" +values[i]+">:")
        valuesVec[i][0], valuesVec[i][1] = input("   upper value: "), input("   lower value: ")
            

def main():
    values = ["temperature","AmountOfRain","windSpeed","WindDirection","NearGroundTemperature","RelativeHumidity","TopGustSpeed","AtmosphericPressure","UpperWindDirection","GlobalRadiation"]
    matUpperDeviation=[]
    matExtremeValues=[]
    defult = input("To fill the deviation and extreme values vectors with defult values- press 0, If no- press 1: ")
    if(defult == "0"):
        matUpperDeviation = [[2.3,1.4],[3.1,5.66],[10.1,11],[0.5,5],[3,9.1],[5,9],[2.97,3],[2,3],[3.7,2],[4,4.5]]
        matExtremeValues = [[5.3,2.4],[4.1,7.99],[15.1,17],[3.5,16],[9,11.1],[9,11],[4.97,5],[3,4],[6.7,6],[5,6.5]]
    elif(defult == "1"): 
        print("--------Please input the deviation values:")        
        enterValues(matUpperDeviation, values)
        print("\n--------Please input the extreme values:")        
        enterValues(matExtremeValues, values)        
    else:
        main()
    
    gw = Getaway(matUpperDeviation, matExtremeValues)
    gw.run_server()

if __name__ == "__main__":
    main()