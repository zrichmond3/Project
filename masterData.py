def masterData(self, data, weeklyOutlook, weekNumber):
#sku, plant, avgAFRatio,sigmaAFRatio, forecastedDemand, muForecast, sigmaForecast, forecastVariability
#Day of Week, Week Number, Date Format, Plant Name, Material, Material Description, Retailer Demand, OOS quantity, BeginningInventoryVolume	, Supply
    del data[0]
    for row in data:
        row[1] = int(row[1])
        row[6] = float(row[6])
        row[7] = float(row[7])
        row[8] = float(row[8])
        row[9] = float(row[9])

    for week in weeklyOutlook:
        beginningInventoryVolume = 0
        retailerDemand = 0
        supply = 0
        for row in data:
            if row[3] == week[1] and row[4] == week[0] and row[1]==(weekNumber-1):
                if row[0]=="Saturday":
                    beginningInventoryVolume = row[8]
                retailerDemand += row[6]
                supply += row[9]
        week.append(beginningInventoryVolume)
        week.append(retailerDemand)
        week.append(supply)
    return weeklyOutlook




