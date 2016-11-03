# This code is broken down into individual files that do a specific task.
# The code also follows camelCase coding for all naming conventions.
# SciPy, Statistics, cx_Freeze, and all other packages are imported through PyCharm.
# If a user clones the this project and runs it individual, all files will need to be in the same folder and all imports will need to be installed relevative to their operating system

#Imports
import csv
import urllib.request
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from conversions.stringToNumber import *
from expectedOOS import *
from firstModel.masterData import *
from secondModel.averageDaysOfSupply import *
from secondModel.determineOrderQuantity import *
from thirdModel import *
from firstModel.weeklyDemand import *

#Class created to run GUI
class simulation:
    def __init__(self,w):

#Create the frames to pack individual frames inside the GUI for better organization
        self.myTOPFrame = Frame(w)
        self.myTOPFrame.pack(side=TOP)
        self.myLeftFrame = Frame(w)
        self.myLeftFrame.pack(side=LEFT)

#Create frames within the main frames above for organization
        self.left0 = Frame(self.myLeftFrame)
        self.left0.pack()
        self.left1 = Frame(self.myLeftFrame)
        self.left1.pack()
        self.left2 = Frame(self.myLeftFrame)
        self.left2.pack()
        self.left3 = Frame(self.myLeftFrame)
        self.left3.pack()

#Get GT logo, no real value, just thought it looked nice
        url = "http://w4aql.gtorg.gatech.edu/images/buzzzap.gif"
        response = urllib.request.urlopen(url)
        myPicture = response.read()
        import base64
        b64_data = base64.encodebytes(myPicture)
        self.mainImage = PhotoImage(data=b64_data)
#These values can be used throughout the code because they are global
        self.totalOrders = 0
        self.kValue = .999
        self.switch = True
        self.iteration = 0
#Image
        self.photoLabel = Label(self.myTOPFrame, image=self.mainImage)
        self.photoLabel.grid(row=0, column=0)
#Load Buttons
        self.loadFirstInputCSVFile = Button(self.left1, width=78, text="Load Weekly Demand", command=self.loadFirstCSVclicked).grid(row=0, column=0, sticky=E+W)
        self.loadSecondInputCSVFile = Button(self.left1, width=78, text="Load Master Data", command=self.loadSecondCSVclicked).grid(row=1, column=0, sticky=E+W)

#Week Number Variable and Week Number Entry
        self.entryWeekNumber = StringVar()
        self.weekNumber = Label(self.left2, text="Week Number:").grid(row=0, column=0, sticky=E)
        self.weekNumber = Entry(self.left2, width=60, state=NORMAL, text=self.entryWeekNumber).grid(row=0, column=1, sticky=W)

#Allocation Variable and Allocation Entry
        self.entryAllocationAmount = StringVar()
        self.allocationAmount = Label(self.left2, text="Allocation Amount:").grid(row=1, column=0, sticky=E)
        self.allocationAmount = Entry(self.left2, width=60, state=NORMAL, text=self.entryAllocationAmount).grid(row=1, column=1, sticky=W)

#I thought it would be beneficial to show the file location
        self.inputFirstCSVFile = Label(self.left2, text="Weekly Demand File Path:").grid(row=2, column=0, sticky=E)
        self.inputFirstCSVFileEntry = Entry(self.left2, width=60, state="readonly")
        self.inputFirstCSVFileEntry.grid(row=2, column=1)

#File location
        self.inputSecondCSVFile= Label(self.left2, text ="Master Data File Path:").grid(row=3, column=0, sticky=E)
        self.inputSecondCSVFileEntry=Entry(self.left2, width =60, state="readonly")
        self.inputSecondCSVFileEntry.grid(row=3, column=1)

#Output file location, needs to be saved as file.csv
        self.outputCSVFile = Label(self.left2, text="DV Model File Path:").grid(row=5, column=0, sticky=E)
        self.outputCSVFileEntry = Entry(self.left2, width=60, state="readonly")
        self.outputCSVFileEntry.grid(row=5, column=1)


        self.outputCSVFile1 = Label(self.left2, text="DOS Model File Path:").grid(row=6, column=0, sticky=E)
        self.outputCSVFileEntry1 = Entry(self.left2, width=60, state="readonly")
        self.outputCSVFileEntry1.grid(row=6, column=1)
#After all the data has been entered, click process button
        self.process_Data = Button(self.left3, text="Process Data", width=78, state="disabled", command=self.processDataButtonClicked)
        self.process_Data.grid(row=0, column=0, sticky=E+W)


        self.convertData = 0

#Asks for the file for Weekly Demand
    def loadFirstCSVclicked(self):

        self.inputFirstCSVFILE=filedialog.askopenfilename()
        self.inputFirstCSVFileEntry.config(state=NORMAL)
        self.inputFirstCSVFileEntry.delete(0,END)
        self.inputFirstCSVFileEntry.insert(0,self.inputFirstCSVFILE)
        self.inputFirstCSVFileEntry.config(state="readonly")

        self.loadFirstCSVFile()

#Loads Weekly Demand (Remove Try Statement)
    def loadFirstCSVFile(self):
        
        self.dataFirstSet=[]
        try:
            file = open(self.inputFirstCSVFILE, "r")
            csvReader=csv.reader(file, delimiter = ",")
            for row in csvReader:
                self.dataFirstSet.append(row)
            file.close()
            #self.process_Data.config(state="active")
            del self.dataFirstSet[0]
        except:
            messagebox.showwarning("Oh NO!", "Invalid CSV File")
            return None

