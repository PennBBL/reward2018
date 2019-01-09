'''
This script generates the data necessary
to cross check our Flywheel and CfN data for reward.

It writes CSVs of existing data on each to file in TMPDIR
'''

import os
import sys
import flywheel
import pandas as pd
import pydicom

def Collect_XNAT_Sessions():
    '''
    Loop through the joy directory collecting the XNAT sessions
    '''

    joy = "/data/joy/BBL/studies/reward2018/dicomsFromXnat/"
    bblids = [x for x in os.listdir(joy) if x.isdigit()]
    scanids = [os.listdir("{}{}/".format(joy,x)) for x in bblids]
    bbl_dict = dict(zip(bblids,scanids))

    return(bbl_dict)

def Collect_FW_Sessions(fw_client):
    '''
    Use flywheel SDK to collect all of
    the existing sessions
    '''

    project = fw_client.lookup("mcieslak/Reward2018")
    view = fw_client.View(columns='session')
    df = fw_client.read_view_dataframe(view, project.id)
    return(df)

def Load_Projects():
    '''
    Get the project names for scanIDs
    '''

    fpath = "/data/jux/BBL/projects/reward2018/reward2018/data/RewardAudit.csv"
    projects = pd.read_csv(fpath, index_col=0)
    return(projects)

def Unzip_Dicom(dcm, dest_dir):
    '''
    Unzip a dicom file to a destination directory
    '''

    dest_file = os.path.join(dest_dir, os.path.split(dcm)[1][:-3])
    os.system('gunzip -c %s > %s' % (dcm, dest_file))
    return(dest_file)

def Project_Lookup(proj):
    '''
    Get the project switch-statement style
    '''

    name_lookup = {
    'NODRA_MBREST': 'nodra',
    'NEFF_V2': 'neff2',
    'NEFF_PILOT': 'neff',
    'MOTIVE': 'neff2',
    'FNDM2_810211':'fndm1',
    'FNDM1_810211':'fndm2',
    'DAY2_808799':'day2',
    'NODRA_816281':'nodra'
    }

    return(name_lookup.get(proj))

def Get_Example_Dicom(bblid, scanid, dest_dir):
    '''
    Get an example dicom with pydicom
    '''

    dicom_path = "/data/joy/BBL/studies/reward2018/dicomsFromXnat/{}/{}/".format(str(bblid), str(scanid))
    all_files = os.listdir(dicom_path)

    if len(all_files) < 1:
        return(None)
    else:
        dcm_ex_file = all_files[0]
        ex_path = os.path.join(dicom_path, dcm_ex_file)

    if ex_path.endswith('.gz'):
        example = pydicom.dcmread(Unzip_Dicom(ex_path, dest_dir))
        os.system('rm $TMPDIR/*')
        return(example)
    else:
        example = pydicom.dcmread(ex_path)
        return(example)

def Get_Session_Date(bblid, scanid, dest_dir):

    dcm = Get_Example_Dicom(bblid, scanid, dest_dir)
    try:
        return(dcm.StudyDate)
    except:
        return(None)

if __name__ == "__main__":

    temp_dir = os.getenv("TMPDIR")
    if temp_dir is None:
        sys.exit(1)

    # load and parse the existing reward projects on flywheel
    fw = flywheel.Client()
    fw_reward = Collect_FW_Sessions(fw)
    fw_reward['date'] = pd.to_datetime(fw_reward['session.timestamp'])

    # load and parse the scans on CFN
    cfn = Load_Projects()
    cfn['project2'] = cfn.apply(lambda row: Project_Lookup(row['project']), axis=1)
    cfn['date'] = cfn.apply(lambda row: Get_Session_Date(row["bblid"], row["scanid"], temp_dir), axis=1)
    cfn['date'] = pd.to_datetime(cfn['date'])

    cfn.to_csv(os.path.join(temp_dir,"cfn.csv"), index=False)
    fw_reward.to_csv(os.path.join(temp_dir,"flywheel.csv"), index=False)
