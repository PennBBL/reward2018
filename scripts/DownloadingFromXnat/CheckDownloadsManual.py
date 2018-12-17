# A python script to downlaod all of the reward dicoms to a directory
#
# This script takes all of the reward project participants, scans
# the directory for each, and download all of their dicoms
# from XNAT by scanID
# script is modified to take an input as opposed to the dictionary

import sys
import os
import re
import XnatDownloadHelper
from pyxnat import Interface
import pyxnat
xnat_config = "/home/ttapera/.xnat.cfg"
central = Interface(config=xnat_config)
import urllib3
urllib3.disable_warnings()
import pandas as pd

def GetParticipants():
	
	# This function gathers all of the participant IDs and scan IDs
	# Output: dictionary of {ScanID: BBLID}

	scansDict = {}

	#list everything in the directory that could be a participant ID
	main_directory = "/data/joy/BBL/studies/reward2018/dicomsFromXnat"
	reward_participants = os.listdir(main_directory)
	reward_participants = [x for x in reward_participants if x.isdigit()]

	#loop through each and 
	for participant in reward_participants:
		
		#list everythin that could be a scan ID
		scanIDs = os.listdir(main_directory+"/"+participant)
		scanIDs = [re.sub('\d+x','', x) for x in scanIDs]
		
		#loop through IDs; if unique, add to dictionary with BBLID
		for sequence in scanIDs:
			
			if sequence not in scansDict.keys():
				scansDict[sequence] = participant

	return(scansDict)

def DownloadLoop(scansDict):
	
	# This function loops through a dictionary of ScanID: BBLID
	# and downloads the scans to a destination built by the dictionary
	# Input: dictionary of {ScanID:BBLID}
	# Output: None

	main_directory = "/data/joy/BBL/studies/reward2018/dicomsFromXnat/"
	# loop through the dictionary
	for scanid, bblid in scansDict.iteritems():
		
		print "Processing participant %s, scan %s" % (bblid, scanid)
		
		#make the appropriate directory:
		cwd = main_directory+"%s/%s/" % (bblid,scanid)
		if not os.path.exists(cwd):
			os.makedirs(cwd)
		
		# if there are no files in the directory, start downloading	
		#if len(os.listdir(cwd)) == 0:
		# query and downlaod, using helpers
		try:
			query = XnatDownloadHelper.MakeQuery(bblid, scanid, central)
			
			XnatDownloadHelper.DownloadQuery(query, cwd, central)
		except:
			print "Could not process participant %s, scan %s" % (bblid, scanid)
			with open('/data/jux/BBL/projects/reward2018/reward2018/results/XnatDownloadErrors.txt','a') as f:
				f.write("%s,%s/" % (bblid,scanid))
		
		# if after attempt, still no files, note down (XNAT error)
		#if len(os.listdir(cwd)) ==0:
		#	print "Could not process participant %s, scan %s" % (bblid, scanid)
		#	with open('/data/jux/BBL/projects/reward2018/reward2018/results/XnatDownloadErrors.txt','a') as f:
		#		f.write("%s,%s/" % (bblid,scanid))

def main():

	# Main Namespace Function
	print("Running download script...")
	scansDict = GetParticipants()
	
	#csv_in=sys.argv[1]
	#scans = pd.read_csv(csv_in, names=["bblid", "scanid"])
	
	#scansDict = {row['scanid'] : row['bblid'] for _, row in scans.iterrows()}
	#scans=scans.set_index("scanid").to_dict('index')
	#print(scansDict)
	DownloadLoop(scansDict)

if __name__ == "__main__":
	main()
