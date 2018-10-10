#!/usr/bin/env python
import shutil
import os
import urllib3
urllib3.disable_warnings()
from tqdm import tqdm

from pyxnat import Interface
xnat_config = "/Users/annaxu/PROJECTS/XNAT/xnat.cfg"
central = Interface(config=xnat_config)

def get_sequences(scan_id):
    constraints = [
            ('xnat:mrSessionData.XNAT_COL_MRSESSIONDATALABEL', 
                'LIKE', '%'+ scan_id+'%' ),
            ('xnat:mrSessionData.SESSION_ID',
                'LIKE', '%'+ scan_id+'%' ), 
            ('xnat:mrSessionData.XNAT_COL_MRSESSIONDATASHARINGSHARELABEL', 
                'LIKE', '%' + scan_id + '%'), 'OR']
    seqs = central.select('bbl:Sequence',
            ['xnat:mrSessionData/XNAT_COL_MRSESSIONDATASHARINGSHARELABEL',
                'xnat:mrSessionData/SESSION_ID','bbl:Sequence/session_type'
             'xnat:mrSessionData/XNAT_COL_MRSESSIONDATALABEL', 
             'bbl:Sequence/SUBJECT_ID', 'bbl:Sequence/PROJECT', 
             'bbl:Sequence/QLUX_QLUXNAME', 'bbl:Sequence/IMAGESCAN_ID',
             'bbl:Sequence/date','bbl:Sequence/label']).where(constraints)
    if len(seqs) == 0:
        raise ValueError("No scans found for scan id "+scan_id)
    return seqs


def download_scanid(scan_id, output_dir, project=""):
    seqs = get_sequences(scan_id)

    unique_projects = set()
    unique_dates = set()
    unique_subject_ids = set()
    unique_session_ids = set()
    unique_session_labels = set()
    scans = []
    scan_to_id = []

    # If a project name is given, select only matching sequences
    if project:
        matching_seqs = []
        for line in seqs:
            if project in line["project"].lower():
                matching_seqs.append(line)
        seqs = matching_seqs

    for line in seqs:
        unique_projects.update([line.get("project")])
        unique_dates.update([line.get("date")])
        unique_subject_ids.update([line.get("subject_id")])
        unique_session_ids.update([line.get("xnat_mrsessiondata_session_id")])
        unique_session_labels.update(
                [line.get('xnat_mrsessiondata_xnat_col_mrsessiondatalabel')])
        scan_name = line.get("qlux_qluxname", "missing_name")
        scans.append(scan_name)
        scan_to_id.append((scan_name, line.get("imagescan_id")))
        
    if not len(unique_projects) == 1 :
        raise ValueError("Scan ID assigned to more than 1 project")
    project_id, = unique_projects
    
    if not len(unique_dates) == 1:
        print "WARNING: Scan ID assigned to more than 1 date"
    
    if not len(unique_subject_ids) == 1:
        raise ValueError("Scan ID assigned to more than 1 subject ID")
    bbl_id, = unique_subject_ids

    if not len(unique_session_ids) == 1:
        raise ValueError("Session ID assigned to more than 1 subject ID")
    session_id, = unique_session_ids
    
    # Get the subject object
    subject = central.select(
        "/projects/%s/subjects/%s"%(project_id,bbl_id))
    subject_label = subject.attrs.get("xnat:subjectData/label")
    
    all_files_to_get = {}
    for scan_name, seq_id in scan_to_id:
        rest_query = "/" + "/".join(
            [ "projects", project_id, "subjects", bbl_id, 
              "experiments", session_id, "scans", seq_id, 
              "resources", "DICOM", "files"])
        print rest_query
        all_files_to_get[seq_id] = list(central.select(rest_query))
    
    total_num_dicoms = sum([len(dcms) for dcms in all_files_to_get.values()])
    
    with tqdm(total=total_num_dicoms, unit="files") as pbar:
        for scan_name, seq_id in scan_to_id:
            pbar.set_postfix(scan=scan_name)
            for fileobj in all_files_to_get[seq_id]:
                output_file = output_dir + "/" + fileobj._urn
                
                if os.path.exists(output_file):
                    pbar.update(1)
                    continue
                
                fileobj.get(output_file)
                pbar.update(1)

    
        
    
        
        
        
        
        
