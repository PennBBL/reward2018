###################################################################################
# setup
###################################################################################

source("setup.R")

###################################################################################
# read file of what's in chead & change the headings to the appropriate name
###################################################################################

cfn_reward_dicoms <- as.data.frame(read.csv("rewardDicoms_09-24-2018.csv"))

# clean up this CSV because it makes the first subject the headers of the csv
# when it should, instead, be an observation
subj1 <- names(cfn_reward_dicoms)

# clean this up by taking out the "X"
library(stringr)
subj1 <- str_replace_all(subj1, "X", "") 

# coerve this to a dataframe so we can bind it to the prev df
subj1 <- as.data.frame(t(subj1)) 
names(subj1) <- names(cfn_reward_dicoms)

# now we add it as the last observation
cfn_reward_dicoms <- rbind(cfn_reward_dicoms, subj1) 

# replace the name w/ something that makes sense
names(cfn_reward_dicoms) <- c("subject_label", "timepoint", "date", "scan_id")

###################################################################################
# read the info from XNAT
###################################################################################

xnat_reward <- read.tsv("reward_query_info.tsv")

###################################################################################
# look at what subjects are missing on chead that are on xnat
###################################################################################

# note: this produces a dataframe of the included subjects and the missing subjects
cfn_missing <- findMissing(cfn_reward_dicoms$subject_label, xnat_reward$subject_label)

###################################################################################
# get the subject information of what's missing (based on what's provided on XNAT)
###################################################################################

cfn_missing_info <- subset(xnat_reward, is.element(subject_label, cfn_missing$missing))

# produce a CSV that can be uploaded for info on the missing subjects
write.csv(cfn_missing_info, "cfn_missing_info.csv")