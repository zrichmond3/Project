from tkinter import *
from tkinter import filedialog
import csv
import urllib.request
from weeklyDemand import *
from determineOrderQuantity import *
from masterData import *

class simulation:
    def __init__(self,w):

        self.myTOPFrame = Frame(w)
        self.myTOPFrame.pack(side=TOP)
        self.myLeftFrame = Frame(w)
        self.myLeftFrame.pack(side=LEFT)


        self.left0 = Frame(self.myLeftFrame)
        self.left0.pack()
        self.left1 = Frame(self.myLeftFrame)
        self.left1.pack()
        self.left2 = Frame(self.myLeftFrame)
        self.left2.pack()
        self.left3 = Frame(self.myLeftFrame)
        self.left3.pack()


        url = "http://w4aql.gtorg.gatech.edu/images/buzzzap.gif"
        response = urllib.request.urlopen(url)
        myPicture = response.read()
        import base64
        b64_data = base64.encodebytes(myPicture)
        self.mainImage = PhotoImage(data=b64_data)

        self.totalOrders = 0
        self.kValue = .99
        self.counter = 0

        self.photoLabel = Label(self.myTOPFrame, image=self.mainImage)
        self.photoLabel.grid(row=0, column=0)

        self.loadFirstInputCSVFile = Button(self.left1, width=78, text="Load Weekly Demand", command=self.loadFirstCSVclicked).grid(row=0, column=0, sticky=E+W)
        self.loadSecondInputCSVFile = Button(self.left1, width=78, text="Load Master Data", command=self.loadSecondCSVclicked).grid(row=1, column=0, sticky=E+W)

        self.entryWeekNumber = StringVar()
        self.weekNumber = Label(self.left2, text="Allocating Week Number:").grid(row=0, column=0, sticky=E)
        self.weekNumber = Entry(self.left2, width=60, state=NORMAL, text=self.entryWeekNumber).grid(row=0, column=1, sticky=W)


        self.entryAllocationAmount = StringVar()
        self.allocationAmount = Label(self.left2, text="Allocation Amount:").grid(row=1, column=0, sticky=E)
        self.allocationAmount = Entry(self.left2, width=60, state=NORMAL, text=self.entryAllocationAmount).grid(row=1, column=1, sticky=W)


        self.inputFirstCSVFile = Label(self.left2, text="Weekly Demand File Path:").grid(row=2, column=0, sticky=E)
        self.inputFirstCSVFileEntry = Entry(self.left2, width=60, state="readonly")
        self.inputFirstCSVFileEntry.grid(row=2, column=1)

        self.inputSecondCSVFile= Label(self.left2, text ="Master Data File Path:").grid(row=3, column=0, sticky=E)
        self.inputSecondCSVFileEntry=Entry(self.left2, width =60, state="readonly")
        self.inputSecondCSVFileEntry.grid(row=3, column=1)

        self.outputCSVFile = Label(self.left2, text="Output File Path:").grid(row=5, column=0, sticky=E)
        self.outputCSVFileEntry = Entry(self.left2, width=60, state="readonly")
        self.outputCSVFileEntry.grid(row=5, column=1)

        self.process_Data = Button(self.left3, text="Process Data", width=78, state="disabled", command=self.processDataButtonClicked)
        self.process_Data.grid(row=0, column=0, sticky=E+W)

        

    def loadFirstCSVclicked(self):

        self.inputFirstCSVFILE=filedialog.askopenfilename()
        self.inputFirstCSVFileEntry.config(state=NORMAL)
        self.inputFirstCSVFileEntry.delete(0,END)
        self.inputFirstCSVFileEntry.insert(0,self.inputFirstCSVFILE)
        self.inputFirstCSVFileEntry.config(state="readonly")

        self.loadFirstCSVFile()

    def loadFirstCSVFile(self):
        
        self.dataFirstSet=[]
        try:
            file = open(self.inputFirstCSVFILE, "r")
            csvReader=csv.reader(file, delimiter = ",")
            for row in csvReader:
                self.dataFirstSet.append(row)
            file.close()
            self.process_Data.config(state="active")
            del self.dataFirstSet[0]
        except:
            messagebox.showwarning("Oh NO!", "Invalid CSV File")
            return None

    def loadSecondCSVclicked(self):

        self.inputSecondCSVFILE=filedialog.askopenfilename()
        self.inputSecondCSVFileEntry.config(state=NORMAL)
        self.inputSecondCSVFileEntry.delete(0,END)
        self.inputSecondCSVFileEntry.insert(0,self.inputSecondCSVFILE)
        self.inputSecondCSVFileEntry.config(state="readonly")

        self.loadSecondCSVFile()

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



    def processDataButtonClicked(self):
        allocationAmount = int(self.entryAllocationAmount.get())
        weekNumber = int(self.entryWeekNumber.get())
        self.totalOrders =0



        if len(self.dataFirstSet[0])==5:
            weeklyOutlook = weeklyDemand(self, self.dataFirstSet, weekNumber, self.kValue)
        else:
            weeklyOutlook = weeklyDemand(self, self.dataSecondSet, weekNumber, self.kValue)
        if len(self.dataFirstSet[0])==9:
            updatedWeeklyOutlook = masterData(self, self.dataFirstSet, weeklyOutlook, weekNumber)
        else:
            updatedWeeklyOutlook= masterData(self, self.dataSecondSet, weeklyOutlook, weekNumber)


        finalWeeklyOutlook = determineOrderQuantity(self, updatedWeeklyOutlook)

        self.checkOrderConstraint(finalWeeklyOutlook)
        self.counter += 1
        print("iteration: "+self.counter)
        if self.totalOrders > allocationAmount:
            self.kValue = self.kValue - .01
            self.processDataButtonClicked()

        self.outputToCSV(finalWeeklyOutlook)

    def checkOrderConstraint(self, finalWeeklyOutlook):
        for row in finalWeeklyOutlook:
            self.totalOrders += row[11]
        self.totalOrders = int(self.totalOrders)
        for row in self.dataFirstSet:
            del row[5]
        return None

    def outputToCSV(self, finalWeeklyOutlook):
        # sku, plant, avgAFRatio,sigmaAFRatio, forecastedDemand, muForecast, sigmaForecast, forecastVariability, beginningInventoryVolume, retailerDemand, supply, orderQTY, onhand+onOrder-Demand
        print("K-Value: "+self.kValue)
        f = filedialog.asksaveasfilename()

        self.outputCSVFileEntry.config(state=NORMAL)
        self.outputCSVFileEntry.delete(0, END)
        self.outputCSVFileEntry.insert(0, f)
        self.outputCSVFileEntry.config(state="readonly")

        file = open(f, "w", newline="")
        csvWriter = csv.writer(file)
        csvWriter.writerow(
            ["sku", "plant", "avgAFRatio", "sigmaAFRatio", "forecastedDemand", "muForecast", "sigmaForecast",
             "forecastVariability", "beginningInventoryVolume", "retailerDemand", "supply", "orderQTY",
             "onhand+onOrder-Demand", "Supply+Inventory"])
        for row in finalWeeklyOutlook:
            csvWriter.writerow(row)
        file.close()
        return None
    

            
w = Tk()
app=simulation(w)
w.title("Senior Design")
w.mainloop()
