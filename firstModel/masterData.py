#no imports

def masterData( data, weeklyOutlook, weekNumber):
#Below is what each row in the Master Data File should look lilke
#Day of Week, Week Number, Date Format, Plant Name, Material, Material Description, Retailer Demand, OOS quantity, BeginningInventoryVolume	, Supply

#Below is where the necessary calculations will happen
#week is a nested list from the list returned from weeklyDemand file
    for week in weeklyOutlook:
        beginningInventoryVolume = 0 #This allows the variable to be reset each iteration line 16-18
        retailerDemand = 0
        supply = 0
#Manipulate the data
        for row in data:
            if row[3] == week[1] and row[4] == week[0] and row[1]==(weekNumber-1): #matches the SKU in Master Data to SKU in weeklyOutlook and Plant in Master Data to weeklyOutlook, all logic below is for this match
                if row[0]=="Saturday":
                    beginningInventoryVolume = row[8] #Sets the beginningInventoryVolume
                retailerDemand += row[6] #sums Retailer Demand
                supply += row[9] #sums Supply
        #lines 28-30 appends the data created in line 24-26 to the list we returned in weeklyDemand that is a parameter for this function
        week.append(beginningInventoryVolume)
        week.append(retailerDemand)
        week.append(supply)
    return weeklyOutlook #this is a list in the form of [[weeklyOutlook 1],[weeklyOutlook 2],...,[weeklyOutlook N]]
#weeklyOutlookList, what each nested list looks like -> [sku, plant, avgAFRatio,sigmaAFRatio, forecastedDemand, muForecast, sigmaForecast, forecastVariability, beginningInventoryVolume, retailerDemand, supply]


