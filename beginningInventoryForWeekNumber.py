def beginningInventoryForWeekNumber(averageDOSList, mData, weekNumber):
    for arrayList in averageDOSList:
        beginningInventoryVolume = 0
        retailerDemand = 0
        supply = 0
        averageDOSListPlant = arrayList[0]
        averageDOSListSKU = arrayList[2]
        for row in mData:
            mDataPlant=row[3]
            mDataSKU=row[4]
            mDataWeekNumber=row[1]
            if mDataPlant == averageDOSListPlant and mDataSKU == averageDOSListSKU and mDataWeekNumber == (weekNumber - 1):
                if row[0] == "Saturday":
                    beginningInventoryVolume = row[8]
                retailerDemand += row[6]
                supply += row[9]
        arrayList.append(beginningInventoryVolume)
        arrayList.append(retailerDemand)
        arrayList.append(supply)
    for row in averageDOSList:
        beginningInventoryVolume=row[4]
        supply=row[6]
        retailerDemand=row[5]
        beginningInventoryWeekNumber = beginningInventoryVolume+supply-retailerDemand
        if beginningInventoryWeekNumber <0:
            beginningInventoryWeekNumber=0
        row.append(beginningInventoryWeekNumber)
    return averageDOSList