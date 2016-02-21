"""
Code originally from https://software.intel.com/en-us/iot/hardware/sensors/uln200xa-stepper-drive
Adapted by John Martincic and N Vijay Karthikeyan for UHacks2016
Code accesses a stepper motor on an arduino control board and turns it at a set rotation speed and
tells the motor the number of steps to turn
"""
import socket
import time, sys, signal, atexit
import pyupm_uln200xa as ctlr

#UDP_IP = "192.168.0.3"
#UDP_PORT = 5005
#i=True
ctlr_obj = ctlr.ULN200XA(4096, 8, 9, 10, 11) #Instantiate Stepper Motor


#sock = socket.socket(socket.AF_INET, # Internet
#                     socket.SOCK_DGRAM) # UDP
#sock.bind((UDP_IP, UDP_PORT))

#while i:
#    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
#   if len(data):
#       i=False
#   print "Access Granted"

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
