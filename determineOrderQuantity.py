def determineOrderQuantity(self, data):
# sku, plant, avgAFRatio,sigmaAFRatio, forecastedDemand, muForecast, sigmaForecast, forecastVariability, beginningInventoryVolume, retailerDemand, supply, orderQTY, onhand+onOrder-Demand
    orderQuantity = 0
    onHandOnOrderDemand = 0
    for row in data:
        onHandOnOrderDemand = row[8]+row[10]-row[9]
        if row[7]>onHandOnOrderDemand:
            orderQuantity=row[7]-onHandOnOrderDemand
        else:
            orderQuantity = 0
        sum= round(orderQuantity)+onHandOnOrderDemand
        row.append(round(orderQuantity))
        row.append(onHandOnOrderDemand)
        row.append(sum)
    return data