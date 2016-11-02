

def averageDaysOfSupply(self, weeklyDemand, mData, weekNumber,allocationAmount):
    skuList =[] #Sku List, need it for triple for loop below
    plantList =[] #Plant List, need it for triple for loop below
    averageDOSList = [] #This list will be returned
    for row in weeklyDemand: #iteration through the data and to make it usable
        if row[1] not in plantList: #adds all the plants to the Plant List
            plantList.append(row[1])
        if row[2] not in skuList: #adds all the SKUs to the Sku List
            skuList.append(row[2])

    for sku in skuList:
        for plant in plantList:
            for row in weeklyDemand:
                if plant == row[1] and sku == row[2] and row[0]== weekNumber:
                    averageDOS = row[4]/5
                    nestedList = [plant, weekNumber, sku, averageDOS]
                    averageDOSList.append(nestedList)
    print(averageDOSList[0])
    print(mData[0])

    for week in averageDOSList:
        beginningInventoryVolume = 0
        retailerDemand = 0
        supply = 0

        for row in mData:
            if row[3] == week[0] and row[4] == week[2] and row[1] == (weekNumber - 1):
                if row[0] == "Saturday":
                    beginningInventoryVolume = row[8]
                retailerDemand += row[6]
                supply += row[9]
        week.append(beginningInventoryVolume)
        week.append(retailerDemand)
        week.append(supply)
    for i in averageDOSList:
        beginningInventoryWeekNumber = i[4]+i[6]-i[5]#BeginningInventoryVolume+supply-retailerDemand
        if beginningInventoryWeekNumber <0:
            beginningInventoryWeekNumber=0
        i.append(beginningInventoryWeekNumber)
    print(averageDOSList[0])

    sumBIWK=0
    sumADS=0
    for j in averageDOSList:
        sumBIWK+=j[7]
        sumADS+=j[3]

    systemDaysOfSupply=sumBIWK/sumADS

    for k in averageDOSList:
        fairShareInventory= k[3]*systemDaysOfSupply
        k.append(fairShareInventory)
    for d in averageDOSList:
        underOver= d[8]-d[7]
        d.append(underOver)
    for row in averageDOSList:
        rawAllocation= (row[3]/systemDaysOfSupply)*allocationAmount
        row.append(rawAllocation)
        netSuppy = rawAllocation + row[9]
        row.append(netSuppy)



    return averageDOSList