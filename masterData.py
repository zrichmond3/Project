def masterData(data, outputList, weekNumber):


    for item in outputList:
        beginningInventoryVolume = 0
        retailerDemand = 0
        supply = 0
        for row in data:
            if row[3] == item[1] and row[4] == item[0] and row[1]==(weekNumber-1): #matches the SKU in Master Data to SKU in outputList and Plant in Master Data to outputList
                if row[0]=="Saturday":
                    beginningInventoryVolume = row[8] #Gets the beginningInventoryVolume
                retailerDemand += row[6] #Sums Retailer Demand
                supply += row[9] #Sums Supply
        #lines 15-17 appends the data created in line 11-13 to outputList
        item.append(beginningInventoryVolume)
        item.append(retailerDemand)
        item.append(supply)
    return outputList #this is a list in the form of [[outputList 1],[outputList 2],...,[outputList N]]
#outputList, what each item looks like -> [sku, plant, avgAFRatio,sigmaAFRatio, forecastedDemand, muForecast, sigmaForecast, forecastVariability, beginningInventoryVolume, retailerDemand, supply]


