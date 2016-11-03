def systemDOS(averageDOSList):

    sumOfBeginningInventoryForWeeKNumber = 0
    sumOfAverageDaysOfSupply = 0
    for j in averageDOSList:
        sumOfBeginningInventoryForWeeKNumber += j[7]
        sumOfAverageDaysOfSupply += j[3]
    value = sumOfBeginningInventoryForWeeKNumber/sumOfAverageDaysOfSupply
    return value, sumOfAverageDaysOfSupply
