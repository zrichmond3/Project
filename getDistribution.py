def getDistribution(self):
    DistributionDictionary = {"Distribution": ["Mean Formula", "Sigma Formula"],
                              "Normal": ["Mean Formula", "Sigma Formula"],
                              "Lognormal": ["Mean Formula", "Sigma Formula"]}
    self.meanFormula = []
    self.sigmaFormula = []
    for distKey in DistributionDictionary.keys():
        if distKey == self.distribution:
            self.meanFormula = DistributionDictionary[distKey][0]
            self.sigmaFormula = DistributionDictionary[distKey][1]
    print(self.meanFormula, self.sigmaFormula)