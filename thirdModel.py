from thirdModelProc1 import *
from weeklyDemand import *

def thirdModel(self, weeklyDemandData, masterData, weekNumber, allocationAmount):
    kValue=.99
    output = weeklyDemand(weeklyDemandData, weekNumber, kValue)
    print(output[0])
    #output = thirdModelProcess2()

    return output