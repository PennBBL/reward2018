#!/bin/bash
#$ -t 1-64
unset PYTHONPATH; unalias python

export PATH=/data/joy/BBL/applications/miniconda3/bin:$PATH
source activate py2k
my_input=/data/jux/BBL/projects/reward2018/reward2018/scripts/sandbox/SubjectList${SGE_TASK_ID}.csv
python /data/jux/BBL/projects/reward2018/reward2018/scripts/sandbox/CheckDownloadsParallel.py $my_input
