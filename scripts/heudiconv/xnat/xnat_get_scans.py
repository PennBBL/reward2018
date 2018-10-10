#!/data/joy/BBL/applications/miniconda3/envs/py2k/bin/python
import os
from glob import glob
import pandas as pd
import sys
from xnat2BIDS import central

# replace w/ the relevant project names
project_names = ["DAY2_808799",
                 "FNDM1_810211",
                 "FNDM2_810211",
                 "NEFF_PILOT",
                 "NEFF_V2",
                 "NODRA_816281",
                 "NODRA_MBREST"]
project_experiments = {}

for project in project_names:
      project_experiments[project] = list(
              central.select.project(project).experiments()) 

query_infos = []

# Each experiment has some IDs we need to get to query 
for project, experiments in project_experiments.items():
    for experiment in experiments:
        query_infos.append({
            "subject_label": experiment.attrs.get("subject_label"),
            "project": project,
            "scan_id":  experiment.label(),
            "experiment_ID":experiment.attrs.get("ID"),
            "subject_ID": experiment.attrs.get("subject_ID")})
        print query_infos[-1]

all_subjects = pd.DataFrame(query_infos)
all_subjects.to_csv("reward_query_info.tsv", sep="\t",
        index=False)

# output file
all_subjects = pd.read_table("reward_query_info.tsv")
# For each subject are we able to find scans in xnat?
session_infos = []
for rownum,row in tqdm(all_subjects.iterrows()):
    scans_query = "/" + "/".join(
        [ "projects", row.project, "subjects", row.subject_ID, 
          "experiments", row.experiment_ID, "scans"])
    
    # Get the info about all the scans
    scan_ids = central.select(scans_query).get()
    infodict = row.to_dict()
    for scan_id in scan_ids:
        scan_query = scans_query + "/" + scan_id
        scan_obj = central.select(scan_query)
        scan_type = scan_obj.attrs.get("series_description")
        infodict[scan_type] = scan_id
    session_infos.append(infodict)

all_info = pd.DataFrame(session_infos)
all_info.to_csv("reward_scan_info.tsv", sep="\t",
        index=False)


          

