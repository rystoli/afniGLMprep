# afniGLMprep
afniGLMprep is python code which prepares and runs GLMs on neuroimaging data stored in the BIDS format (http://bids.neuroimaging.io/). This is done via AFNI's 3dDeconvolve function. 

## Purpose
Standardized structures for neuroimaging data have allowed the development of tools which perform various functions and analyses on data with relative automaticity and ease. The [BIDS (Brain Imaging Data Structure)](http://bids.neuroimaging.io/) has many tools for preprocessing and analysis of data (e.g., [BIDS apps](http://bids-apps.neuroimaging.io/)). Here is an initial set of functions to run first-level analyses via GLM on fMRI data. Specifically, this code automates generation of AFNI files and scripts necessary to estimate whole-brain response patterns to experimental conditions. 

In its current form, it gives whole-brain activation patterns per conditions, per functional 4D brain data. 

It reduces this large effort to a single line of code:
```
python BIDS_afniGLM_run.py prep1D prepGLM
```

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
- Input (which functional datasets, events files, and masks) should be specified in one of two ways:
1. It may automatically be generated, assuming it is to be created for all '\*event.tsv' files in subject/func/ directories. If this is the case, make sure to specify 'input_prefix' and 'mask_prefix', then include 'prepInput' in arguments for BIDS_afniGLM_run.py (see below)
2. Specify in 'BIDS_afniGLM_params.py', in the 'input_dict' format (see BIDS_afniGLM_params.py). For example:
```
input dict = { 
  # first input
  '/BIDS_folder/sub-01/func/sub-01_task-taskname_run-01_bold_preprocfinal.nii.gz': 
    {'eventTSV_path': '/BIDS_folder/sub-01/func/sub-01_task-taskname_run-01_events.tsv', 
    'mask_path': '/BIDS_folder/sub-01/anat/sub-01_task-taskname_brainmask.nii.gz'},
  # second input
  '/BIDS_folder/sub-01/func/sub-01_task-taskname_run-02_bold_preprocfinal.nii.gz': 
    {'eventTSV_path': '/BIDS_folder/sub-01/func/sub-01_task-taskname_run-02_events.tsv', 
    'mask_path': '/BIDS_folder/sub-01/anat/sub-01_task-taskname_brainmask.nii.gz'},
  # ... you  may include as many as you like!
               }
```
*note: currently requires a mask, though this may be the same for all subjects if you want*

## Execution
Execution is easily done from the command-line. After parameters are set in BIDS_afniGLM_params.py, simply run the 'BIDS_afniGLM_run.py', along with arguments which specify the actions you would like completed. You may enter as many actions as you would like, but must at least specify one action command: e.g., 'prep1D' or 'prepGLM'. The options at this time are:
- 'prepInput': prep input_dict of all functional runs to prepare the GLM for
- 'prep1D': prep AFNI 1D stimulus onset timing files
- 'prepGLM': prep AFNI 3dDeconvolve scripts
Example calls:
```
python BIDS_afniGLM_run.py prep1D
python BIDS_afniGLM_run.py prepGLM
python BIDS_afniGLM_run.py prep1D prepGLM 
python BIDS_afniGLM_run.py prepInput prep1D prepGLM 
```

## Output
- Stimulus onset timing files (1Ds) are placed in a directory 'GLM_1Ds' in the BIDS home folder you specified in BIDS_afniGLM_params.py
- AFNI 3dDeconvolve scripts are placed in the BIDS home folder specified in BIDS_afniGLM_params.py

Feel free to try it out on public [BIDS example datasets](https://github.com/INCF/BIDS-examples)!
## To-do / Limitations
- Create method and option to include motion estimates in design matrix
- Create fully flexible 3dDeconvolve script generation, allowing user to add additional parameters
- Create additional forms of 3dDeconvolve, eg, if user prefers more advanced models, or estimates per onset/trial
- Allow option to begin analyses
