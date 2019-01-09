
from tqdm import tqdm
import pandas as pd
import os
import sys
from glob import glob
import subprocess

projects = pd.read_csv("/data/jux/BBL/projects/reward2018/reward2018/results/subjectInfo/Protocol_Summary_with_Projects.csv")

projectscp = projects[["bblid","scanid","project"]].drop_duplicates()

name_lookup = {
    'NODRA_MBREST':'nodra', 
    'NEFF_V2':'neff2', 
    'NEFF_PILOT':'neff',
    'MOTIVE':'neff2', 
    'FNDM2_810211':'fndm1',
    'FNDM1_810211':'fndm2', 
    'DAY2_808799':'day2', 
    'NODRA_816281':'nodra'
}

temp_dir = os.getenv("TMPDIR")
if temp_dir is None:
    sys.exit(1)

nperchunk = projectscp.shape[0] // 33
task_id = os.getenv('SGE_TASK_ID')
chunknum = int(task_id)
start_index = nperchunk * (chunknum - 1)
end_index = min(projectscp.shape[0]-1, nperchunk * chunknum)

def unzip_directory(dirname, subjectname, projectname):
    files = glob(dirname + "/*")
    dest_dir = os.path.join(temp_dir, subjectname, projectname)
    os.makedirs(dest_dir, exist_ok=True)
    for fname in files:
        if fname.endswith('.gz'):
            dest_file = os.path.join(dest_dir, os.path.split(fname)[1][:-3])
            os.system('gunzip -c %s > %s' % (fname, dest_file))
        else:
            dest_file = os.path.join(dest_dir, os.path.split(fname)[1])
            os.system('cp %s %s' %(fname, dest_file))
    return dest_dir

error_cmds = []
for index, row in projectscp[start_index:end_index].iterrows():
    subject_id = str(row['bblid'])
    ses = str(row['scanid'])
    project = name_lookup[row['project']]
    dicoms_dir = "/data/joy/BBL/studies/reward2018/dicomsFromXnat/%s/%s" %(subject_id, ses)
    unzipped_dir = unzip_directory(dicoms_dir, subject_id, project)
    fw_cmd = 'fw import dicom --subject {subj_id} --session {ses_id} --de-identify ' \
             '{folder} {group_id} {project_label}'.format(subj_id=subject_id, ses_id=project,
                                                          folder=unzipped_dir, group_id='mcieslak',
                                                          project_label='Reward2018')
    proc = subprocess.Popen([fw_cmd], stdin=subprocess.PIPE, shell=True)
    proc.communicate(input=b'yes\n')

