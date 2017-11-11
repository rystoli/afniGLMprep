# afniGLMprep
afniGLMprep is python code which prepares and runs GLMs on neuroimaging data stored in the BIDS format (http://bids.neuroimaging.io/). This is done via AFNI's 3dDeconvolve function. 

## Purpose
Standardized structures for neuroimaging data have allowed the development of tools/apps which perform various functions and analyses on data with relative automaticity and ease. The [BIDS (Brain Imaging Data Structure)](http://bids.neuroimaging.io/) 

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

