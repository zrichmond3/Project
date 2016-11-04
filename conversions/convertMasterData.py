def convertMasterData( data):

    for row in data:
        row[1] = int(row[1]) #changes Week Number from string to int
        row[6] = float(row[6]) #changes Retailer Demand from string to float
        row[7] = float(row[7]) #changes OOS Quantity from string to float
        row[8] = float(row[8]) #changes BeginningInventoryVolume from string to float
        row[9] = float(row[9]) #changes Supply from string to float
    return data