from Getaway import Getaway   
    
#The function fills the deviation or extreme values vector with the values that the user enters or with the default values of his choice.
#if it is the extreme values vector- devVec != None, and there will be a check that the extreme values are indeed greater than the deviation values
def __enterValues(valuesVec, values, devVec = None):
    for i in range (10):
        valuesVec.append([])
        for j in range (2):
            valuesVec[i].append([])
    
    for i in range (10):
        while True:
            print("<" +values[i]+">:")
            valuesVec[i][0], valuesVec[i][1] = input("   upper value: "), input("   lower value: ")
            
            #Input test - if not a positive numbers print message and ask for input again
            try:
                val1 = float(valuesVec[i][0])
                val2 = float(valuesVec[i][1])
                if val1 <= 0 or val2 <= 0:
                    print("Input must be a positive numbers, try again")
                    continue
                #if it's the extreme values vector- there will be a check that the extreme values are indeed greater than the deviation values
                if(devVec != None):
                    if valuesVec[i][0] <= devVec[i][0] or valuesVec[i][1] <= devVec[i][1]:
                        print("The extreme values must be greater than the deviation values, try again")                
                        continue
                break
            except ValueError:
                print("Input must be a positive numbers, try again")

def main():
    values = ["temperature","AmountOfRain","windSpeed","WindDirection","NearGroundTemperature","RelativeHumidity","TopGustSpeed","AtmosphericPressure","UpperWindDirection","GlobalRadiation"]
    matUpperDeviation=[]
    matExtremeValues=[]
    defult = input("To fill the deviation and extreme values vectors with defult values- press 0, If no- press 1: ")
    if(defult == "0"):
        matUpperDeviation = [[200.3,100.4],[300.1,500.66],[100.1,110],[100.5,500],[30,90.1],[500,900],[200.97,300],[200,300],[140.7,140],[140,140.5]]
        matExtremeValues = [[500.3,200.4],[400.1,700.99],[150.1,170],[300.50,1600],[90,110.1],[900,1100],[400.97,500],[300,400],[240,250],[150,160.5]]
    elif(defult == "1"): 
        print("--------Please input the deviation values:")        
        __enterValues(matUpperDeviation, values)
        print("\n--------Please input the extreme values:")        
        __enterValues(matExtremeValues, values, matUpperDeviation)   
    else:
        main()
    
    gw = Getaway(matUpperDeviation, matExtremeValues)
    gw.run_server()

if __name__ == "__main__":
    main()