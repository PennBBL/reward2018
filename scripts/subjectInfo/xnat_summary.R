source("setup.R")

# this script provides summaries of numbers from XNAT

# first read in the qeury & scan files
query <- read.tsv("reward_query_info.tsv") # will give n for each project
scans <- read.tsv("reward_scan_info.tsv") # will give n for each scan

######################################
# Number of subjects in each project
# saved as variable n.projects
######################################

n.projects <- num.query(query)

######################################
# Number of subjects in each project
######################################

n.scans <- num.scans(scans)

######################################
# output as CSV files
######################################

write.csv(n.projects, "reward_query_summary.csv")
write.csv(n.scans, "reward_scans_summary.csv")
