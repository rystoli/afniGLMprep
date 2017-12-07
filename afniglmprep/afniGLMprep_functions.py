# afniGLMprep version: 11/21/17
import pandas as pd
import numpy as np
import glob, os, sys
sys.dont_write_bytecode = True

#######################################################
# Prepare input
#######################################################

def prep_csv_to_inputdict( BIDS_path, inputcsv_path ):
    '''
    Prepares input_dict from a csv specifying inputs

    --------------
    ARGS:
    BIDS_path = str, glob path to BIDS formatted directory holding all data
    inputcsv_path = csv with input data (see afniGLMprep_params.py)
                    ...first row is column names, each subsequent row a single inputs
                    ...various required parameters: 'func_input_path', 'eventTSV_path', 'mask_path'
                    ...optional parameter: 'confoundsTSV_path' if including nuisance regressors
    --------------                
    Return: dict, keys: functional input paths, values: dicts, keys: eventTSV_path,
                        ...mask_path, confoundsTSV_path, values: corresponding paths - used as input in 
                        ...afniGLMprep_run.py
    '''

    data = pd.read_csv(inputcsv_path,delimiter=',')
    input_dict = {}
    for i,func_input_path in enumerate(data['func_input_path']):
        func_input_path = os.path.join(BIDS_path, func_input_path)
        eventTSV_path = os.path.join(BIDS_path, data['eventTSV_path'][i])
        mask_path = os.path.join(BIDS_path, data['mask_path'][i])
        
    #If there is a column with information about nuisance regressors,
    #add this to the input_dict and set a boolean variable to let other functions know
	if 'confoundsTSV_path' in data.columns:
	    confoundsTSV_path = os.path.join(BIDS_path, data['confoundsTSV_path'][i])
            regressOut = True
            input_dict[func_input_path] = {'eventTSV_path': eventTSV_path,
                                           'mask_path': mask_path,
                                           'confoundsTSV_path': confoundsTSV_path }
        else:
            regressOut = False
            input_dict[func_input_path] = {'eventTSV_path': eventTSV_path,
                                           'mask_path': mask_path }
    return input_dict,regressOut

###################################

def prep_alleventTSVs( BIDS_path, input_suffix, mask_path ):
    '''
    Prepares 'input_dict' used as input to all prep functions (1Ds, 3dDeconvolve)

    --------------
    ARGS:
    BIDS_path = str, glob path to BIDS formatted directory holding all data
    input_suffix = str, suffix after '_bold_' in functional input filenames, e.g.,
                'preprocessed' (no need for underscores, file extensions etc).
                *Leave empty string if no suffix (eg, filename ends in 'bold'
    mask_path = str, path to single mask to be applied to all subjects 
    --------------
    Return: dict, input_dict - see afniGLMprep_params.py for description   
    '''
    input_dict = {}
    # loop all subjects
    for s in glob.glob(os.path.join(BIDS_path,'sub-*/func/')):
        # loop all events.tsv files per subject
        for tsv_path in glob.glob(os.path.join( s, '*events.tsv' )):
            if input_suffix == '':
                func_input_path = tsv_path.split('events')[-2] + 'bold.nii.gz'
            else: 
                func_input_path = tsv_path.split('events')[-2] + 'bold_' + input_suffix + '.nii.gz'
            input_dict[func_input_path] = { 'eventTSV_path': tsv_path,
                                            'mask_path': mask_path }
    return input_dict
            

#######################################################
# Create 1D AFNI onset files per task/subject/run/trial_type
# does so based on trial_type column in *events.TSV per subject
#######################################################

def eventTSV_to_1D( BIDS_path, eventTSV_path, TR ):
    '''
    1. Reads events TSV
    2. takes pandas dataframe of BIDS events TSV
    3. then saves AFNI 1D onsets file per 'trial_type'
       * currently saves 1Ds in seconds

    --------------
    ARGS: 
    BIDS_path = str, glob path to BIDS formatted directory holding all data
    eventTSV_path = str, BIDS events TSV per run
    TR = int, length of TR in seconds
    --------------
    Return: No return, writes 1D files per trial_type
    '''

    if os.path.join(BIDS_path,'GLM_1Ds') not in glob.glob( os.path.join(BIDS_path,'*' )): os.makedirs( os.path.join( BIDS_path, 'GLM_1Ds' ) )
    else: pass
 
    data = pd.read_csv(eventTSV_path,delimiter='\t')

    for trial_type in np.unique(data['trial_type']):
        # create list of onsets per trial_type 
        # (conditions you want one GLM estimate for in each run)
        trial_type_onsets = list(data['onset'][data['trial_type'] == trial_type])
        trial_type_onsets_str = np.array([' '.join([str(onset*TR) for onset in trial_type_onsets])])

        # write
        prefix = os.path.join( BIDS_path, 'GLM_1Ds', eventTSV_path.split('/')[-1].split('.')[-2]) # define location and prefix for output
        np.savetxt('%s_%s.1D' % (prefix,trial_type), trial_type_onsets_str, fmt = '%s')
    return

###################################

