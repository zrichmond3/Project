from scipy.stats import norm

#This is a function that determines the expected stockouts
def expectedOOS(self, data):
    for row in data:
        mu = row[5]
        sigma = row[6]
        q = row[7]
        z = (q-mu)/q
        standardNormalLoss = (norm.pdf(z, loc=0, scale=1))-z*(norm.sf(z,loc=0, scale=1))
        expOOS = standardNormalLoss*sigma
        row.append(expOOS)
    return data

