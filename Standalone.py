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
from serial.tools.list_ports_windows import NULL
 
fig = plt.figure()
graph = fig.add_subplot(1,1,1)
X_axis=[]
Y_axis=[]
Data=""
ArduinoDataPort=""
title="Creep Testing Software"
InitTime=0.0
root = tk.Tk()
class StatusBar(tk.Frame):
 
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, anchor=tk.W)
        self.label.pack(fill=tk.X)
 
    def set(self, format, *args):
        self.label.config(text= format % args)
        self.label.update_idletasks()
 
    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()
StatusLabel = StatusBar(root)
StatusLabel.clear()
StatusLabel.set("Initiated")

StartFlag=True
StopFlag = False
    
##############################################################################################
# The below functions are the action listeners which means when buttons will be pressed the  #
# actions described in the functions will be
# Application are pressed then the following functions will be called and executed ###########
##############################################################################################
def initiateSystem():
    global InitTime
    InitTime = time.time()
    
def completeTest():
    StatusLabel.clear()
    StatusLabel.set("Test Completed")
    global StartFlag, StopFlag
    StopFlag = True
    
def getTestData():
    StatusLabel.clear()
    StatusLabel.set("Fetching Data from System")
    global StartFlag, StopFlag
    StartFlag =True
    print(StartFlag) 
    
def plotTestData():
    global X_axis, Y_axis
    graph_data = open('Test.csv','r').read()
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
root.title("Creep Testing Software")
StartButton = tk.Button(root, text="Start", width=10, height=2, command = initiateSystem)
StopButton = tk.Button(root, text="Stop", width=10, height=2, command = completeTest)
AcquireButton = tk.Button(root, text="Acquire Data", width=10, height=2, command = getTestData)
PlotButton = tk.Button(root, text="Plot Graph", width=10, height=2, command = plotTestData)
StartButton.grid(row=0,column=0, sticky=tk.W)
AcquireButton.grid(row=0,column=1, sticky=tk.W)
PlotButton.grid(row=0,column=3, sticky=tk.W)
StopButton.grid(row=0,column=2, sticky=tk.W)
StatusLabel.grid(row=2,columnspan=3, sticky=tk.W)
##############################################################################################
# Till Here ##################################################################################
##############################################################################################
# Data Acquisition While Loop Starts Here ####################################################
##############################################################################################
StatusLabel.clear()
StatusLabel.set("Please Wait, Discovering Ports")  
print("Please Wait, Discovering Ports")
ports = list(serial.tools.list_ports.comports())
if ports:
    for p in ports:
        print(p)
        if "(COM" in p.description:
            ArduinoDataPort = p.device
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
ArduinoData = serial.Serial(ArduinoDataPort, 9600, timeout=.1)
while StartFlag:
    if(StopFlag):
        break
    Data = open('Test.csv', 'a')
    currentTime = time.time() - InitTime
    currentTime = currentTime/3600 #Seconds to hour Conversion
    while (ArduinoData.inWaiting() == 0):
        pass
    CharStream  = ArduinoData.readline()[:-2]
    print(CharStream)
    CreepValue= float(CharStream)
    CreepPerHourValue = CreepValue/currentTime
    Data.write(str(float(currentTime))+","+str(CreepPerHourValue)+"\n")
    Data.close() 
    time.sleep(1)

        
root.mainloop()