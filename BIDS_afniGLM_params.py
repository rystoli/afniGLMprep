#######################################################
# Set paths

BIDS_path = './'      # set path to BIDS study top directory


#######################################################
# Set GLM Parameters - see 3dDeconvolve doc: https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dDeconvolve.html

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
TR          =   2     # length of TR in seconds


#######################################################
# Set inputs
### Here, each key in 'input_dict' is an input nifti file you wish to run the GLM on.
### For each input file (keys), there is a dictionary assigned, holding both the
### event TSV file and mask.

input_dict = { 

# example input, multiply these for additional runs, or create script to automate
'func_input_path': {       # string specifying functional input file (*.nii.gz)
    'eventTSV_path': '',  # string specifying events tsv file (*.tsv)
    'mask_path': ''        # string specifying mask file (*.nii.gz)
                   },

}