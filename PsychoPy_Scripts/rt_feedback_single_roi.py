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

## Specify analysis_listener outputs folder ##
outPath = '/Users/julianawall/rt-cloud/outDir'

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.2.5'
expName = 'acc_feedback'  # from the Builder filename that created this script
expInfo = {
    'participant': '',
    'session': '001',
    'numRuns': 2,
    'run': '1',
    'starting_TR': 20,
    'end_TR': 300,
}
# --- Show participant info dialog --
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

starting_TR = expInfo['starting_TR']
numRuns = expInfo['numRuns']
end_TR = expInfo['end_TR']

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + \
    'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
                                 extraInfo=expInfo, runtimeInfo=None,
                                 originPath='',
                                 savePickle=True, saveWideText=True,
                                 dataFileName=filename)
# this outputs to the screen, not a file
logging.console.setLevel(logging.ERROR)

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation
# --- Setup the Window ---
win = visual.Window(
    size=(1920, 1080),
    #size=(1200, 800),  # MacBook size, for testing
    fullscr=False, allowGUI=False, screen=1,
    allowStencil=False,
    monitor='Dell', color=[0, 0, 0], colorSpace='rgb', pos=[0, 180],
    #pos=[50,0], #MacBook position, for testing,
    blendMode='avg', useFBO=True,
    units='height')
win.mouseVisible = False
aspect_ratio = 9/16  # aspect ratio of display computer (LCD monitor)

# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='event')

# --- Initialize components for Routine "instructions" ---
instr_text = visual.TextStim(win=win, name='instr_text',
                             text='ATTENTION PRACTICE\nIn this run you will see two circles.\nThe blue circle represents the brain process that corresponds to attention.\nTry to move the white dot into that circle and keep it there for 5 sec!\nIf you succeed, the circle will shrink and the dot will move back to the center.\nHow much can you shrink the circle?\nThis experiment will last 5 min.\nPress any button to start.',
                             font='Open Sans',
                             pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0,
                             color='white', colorSpace='rgb', opacity=None,
                             languageStyle='LTR',
                             depth=0.0)
instr_key_resp = keyboard.Keyboard()

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
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=0.0, interpolate=True)

# --- Initialize components for Routine "feedback" ---
# prepare the targets
colors = ['blue', 'yellow', 'red', 'green', 'cyan',
          'magenta', 'black', 'honeydew', 'indigo', 'maroon']
roi_names_list = ['acc']
roi_values = []

# target_positions:
baseline_pos = [0, 0]
roi_circle_size = 0.75
roi_circle_radius = roi_circle_size/2
roi_circle = visual.Circle(win, pos=(0, 0.70), radius=roi_circle_radius, fillColor=None,
                           lineColor=colors[0], units='norm', size=(roi_circle_size*aspect_ratio, roi_circle_size))
in_target_counter = 0

FeedbackCircle_X = 0
FeedbackCircle_Y = 0
FeedbackCircle_size = 0.35
FeedbackCircle_radius = FeedbackCircle_size/2
FeedbackCircle = visual.Circle(win,
                               radius=FeedbackCircle_radius,
                               fillColor='white',
                               lineColor='white',
                               lineWidth=3,
                               units='norm',
                               size=(FeedbackCircle_size*aspect_ratio, FeedbackCircle_size))


def in_circle(center_x, center_y, radius, x, y):
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2


# --- Initialize components for Routine "finish" ---
finish_text = visual.TextStim(win=win, name='finish_text',
                              text='Thank You!',
                              font='Open Sans',
                              pos=(0, 0), height=0.15, wrapWidth=None, ori=0.0,
                              color='white', colorSpace='rgb', opacity=None,
                              languageStyle='LTR',
                              depth=0.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
# to track time remaining of each (possibly non-slip) routine
routineTimer = core.Clock()

# --- Prepare to start Routine "instructions" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
instr_key_resp.keys = []
instr_key_resp.rt = []
_instr_key_resp_allKeys = []
# keep track of which components have finished
instructionsComponents = [instr_text, instr_key_resp]
for thisComponent in instructionsComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "instructions" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *instr_text* updates
    if instr_text.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
        # keep track of start time/frame for later
        instr_text.frameNStart = frameN  # exact frame index
        instr_text.tStart = t  # local t and not account for scr refresh
        instr_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(instr_text, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'instr_text.started')
        instr_text.setAutoDraw(True)

    # *instr_key_resp* updates
    waitOnFlip = False
    if instr_key_resp.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
        # keep track of start time/frame for later
        instr_key_resp.frameNStart = frameN  # exact frame index
        instr_key_resp.tStart = t  # local t and not account for scr refresh
        instr_key_resp.tStartRefresh = tThisFlipGlobal  # on global time
        # time at next scr refresh
        win.timeOnFlip(instr_key_resp, 'tStartRefresh')
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'instr_key_resp.started')
        instr_key_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(instr_key_resp.clock.reset)  # t=0 on next screen flip
        # clear events on next screen flip
        win.callOnFlip(instr_key_resp.clearEvents, eventType='keyboard')
    if instr_key_resp.status == STARTED and not waitOnFlip:
        theseKeys = instr_key_resp.getKeys(
            keyList=['a', 'b', 'c', 'd'], waitRelease=False)
        _instr_key_resp_allKeys.extend(theseKeys)
        if len(_instr_key_resp_allKeys):
            # just the last key pressed
            instr_key_resp.keys = _instr_key_resp_allKeys[-1].name
            instr_key_resp.rt = _instr_key_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False

    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "instructions" ---
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if instr_key_resp.keys in ['', [], None]:  # No response was made
    instr_key_resp.keys = None
