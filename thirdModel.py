

from scipy.stats import norm
from numpy import mean, std
import warnings


def thirdModel( weeklyDemandData, masterData, weekNumber, allocationAmount):
    kValue=.99
    skuList =[]
    plantList =[]
    output =[]
    for row in weeklyDemandData: #iteration through the data and to make it usable
        if float(row[4]) != 0: #Prevents dividing by 0 for AF Ratio
            afRatio = row[3]/row[4] #creates AF Ratio
            row.append(afRatio) #appends data to add the AF Ratio
        else: #if Forecast is 0 then append data to add 0
            row.append(0)
        if row[1] not in plantList: #adds all the plants to the Plant List
            plantList.append(row[1])
        if row[2] not in skuList: #adds all the SKUs to the Sku List
            skuList.append(row[2])


    for sku in skuList:
        for plant in plantList:
            afRatioList = [] #Placing this list here allows for it to be resetted for each SKU Plant combo
            for row in weeklyDemandData:
                weeklyDemandPlant = row[1]
                weeklyDemandSKU = row[2]
                weeklyDemandWeekNumber = row[0]
                if plant == weeklyDemandPlant and sku == weeklyDemandSKU and weeklyDemandWeekNumber<=(weekNumber-2): #appends afRatioList for the correct SKU Plant combo
                    afRatioList.append(row[5])
                if plant == weeklyDemandPlant and sku == weeklyDemandSKU and weeklyDemandWeekNumber == weekNumber: #grabs the correct forecasted demand for calculations
                    forecastedDemand = row[4]
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                avgAFRatio = mean(afRatioList)
                sigmaAFRatio = std(afRatioList)
                muForecast = forecastedDemand*avgAFRatio
                sigmaForecast = forecastedDemand*sigmaAFRatio
                forecastVariability = norm.ppf(kValue, loc=muForecast, scale=sigmaForecast)
            #The above is the equivalent norm.inv function in Excel from SciPy
            weeklyOutlook = [sku, plant, avgAFRatio,weekNumber, forecastedDemand, muForecast, sigmaForecast, forecastVariability]
            #The above creates a list and based on line 42, if this list is not already in the weeklyOutlookList then it is added
            if weeklyOutlook not in output:
                output.append(weeklyOutlook)

    for sku in skuList:
        for plant in plantList:
            for row in output:
                weeklyDemandPlant = row[1]
                weeklyDemandSKU = row[0]
                weeklyDemandWeekNumber = row[3]
                if plant == weeklyDemandPlant and sku == weeklyDemandSKU and weeklyDemandWeekNumber == weekNumber:
                    weeklyDemandForecast = row[4]
                    averageDOS = weeklyDemandForecast / 6
                    row.append(averageDOS)

    for arrayList in output:
        beginningInventoryVolume = 0
        retailerDemand = 0
        supply = 0
        averageDOSListPlant = arrayList[1]
        averageDOSListSKU = arrayList[0]
        for row in masterData:
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
    print(output[0])
    for row in output:
        beginningInventoryVolume=row[9]
        supply=row[10]
        retailerDemand=row[11]
        beginningInventoryWeekNumber = beginningInventoryVolume+supply-retailerDemand
        if beginningInventoryWeekNumber <0:
            beginningInventoryWeekNumber=0
        row.append(beginningInventoryWeekNumber)

    sumOfBeginningInventoryForWeeKNumber = 0
    sumOfAverageDaysOfSupply = 0
    for row in output:
        sumOfBeginningInventoryForWeeKNumber += row[12]
        sumOfAverageDaysOfSupply += row[8]
    print("BIWK",sumOfBeginningInventoryForWeeKNumber)
    print("ADOS", sumOfAverageDaysOfSupply)
    systemDOS = sumOfBeginningInventoryForWeeKNumber / sumOfAverageDaysOfSupply
    for i in output:
        fairShare = i[8]*systemDOS
        i.append(fairShare)
    for d in output:
        underOver= d[13]-d[12]
        d.append(underOver)
    for row in output:
        rawAllocation= (row[8]/systemDOS)*allocationAmount
        row.append(rawAllocation)
        netSuppy = rawAllocation + row[14]
        if netSuppy < 0:
            netSuppy = 0
        row.append(netSuppy)
    return output