def afni1D_per_task_subj_run( BIDS_path, TR ):
    '''
    Creates GLM_1Ds folder, and write 1D onsets file per 
    ...subject, per run, per trial_type in event TSV files per subject/run

    --------------
    ARGS:

    BIDS_path = str, glob path to BIDS formatted directory holding all data
    TR = int, TR in seconds
    --------------
    Return: No return, writes 1D files to GLM_1Ds, per subject/run/trial_type
    '''
  

    if os.path.join(BIDS_path,'GLM_1Ds') not in glob.glob( os.path.join(BIDS_path,'*' )): os.makedirs( os.path.join( BIDS_path, 'GLM_1Ds' ) )
    else: pass
 
    subdirs = [os.path.join(BIDS_path,i,'func') for i in glob.glob('sub-*')]
    for subdir in subdirs:
        for eventTSV_path in glob.glob(os.path.join(subdir,'*events.tsv')):
            eventTSV_to_1D( BIDS_path, eventTSV_path, TR )
    return

#######################################################
# Create 1D AFNI timecourse files for each nuisance regressor
# does so based on user-specified confounds.tsv file for each functional run
#######################################################

def confoundsTSV_to_1D( BIDS_path, confoundsTSV_path ):
    '''
    1. Reads confounds.tsv. This is a tab-delimited text file 
    that has one named column for each nuisance regressor. The number
    of rows should be equal to the number of volumes in each functional run.
    2. Takes pandas dataframe of confounds.tsv
    3. Saves AFNI 1D file for each column in confounds.tsv
    
    --------------
    NOTE: 
    Nuisance regressor timecourses can be generated using AFNI's 3dvolreg (for
    motion regressors), 3dSeg (for tissue-based regressors), or FSL's FAST
    --------------
    ARGS: 
    BIDS_path = str, glob path to BIDS formatted directory holding all data
    confoundsTSV_path = str, confounds TSV per run
    --------------
    Return: No return, writes 1D files per confound
    '''

    #Read confounds.tsv and create pandas dataframe
    data = pd.read_csv(confoundsTSV_path,delimiter='\t')

    #Figure out how many nuisance regressors the user has
    regressors = list(data)

    #Create 1D file for each regressor
    for r in regressors:
        confound_timecourse = list(data[r])
        prefix = os.path.join( BIDS_path, 'GLM_1Ds', confoundsTSV_path.split('/')[-1].split('.')[-2])
	confound_timecourse_str = np.array([' '.join([str(timepoint) for timepoint in confound_timecourse])])
        np.savetxt('%s_%s.1D' % (prefix,r), confound_timecourse_str, fmt = '%s')
    return

##################

def afni1D_per_confound_subj_run( BIDS_path ):
    '''
    Creates GLM_1Ds folder if necessary, and write 1D timecourse file
    ...per subject, per run, and per confound specified in _confounds.tsv

    --------------
    ARGS:

    BIDS_path = str, glob path to BIDS formatted directory holding all data
    confoundsTSV_path = str, confounds TSV per run
    --------------
    Return: No return, writes 1D files to GLM_1Ds, per subject/run/confound
    '''
  
    if os.path.join(BIDS_path,'GLM_1Ds') not in glob.glob( os.path.join(BIDS_path,'*' )): os.makedirs( os.path.join( BIDS_path, 'GLM_1Ds' ) )
    else: pass
     
    subdirs = [os.path.join(BIDS_path,i,'func') for i in glob.glob('sub-*')]
    for subdir in subdirs:
        for confoundsTSV_path in glob.glob(os.path.join(subdir,'*confounds.tsv')):
            confoundsTSV_to_1D( BIDS_path, confoundsTSV_path )
    return


#######################################################
# Write 3dDeconvolve function per subject/task/run 
#######################################################

