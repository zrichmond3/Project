
from statistics import *
from scipy.stats import norm
def weeklyDemand(self, data):
    del data[0]
    skuList =[]
    plantList =[]
    weeklyOutlookList = []
    for row in data:
        row[3]=float(row[3])
        row[4]=float(row[4])
        row[0]=int(row[0])
        if float(row[4]) != 0:
            afRatio = row[3]/row[4]
            row.append(afRatio)
        else:
            row.append(0)
        if row[1] not in plantList:
            plantList.append(row[1])
        if row[2] not in skuList:
            skuList.append(row[2])
    for sku in skuList:
        for plant in plantList:
            afRatioList = []
            sigmaList = []
            demandList = []
            for row in data:
                if plant == row[1] and sku == row[2] and row[0]<=29:
                    afRatioList.append(row[5])
                if plant == row[1] and sku == row[2] and row[0] == 31:
                    forecastedDemand = row[4]
            avgAFRatio = mean(afRatioList)
            sigmaAFRatio = pstdev(afRatioList)
            muForecast = forecastedDemand*avgAFRatio
            sigmaForecast = forecastedDemand*sigmaAFRatio
            forecastVariability = norm.ppf(.98, loc=muForecast, scale=sigmaForecast)
            weeklyOutlook = [sku, plant, avgAFRatio,sigmaAFRatio, forecastedDemand, muForecast, sigmaForecast, forecastVariability]
            if weeklyOutlook not in weeklyOutlookList:
                weeklyOutlookList.append(weeklyOutlook)

#push












         #Week Number, Plant Name, Material, Weekly Demand, Forecast, A/F
        #createKey = row[0] +"-"+row[1]
        #self.weeklyDemandDict[createKey] = [row[2], row[3], row[4]]