#Asks for the file for Master Data

#Asks for the file for Master Data
    def loadSecondCSVclicked(self):

        self.inputSecondCSVFILE=filedialog.askopenfilename()
        self.inputSecondCSVFileEntry.config(state=NORMAL)
        self.inputSecondCSVFileEntry.delete(0,END)
        self.inputSecondCSVFileEntry.insert(0,self.inputSecondCSVFILE)
        self.inputSecondCSVFileEntry.config(state="readonly")

        self.loadSecondCSVFile()

#Loads Master Data (Remove Try Statement)
    def loadSecondCSVFile(self):

        self.dataSecondSet=[]
        try:
            file = open(self.inputSecondCSVFILE, "r")
            csvReader=csv.reader(file, delimiter = ",")
            for row in csvReader:
                self.dataSecondSet.append(row)
            file.close()
            self.process_Data.config(state="active")
            del self.dataSecondSet[0]
        except:
            messagebox.showwarning("Oh NO!", "Invalid CSV File")
            return None

#The beginning of processes the data

#Do cool stuff
    def processDataButtonClicked(self):

        allocationAmount = int(self.entryAllocationAmount.get())
        weekNumber = int(self.entryWeekNumber.get())


        if self.switch == True:
            self.dataFirstSet, self.dataSecondSet = stringToNumber(self.dataFirstSet,self.dataSecondSet)
            self.output = averageDaysOfSupply( self.dataFirstSet, self.dataSecondSet, weekNumber, allocationAmount)
            thirdModelOutput = thirdModel(self.dataFirstSet, self.dataSecondSet, weekNumber, allocationAmount)
            self.switch = False
            print("Average Days of Supply: ", self.output[0])
            print("Third Model Ouput: ", thirdModelOutput[0])

        self.totalOrders = 0

        weeklyOutlook = weeklyDemand( self.dataFirstSet, weekNumber, self.kValue)
        updatedWeeklyOutlook= masterData( self.dataSecondSet, weeklyOutlook, weekNumber)

        finalWeeklyOutlook = determineOrderQuantity(self, updatedWeeklyOutlook)

        self.checkOrderConstraint(finalWeeklyOutlook)

        self.iteration += 1
        print("1st Model Iteration: ", self.iteration)

        if self.totalOrders > allocationAmount:
            self.kValue = self.kValue - .001
            self.processDataButtonClicked()

        finalData = expectedOOS(self, finalWeeklyOutlook)

        self.outputToCSV(finalData)
        self.outputToCSV1(self.output)

    def checkOrderConstraint(self, finalWeeklyOutlook):

        #sums the totalOrders
        for row in finalWeeklyOutlook:
            self.totalOrders += row[11]
        self.totalOrders = int(self.totalOrders)

        #removes afRatio so weeklyDemand can be reused when totalOrders is greater than allocationAmount
        for row in self.dataFirstSet:
            del row[5]
        return None

    def outputToCSV(self, finalWeeklyOutlook):
        # sku, plant, avgAFRatio,sigmaAFRatio, forecastedDemand, muForecast, sigmaForecast, forecastVariability, beginningInventoryVolume, retailerDemand, supply, orderQTY, onhand+onOrder-Demand
        print("K-Value: ", self.kValue)
        f = filedialog.asksaveasfilename(message="Demand Variablitiy Model")

        self.outputCSVFileEntry.config(state=NORMAL)
        self.outputCSVFileEntry.delete(0, END)
        self.outputCSVFileEntry.insert(0, f)
        self.outputCSVFileEntry.config(state="readonly")

        file = open(f, "w", newline="")
        csvWriter = csv.writer(file)
        csvWriter.writerow(
            ["Sku", "Plant", "Average AF Ratio", "Sigma AFRatio", "Forecasted Demand", "Mu Forecast", "Sigma Forecast",
             "Forecast With Variability", "Beginning Inventory Volume", "Retailer Demand", "Supply", "Order Quantity",
             "OnHand+OnOrder-Demand", "Supply+Inventory","Expected OOS"])
        for row in finalWeeklyOutlook:
            csvWriter.writerow(row)
        file.close()
        return None
    def outputToCSV1(self, output):
        # sku, plant, avgAFRatio,sigmaAFRatio, forecastedDemand, muForecast, sigmaForecast, forecastVariability, beginningInventoryVolume, retailerDemand, supply, orderQTY, onhand+onOrder-Demand
        print("K-Value: ", self.kValue)
        f = filedialog.asksaveasfilename(message="Days of Supply Model")
        self.outputCSVFileEntry1.config(state=NORMAL)
        self.outputCSVFileEntry1.delete(0, END)
        self.outputCSVFileEntry1.insert(0, f)
        self.outputCSVFileEntry1.config(state="readonly")

        file = open(f, "w", newline="")
        csvWriter = csv.writer(file)
        csvWriter.writerow(
            ["Plant", "WeekNumber", "Sku", "Average Days Of Supply", "Beginning Inventory Volume", "Retailer Demand", "Supply",
             "Beginning Inventory Week Number", "Fair Share Inventory", "Under Over", "Raw Allocation", "Net Suppy"]
        )
        for row in output:
            csvWriter.writerow(row)
        file.close()
        return None
    


w = Tk()
app=simulation(w)
w.title("Senior Design")
w.mainloop()