thisExp.addData('instr_key_resp.keys', instr_key_resp.keys)
if instr_key_resp.keys != None:  # we had a response
    thisExp.addData('instr_key_resp.rt', instr_key_resp.rt)
thisExp.nextEntry()
# the Routine "instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

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
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'trigger_key_resp.started')
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
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'trigger_wait_text.started')
        trigger_wait_text.setAutoDraw(True)
    if trigger_wait_text.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > trigger_wait_text.tStartRefresh + trigger_key_resp.status == STARTED-frameTolerance:
            # keep track of stop time/frame for later
            trigger_wait_text.tStop = t  # not accounting for scr refresh
            trigger_wait_text.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'trigger_wait_text.stopped')
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
thisExp.addData('trigger_key_resp.keys', trigger_key_resp.keys)
if trigger_key_resp.keys != None:  # we had a response
    thisExp.addData('trigger_key_resp.rt', trigger_key_resp.rt)
thisExp.nextEntry()
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
timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "fixation" ---
while continueRoutine and routineTimer.getTime() < 10.0:
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
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'cross.started')
        cross.setAutoDraw(True)
    if cross.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > cross.tStartRefresh + 30-frameTolerance:
            # keep track of stop time/frame for later
            cross.tStop = t  # not accounting for scr refresh
            cross.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'cross.stopped')
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
else:
    routineTimer.addTime(-30.000000)

# --- Prepare to start Routine "feedback" ---
continueRoutine = True
routineForceEnded = False
# reset timers
t = 0
routineTimer.reset()
timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "feedback" ---
activity = 0
continueRoutine = True

print("ready to start feedback!")
for run in range(1, numRuns+1):
    for TR in range(starting_TR, end_TR+1):
        filename = f'{outPath}/run{run}_TR{TR}.json'
        # Wait for file to be synced
        while not os.path.exists(filename):
            keys_pressed = event.getKeys()
            if "escape" in keys_pressed:
                core.quit()  # allow escape key to quit experiment
            time.sleep(.1)  # retry every 100ms
        time.sleep(.1)  # buffer to prevent opening file before fully saved

        with open(filename, encoding="utf-8") as f:
            results = json.load(f)
        roi_value = np.round(float(results['values']), 2)

        cursor_position = np.dot(0, roi_value)
        
        print("TR", TR, "new x:", roi_value)
        # Set the new position of the stimulus
        FeedbackCircle.setPos([0, roi_value])

        if in_circle(roi_circle.pos[0], roi_circle.pos[1], roi_circle.radius, FeedbackCircle.pos[0], FeedbackCircle.pos[1]) == True:
            in_target_counter = in_target_counter+1
        else:
            in_target_counter = in_target_counter

        if in_target_counter == 5:
            roi_circle.radius = roi_circle_radius - (0.1*roi_circle_radius)
            #FeedbackCircle.radius = FeedbackCircle_radius - (0.1*FeedbackCircle_radius)
            FeedbackCircle.setPos([0, 0])
            FeedbackCircle.draw()
        elif in_target_counter == 10:
            roi_circle.radius = roi_circle_radius - (0.25*roi_circle_radius)
            #FeedbackCircle.radius = FeedbackCircle_radius - (0.25*FeedbackCircle_radius)
            FeedbackCircle.setPos([0, 0])
            FeedbackCircle.draw()
        elif in_target_counter == 20:
            roi_circle.radius = roi_circle_radius - (0.5*roi_circle_radius)
            #FeedbackCircle.radius = FeedbackCircle_radius - (0.5*FeedbackCircle_radius)
            FeedbackCircle.setPos([0, 0])
            FeedbackCircle.draw()
        else:
            FeedbackCircle.draw()
            
        print(roi_names_list, "TR:", TR, ";", "hits:", in_target_counter)

        # Draw the stimulus
        time.sleep(1)
        FeedbackCircle.draw()
        roi_circle.draw()
        win.flip()
        
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()

        # check if all components have finished
        continueRoutine = False  # will revert to True if at least one component still running

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()


# --- Ending Routine "feedback" ---
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    # else:
    #    routineTimer.addTime(-30.000000)

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
timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "fixation" ---
while continueRoutine and routineTimer.getTime() < 30:
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
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'cross.started')
        cross.setAutoDraw(True)
    if cross.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > cross.tStartRefresh + 30-frameTolerance:
            # keep track of stop time/frame for later
            cross.tStop = t  # not accounting for scr refresh
            cross.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'cross.stopped')
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
else:
    routineTimer.addTime(-30.000000)

# --- Prepare to start Routine "finish" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# keep track of which components have finished
finishComponents = [finish_text]
for thisComponent in finishComponents:
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

# --- Run Routine "finish" ---
while continueRoutine and routineTimer.getTime() < 5.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *finish_text* updates
    if finish_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        finish_text.frameNStart = frameN  # exact frame index
        finish_text.tStart = t  # local t and not account for scr refresh
        finish_text.tStartRefresh = tThisFlipGlobal  # on global time
        # time at next scr refresh
        win.timeOnFlip(finish_text, 'tStartRefresh')
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'finish_text.started')
        finish_text.setAutoDraw(True)
    if finish_text.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > finish_text.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            finish_text.tStop = t  # not accounting for scr refresh
            finish_text.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'finish_text.stopped')
            finish_text.setAutoDraw(False)

    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in finishComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "finish" ---
for thisComponent in finishComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-5.000000)

# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip()
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsPickle(filename)

win.close()
core.quit()
