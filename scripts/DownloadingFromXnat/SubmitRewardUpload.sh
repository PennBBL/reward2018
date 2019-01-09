#!/bin/sh

#$ -t 1-32

unset PYTHONPATH; unalias python

export PATH=/data/joy/BBL/applications/miniconda3/bin:$PATH:/data/joy/BBL/applications/fw_bins

python /data/joy/BBL-extend/upload_reward.py
