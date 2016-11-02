#import statistical packages
from statistics import *
from scipy.stats import norm

def weeklyDemand(self, data, weekNumber, kValue):

    skuList =[] #Sku List, need it for triple for loop below
    plantList =[] #Plant List, need it for triple for loop below
    weeklyOutlookList = [] #This list will be returned
    for row in data: #iteration through the data and to make it usable
        # row[3]=float(row[3]) #Weekly Demand - change from string to a float
        # row[4]=float(row[4]) #Forecast - change from string to a float
        # row[0]=int(row[0]) #Week Number - Change from string to an int
        if float(row[4]) != 0: #Prevents dividing by 0 for AF Ratio
            afRatio = row[3]/row[4] #creates AF Ratio
            row.append(afRatio) #appends data to add the AF Ratio
        else: #if Forecast is 0 then append data to add 0
            row.append(0)
        if row[1] not in plantList: #adds all the plants to the Plant List
            plantList.append(row[1])
        if row[2] not in skuList: #adds all the SKUs to the Sku List
            skuList.append(row[2])

#At this point the the data as been prepared to make all the necessary calculations
    for sku in skuList:
        for plant in plantList:
            afRatioList = [] #Placing this list here allows for it to be resetted for each SKU Plant combo
            for row in data:
                if plant == row[1] and sku == row[2] and row[0]<=(weekNumber-2): #appends afRatioList for the correct SKU Plant combo
                    afRatioList.append(row[5])
                if plant == row[1] and sku == row[2] and row[0] == weekNumber: #grabs the correct forecasted demand for calculations
                    forecastedDemand = row[4]
            avgAFRatio = mean(afRatioList) #finds the mean of the afRatioList
            sigmaAFRatio = pstdev(afRatioList) #finds the standard deviation of the afRatioList
            muForecast = forecastedDemand*avgAFRatio #this should be obvious based on line 34
            sigmaForecast = forecastedDemand*sigmaAFRatio #this should be obvious based on line 35
            forecastVariability = norm.ppf(kValue, loc=muForecast, scale=sigmaForecast)
            #The above is the equivalent norm.inv function in Excel from SciPy
            weeklyOutlook = [sku, plant, avgAFRatio,sigmaAFRatio, forecastedDemand, muForecast, sigmaForecast, forecastVariability]
            #The above creates a list and based on line 42, if this list is not already in the weeklyOutlookList then it is added
            if weeklyOutlook not in weeklyOutlookList:
                weeklyOutlookList.append(weeklyOutlook)
    return weeklyOutlookList #this is a list in the form of [[weeklyOutlook 1],[weeklyOutlook 2],...,[weeklyOutlook N]]
#weeklyOutlookList, what each nested list looks like -> [sku, plant, avgAFRatio,sigmaAFRatio, forecastedDemand, muForecast, sigmaForecast, forecastVariability]