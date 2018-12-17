

def MakeQuery(bblid, scanid, interface):
	
	# A function to build and make a query on XNAT
	# Input: BBLID, ScanID, XNAT interface
	# Return: JSON table of XNAT query results

	# assign constraints to get matching data rows
	constraints = [('xnat:subjectData/LABEL','LIKE', str(bblid).rjust(6,"*")), "AND", ('xnat:MRsession/LABEL','LIKE', str(scanid).rjust(6,"*"))]

	query = interface.select('bbl:Sequence',['bbl:Sequence/QLUX_QLUXNAME','bbl:Sequence/IMAGESCAN_ID','bbl:Sequence/SUBJECT_ID', 'bbl:Sequence/imageSession_ID', 'bbl:Sequence/date', 'bbl:Sequence/PROTOCOL', 'bbl:Sequence/PROJECT','bbl:Sequence/MR_SERIESDESCRIPTION','bbl:Sequence/MR_IMAGEORIENTATIONPATIENT','bbl:Sequence/QLUX_MATCHED']).where(constraints)

	# if the query fails, return NULL; if not, return the JSON table
	if len(query.data) < 1:
		
		print "Query Failed for %s: %s!" % (bblid, scanid)
		return(NULL)
	else:
		
		return(query)

def DownloadQuery(xnat_query, dest, interface):
	
	# A function to download the dicoms referenced by an XNAT query
	# Input: XNAT query (a JsonTable of bbl:Seqeunce data);
	#	 download destination;
	#	 XNAT interface;
	# Output: None
	
	# Build request, looping through each scanning sequence
	import os
	files_location = "/projects/%s/subjects/%s/experiments/%s/scans/%s/resources/DICOM/files"
	
	for sequence in xnat_query.data:
		
		string_request = files_location % (sequence['project'], sequence['subject_id'], sequence['session_id'], sequence['imagescan_id'])

		# Request files collection
		files = interface.select(string_request)
		
		# Loop through collection, download to destination
		for f in files:
			
			fname=f._urn	
			if os.path.isfile(dest+"/"+fname):
				print(str(fname) + " exists.")
				next
			else:
				print "Downloading all files to %s..." % dest
				f.get(dest+"/"+fname)
