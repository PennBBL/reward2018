# Reward Dataset 2018

*By Tinashe M. Tapera*

*Updated 17 December 2018*

This repo is the project version of the repository on `/data/joy/studies/reward2018`. It contains initial attempts to gather, collate, aggregate, etc.-ate all of the scans from a number of projects. According to PI **Dan Wolf**, these projects include:

* day2
* fndm1
* fndm2
* motive
* neffpilot
* neffv2
* nodra81
* nodrambrest

The dicoms from these scans were stored on XNAT, but were somewhat scattered. After a lot of back and forth, we consolidated existing and missing scan IDs into what you currently see on `joy`.

## Prior Work

Prior work corresponding to this attempt can be found in <a href="https://github.com/PennBBL/reward2018/wiki/Reward-File-Management-&-Heudiconv">Anna's repo</a>. Aside from `/data/jux/BBL/projects/reward2018/reward2018/scripts/DownloadingFromXnat/` and various `sandbox`es, most of the scripts in this repository are results of the prior work.

## Defining Ground Truth

The first few weeks of this procedure were littered with emails, google sheets, and in-person discussions that make it difficult to be entirely precise about reproducibility and how we produced the ground truth. In sum:

* There were BBLID/ScanID directories that existed here on `/data/jux/BBL/reward2018/data/rawData`. These were the priors.
* We discovered that some data was missing from this; we consulted Dan Wolf who helped to define the projects that should be in there and any BBLID/ScanID pairs that he considered ground truth, and manually added these with a smattering of XNAT download scripts, resulting in a directory of priors and posteriors.

## Heudiconv

We wanted to use `heudiconv` to convert the data into a BIDS-compliant directory; to do this, we needed to run a script that summarises the dicoms according to their headers. In doing so, we discovered that previous work had not downloaded the full scanning session/sequence onto `jux` (instead, a single example dicom of each session exists for each BBLID/ScanID directory). As such, we had to double back our efforts and download *everything*.

## Downloading

We decided to download all of our reward data to `/data/joy/studies/reward2018/dicomsFromXnat/`. The following scripts are all located in `data/jux/BBL/projects/reward2018/scripts/DownloadingFromXnat/`

1. Using the priors and posteriors in `jux/.../rawData`, we construct bite-sized CSVs of the BBLID:ScanID pairs using the script `MakeSubjectCsvs.py` (note that the CSVs it creates end up located in the same directory it's run in, such that the next script has immediate access to these).
2. With these CSVs, we can parallelise our downloads to speed up the process. We use the script `DownloadRewardParallel.py`, and submit it to `qsub` using an <a href="http://wiki.gridengine.info/wiki/index.php/Simple-Job-Array-Howto">`SGE` task array</a> and the script `SubmitDownloadRewardParallel.sh`. This is done using the `XnatDownloadHelper` python module, which:
    1. Makes a query to Xnat using the BBLID:ScanID pair and checks for validity of this query's returned JSON table
    2. Loops through the data returned by the JSON table and downloads the scan sequences for each line
3. If you are skeptical (as I was), use the script `CheckDownloadsManual.py` which goes through each directory in `jux/.../rawData` and checks to see if data has been downloaded to `joy/.../dicomsFromXnat`.

## Flywheel

Now that all of the imaging data is on `/data/joy/BBL/studies/reward2018/dicomsFromXnat/`, we can switch it over to our new data warehouse on Flywheel. More information on how to use Flywheel will come soon, but for now, the remainder of this document describes how data was uploaded to their platform.

1. Dicoms on `/data/joy/studies/reward2018/dicomsFromXnat/` do not contain project names, hence it was necessary to once again interface with XNAT to obtain these. This was done using the script `GetStudyNamesForProtocols.py`, located at `/data/jux/BBL/projects/reward2018/reward2018/scripts/heudiconv`, and resulting in the file `Protocol_Summary_with_Projects.csv`, located in `/data/jux/BBL/projects/reward2018/reward2018/results/subjectInfo`.

2. Using `Protocol_Summary_with_Projects.csv`, we wrote a script `upload_reward.py` to upload the data to Flywheel. Again, the details of how to use Flywheel will be covered separately, but `upload_reward.py` loops through the data on `/data/joy/.../dicomsFromXnat`, x-checks the BBLID:ScanID pair against the protocol summary (to get the project name), unzips the zipped dicoms (because XNAT seemed to only give us zipped stuff), and creates an upload statement as a string. This string is then executed in the command line with Flywheel's `fw_cmd` (command line tools). This script is parallelised with another `SGE` task array tool, and submitted to a `qsub` job with `SubmitRewardUpload.sh`.

3. Unfortunately, not all of the data was uploaded on the first try (as `Protocol_Summary_with_Projects.csv` was not fully up to date). This was remedied later by auditing the directory and producing the static file `data/jux/BBL/projects/reward2018/data/RewardAudit.csv`. This contains the full list of reward participants and their projects, and hopefully helps to clarify all of the spread mentioned in parts 1 and 2.

4. Lastly, using the audit, we ran the following scripts from `data/jux/BBL/projects/reward2018/reward2018/scripts/DownloadingFromXnat` in a `qlogin` session:
* `consolidate_flywheel_cfn.py`, which audits data from Flywheel and CFN in the `TMPDIR`
* `consolidate_flywheel_cfn.R`, which matched and joined the audits and filtered out redundancies, creating a new file in `TMPDIR` that lists the remaining uploads still missing from Flywheel
* `upload_missing_reward.py`, which uploads the remaining data to Flywheel

Done!
