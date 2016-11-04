#import statistical packages
from scipy.stats import norm
from numpy import mean, std
import warnings

def weeklyDemand(data, weekNumber, kValue):

    skuList =[] #Creates SKU list for iteration below
    plantList =[] #Creates Plant List for iteration below
    outputList = [] #Creates the Ouput List - this is returned
    for row in data: #For loop iterates through the data, which is a nested list --> [[row1],[row2],...[rowN]]
        if float(row[4]) != 0: #Prevents dividing by 0 for AF Ratio
            afRatio = row[3]/row[4] #Creates AF Ratio
            row.append(afRatio) #appends data to add the AF Ratio
        else: #if Forecast is 0 then append data to add 0
            row.append(0)
        if row[1] not in plantList: #adds all the plants in data to the Plant List
            plantList.append(row[1])
        if row[2] not in skuList: #adds all the SKUs in data to the Sku List
            skuList.append(row[2])

#The lines 8-20 preps the data for all the necessary calculations that will be made in lines 23-49
    for sku in skuList:
        for plant in plantList:
            afRatioList = [] #Placing this list here allows for it to be resetted for each SKU Plant combo
            for row in data:
                weeklyDemandPlant = row[1]
                weeklyDemandSKU = row[2]
                weeklyDemandWeekNumber = row[0]
                if plant == weeklyDemandPlant and sku == weeklyDemandSKU and weeklyDemandWeekNumber<=(weekNumber-2): #appends afRatioList for the correct SKU Plant combo
                    afRatioList.append(row[5])
                if plant == weeklyDemandPlant and sku == weeklyDemandSKU and weeklyDemandWeekNumber == weekNumber: #grabs the correct forecasted demand for calculations
                    forecastedDemand = row[4]
                else:
                    forecastedDemand = 0
            #lines 37-38 remove runtime warnings from the python console
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                avgAFRatio = mean(afRatioList) #finds the mean of the afRatioList
                sigmaAFRatio = std(afRatioList) #finds the standard deviation of the afRatioList
                muForecast = forecastedDemand*avgAFRatio
                sigmaForecast = forecastedDemand*sigmaAFRatio
                forecastVariability = norm.ppf(kValue, loc=muForecast, scale=sigmaForecast) #This is the equivalent to Excel's NORM.INV
            rowInOutputList = [sku, plant, avgAFRatio,sigmaAFRatio, forecastedDemand, muForecast, sigmaForecast, forecastVariability]
            if rowInOutputList not in outputList:
                outputList.append(rowInOutputList)
    return outputList #this is a list in the form of [[rowInOutputList 1],[rowInOutputList 2],...,[rowInOutputList N]]
#outputList, what each rowInOutputList looks like -> [sku, plant, avgAFRatio,sigmaAFRatio, forecastedDemand, muForecast, sigmaForecast, forecastVariability]

