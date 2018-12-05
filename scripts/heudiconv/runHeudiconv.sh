#/bin/bash

# obtain scan and session labels
scans=/data/jux/BBL/projects/reward2018/reward2018/data/rawData/*/*/

for sc in $scans; 
	do ses=$(echo $sc|cut -d'/' -f11); 
	subID=$(echo $sc|cut -d'/' -f10);

# USE SINGULARITY HERE TO RUN HEUDICONV FOR BIDS FORMATTING
# note to replace axu with your chead name instead

	singularity run -B /data/jux/BBL/projects/reward2018/reward2018/data/rawData:/home/axu/base /data/joy/BBL/applications/heudiconv/heudiconv-latest.simg -d /home/axu/base/{subject}/{session}/*/*/*.dcm -o /home/axu/base/NIFTI -f /home/axu/base/reward_heuristic.py -s ${subID} -ss ${ses}  -c dcm2niix -b --overwrite;

done 
