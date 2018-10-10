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

    # create keys
    t1w = create_key('sub-{subject}/anat/sub-{subject}_t1w')
    pcasl = create_key('sub-{subject}/asl/sub-{subject}_pcasl')
    
    # tasks
    face_01 = create_key('sub-{subject}/func/sub-{subject}_task-face_run-01')
    face_02 = create_key('sub-{subject}/func/sub-{subject}_task-face_run-02')

    card_01 = create_key('sub-{subject}/func/sub-{subject}_task-card_run-01')
    card_02 = create_key('sub-{subject}/func/sub-{subject}_task-card_run-02')
    
    effort_01 = create_key('sub-{subject}/func/sub-{subject}_task-effort_run-01')
    effort_02 = create_key('sub-{subject}/func/sub-{subject}_task-effort_run-02')
    effort_03 = create_key('sub-{subject}/func/sub-{subject}_task-effort_run-03')
    effort_04 = create_key('sub-{subject}/func/sub-{subject}_task-effort_run-04')
    
    itc_01 = create_key('sub-{subject}/func/sub-{subject}_task-itc_run-01')
    itc_02 = create_key('sub-{subject}/func/sub-{subject}_task-itc_run-02')
    
    # field maps --- NEED TO EDIT
    b0_map_01 = create_key('sub-{subject}/fmap/sub-{subject}_b0_map_run-01')
    b0_map_02 = create_key('sub-{subject}/fmap/sub-{subject}_b0_map_run-02')
    
    # resting state
    rest = create_key('sub-{subject}/func/sub-{subject}_task-rest')

    # create the heuristic
    info = {t1w: [], pcasl: [], face_01: [], face_02: [], 
            card_01: [], card_02: [], effort_01: [], effort_02: [], 
            effort_03: [], effort_04: [], itc_01: [], itc_02: [], 
            b0_map_01: [], b0_map_02: [], rest: [],
            }
    
    for s in seqinfo:
        protocol = s.protocol_name.lower()
        if "MPRAGE" in protocol:
            info[t1w].append(s.series_id)
        elif "pcasl" in protocol:
            info[pcasl].append(s.series_id)
        elif "faceA0" in protocol:
            info[face_01].append(s.series_id)
        elif "faceB0" in protocol:
            info[face_02].append(s.series_id)
        elif "cardA0" in protocol:
            info[card_01].append(s.series_id)
        elif "cardB0" in protocol:
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