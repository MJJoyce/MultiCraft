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
import shutil
import errno
import stat
from time import sleep

defaultDirectory = ""
saveDirectory = ""

###############################################################################
def defaultOSInstallDir():
	'''Helper used to return the OS specific install directory.'''
	if (os.name == "nt"):
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
		defDir = defaultOSInstallDir()

	print "\nEnter the directory where you would like to store different versions"
	print "Leave blank for default (Same directory as OS default for Minecraft)"
	saveDir = raw_input("-->")

	if (saveDir == ""):
		saveDir = defaultOSInstallDir()

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
def playDefault():
	'''Play the default Minecraft install.
	   
	   This simply launches either Minecraft.exe or minecraft.jar from the
	   MultiCraft directory. Proper installation means that one of the two
	   should be there. Report an error if they're not.
	'''
	exeLocal = os.getcwd() + "\\Minecraft.exe"
	jarLocal = os.getcwd() + getPathSlash() + "minecraft.jar"

	clearScreen()
	print "---MultiCraft---\n"
	if (os.path.isfile(exeLocal)):
		subprocess.Popen("Minecraft.exe")
	elif (os.path.isfile(jarLocal)):
		subprocess.Popen("java -cp minecraft.jar net.minecraft.LauncherFrame")
	else:
		print "*** Multicraft cannot run Minecraft ***\n"
		print "You need to put either Minecraft.exe or minecraft.jar in with MultiCraft"
		print "Check the README for further instructions\n"
		raw_input("Press any key to return to the menu...")
		return

	print "Running Minecraft..."
	exit(1)


###############################################################################
def add():
	'''Add new versions of Minecraft to manage.'''
    sel = Null
    while sel not in ['1', '2']:
        clearScreen()
        print "---MultiCraft Version Add---\n"
        print "1) Copy default install over"
        print "2) Add from a different location"
        sel = raw_input("-->")

    if (sel == '1'):
        print "\nWhat would you like to call this version?"
        name = raw_input("-->")

        newSaveDir = saveDirectory + getPathSlash() + name + ".minecraft"
        shutil.copytree(defaultDirectory + getPathSlash() + ".minecraft", newSaveDir) 
    elif (sel == '2'):
    else:



###############################################################################
def remove():
	''''''
	pass


###############################################################################
def handleReadOnlyError(func, path, exception):
	'''Used for handling read-only errors when using shutil.rmtree'''
	exceptionVal = exception[1]
	# If the error is caused by a file being read-only, give it full 
	#   permissions (777) and try again
	if (func in (os.rmdir, os.remove) and exceptionVal.errno == errno.EACCES):
		os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
		func(path)
	else:
		raise


###############################################################################
def revertDefault():
	'''Restores the "default" Minecraft directory to the current version.
	   
	   Simply deletes the entire .minecraft folder, SAVES INCLUDED. When it 
	   next run, a clean version of Minecraft will be installed over it.
	'''
	clearScreen()
	print "This will remove everything in your default minecraft directory."
	print "*** INCLUDING SAVES, TEXTURE PACKS, MODS, SETTINGS, ETC ***"
	print "*** BACK YOUR STUFF UP IF YOU WANT TO SAVE ANYTHING!!!  ***\n"
	print "Do you want to restore to default?"
	sel = raw_input("[y/N] -->")

	if (sel not in ['y', 'yes', 'Y', 'Yes']):
		return

	print "\nSeriously, are you absolutely sure?"
	sel2 = raw_input("[y/N] -->")

	if (sel2 not in ['y', 'yes', 'Y', 'Yes']):
		return

	dirPath = os.path.normpath(defaultDirectory + "/.minecraft")
	if (os.path.isdir(dirPath)):
		shutil.rmtree(dirPath, ignore_errors=False, onerror=handleReadOnlyError)
		print "\nSuccessfully removed default install."
		print "Run default install again to reinstall a clean version"
		raw_input("Press any key to return to the main menu...")
	else:
		print "Could not remove default directory:"
		print dirPath
		raw_input("Press any key to return to menu...")
	


###############################################################################
def menu():
	'''MultiCraft's main menu'''
	while(1):
		clearScreen()
		print "---MultiCraft---"
		print "1: Play backup version"
		print "2: Play default version"
		print "3: Add Version"
		print "4: Remove Version"
		print "5: Reset Default Install"
		print "6: Exit"
		selection = raw_input("-->");

		if (selection == '1'):
			play()
		elif (selection == '2'):
			playDefault()
		elif (selection == '3'):
			add()
		elif (selection == '4'):
			remove()
		elif (selection == '5'):
			revertDefault()
		elif (selection == '6'):
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
