#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.5),
    on Wed Feb 22 16:09:04 2023
If you publish work using this script the most relevant publication is:

   Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019)
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
import os
import time
import json
import numpy as np
from psychopy import gui, visual, core, data, event, logging, colors
from psychopy.constants import (NOT_STARTED, STARTED, FINISHED)
from psychopy.hardware import keyboard

# Store info about the experiment session
psychopyVersion = '2022.2.5'

# this outputs to the screen, not a file
logging.console.setLevel(logging.ERROR)

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame
# Start Code - component code to be run after the window creation
# --- Setup the Window ---
win = visual.Window(
    size=(1920, 1080),
    fullscr=False, allowGUI=False, screen=1,
    allowStencil=False,
    monitor='Dell', color=[0, 0, 0], colorSpace='rgb', pos=[0, 180],
    blendMode='avg', useFBO=True,
    units='height')
win.mouseVisible = False
aspect_ratio = 9/16  # aspect ratio of display computer (LCD monitor)

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='event')

# --- Initialize components for Routine "trigger" ---
trigger_key_resp = keyboard.Keyboard()
trigger_wait_text = visual.TextStim(win=win, name='trigger_wait_text',
                                    text='Waiting for scanner...',
                                    font='Open Sans',
                                    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0,
                                    color='white', colorSpace='rgb', opacity=None,
                                    languageStyle='LTR',
                                    depth=-1.0)

# --- Initialize components for Routine "fixation" ---
cross = visual.ShapeStim(
    win=win, name='cross', vertices='cross',
    size=(0.05, 0.05),
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=1.0, colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=0.0, interpolate=True)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
# to track time remaining of each (possibly non-slip) routine
routineTimer = core.Clock()
 
# --- Prepare to start Routine "trigger" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
trigger_key_resp.keys = []
trigger_key_resp.rt = []
_trigger_key_resp_allKeys = []
# keep track of which components have finished
triggerComponents = [trigger_key_resp, trigger_wait_text]
for thisComponent in triggerComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "trigger" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *trigger_key_resp* updates
    waitOnFlip = False
    if trigger_key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        trigger_key_resp.frameNStart = frameN  # exact frame index
        trigger_key_resp.tStart = t  # local t and not account for scr refresh
        trigger_key_resp.tStartRefresh = tThisFlipGlobal  # on global time
        # time at next scr refresh
        win.timeOnFlip(trigger_key_resp, 'tStartRefresh')
        trigger_key_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(trigger_key_resp.clock.reset)  # t=0 on next screen flip
        # clear events on next screen flip
        win.callOnFlip(trigger_key_resp.clearEvents, eventType='keyboard')
    if trigger_key_resp.status == STARTED and not waitOnFlip:
        theseKeys = trigger_key_resp.getKeys(
            keyList=['num_add', 't', '+', '5', 's'], waitRelease=False)
        _trigger_key_resp_allKeys.extend(theseKeys)
        if len(_trigger_key_resp_allKeys):
            # just the last key pressed
            trigger_key_resp.keys = _trigger_key_resp_allKeys[-1].name
            trigger_key_resp.rt = _trigger_key_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False

    # *trigger_wait_text* updates
    if trigger_wait_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        trigger_wait_text.frameNStart = frameN  # exact frame index
        trigger_wait_text.tStart = t  # local t and not account for scr refresh
        trigger_wait_text.tStartRefresh = tThisFlipGlobal  # on global time
        # time at next scr refresh
        win.timeOnFlip(trigger_wait_text, 'tStartRefresh')
        trigger_wait_text.setAutoDraw(True)
    if trigger_wait_text.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > trigger_wait_text.tStartRefresh + trigger_key_resp.status == STARTED-frameTolerance:
            # keep track of stop time/frame for later
            trigger_wait_text.tStop = t  # not accounting for scr refresh
            trigger_wait_text.frameNStop = frameN  # exact frame index
            trigger_wait_text.setAutoDraw(False)

    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in triggerComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "trigger" ---
for thisComponent in triggerComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if trigger_key_resp.keys in ['', [], None]:  # No response was made
    trigger_key_resp.keys = None
# the Routine "trigger" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "fixation" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# keep track of which components have finished
fixationComponents = [cross]
for thisComponent in fixationComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "fixation" ---
while continueRoutine and routineTimer.getTime() < 120:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *cross* updates
    if cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        cross.frameNStart = frameN  # exact frame index
        cross.tStart = t  # local t and not account for scr refresh
        cross.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(cross, 'tStartRefresh')  # time at next scr refresh
        cross.setAutoDraw(True)
    if cross.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > cross.tStartRefresh + 30-frameTolerance:
            # keep track of stop time/frame for later
            cross.tStop = t  # not accounting for scr refresh
            cross.frameNStop = frameN  # exact frame index
            cross.setAutoDraw(False)

    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in fixationComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "fixation" ---
for thisComponent in fixationComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()

# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip()
# and win.timeOnFlip() tasks get executed before quitting
win.flip()


win.close()
core.quit()
