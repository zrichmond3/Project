# This code is broken down into individual files that do a specific task.
# The code also follows camelCase coding for all naming conventions.
# SciPy, Statistics, cx_Freeze, and all other packages are imported through PyCharm.
# If a user clones the this project and runs it individual, all files will need to be in the same folder and all imports will need to be installed relevative to their operating system

#Imports
import csv

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from averageDaysOfSupply import *
from conversions.stringToNumber import *
from determineOrderQuantity import *


#Class created to run GUI
class simulation:
    def __init__(self,w):


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


        self.totalOrders = 0
        self.kValue = .999
        self.switch = True
        self.iteration = 0
        self.sDOS = 0

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


        self.dataFirstSet, self.dataSecondSet = stringToNumber(self.dataFirstSet,self.dataSecondSet)
        self.output = averageDaysOfSupply(self, self.dataFirstSet, self.dataSecondSet, weekNumber, allocationAmount, self.sDOS)

        for row in self.output:
            self.totalOrders += row[11]
        if self.totalOrders> allocationAmount:
            print("greater", self.sDOS)
            counter =0
            while self.totalOrders > allocationAmount:
                self.sDOS -= .1
                self.output = averageDaysOfSupply(self, self.dataFirstSet, self.dataSecondSet, weekNumber, allocationAmount, self.sDOS)
                self.totalOrders = 0
                counter += 1
                print("iteration: ", counter)
                for row in self.output:
                    self.totalOrders += row[11]
                print("total MOTHERFUCKING ORDERS: :D ", self.totalOrders)
            counter = 0
            while self.totalOrders < allocationAmount:
                self.sDOS += .01
                self.output = averageDaysOfSupply(self, self.dataFirstSet, self.dataSecondSet, weekNumber, allocationAmount, self.sDOS)
                counter += 1
                self.totalOrders = 0
                print("iteration: ", counter)
                for row in self.output:
                    self.totalOrders += row[11]
                print("Huh FUCK WE GOING BACK UP NOW HOMIE ", self.totalOrders)
            self.sDOS -= .01
            self.output = averageDaysOfSupply(self, self.dataFirstSet, self.dataSecondSet, weekNumber, allocationAmount, self.sDOS)
            self.totalOrders = 0
            for row in self.output:
                row[11]=round(row[11])
                self.totalOrders += row[11]
            print("I AINT FUCKING INCREMENTING ANYTHING ELSE ", self.totalOrders)

        elif self.totalOrders < allocationAmount:
            print("lesser", self.sDOS)
            counter = 0
            while self.totalOrders < allocationAmount:
                self.sDOS += .1
                self.output = averageDaysOfSupply(self, self.dataFirstSet, self.dataSecondSet, weekNumber,
                                                  allocationAmount, self.sDOS)
                counter += 1
                self.totalOrders = 0
                print("iteration: ", counter)
                for row in self.output:
                    self.totalOrders += row[11]
                print(" SHIT GOING TO THE TOP ", self.totalOrders)
            counter =0
            while self.totalOrders > allocationAmount:
                self.sDOS -= .01
                self.output = averageDaysOfSupply(self, self.dataFirstSet, self.dataSecondSet, weekNumber, allocationAmount, self.sDOS)
                self.totalOrders = 0
                counter += 1
                print("iteration: ", counter)
                for row in self.output:
                    self.totalOrders += row[11]
                print("DOWN DOWN BABY, UPSTREET - NAME THAT SONG: :D ", self.totalOrders)
            self.sDOS += .01
            self.output = averageDaysOfSupply(self, self.dataFirstSet, self.dataSecondSet, weekNumber, allocationAmount, self.sDOS)
            self.totalOrders = 0
            for row in self.output:
                row[11]=round(row[11])
                self.totalOrders += row[11]
            print("WHY ", self.totalOrders)




        self.totalOrders = 0


        self.iteration += 1

        self.outputToCSV1(self.output)



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
