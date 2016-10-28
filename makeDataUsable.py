#Fix Data Manipluation

def makeDataUsable(self):

    #print(self.dataFirstSet) WORKS!
    self.usableDataDict = {}
    for row in (1, len(self.dataFirstSet)):
        if int(self.dataFirstSet[row][1]) == 1:
            createKey = self.dataFirstSet[row][0] +"-"+self.dataFirstSet[row][2]+"-"+self.dataFirstSet[row][3]
            self.usableDataDict[createKey] = [self.dataFirstSet[row][5], self.dataFirstSet[row][6], self.dataFirstSet[row][7]]
    print(self.usableDataDict)
    return