# afniGLMprep version: 11/13/17
import os, sys
sys.dont_write_bytecode = True

#######################################################
# Set paths

# set path to BIDS study top directory
### tip: don't use variables to refer to path components, e.g., tilda (~) to refer to home path
BIDS_path = ''

#######################################################
# Paths for input specification

##### OPTION 1
# If intending to use 'csvInput', see doc, and specify input csv path:
inputcsv_path = 'afniGLMprep_input.csv'

##### NUISANCE REGRESSORS (MOTION ETC.)
# If intending to use nuisance regressor option with csvInput (see README.md), set regressOut to 1 (True):
regressOut = ''

##### OPTION 2
# If intending to use 'prepInput' automatic input generation, please see option doc, and specify:
# sub-01_task-taskname_run-01_bold_preprocfinal.nii.gz
input_suffix = 'preprocfinal' 
# set path to mask applied to all subjects if having afniGLMprep automatically generate the input_dict (instead of doing so below)
mask_path = 'union_brain_mask.nii.gz' 

#######################################################
# Set GLM Parameters - see 3dDeconvolve doc: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dDeconvolve.html

TR          =   2     # length of TR in seconds
polort      =   'A'   # the degree with which to model the baseline 
                      # ...in each run. Degree 0 is a constant, 1 is 
                      # ...linear drift, 2 is quadratic 
                      # 'A' default sets automatically, see 3dDeconvolve doc
jobs        =   8     # J should be a number from 1 up to the number of CPUs 
                      # ...sharing memory on the system
goforit     =   0     # Number of warnings to allow 3dDeconvolve to ignore... 
                      # ...see doc! important.
nfirst      =   0     # number of first dataset image to use in the 
                      # ...deconvolution procedure
hrf_func    =   'GAM' # response model, see 3dDeconvolve doc for options, 
                      # ...defaults to gamma function

