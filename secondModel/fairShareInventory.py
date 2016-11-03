def fairShare(averageDOSList, systemDaysOfSupply):
    for row in averageDOSList:
        averageDOS = row[3]
        fairShareInventory = averageDOS * systemDaysOfSupply
        row.append(fairShareInventory)
    return averageDOSList