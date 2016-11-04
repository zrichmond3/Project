from beginningInventoryForWeekNumber import *
from fairShareInventory import *
from systemDOS import *


def averageDaysOfSupply(self, weeklyDemand, mData, weekNumber,allocationAmount, sDOS):
    skuList =[] #Sku List, need it for triple for loop below
    plantList =[] #Plant List, need it for triple for loop below
    averageDOSList = [] #This list will be returned
    sumOfADS =0
    for row in weeklyDemand: #iteration through the data and to make it usable
        if row[1] not in plantList: #adds all the plants to the Plant List
            plantList.append(row[1])
        if row[2] not in skuList: #adds all the SKUs to the Sku List
            skuList.append(row[2])

    for sku in skuList:
        for plant in plantList:
            for row in weeklyDemand:
                weeklyDemandPlant = row[1]
                weeklyDemandSKU = row[2]
                weeklyDemandWeekNumber = row[0]
                if plant == weeklyDemandPlant and sku == weeklyDemandSKU and weeklyDemandWeekNumber== weekNumber:
                    weeklyDemandForecast = row[4]
                    averageDOS = weeklyDemandForecast/5
                    nestedList = [plant, weekNumber, sku, averageDOS]
                    averageDOSList.append(nestedList)

    averageDOSList = beginningInventoryForWeekNumber(averageDOSList, mData, weekNumber)

    if self.sDOS == 0:
        self.sDOS, sumOfADS = systemDOS(averageDOSList)
        print(self.sDOS)
        print("self.sDOS is equal to zero")
    else:
        print("else statement hi")
        for i in averageDOSList:
            sumOfADS += i[3]


    print(self.sDOS)
    print(sumOfADS)
    averageDOSList = fairShare(averageDOSList, self.sDOS)

    #Place in functionblah
    for d in averageDOSList:
        underOver= d[8]-d[7]
        d.append(underOver)
    for row in averageDOSList:
        rawAllocation= (row[3]/sumOfADS)*allocationAmount
        row.append(rawAllocation)
        netSuppy = rawAllocation + row[9]
        if netSuppy < 0:
            netSuppy = 0
        row.append(netSuppy)



    return averageDOSList