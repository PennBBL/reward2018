#!/bin/bash

# obtain scan and session labels
scans=/data/jux/BBL/studies/reward/rawData/*/*/

for sc in $scans; 
	do ses=$(echo $sc|cut -d'/' -f9); 
	subID=$(echo $sc|cut -d'/' -f8);

	fileName=$(echo /data/jux/BBL/studies/reward/rawData/${subID}/${ses}/*/dicom*/*.dcm);

# look for what doesn't exist 

for fn in $fileName
	do if [ ! -f ${fn} ]; then
	missingFile=${fn}
	echo ${subID},${ses} >> scansOnCheadWithoutDicomFILE.tsv
	fi
done 

done 
