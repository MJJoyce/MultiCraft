#!/usr/bin/env python
###############################################################################
#
#	MultiCraft - MineCraft Jar Version Control and Launcher
#
#	See the README for more information
#
#   Coded by Michael Joyce, mltjoyce (at) gmail (dot) com
#
###############################################################################
import os
import sys
import subprocess
import getpass

defaultDirectory = ""
saveDirectory = ""

###############################################################################
def defaultInstallDir():
	'''Helper used to return the OS specific install directory.'''
	if (os.name == "nt"):
#return "C:\\Users\\" + getpass.getuser() + "\\AppData\\Roaming\\"
		return "C:/Users/" + getpass.getuser() + "/AppData/Roaming/"
	else:
		print "Currently not supporting your OS...Sorry"


###############################################################################
def winToUnx(winPath):
	'''Helper used to convert Windows paths to Unix paths

	   Makes dealing with paths easier in the code.
	'''
	converted = ['/' if char == '\\' else char for char in list(winPath)]
	return ''.join(converted)


###############################################################################
def getPathSlash():
	'''Returns the slash used in paths for the current OS'''
	if (os.name == "nt"):
		return '\\'
	else:
		 return '/'


###############################################################################
def writeCfg(default, save):
	'''Helper used to write the config file.'''
	if (os.name == "nt"):
		# Checks that the user terminated their paths 
		# If I always terminate the paths with \ and convert to unix file names
		#   I don't have to check for which OS I'm on
		if (default[-1] != '\\' and default[-1] != '/'):
			default += '\\'

		if (save[-1] != '\\' and save[-1] != '/'):
			save += '\\'

		default = winToUnx(default)
		save = winToUnx(save)

		config = open("cfg", "w")
		config.write("default " + default + "\n")
		config.write("save " + save + "\n")
		config.close()

		if (os.path.isfile("cfg")):
			# Make the file hidden
			subprocess.Popen("attrib +h cfg")
		else:
			print "Error generating config file"
	else:
		print "Currently not supporting your OS...Sorry"


###############################################################################
def initRun():
	'''Does first run setup of MultiCraft'''
	print "---------------------------"
	print "Welcome to MultiCraft Setup"
	print "---------------------------\n"
	print "*** If you're not sure how to use this program, start with the README ***\n"

	print "Enter your MineCraft install directory (Leave blank for OS default)"
	defDir = raw_input("-->")

	if (defDir == ""):
		defDir = defaultInstallDir()

	print "\nEnter the directory where you would like to store different versions"
	print "Leave blank for default (Same directory as OS default for Minecraft)"
	saveDir = raw_input("-->")

	if (saveDir == ""):
		saveDir = defaultInstallDir()

	writeCfg(defDir, saveDir)

	print "\nThank you for configuring MuliCraft. Please exit and restart."
	print "Press any button to exit..."
	raw_input()


###############################################################################
def clearScreen():
	'''Helper for clearing the terminal'''
	if (os.name == 'nt'):
		os.system('cls')
	else:
		os.system('clear')



###############################################################################
def setup():
	'''Gets config information for normal MultiCraft run'''
	global defaultDirectory, saveDirectory
	with open('cfg') as config:
		for line in config:
			temp = line.split()

			if (temp[0] == "default"):
				defaultDirectory = temp[1]
			elif (temp[0] == "save"):
				saveDirectory = temp[1]
			else:
				 print "Error processing config file"
				 sys.exit(1)


###############################################################################
def run(directory):
	pass


###############################################################################
def play():
	'''Lets the user select which version of MineCraft they want to run'''
	# Get a list of all minecraft versions in the version save location
	dirs = [item for item in os.listdir(os.path.normpath(saveDirectory)) if os.path.isdir(os.path.normpath(saveDirectory) + getPathSlash() + item)]
	
	listPage = 0
	while(1):
		clearScreen()

		lastEle = (9 * (listPage + 1)) if (9 * (listPage + 1)) <= len(dirs) else len(dirs)
		for count, dir in enumerate(dirs[listPage * 9:lastEle]):
			print str(count + 1) + ") " + dir
		
		print ""
		print "0) Prev"
		print "-) Next"
		print "=) Main Menu"

		selection = raw_input("-->")

		if (selection in ['1', '2', '3', '4', '5', '6', '7', '8', '9']):
			run(os.path.normpath(saveDirectory) + dirs[int(selection) - 1] + getPathSlash())
		elif (selection == '0'):
			listPage = 0 if (listPage == 0) else (listPage - 1)
		elif (selection == '-'):
			listPage = listPage if (((9 * listPage) + 1) >= len(dirs)) else (listPage + 1)
		elif (selection == '='):
			menu()
		else:
			continue



###############################################################################
def add():
	''''''
	pass


###############################################################################
def remove():
	''''''
	pass


###############################################################################
def revertDefault():
	''''''
	pass


###############################################################################
def menu():
	'''MultiCraft's main menu'''
	while(1):
		clearScreen()
		print "---MultiCraft---"
		print "1: Play"
		print "2: Add Version"
		print "3: Remove Version"
		print "4: Reset Default Install"
		print "5: Exit"
		selection = raw_input("-->");

		if (selection == '1'):
			play()
		elif (selection == '2'):
			add()
		elif (selection == '3'):
			remove()
		elif (selection == '4'):
			revertDefault()
		elif (selection == '5'):
			sys.exit(0)
		else:
			continue


###############################################################################
# Main
###############################################################################
if (not os.path.isfile('cfg')):
	initRun()
else:
	setup()
	menu()
