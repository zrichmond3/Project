from conversions.convertMasterData import *
from conversions.convertWeeklyDemand import *


def stringToNumber(weeklyDemand, masterData):
    wDemand = convertWeeklyDemand(weeklyDemand)
    mData = convertMasterData(masterData)
    return wDemand, mData