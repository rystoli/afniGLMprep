# afniGLMprep
afniGLMprep prepares and runs is a set of python functions and scripts which automatically generate AFNI files and scripts used 


# files need to be in diretory steructure that matches bids (./sub-*/func/*nii.gz
# dont put 'events' in trial_type ; watch for split specifics...
# lets recommend a filename convention



# move to git doc
##### Example, two inputs
#input dict = { 
#  './preprocessed/out/fmriprep/sub-20/func/sub-20_task-emoculture_run-10_bold_space-MNI152NLin2009cAsym_preproc_smoothed.nii.gz': 
#    {'eventTSV_path': './sub-20/func/sub-20_task-emoculture_run-10_events.tsv', 
#    'mask_path': './preprocessed/out/fmriprep/sub-20/func/sub-20_task-emoculture_run-10_bold_space-MNI152NLin2009cAsym_brainmask.nii.gz'},
#
#  './preprocessed/out/fmriprep/sub-20/func/sub-20_task-emoculture_run-09_bold_space-MNI152NLin2009cAsym_preproc_smoothed.nii.gz': 
#    {'eventTSV_path': './sub-20/func/sub-20_task-emoculture_run-09_events.tsv', 
#    'mask_path': './preprocessed/out/fmriprep/sub-20/func/sub-20_task-emoculture_run-09_bold_space-MNI152NLin2009cAsym_brainmask.nii.gz'},
#}

