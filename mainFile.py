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
        self.myRightFrame = Frame(w)
        self.myRightFrame.pack(side=RIGHT)
        self.myBottomFrame = Frame(w)
        self.myBottomFrame.pack(side=BOTTOM)

        self.left0 = Frame(self.myLeftFrame)
        self.left0.pack()
        self.left1 = Frame(self.myLeftFrame)
        self.left1.pack()
        self.left2 = Frame(self.myLeftFrame)
        self.left2.pack()
        self.left3 = Frame(self.myLeftFrame)
        self.left3.pack()
        self.right1 = Frame(self.myRightFrame)
        self.right1.pack()
        self.right2 = Frame(self.myRightFrame)
        self.right2.pack()

        url = "http://w4aql.gtorg.gatech.edu/images/buzzzap.gif"
        response = urllib.request.urlopen(url)
        myPicture = response.read()
        import base64
        b64_data = base64.encodebytes(myPicture)
        self.mainImage = PhotoImage(data=b64_data)

        self.photoLabel = Label(self.myTOPFrame, image=self.mainImage)
        self.photoLabel.grid(row=0, column=0)

        self.weekTitle = Label(self.right1, text="Enter Some Cool SHIT for the w-w-weee-kk").grid(row=0, columnspan=1, sticky= E+W)

        self.entryAllocationAmount = StringVar()
        self.allocationAmount = Label(self.right2, text="Allocation Amount:").grid(row=0, column=0)
        self.allocationAmount = Entry(self.right2, width=30, state=NORMAL, text=self.entryAllocationAmount).grid(row=0, column=1)

        self.entryKValue = StringVar()
        self.kValue = Label(self.right2, text="k-value:").grid(row=1, column=0)
        self.kValue = Entry(self.right2, width=30, state=NORMAL, text=self.entryKValue).grid(row=1, column=1)

        self.entryWeekNumber = IntVar()
        self.weekNumber = Label(self.right2, text="Allocating Week Number").grid(row=2, column=0)
        self.weekNumber = Entry(self.right2, width=30, state=NORMAL, text=self.entryWeekNumber).grid(row=2, column=1)

        self.moesBBQ = Label(self.right2, text="Do I need this?").grid(row=3, column=0)
        self.moesBBQ = Entry(self.right2, width=30, state="readonly").grid(row=3, column=1)

        self.loadFirstInputCSVFile = Button(self.left1, width=75, text="Load Weekly Demand", command=self.loadFirstCSVclicked).grid(row=0, column=0, sticky=E + W)
        self.file_Path = Label(self.left1, text="File Path").grid(row=1, column=0)
        self.loadSecondInputCSVFile = Button(self.left1, width=75, text="Load Master Data", command=self.loadSecondCSVclicked).grid(row=1, column=0, sticky=E+W)
        self.file_Path2=Label(self.left1, text="File Path").grid(row=2, column=0)

        self.inputFirstCSVFile = Label(self.left2, text="Input First CSV File").grid(row=0, column=0)
        self.inputFirstCSVFileEntry = Entry(self.left2, width=60, state="readonly")
        self.inputFirstCSVFileEntry.grid(row=0, column=1)

        self.inputSecondCSVFile= Label(self.left2, text ="Input Second CSV File").grid(row=1, column=0)
        self.inputSecondCSVFileEntry=Entry(self.left2, width =60, state="readonly")
        self.inputSecondCSVFileEntry.grid(row=1, column=1)

        self.outputCSVFile = Label(self.left2, text="Output CSV File").grid(row=2, column=0)
        self.outputCSVFileEntry = Entry(self.left2, width=60, state="readonly")
        self.outputCSVFileEntry.grid(row=2, column=1)

        self.process_Data = Button(self.left3, text="Process Data", width=75, state="disabled", command=self.processDataButtonClicked)
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
        except:
            messagebox.showwarning("Oh NO!", "Invalid CSV File")
            return None


                
    def processDataButtonClicked(self):
        allocationAmount = self.entryAllocationAmount.get()
        weekNumber = self.entryWeekNumber.get()
        kValue = self.entryKValue.get()
        print(allocationAmount, weekNumber, kValue)



        if len(self.dataFirstSet[0])==5:
            weeklyOutlook = weeklyDemand(self, self.dataFirstSet, weekNumber, kValue)
        else:
            weeklyOutlook = weeklyDemand(self, self.dataSecondSet, weekNumber, kValue)
        if len(self.dataFirstSet[0])==9:
            self.dataSecondSet= 0
            updatedWeeklyOutlook = masterData(self, self.dataFirstSet, weeklyOutlook, weekNumber)
        else:
            self.dataFirstSet = 0
            updatedWeeklyOutlook= masterData(self, self.dataSecondSet, weeklyOutlook, weekNumber)

        finalWeeklyOutlook = determineOrderQuantity(self, updatedWeeklyOutlook)

        self.outputToCSV(finalWeeklyOutlook)

    def outputToCSV(self, finalWeeklyOutlook):
        # sku, plant, avgAFRatio,sigmaAFRatio, forecastedDemand, muForecast, sigmaForecast, forecastVariability, beginningInventoryVolume, retailerDemand, supply, orderQTY, onhand+onOrder-Demand
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
             "onhand+onOrder-Demand"])
        for row in finalWeeklyOutlook:
            csvWriter.writerow(row)
        file.close()
    

            
w = Tk()
app=simulation(w)
w.title("Senior Design Simulation")
w.mainloop()
