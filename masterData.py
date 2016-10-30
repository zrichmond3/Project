def masterData(self, data):
    self.masterDataDict = {}
    for row in data:
#Day of Week, Week Number, Date Format, Plant Name, Material, Material Description, Retailer Demand, OOS quantity, BeginningInventoryVolume, Supply
        createKey = row[1] +"-"+row[3]
        self.masterDataDict[createKey] = [row[0], row[4], row[6], row[7], row[8], row[9]]
    return None