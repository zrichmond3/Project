def weeklyDemand(self, data):

    self.weeklyDemandDict = {}
    for row in data:
         #Week Number, Plant Name, Material, Weekly Demand, Forecast
        createKey = row[0] +"-"+row[1]
        self.weeklyDemandDict[createKey] = [row[2], row[3], row[4]]
    return None