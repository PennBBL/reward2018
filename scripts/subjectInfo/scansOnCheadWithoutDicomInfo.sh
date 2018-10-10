#!/bin/bash

# obtain scan and session labels
scans=/data/jux/BBL/studies/reward/rawData/*/*/

for sc in $scans; 
	do ses=$(echo $sc|cut -d'/' -f9); 
	subID=$(echo $sc|cut -d'/' -f8);

	fileName=$(echo /data/jux/BBL/studies/reward/rawData/output/.heudiconv/${subID}/info/dicominfo_ses-${ses}.tsv);

# look for what doesn't exist 

	if [ ! -f ${fileName} ]; then
	missingFile=${fileName}
	echo ${subID},${ses} >> scansOnCheadWithoutDicomInfo.tsv
	fi

done 
