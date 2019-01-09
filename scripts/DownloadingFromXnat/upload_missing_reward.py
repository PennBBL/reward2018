'''
This script reads in the csv designating the missing reward
data and uploads this to flywheel similar to the first upload script
'''

from tqdm import tqdm
import pandas as pd
import os
import sys
from glob import glob
import subprocess

temp_dir = os.getenv("TMPDIR")
if temp_dir is None:
    sys.exit(1)

projects = pd.read_csv(os.path.join(temp_dir, "consolidated_projects.csv"))

def unzip_directory(dirname, subjectname, projectname):
    files = glob(dirname + "/*")
    dest_dir = os.path.join(temp_dir, subjectname, projectname)
    os.makedirs(dest_dir)
    for fname in files:
        if fname.endswith('.gz'):
            dest_file = os.path.join(dest_dir, os.path.split(fname)[1][:-3])
            os.system('gunzip -c %s > %s' % (fname, dest_file))
        else:
            dest_file = os.path.join(dest_dir, os.path.split(fname)[1])
            os.system('cp %s %s' %(fname, dest_file))
    return dest_dir

error_cmds = []
for index, row in projects.iterrows():
    subject_id = str(row['bblid'])
    ses = str(row['scanid'])
    project = str(row['project'])
    dicoms_dir = "/data/joy/BBL/studies/reward2018/dicomsFromXnat/%s/%s" %(subject_id, ses)
    unzipped_dir = unzip_directory(dicoms_dir, subject_id, project)
    fw_cmd = 'fw import dicom --subject {subj_id} --session {ses_id} --de-identify ' \
             '{folder} {group_id} {project_label}'.format(subj_id=subject_id, ses_id=project,
                                                          folder=unzipped_dir, group_id='mcieslak',
                                                          project_label='Reward2018')
    proc = subprocess.Popen([fw_cmd], stdin=subprocess.PIPE, shell=True)
    proc.communicate(input=b'yes\n')
