# afniGLMprep
afniGLMprep is python code which prepares and runs GLMs on neuroimaging data stored in the BIDS format (http://bids.neuroimaging.io/). This is done via AFNI's 3dDeconvolve function. 

## Purpose
Standardized structures for neuroimaging data have allowed the development of tools which perform various functions and analyses on data with relative automaticity and ease. The [BIDS (Brain Imaging Data Structure)](http://bids.neuroimaging.io/) has many tools for preprocessing and analysis of data (e.g., [BIDS apps](http://bids-apps.neuroimaging.io/)). Here is an initial set of functions to run first-level analyses via GLM on fMRI data. Specifically, this code automates generation of AFNI files and scripts necessary to estimate whole-brain response patterns to experimental conditions. 

## Specific Functions 
- Generates AFNI 3dDeconvolve scripts per functional dataset specified
- Generates AFNI 1D stimulus onset timing files for GLM design matrices (input for 3dDeconvolve)

## Requirements
- Uses several scientific python libraries (pandas, numpy)
- Data must be stored in the BIDS format. All functions require very specific directory structures and file names.
- Stimulus onset timing files (1Ds) are made from BIDS formatted \*events.tsv files

## Content
- BIDS_afniGLM_run.py: command-line script to execute functions (see instructions below)
- BIDS_afniGLM_params.py: text file where user specifies input and analysis parameters
- BIDS_afniGLM_functions.py: functions used to generate analysis files

## Preparation
- Experimental conditions to be estimated (design matrix columns) come from events.tsv files. One is required per functional input dataset you wish to execute the GLM on (so if you have a constant design, simply duplicate the files and name them appropriately in BIDS format).
-- e.g., '/BIDS_folder/sub-01/func/sub-01_task-taskname_run-01_events.tsv'
- Input datasets must be named in BIDS format, and placed in directories with subject functional data. If using preprocessed data (obv), it is recommended you use the same filename as the raw data in the /func/ directory, with a suffix 
-- e.g., 'preprocfinal', e.g., '/BIDS_folder/sub-01/func/sub-01_task-taskname_run-01_bold_preprocfinal.nii.gz'
*note, it is recommended user-specified strings in filenames (e.g., task names, suffixes) do not overlap with strings in filenames as part of the BIDS format (e.g., 'events', 'run', 'bold'), as BIDS filenames are split to navigate and produce files*
- GLM parameters (for 3dDeconvolve scripts) should be specified or checked in 'BIDS_afniGLM_params.py'
- Input (which functional datasets, events files, and masks) should be specified in 'BIDS_afniGLM_params.py', in the 'input_dict' format (see BIDS_afniGLM_params.py). For example:
```
input dict = { 
  \# first input
  '/BIDS_folder/sub-01/func/sub-01_task-taskname_run-01_bold_preprocfinal.nii.gz': 
    {'eventTSV_path': '/BIDS_folder/sub-01/func/sub-01_task-taskname_run-01_events.tsv', 
    'mask_path': '/BIDS_folder/sub-01/anat/sub-01_task-taskname_brainmask.nii.gz'},
  \# second input
  '/BIDS_folder/sub-01/func/sub-01_task-taskname_run-02_bold_preprocfinal.nii.gz': 
    {'eventTSV_path': '/BIDS_folder/sub-01/func/sub-01_task-taskname_run-02_events.tsv', 
    'mask_path': '/BIDS_folder/sub-01/anat/sub-01_task-taskname_brainmask.nii.gz'},
  \# ... you  may include as many as you like!
               }
```

## To-do
- motion
- analysis run

