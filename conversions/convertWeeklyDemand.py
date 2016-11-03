
def convertWeeklyDemand( data):

    for row in data: #iteration through the data and to make it usable
        row[3]=float(row[3]) #Weekly Demand - change from string to a float
        row[4]=float(row[4]) #Forecast - change from string to a float
        row[0]=int(row[0]) #Week Number - Change from string to an int
    return data