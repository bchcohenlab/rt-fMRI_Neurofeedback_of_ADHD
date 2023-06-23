Contains scripts and masks needed by the DATA_ANALYSER computer for the ACC neurofeedback task.

'msit_preproc_script.py' is used to calculate the subject-space ACC mask for each participant. It takes an MNI-space ACC mask as input, then performs a GLM on this region, comparing the level of activation during interference trials and control trials (see https://github.com/ccraddock/msit for more information on the task). 

'initialize.py' copies template folders and MNI masks to the current subject's directory in preparation for the neurofeedback session. 

'adhd_rt.py' is the main neurofeedback calculation script. A neurofeedback score is calculated at each TR using an incremental GLM. This score is equal to the residual between the actual and predicted values.(This code is adapted from https://nilearn.github.io/stable/auto_examples/04_glm_first_level/plot_predictions_residuals.html). After the raw score is calculated, it is standardized. Finally, each score is sent to the stimulus presentation laptop as a json file.

'finalize.py' is run at the end of a neurofeedback session and can be used to transfer files to their proper location, delete temporary files, etc. Currently, this script is identical to the template provided by the rt-Cloud platform, but it can be edited as necessary for the purposes of this study.
