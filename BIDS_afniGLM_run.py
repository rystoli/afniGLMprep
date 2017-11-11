import sys
sys.dont_write_bytecode = True
import BIDS_afniGLM_functions as afniGLMprep
import BIDS_afniGLM_params as p

assert (len(sys.argv) > 1),'Please specify functions. Options: prep1D prepGLM'

# Create any 1Ds currently missing corresponding to input_dict event TSVs
if 'prep1D' in sys.argv:
    for inputfile in p.input_dict:
        afniGLMprep.eventTSV_to_1D( p.BIDS_path, inputfile['eventTSV_path'], p.TR )
else: pass

# Creat GLM script per input_dict keys
if 'prepGLM' in sys.argv:
    afniGLMprep.write_GLM_script_per_task_subj_run( BIDS_path = p.BIDS_path, 
                                                input_dict = p.input_dict,
                                                afniGLM_params = p )
else: pass