def write_GLM_script( BIDS_path, func_input_path, eventTSV_path, mask_path, afniGLM_params, confoundsTSV_path = []):
    '''
    Write GLM 3dDeconvolve script per individual functional dataset in BIDS format, with TSV and AFNI 1Ds created via functions above

    --------------

    ARGS:
    BIDS_path = str, glob path to BIDS formatted directory holding all data
    func_input_path = str, path to functional 4D file to run GLM on
    eventTSV_path = str, path to TSV file holding task design for the functional input file
    mask_path = str, path to mask to apply
    afniGLM_params = object holding various parameters as attributes, via afniGLMprep_params.py
                     ...includes: hrf_func, polort, jobs, goforit, nfirst
    confoundsTSV_path = optional str, path to TSV file holding all nuisance regressor timecourses
    --------------
    Return: No return, saves script to current directory
    --------------

    TO DO:
    # need to add in motion: requires pandas read tsv from fmriprep, make 1D from motion columns
    '''    

    input_prefix = eventTSV_path.split('/')[-1][:-11]
    glmout_prefix = '/'.join(eventTSV_path.split('/')[:-1] + [eventTSV_path.split('/')[-1][:-11]])
    input_1Ds = glob.glob(os.path.join(BIDS_path, 'GLM_1Ds' , '%s*1D' % (input_prefix)))

    # if there are nuisance regressors, split the 1D files into two groups
    if confoundsTSV_path <> []:
        stim_files = []
        stim_times = []
        input1D_model = []
        input1D_confound = []
        for input1D in input_1Ds:
            elements = input1D.split('_')
            if 'confounds' in elements:
                input1D_confound.append(input1D)
            else:
                input1D_model.append(input1D)
        
        #for convenience: alphabetize stim labels so they will be the same for each subject and run
        input1D_confound = sorted(input1D_confound)
        input1D_model = sorted(input1D_model)

        #separately make -stim_times and -stim_file calls for each list
        for i,input1Dmodel in enumerate(input1D_model):
            trial_type,i = input1Dmodel.split('events_')[-1].split('.')[-2], i + 1 
            stim_times.append( "-stim_times %s %s '%s' -stim_label %s %s -iresp %s %s" % (i,input1Dmodel,afniGLM_params.hrf_func,i,trial_type,i,'iresp_%s_%s.nii.gz' % (input_prefix,trial_type)))

        for i,input1Dconfound in enumerate(input1D_confound):
            confound,i = input1Dconfound.split('confounds_')[-1].split('.')[-2], i + len(input1D_model) + 1 
            stim_files.append( "-stim_file %s %s -stim_base %s -stim_label %s %s" % (i,input1Dconfound,i,i,confound))

    else:
        stim_times = []
        input_1Ds = sorted(input_1Ds)
        for i,input1D in enumerate(input_1Ds):
            trial_type,i = input1D.split('events_')[-1].split('.')[-2], i + 1 
            stim_times.append( "-stim_times %s %s '%s' -stim_label %s %s -iresp %s %s" % (i,input1D,afniGLM_params.hrf_func,i,trial_type,i,'iresp_%s_%s.nii.gz' % (input_prefix,trial_type)) )

    # create function call + params set 
    params = '-polort %s -jobs %s -mask %s  -input %s  -fitts %s -errts %s  -bucket %s -fout -tout  -xjpeg %s  -GOFORIT %s  -nfirst %s  -num_stimts %s' % ( afniGLM_params.polort, afniGLM_params.jobs, mask_path, func_input_path, '%s_fitts.nii.gz' % (glmout_prefix), '%s_errts.nii.gz' % (glmout_prefix), '%s_bucket.nii.gz' % (glmout_prefix), '%s_designmatrix.jpg' % (glmout_prefix), afniGLM_params.goforit, afniGLM_params.nfirst, len(input_1Ds) )
    
    # combine params and stim_times for final script
    outpath = os.path.join( BIDS_path, 'GLM_1Ds' )
    if 'stim_files' in locals():
        glm_script = '3dDeconvolve ' + params + ' ' + ' '.join(stim_times) + ' ' + ' '.join(stim_files)
    else:
        glm_script = '3dDeconvolve ' + params + ' ' + ' '.join(stim_times)
    
    # write script
    np.savetxt(os.path.join(outpath,'GLM_%s.sh' % (input_prefix)), np.array([glm_script]), fmt = '%s')
    
    #Clear the default variable argument
    del confoundsTSV_path

    return

###################################

def write_GLM_script_per_task_subj_run( BIDS_path, input_dict, afniGLM_params ):
    '''
    Write GLM 3dDeconvolve script for multiple inputs: wraps 'write_GLM_script()'

    --------------
    ARGS:
    BIDS_path = str, glob path to BIDS formatted directory holding all data
    input_dict = dict, keys: input functional datasets ('func_input_path' variable), 
                       values: dictionary of TSV & mask:
                               'eventTSV_path': path to functional inputs events TSV file
                               'mask_path': path to mask file

                 Example: input_dict = {
                          'sub-01/func/sub-01_task-taskname_run-01_bold_preprocessed.nii.gz': { 
                              'eventTSV_path': 
                                  'sub-01/func/sub-01_task-taskname_run-01_events.tsv', 
                              'mask_path': 
                                  'sub-01/anat/sub-01_brain_mask.nii.gz' },
                          'sub-01/func/sub-01_task-taskname_run-02_bold_preprocessed.nii.gz': { 
                              'eventTSV_path': 
                                  'sub-01/func/sub-01_task-taskname_run-02_events.tsv', 
                              'mask_path': 
                                  'sub-01/anat/sub-01_brain_mask.nii.gz' },
                                        }

    afniGLM_params = object holding various parameters as attributes, via afniGLMprep_params.py
                     ...includes: hrf_func, polort, jobs, goforit, nfirst
    --------------
    Return: None, writes script per input
    '''
    
    for func_input_path,etc in input_dict.iteritems():
        if 'confoundsTSV_path' in etc.keys():
            write_GLM_script( BIDS_path = BIDS_path, 
                              func_input_path = func_input_path, 
                              eventTSV_path = etc['eventTSV_path'],
                              mask_path = etc['mask_path'],
                              afniGLM_params = afniGLM_params,
                              confoundsTSV_path = etc['confoundsTSV_path'] )
        else:
            write_GLM_script( BIDS_path = BIDS_path, 
                              func_input_path = func_input_path, 
                              eventTSV_path = etc['eventTSV_path'],
                              mask_path = etc['mask_path'],
                              afniGLM_params = afniGLM_params )
    return
