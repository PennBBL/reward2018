#!/bin/bash

# A script for obtaining dicom info from a directory of dicoms, structured: {subjID}/{scanID}/{scantype}/dicoms/{dicom}.nii.gz
# Modified to get dicom info for recently downloaded XNAT dicoms in /data/joy/BBL/studies/reward2018

# obtain scan and session labels
scans=/data/joy/BBL/studies/reward2018/dicomsFromXnat/*/*/

for sc in $scans; do
	
	ses=$(echo $sc|cut -d'/' -f9); 
	subID=$(echo $sc|cut -d'/' -f8);
	
# USE SINGULARITY HERE TO RUN HEUDICONV FOR DICOM INFO
# note to replace axu with your chead name instead
	
	/share/apps/singularity/2.5.1/bin/singularity run -B /data:/home/ttapera/data /data/joy/BBL/applications/heudiconv/heudiconv-latest.simg -d /home/ttapera/data/joy/BBL/studies/reward2018/dicomsFromXnat/{subject}/{session}/*.dcm.gz -o /home/ttapera/data/joy/BBL/studies/reward2018/dicomsFromXnat/output -f convertall -s ${subID} -ss ${ses}  -c none --overwrite;

done 

