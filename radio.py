import os
import sys
import subprocess
import shlex

#'Werners RadioPlayer' plays radio
#Depends on package mplayer
#supposably needs GNU/Linux

#Global variables
PathToControlFile="/tmp/RadioControl"
MPlayerCommand = "mplayer -input file=/tmp/RadioControl -slave -playlist "

#Playslists' global variables
Playlists=[]        
NumberOfPlaylists = 0 
RadioNames=[]      
PlaylistTarget=0 

RadioName1="Deutschlandfunk"
RadioName2="WDR5"
RadioName3="NDR Info"

#Function: init of playlists' list
#Params: none
#Return: none
def InitPlaylistList():
	global Playlists
	global RadioNames
	global NumberOfPlaylists

	#playlist 1
	Playlists.append("http://www.deutschlandradio.de/streaming/dlf_hq_ogg.m3u")
	RadioNames.append("Deutschlandfunk")

	#playlist 2
	Playlists.append("http://www.wdr.de/wdrlive/media/hls/wdr3.m3u8")
	RadioNames.append("WDR5")

	#playlist 3
	Playlists.append("https://www.ndr.de/resources/metadaten/audio/m3u/ndrinfo_nds.m3u")
	RadioNames.append("NDR Info")

	NumberOfPlaylists=3
	return

#Function: play choosen playlst / target playlist
#Params: none
#Return: none
def PlayPlaylist(TgtPlaylist):
	global Playlists
	global MPlayerCommand

	os.system("pkill -f mplayer")
	PlaylistCmd = MPlayerCommand + Playlists[TgtPlaylist]
	
	#starts mplayer process and e direct its stdout to /dev/null (so nothing of mplayer will be displayed, except errors)
	FNULL = open(os.devnull,'w')
	args = shlex.split(PlaylistCmd)
	InterfaceMPlayer = subprocess.Popen(args, shell=False, stdin=subprocess.PIPE, stdout=FNULL, stderr=subprocess.STDOUT)

	#volume set to 50%
	os.system('echo "volume 50" >'+PathToControlFile)

	return


#Function: create control file of mplayer (fifo file)
#Params: none
#Return: none
def CreateControlFile():
	if (os.path.exists(PathToControlFile)):
		return

	try:
		os.mkfifo(PathToControlFile)
	except:
		print ("[ERROR] Failed to create control file. Please, check path to this file.")
		exit(1)

#Function: show menu
#Params: none
#Return:  option
def ShowMenu():
	global RadioNames
	global PlaylitsEscolhida

	print ("-----------------------")
	print ("|    Werners Radio    |")
	print ("-----------------------")
	print ("| XXXXXXXXXX          |")
	print ("| XXXXXXXXXX          |")
	print ("| XXXXXXXXXX          |")
	print ("| XXXXXXXXXX  O   O   |")
	print ("-----------------------")
	print ("Aktueller Sender: "+RadioNames[PlaylistTarget])
	print (" ")
	print ("<p> Play/Pause")
	print ("<s> Exit")
	print ("<+> Lauter")
	print ("<-> Leiser")
	print ("<d> Naechster Sender")
	print ("<a> Voriger Sender")
	print (" ")
	option = input("Waehle eine Option aus>")

	return option


#------------------
#Main program
#------------------

InitPlaylistList()
CreateControlFile()

PlayPlaylist(PlaylistTarget)

while True:
	try:
		os.system("clear")
		KeyPressed = ShowMenu()

		if (KeyPressed == "p"):
			print ("[ACTION] Play/Pause")
			os.system('echo "pause" > '+PathToControlFile)

		if (KeyPressed == "s"):
			print ("[ACTION] Exit")
			os.system('echo "quit 0" > '+PathToControlFile)
			os.system("pkill -f mplayer")
			print ("Auf Wiedersehen!")
			exit(1)

		if (KeyPressed == "+"):
			print ("[ACTION] Lauter")
			os.system('echo "volume +10" > '+PathToControlFile)

		if (KeyPressed == "-"):
			print ("[ACTION] Leiser")
			os.system('echo "volume -10" > '+PathToControlFile)

		if (KeyPressed == "d"):
			print ("[ACTION] Naechster Sender")
			PlaylistTarget = PlaylistTarget + 1
			if (PlaylistTarget == NumberOfPlaylists):
				PlaylistTarget = 0
			PlayPlaylist(PlaylistTarget)

		if (KeyPressed == "a"):
			print ("[ACTION] Voriger Sender")
			PlaylistTarget = PlaylistTarget - 1
			if (PlaylistTarget < 0):
				PlaylistTarget = NumberOfPlaylists-1
			PlayPlaylist(PlaylistTarget)


	except (KeyboardInterrupt):
		print ("Auf Wiedersehen!")
		exit(1)
