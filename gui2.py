from Tkinter import *
from tkFileDialog import askopenfilename
from tkMessageBox import *
import paramiko
import os
import time
import webbrowser
import csv
import pprint

master = Tk()

ssh_stdin = None
ssh_stdout = None
ssh_stdout = None

quit = False
IPofPi = "192.168.1.106"
IPofPhone = "192.168.1.66"
username="pi"
password="raspberry"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
connected = False
executeIsPressed = False

#def help():
#	os.startfile("cmdList.txt")

def loadMission():
	name = askopenfilename()
	Col1 = "latitude"
	Col2 = "longitude"
	Col3 = "altitude"
	Col4 = "heading"
	mydictionary={Col1:[], Col2:[], Col3:[], Col4:[]}
	csvFile = csv.reader(open(name, "rb"))
	firstRow = True
	for row in csvFile:
	  if(not firstRow):
		mydictionary[Col1].append(row[0])
		mydictionary[Col2].append(row[1])
		mydictionary[Col3].append(row[2])
		mydictionary[Col4].append(row[3])
	  firstRow = False
	print mydictionary
	

def executeVerify():
	global executeIsPressed
	if askyesno('Verify', "Are you sure this is the command/mission you wish to execute?"):
		executeIsPressed = True
	else:
		showinfo("Cancelled", "Command/mission not executed")

def toWebInterface():
	webbrowser.open("https://flylitchi.com/hub")

def quitTask():
	global ssh_stdin
	global ssh_stdout
	global ssh_stderr
	
	ssh_stdin.write('h\n')
	ssh_stdin.flush()
	time.sleep(5)	
	ssh_stdin.write('n\n')
	time.sleep(5)
	outputyay = ssh_stdout.read()
	print(outputyay)
	ssh.close()
	master.quit()
	master.destroy()

def var_states():
   print("male: %d,\nfemale: %d" % (var1.get(), var2.get()))
def create_buts():
	for index, item in enumerate(buts_text):
		var.append(IntVar())
		buts.append(Checkbutton(master, text=item, variable=var[index]))
		buts[index].grid(row=index+1,sticky=W+E+N+S)
def select_all():
	for i in buts:
		i.select()
def deselect_all():
	for i in buts:
		i.deselect()
def connect():
	global connected
	global ssh_stdin
	global ssh_stdout
	global ssh_stderr
	
	if(not connected):
		ssh.connect(IPofPi, port=22, username=username, password=password)
		#ssh.connect(IPofPhone, port=2222, username="james", password="admin")
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('cd raspberrypi-support/build/bin && ./djiosdk-linux-sample -interactive')
		connectButton.config(text="Connected", fg="green4")
		connected = True
		getInput()
	else:
		showinfo("Already connected", "You are already connected!")

def getInput():
	global executeIsPressed
	global ssh_stdin
	global ssh_stdout
	global ssh_stderr
	
	if(executeIsPressed):
		executeIsPressed = False
		if(cmdText.get() != ""):
			print(cmdText.get())
			ssh_stdin.write(cmdText.get() + '\n')
			ssh_stdin.flush()
			time.sleep(5)
		else:
			chosenCommand = cmdDict[direction.get()]
			print(chosenCommand)
			ssh_stdin.write(chosenCommand + '\n')
			ssh_stdin.flush()
			time.sleep(5)
	master.after(500, getInput)
	
cmdDict = {1: "1 5", 2 : "2 5", 3 : "3 5", 4 : "4 5", 5 : "5 5", 6 : "6 5", 7 : "7", 8 : "8", 9 : "h", 10 : "i", 11 : "c", 12 : "e", 13 : "f"}
buts_text = ['1','2','3','4','5','6']
directions = [("up",1),("down",2),("left",3),("right",4),("fw",5),("bw",6),("yleft",7),("yright",8),("land",9),("rth",10), ("arm",11),("takeoff",12),("waypoint",13)]

direction = IntVar()
direction.set(1) # initializing the choice, i.e. up

buts = []
var  = []
Label(master, text="Choose Drone(s):").grid(row=0)
Label(master, text="Choose Command:").grid(column=2,row=0)
create_buts()
Button(master, text='All', command=select_all).grid(row=7)
Button(master, text='None', command=deselect_all).grid(row=8, pady=4)
Button(master, text='Quit', command=quitTask).grid(row=9, pady=4)
connectButton=Button(master, text="Connect", command=connect)
connectButton.grid(column=4,row=0, pady=4)

#menubar = Menu(master)
#menubar.add_command(label=Help, command=help)
#master.config(menu=menubar)

for txt, val in directions:
	Radiobutton(master, text=txt, variable=direction, value=val).grid(column=2,row=val)
Label(master, text="--OR--").grid(column=2,row=14, pady=8)
Label(master, text="Type command:").grid(column=2,row=15, pady=4)

cmdText = StringVar()
e1 = Entry(master, textvariable=cmdText)
e1.grid(row=16,column=2, pady=4)

Button(text='Load Mission', command=loadMission).grid(column=4,row=1)
Button(text='Create Mission', command=toWebInterface).grid(column=4,row=2)
Button(text='Execute command/mission', command=executeVerify).grid(column=4,row=3)

master.mainloop()
