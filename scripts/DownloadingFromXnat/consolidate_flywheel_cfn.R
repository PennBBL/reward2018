library(dplyr)

# This script does a simple join and filter on the data present on
# flywheel and on CFN, and cross checks the data to filter out anything
# on flywheel already. It then writes the remaining to csv in TMPDIR

flywheel <- read.csv(paste0(Sys.getenv("TMPDIR"),"/flywheel.csv"),
                    stringsAsFactors = FALSE) %>%
  as_tibble() %>%
  rename(bblid = "subject.label", project2 = "session.label")

cfn <- read.csv(paste0(Sys.getenv("TMPDIR"),"/cfn.csv"),
               stringsAsFactors = FALSE) %>%
  as_tibble()

cfn$bblid <- as.character(cfn$bblid)

joined <- cfn %>%
  left_join(flywheel, by = c("bblid","project2"))

joined <- joined %>%
  group_by(bblid,  project2) %>%
  mutate(index = row_number()) %>%
  ungroup() %>%
  mutate(project2 = ifelse(index > 1,
                           paste(project2,index, sep="_"),
                           project2)) %>%
  filter(is.na(project.id)) %>%
  select(bblid, scanid, project = project2)

write.csv(joined, paste0(Sys.getenv("TMPDIR"),"/consolidated_projects.csv"))

UnzipOrCopyFile <- function(fpath, target){

  if(grepl(".gz$", fpath)) {

    target <- file.path(target, basename(fpath))

    system(sprintf('gunzip -c %s > %s', fpath, target))

  } else {

    file.copy(fpath, target)

  }
}

UnzipDirectory <- function(bblid, scanid){

  joy_path <- "/data/joy/BBL/studies/reward2018/dicomsFromXnat"

  scans_directory <- file.path(joy_path, bblid, scanid)

  scans <- sapply(list.files(scans_directory),
                  function(x) file.path(scans_directory,x),
                  USE.NAMES=FALSE)

  targetDir <- file.path(Sys.getenv("TMPDIR"), scanid)

  if(!file.exists(targetDir)) {
    dir.create(targetDir)
  }

  lapply(scans, UnzipOrCopyFile, targetDir)
  return(targetDir)
}

UploadFlywheel <- function(bblid, scanid, study){

  dir_to_upload <- UnzipDirectory(bblid, scanid)

  fw_cmd <- sprintf('fw import dicom --subject %s --session %s --de-identify %s %s %s',
                    bblid, study, dir_to_upload, 'mcieslak', 'Reward2018')
  system(fw_cmd)
  unlink(dir_to_upload, recursive=TRUE)
}
