#####################################################
#                                                   #
# Heaudiconv Heuristic Summary: Part 1              #
#                                                   #
# 20181116                                          #
# Tinashe M. Tapera                                 #
#                                                   #
# This script generates a dataframe that            #
# gathers all of the dicom-info files               #
# created in the reward pipeline. It's              #
# useful for knowing the different protocols        #
# and scan types available in the repo              #
# so that we can build appropriate heuristics       #
# before Heudiconv-ing the repo.                    #
#                                                   #
#####################################################

message("Gathering Dicom info & Writing to \"*/results/subjectInfo/Protocol_Summary.csv\"...")

library(dplyr, quietly=TRUE)
library(tibble, quietly=TRUE)
setwd("/data/jux/BBL/projects/reward2018/reward2018/data/rawData/output/.heudiconv/")

# a function to extract the BBLID from the path variable
ExtractBBLID = function(x){
  x%>%
    as.character()%>%
    strsplit("/")%>%
    .[[1]]%>%
    .[grepl(pattern="^[[:digit:]]+", x = .)]%>%
    return()
}

ExtractSCANID = function(x){
  
  x%>%
    as.character()%>%
    gsub(".*x([[:digit:]]+)\\.tsv", "\\1", ., perl=TRUE)%>%
    return()
}


# get path of all dicoms
all_files = list.files(".", recursive = TRUE)%>%
  .[grep(pattern = ".*dicominfo.*\\.tsv$", x=.)]%>%
  paste(getwd(),.,sep = "/")

# instantiate
dicoms=tibble()

# loop through dicoms, download, and bind
for(x in 1:length(all_files)){
  dicoms = read.table(all_files[x], sep="\t", fill=TRUE, header = TRUE, stringsAsFactors = FALSE)%>%
    mutate(source=all_files[x])%>%
    rbind(dicoms,data.frame(.))
}

# Extract the bblid & scanID
dicoms = as_tibble(dicoms)%>%
  mutate(bblid = sapply(X = .$source, FUN = ExtractBBLID),
	 scanid = sapply(X = .$source, FUN = ExtractSCANID))%>%
  select(-source)

# write out
dicoms%>%
  write.csv("/data/jux/BBL/projects/reward2018/reward2018/results/subjectInfo/Protocol_Summary.csv")
