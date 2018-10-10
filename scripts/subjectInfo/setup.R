# Load packages
library(dplyr)
library(reshape2)

# USEFUL FUNCTIONS

#############################################################################
# cleanly look at tsv files
#############################################################################

read.tsv <- function(tsv){
  read.table(file=tsv, sep="\t", header=TRUE)
}

#############################################################################
# Function for finding n for each scan using tsv file
#############################################################################

num.scans <- function(df){
  tmp.df <- melt(df, id=c("scan_id","project"))
  tmp.df2 <-
    tmp.df %>%
    na.omit() %>%
    group_by(variable, project) %>%
    summarise(n()) %>%
    filter((variable != "X") &
             (variable != "subject_ID") &
             (variable != "experiment_ID") &
             (variable != "subject_label"))
  final.df <- dcast(tmp.df2, project~variable)
  return(final.df)
}

#############################################################################
# Function for finding n for each project using tsv file
#############################################################################
num.query <- function(df){
  df %>%
    group_by(project) %>%
    summarise(n())
}

#############################################################################
# find what's included and missing from A to B
# B is the what we predict might contain some elements that A does not have
#############################################################################

findMissing <- function(varOfInterest, groundTruthVar){
  # initialize vectors that will contain included and missing datapoints
  includedDat <- c()
  missingDat <- c()
  # loop through all of the ground truth datapoints to see if they exist in vector of interest
  for (i in 1:length(groundTruthVar)){
    if (is.element(groundTruthVar[i], varOfInterest)){
      includedDat <- c(includedDat, groundTruthVar[i])
    } else {missingDat <- c(missingDat, groundTruthVar[i])}
  }
  # create a dataframe of the ones that are included and the ones that aren't
  existenceDF <- data.frame(matrix(NA, ncol=2, 
                                   nrow=max(length(includedDat), length(missingDat))))
  names(existenceDF) <- c("included", "missing")
  existenceDF$included[1:length(includedDat)] <- includedDat
  existenceDF$missing[1:length(missingDat)] <- missingDat
  # return this dataframe
  return(existenceDF)
}

