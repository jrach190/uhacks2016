"""
Code originally from https://software.intel.com/en-us/iot/hardware/sensors/uln200xa-stepper-driver
Adapted by John Martincic and N Vijay Karthikeyan for UHacks2016
Code accesses a stepper motor on an arduino control board and turns it at a set rotation speed and
tells the motor the number of steps to turn
"""
import time, sys, signal, atexit
import pyupm_uln200xa as ctlr

# Instantiate a Stepper motor on a ULN200XA Darlington Motor Driver
# This was tested with the Grove Geared Step Motor with Driver

# Instantiate a ULN2003XA stepper object
ctlr_obj = ctlr.ULN200XA(4096, 8, 9, 10, 11)

## Exit handlers ##
# This stops python from printing a stacktrace when you hit control-C
def SIGINTHandler(signum, frame):
    raise SystemExit

# This lets you run code on exit,
# including functions from ctlr_obj
def exitHandler():
    print "Exiting"
    sys.exit(0)

# Register exit handlers
atexit.register(exitHandler)
signal.signal(signal.SIGINT, SIGINTHandler)


ctlr_obj.setSpeed(5) # 5 RPMs
ctlr_obj.setDirection(ctlr.ULN200XA.DIR_CW)

#assumes 5:1 gear ratio
print "Opening Door"
ctlr_obj.stepperSteps(8192)

print "Door is now open"

# release
ctlr_obj.release()

# exitHandler is called automatically
