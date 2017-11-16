# afniGLMprep version: 11/16/17

import sys
sys.dont_write_bytecode = True
import afniGLMprep_functions as apf
import afniGLMprep_params as p

###########################################################
# Confirm commands entered correctly
###########################################################

print('Input options: prepInput, csvInput, prep1D, prepGLM')
print('User input: %s' % (sys.argv[1:]) )

assert ('prep1D' in sys.argv) or ('prepGLM' in sys.argv),'Please specify functions. Options: prep1D prepGLM'

assert ('prepInput' in sys.argv) ^ ('csvInput' in sys.argv),'Please only specify one input source: prepInput (automatic loading, see doc), or csvInput (load input from afniGLMprep_input.csv'

###########################################################
# Prepare input
###########################################################

# Automatically generate input_dicts
if 'prepInput' in sys.argv:
    p.input_dict = apf.prep_alleventTSVs( p.BIDS_path, p.input_suffix, p.mask_path )
    print('%s inputs automatically prepared' % (len(p.input_dict)))
else: pass

if 'csvInput' in sys.argv:
    p.input_dict,p.regressOut = apf.prep_csv_to_inputdict( p.BIDS_path, p.inputcsv_path)
    print('%s inputs loaded from afniGLMprep_input.csv' % (len(p.input_dict)))
    if p.regressOut:
        print('Nuisance regressors will be added to your model.')
    else: pass
else: pass


###########################################################
# Prepare GLM materials
###########################################################

# Create any 1Ds currently missing corresponding to input_dict event TSVs
if 'prep1D' in sys.argv:
    for inputfile in p.input_dict:
        apf.eventTSV_to_1D( p.BIDS_path, p.input_dict[inputfile]['eventTSV_path'], p.TR )
    print('Condition onset timing files (1Ds) prepared in /GLM_1Ds')
    if p.regressOut:
        for inputfile in p.input_dict:
            apf.confoundsTSV_to_1D( p.BIDS_path, p.input_dict[inputfile]['confoundsTSV_path'] )
        print('Confound timecourse files (1Ds) prepared in /GLM_1Ds')
    else: pass        
else: pass

# Creat GLM script per input_dict keys
if 'prepGLM' in sys.argv:
    apf.write_GLM_script_per_task_subj_run( BIDS_path = p.BIDS_path, 
                                                input_dict = p.input_dict,
                                                afniGLM_params = p )
    print('GLM (3dDeconvolve) scripts prepared in BIDS directory')
else: pass

###########################################################

print('afniGLMprep completed')
