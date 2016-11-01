#no imports

def determineOrderQuantity(self, data):

    #Data is the weeklyOutlookList that is returned in the masterData function
    orderQuantity = 0
    onHandOnOrderDemand = 0

    for row in data:
        onHandOnOrderDemand = row[8]+row[10]-row[9]#BeginningInventoryVolume+supply-retailerDemand
        if row[7]>onHandOnOrderDemand: #if forecastVariability is greater than onHandOnOrderDemand
            orderQuantity=row[7]-onHandOnOrderDemand #order quantity = forecastVariablity - onHandOnOrderDemand
        else:
            orderQuantity = 0

        sum= round(orderQuantity)+onHandOnOrderDemand #sum the last two rows for Chuck
        #line 18-20, adds value to our lis
        row.append(round(orderQuantity))
        row.append(onHandOnOrderDemand)
        row.append(sum)
    return data #this is a list in the form of [[weeklyOutlook 1],[weeklyOutlook 2],...,[weeklyOutlook N]]
#weeklyOutlookList, what each nested list looks like -> (see comment on line #23
#[sku, plant, avgAFRatio,sigmaAFRatio, forecastedDemand, muForecast, sigmaForecast, forecastVariability, beginningInventoryVolume, retailerDemand, supply, orderQTY, onhand+onOrder-Demand, sum]



