#version 12/6/17
"""
afniGLMprep is python code which prepares and runs GLMs on neuroimaging data stored in the BIDS format (http://bids.neuroimaging.io/). This is done via AFNI's 3dDeconvolve function.

Git it at:
https://github.com/rystoli/afniGLMprep
"""


__version__ = "0.0.1"

import sys
sys.dont_write_bytecode = True
if sys.version_info[0] == 2 and sys.version_info[1] < 6:
    raise ImportError("Python Version 2.6 or above is required for rymvpa.")
else:
    pass

del sys

# import
import afniGLMprep_functions as apf
import afniGLMprep_params as p
