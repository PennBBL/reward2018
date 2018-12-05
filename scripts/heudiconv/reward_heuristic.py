import os

# create a key
def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

# create the dictionary evaluate the heuristics
def infotodict(seqinfo):

    """Heuristic evaluator for determining which runs belong where
    allowed template fields - follow python string module:
    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """
    
    # Create Keys
    t1w = create_key('sub-{subject}/anat/sub-{subject}_T1w')

    # ASL
    pcasl = create_key('sub-{subject}/asl/sub-{subject}_pcasl')    
    
    # Field maps
    b0_phase = create_key('sub-{subject}/fmap/sub-{subject}_phasediff')
    b0_mag = create_key('sub-{subject}/fmap/sub-{subject}_magnitude')

    # fmri scans
    rest = create_key('sub-{subject}/func/sub-{subject}_task-rest_bold')
    
    face_01 = create_key('sub-{subject}/func/sub-{subject}_task-face_run-01_bold')
    face_02 = create_key('sub-{subject}/func/sub-{subject}_task-face_run-02_bold')

    card_01 = create_key('sub-{subject}/func/sub-{subject}_task-card_run-01_bold')
    card_02 = create_key('sub-{subject}/func/sub-{subject}_task-card_run-02_bold')
    
    effort_01 = create_key('sub-{subject}/func/sub-{subject}_task-effort_run-01_bold')
    effort_02 = create_key('sub-{subject}/func/sub-{subject}_task-effort_run-02_bold')
    effort_03 = create_key('sub-{subject}/func/sub-{subject}_task-effort_run-03_bold')
    effort_04 = create_key('sub-{subject}/func/sub-{subject}_task-effort_run-04_bold')
    
    itc_01 = create_key('sub-{subject}/func/sub-{subject}_task-itc_run-01_bold')
    itc_02 = create_key('sub-{subject}/func/sub-{subject}_task-itc_run-02_bold')

    # create the heuristic
    info = {t1w: [], pcasl: [], face_01: [], face_02: [], 
            card_01: [], card_02: [], effort_01: [], effort_02: [], 
            effort_03: [], effort_04: [], itc_01: [], itc_02: [], 
            b0_mag: [], b0_phase: [], rest: [],
            }
    for s in seqinfo:
        protocol = s.protocol_name.lower()
        if "mprage" in protocol:
            info[t1w].append(s.series_id)
        elif "pcasl" in protocol:
            info[pcasl].append(s.series_id)
        elif "b0map" in protocol and "M" in s.image_type:
            info [b0_mag].append(s.series_id)
        elif "b0map" in protocol and "P" in s.image_type:
            info [b0_phase].append(s.series_id)
        elif "facea0" in protocol:
            info[face_01].append(s.series_id)
        elif "faceb0" in protocol:
            info[face_02].append(s.series_id)
        elif "carda0" in protocol:
            info[card_01].append(s.series_id)
        elif "cardb0" in protocol:
            info[card_02].append(s.series_id)
        elif "effort1" in protocol:
            info[effort_01].append(s.series_id)
        elif "effort2" in protocol:
            info[effort_02].append(s.series_id)
        elif "effort3" in protocol:
            info[effort_03].append(s.series_id)
        elif "effort4" in protocol:
            info[effort_04].append(s.series_id)
        elif "itc1" in protocol:
            info[itc_01].append(s.series_id)
        elif "itc2" in protocol:
            info[itc_02].append(s.series_id)
        elif "bold" in protocol:
            info[rest].append(s.series_id)
    return info
