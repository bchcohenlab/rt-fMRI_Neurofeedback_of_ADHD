This directory contains the scripts used by the rt-Cloud platform. 

'adhd_rt.py' is the main neurofeedback calculation script. A neurofeedback score is calculated at each TR using an incremental GLM. The score is equal to the residual between the actual and predicted values. (This code is adapted from https://nilearn.github.io/stable/auto_examples/04_glm_first_level/plot_predictions_residuals.html). After the raw score is calculated, it is standardized. Finally, each score is sent to the stimulus presentation laptop as a json file. 

