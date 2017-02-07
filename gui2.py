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
waypointMission = None
reverseWaypointMission = None

doReverse = False
specialReturn = False
quit = False
IPofPi = "192.168.1.106"
IPofPhone = "192.168.1.66"
username="pi"
password="raspberry"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
connected = False
executeIsPressed = False
Latitude = "latitude"
Longitude = "longitude"
Altitude = "altitude"
Heading = "heading"
executedCommands = []
cmdInverse = {"a":"b", "b":"a", "c":"d", "d":"c", "e":"h", "h":"e", "1":"2", "2":"1", "3":"4", "4":"3", "5":"6", "6":"5", "7":"8", "8":"7"}

def help():
	os.startfile("cmdList.txt")

def loadMission():
	global waypointMission
	global reverseWaypointMission
	global Latitude
	global Longitude
	global Altitude
	global Heading
	
	name = askopenfilename()
	waypointMission={Latitude:[], Longitude:[], Altitude:[], Heading:[]}
	reverseWaypointMission={Latitude:[], Longitude:[], Altitude:[], Heading:[]}
	csvFile = csv.reader(open(name, "rb"))
	firstRow = True
	for row in csvFile:
	  if(not firstRow):
		waypointMission[Latitude].append(row[0])
		waypointMission[Longitude].append(row[1])
		waypointMission[Altitude].append(row[2])
		waypointMission[Heading].append(row[3])
		reverseWaypointMission[Latitude].insert(0,row[0])
		reverseWaypointMission[Longitude].insert(0,row[1])
		reverseWaypointMission[Altitude].insert(0,row[2])
		reverseWaypointMission[Heading].insert(0,row[3])
	  firstRow = False

def executeVerify():
	global executeIsPressed
	if(not connected):
		showwarning("Not Connected", "You are not connected. Connect first, then execute.")
	elif askyesno('Verify', "Are you sure this is the command/mission you wish to execute?"):
		executeIsPressed = True
	else:
		showinfo("Cancelled", "Command/mission not executed")

def toWebInterface():
	webbrowser.open("https://flylitchi.com/hub")

def quitTask():
	global specialReturn
	global ssh_stdin
	global ssh_stdout
	global ssh_stderr
	global doReverse
	global executedCommands
	
	if(connected and specialReturn):
		for cmd in executedCommands:
			if(cmd.startswith("1") or cmd.startswith("2") or cmd.startswith("3") or cmd.startswith("4") or cmd.startswith("5") or cmd.startswith("6")):
				splitCmd = cmd.split()
				inverseCmd = cmdInverse.get(splitCmd[0]) + " " + splitCmd[1]
				print inverseCmd
				ssh_stdin.write(inverseCmd + '\n')
				ssh_stdin.flush()
				time.sleep(5)
			elif(cmd == "f"):
				doReverse = True
				waypointMissionSend()
			else:
				print cmd	
				print cmdInverse.get(cmd)
				ssh_stdin.write(cmdInverse.get(cmd) + '\n')
				ssh_stdin.flush()
				time.sleep(5)	
	
	elif(connected):
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
		paramiko.util.log_to_file('ssh.log')
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('cd raspberrypi-support/build/bin && ./djiosdk-linux-sample -interactive')
		connectButton.config(text="Connected", fg="green4")
		connected = True
		getInput()
	else:
		showinfo("Already connected", "You are already connected!")

def waypointMissionSend():
	global waypointMission
	global ssh_stdin
	global ssh_stdout
	global ssh_stderr
	global doReverse
	global reverseWaypointMission
	
	if(waypointMission == None):
		showwarning("No mission loaded", "You must load a waypoint mission first!")
	
	if(doReverse):
		mission = reverseWaypointMission
	else:
		mission = waypointMission
		
	else:
		numWaypoints = str(len(mission[Latitude]))
		ssh_stdin.write(numWaypoints + '\n')
		ssh_stdin.flush()
		for index in range(0,len(mission[Latitude])):
			print(mission[Latitude][index])
			ssh_stdin.write(mission[Latitude][index]  + ' ')
			ssh_stdin.write(mission[Longitude][index] + ' ')
			ssh_stdin.write(mission[Altitude][index]  + ' ')
			ssh_stdin.write('\n')
			ssh_stdin.flush()
		
	
def getInput():
	global executeIsPressed
	global ssh_stdin
	global ssh_stdout
	global ssh_stderr
	global specialReturn
	
	if(connected and executeIsPressed):
		executeIsPressed = False
		if(cmdText.get() != ""):
			print(cmdText.get())
			if(cmdText.get() == "r"):
				specialReturn = True
				quitTask()
			ssh_stdin.write(cmdText.get() + '\n')
			ssh_stdin.flush()
			if(cmdText.get() == "f"):
				waypointMissionSend()
			executedCommands.insert(0,cmdText.get())
			time.sleep(5)
		else:
			chosenCommand = cmdDict[direction.get()]
			print(chosenCommand)
			if(chosenCommand == "r"):
				specialReturn = True
				quitTask()
			ssh_stdin.write(chosenCommand + '\n')
			ssh_stdin.flush()
			if(chosenCommand == "f"):
				waypointMissionSend()
			executedCommands.insert(0,chosenCommand)
			time.sleep(5)
	master.after(500, getInput)
	
cmdDict = {1: "1 5", 2 : "2 5", 3 : "3 5", 4 : "4 5", 5 : "5 5", 6 : "6 5", 7 : "7", 8 : "8", 9 : "h", 10 : "i", 11 : "c", 12 : "e", 13 : "f", 14 : "r"}
buts_text = ['1','2','3','4','5','6']
directions = [("up",1),("down",2),("left",3),("right",4),("fw",5),("bw",6),("yleft",7),("yright",8),("land",9),("rth",10), ("arm",11),("takeoff",12),("waypoint",13),("smart rth",14)]

direction = IntVar()
direction.set(1) # initializing the choice, i.e. up

buts = []
var  = []
Label(master, text="Choose Drone(s):").grid(row=0, sticky=W+E+N+S)
Label(master, text="Choose Command:").grid(column=2,row=0, sticky=W+E+N+S)
create_buts()
Button(master, text='All', command=select_all).grid(row=7, sticky=W+E+N+S)
Button(master, text='None', command=deselect_all).grid(row=8, pady=4, sticky=W+E+N+S)
Button(master, text='Quit', command=quitTask).grid(row=9, pady=4, sticky=W+E+N+S)
connectButton=Button(master, text="Connect", command=connect)
connectButton.grid(column=4,row=0, pady=4)

menubar = Menu(master)
menubar.add_command(label="Help", command=help)
master.config(menu=menubar)

for txt, val in directions:
	Radiobutton(master, text=txt, variable=direction, value=val).grid(column=2,row=val, sticky=W+E+N+S)
Label(master, text="--OR--").grid(column=2,row=15, pady=8, sticky=W+E+N+S)
Label(master, text="Type command:").grid(column=2,row=16, pady=4, sticky=W+E+N+S)

cmdText = StringVar()
e1 = Entry(master, textvariable=cmdText)
e1.grid(row=16,column=2, pady=4)

Button(text='Create Mission', command=toWebInterface).grid(column=4,row=1, sticky=W+E+N+S)
Button(text='Load Mission', command=loadMission).grid(column=4,row=2, sticky=W+E+N+S)
Button(text='Execute command/mission', command=executeVerify).grid(column=4,row=3, sticky=W+E+N+S)

master.mainloop()
