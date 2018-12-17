# A python script to create multiple arrays of BBLIDs and SCANIDs for reward
#
# This script takes all of the reward project participants, looks in
# the directory for each, and creates multiple csvs to parralelise downloading

import os
import re
import numpy as np
import pandas as pd

def GetParticipants():
	
	# This function gathers all of the participant IDs and scan IDs
	# Output: dictionary of {ScanID: BBLID}

	scansDict = {}

	#list everything in the directory that could be a participant ID
	main_directory = "/data/jux/BBL/projects/reward2018/reward2018/data/rawData"
	reward_participants = os.listdir(main_directory)
	reward_participants = [x for x in reward_participants if x.isdigit()]

	#loop through each and...
	for participant in reward_participants:
		
		#list everythin that could be a scan ID
		scanIDs = os.listdir(main_directory+"/"+participant)
		scanIDs = [re.sub('\d+x','', x) for x in scanIDs]
		
		#loop through IDs; if unique, add to dictionary with BBLID
		for sequence in scanIDs:
			
			if sequence not in scansDict.keys():
				scansDict[sequence] = participant

    	tuple_list = list(scansDict.items())
    	splits = np.array_split(tuple_list, 64)
    	for splitnum, split in enumerate(splits):
        	
		df=pd.DataFrame(split)
		df.to_csv("SubjectList%d.csv" % splitnum, header=False, index=False)

def main():

	# Main Namespace Function
	print("Creating arrays")
	GetParticipants()

if __name__ == "__main__":
	main()
