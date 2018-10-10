#!/bin/bash

# obtain scan and session labels
scans=/data/jux/BBL/studies/reward/rawData/*/*/

for sc in $scans; 
	do ses=$(echo $sc|cut -d'/' -f9); 
	subID=$(echo $sc|cut -d'/' -f8);

	dir=$(echo /data/jux/BBL/studies/reward/rawData/output/.heudiconv/${subID});

# USE SINGULARITY HERE TO RUN HEUDICONV FOR DICOM INFO
# note to replace axu with your chead name instead

	singularity run -B /data/jux/BBL/studies/reward/rawData:/home/axu/base /data/joy/BBL/applications/heudiconv/heudiconv-latest.simg -d /home/axu/base/{subject}/{session}/*/*/*.dcm -o /home/axu/base/output -f convertall -s ${subID} -ss ${ses}  -c none --overwrite;

done 

