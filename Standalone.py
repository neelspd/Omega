'''
Created on 27-Jan-2018

@author: Neel Shah
'''
##############################################################################################
########### Importing and Declaring Dependencies, Global Variables and Classes ###############
##############################################################################################
import tkinter as tk
import matplotlib.pyplot as plt
import serial
import serial.tools.list_ports
import time
import sys
 
fig = plt.figure()
graph = fig.add_subplot(1,1,1)

title="Creep Testing Software"
HoursCount = ""  
SampleID = "" 


def getTestData(InitialTime): 
    global HoursCount, SampleID
    HoursTick=0
    print(HoursCount)
    StatusLabel.clear()
    StatusLabel.set("Please Wait, Discovering Ports")  
    print("Please Wait, Discovering Ports")
    ports = list(serial.tools.list_ports.comports())
    if ports:
        for p in ports:
            print(p)
            if "(COM" in p.description:
                StatusLabel.clear()
                StatusLabel.set("Connected At:"+p.device)
                print("Connected At:"+p.device) 
            else:
                StatusLabel.clear()
                StatusLabel.set("No COM Port Found, Try Again")
                print("No COM Port Found, Try Again")
                break
    else:
        StatusLabel.clear()
        StatusLabel.set("No Port Found, Try Again")
        print("No Port Found, Try Again")        
    ArduinoData = serial.Serial(p.device, 9600, timeout=.1)
    Data = open(SampleID+'Test-Data.csv', 'a')
    while HoursTick < int(HoursCount):
        TimeLabel.clear()
        TimeLabel.set(str(HoursTick) +" Hour(s) Passed")
        currentTime = time.time() - InitialTime
        currentTime = currentTime/3600 #Seconds to hour Conversion
        HoursTick = int(currentTime)
        while (ArduinoData.inWaiting() == 0):
            pass
        CharStream  = ArduinoData.readline()[:-2]
        print(CharStream)
        CreepValue= float(CharStream)
        CreepPerHourValue = CreepValue/currentTime
        Data.write(str(float(currentTime))+","+str(CreepPerHourValue)+"\n") 
    Data.close()
    time.sleep(1)
                      
##############################################################################################
# The below functions are the action listeners which means when buttons will be pressed the  #
# actions described in the functions will be
# Application are pressed then the following functions will be called and executed ###########
##############################################################################################    
def completeTest():
    StatusLabel.clear()
    StatusLabel.set("Test Completed, Exiting")
    time.sleep(1)
    root.destroy()
    sys.exit(1)

def plotTestData():
    X_axis=[]
    Y_axis=[]
    global SampleID
    graph_data = open(SampleID+'Test-Data.csv','r').read()
    lines = graph_data.split('\n')
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            X_axis.append(float(x))
            Y_axis.append(float(y))
    graph.clear()
    plt.title("Test Graph")
    StatusLabel.clear()
    StatusLabel.set("Testing Completed, Plotting Graph")
    graph.plot(X_axis, Y_axis)
    plt.show()
##############################################################################################
# Till Here ##################################################################################
##############################################################################################
# GUI Starts Here ############################################################################
##############################################################################################
root = tk.Tk()

class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_1 = tk.Label(self, text="Sample Id: ")
        self.label_2 = tk.Label(self, text="Number of Operating Hours: ")

        self.entry_1 = tk.Entry(self)
        self.entry_2 = tk.Entry(self)

        self.label_1.grid(row=0, sticky=tk.W,padx=10,pady=10)
        self.label_2.grid(row=1, sticky=tk.W,padx=10,pady=10)
        self.entry_1.grid(row=0, column=1,padx=10,pady=10)
        self.entry_2.grid(row=1, column=1,padx=10,pady=10)


        self.logbtn = tk.Button(self, text="GO", command = self.login_btn_clickked)
        self.logbtn.grid(columnspan=2)

        self.pack()

    def login_btn_clickked(self):
        #print("Clicked")
        global SampleId, HoursCount
        SampleId = self.entry_1.get()
        HoursCount = self.entry_2.get() 
        print(SampleId + HoursCount)
        if SampleId == "" or HoursCount == "":
            tk.messagebox.showerror("", "Not Enough Data")
        else:
            self.destroy()
                 
        
class StatusBar(tk.Frame):
 
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, anchor=tk.W)
        self.label.pack(fill=tk.X)
 
    def set(self, format, *args):
        self.label.config(text= format %args)
        self.label.update_idletasks()
 
    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

def initiateSystem():  
    window = tk.Toplevel(root)
    lf = LoginFrame(window)
    StatusLabel.clear()
    StatusLabel.set("Initiated")

def initiateAcquireData():
    InitTime = time.time()
    getTestData(InitTime)
        
StatusLabel = StatusBar(root)
StatusLabel.clear()
StatusLabel.set("Welcome")
TimeLabel = StatusBar(root)
TimeLabel.clear()
TimeLabel.set(str(HoursCount) +" Hours Passed")
root.title(" Creep Testing ")
StartButton = tk.Button(root, text="Start", width=13, height=2, command = initiateSystem)
StopButton = tk.Button(root, text="Exit", width=13, height=2, command = completeTest)
PlotButton = tk.Button(root, text="Plot Graph", width=13, height=2, command = plotTestData)
GetDataButton = tk.Button(root, text="Get Data", width=13, height=2, command = initiateAcquireData)
StartButton.grid(row=0,column=0, sticky=tk.W)
GetDataButton.grid(row=0,column=1, sticky=tk.W)
PlotButton.grid(row=0,column=2, sticky=tk.W)
StopButton.grid(row=0,column=3, sticky=tk.W)
StatusLabel.grid(row=2,columnspan=2, sticky=tk.W)
TimeLabel.grid(row=2,column=2, sticky=tk.W)        
root.mainloop()
##############################################################################################
# Till Here ##################################################################################
##############################################################################################



