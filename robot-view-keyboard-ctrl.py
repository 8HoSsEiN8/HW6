#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
# /*
# Copyright (c) 2014, Daniel M. Lofaro <dan (at) danLofaro (dot) com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# */
import diff_drive
import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np

import actuator_sim as ser
#-----------------------------------------------------
#--------[ Do not edit above ]------------------------
#-----------------------------------------------------

# Add imports here
import controller_include as ci
import timeit
from myFunctions import setVelocity
from myFunctions import setAngleLimit

import curses
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)
stdscr.nodelay(1)

stdscr.addstr(0,2,"Hit 'q' to quit")
stdscr.addstr(1,5,"The controller program must be running!")
stdscr.refresh()

def sWait(seconds, tic):
	#[status, framesize] = t.get(tim, wait=False, last=True)
	
	#print "TIC: ", tic
	while(1):	
		[status, framesize] = t.get(tim, wait=False, last=True)
		toc = tim.sim[0]
		if ((toc - tic) > seconds):
			break	
	#print "TOC: ", toc, "\t(", (toc - tic), " seconds )"
	
s = 0
d0 = 1
d1 = 1

F = 20.0
delT = 1.0 / F

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
c = ach.Channel(ci.CONTROLLER_REF_NAME)
controller = ci.CONTROLLER_REF()

#-----------------------------------------------------
#--------[ Do not edit below ]------------------------
#-----------------------------------------------------
dd = diff_drive
ref = dd.H_REF()
tim = dd.H_TIME()

ROBOT_DIFF_DRIVE_CHAN   = 'robot-diff-drive'
ROBOT_CHAN_VIEW   = 'robot-vid-chan'
ROBOT_TIME_CHAN  = 'robot-time'
# CV setup 
r = ach.Channel(ROBOT_DIFF_DRIVE_CHAN)
r.flush()
t = ach.Channel(ROBOT_TIME_CHAN)
t.flush()

i=0


#print '======================================'
#print '============= Robot-View ============='
#print '========== Daniel M. Lofaro =========='
#print '========= dan@danLofaro.com =========='
#print '======================================'
ref.ref[0] = 0
ref.ref[1] = 0
while True:
    [status, framesize] = t.get(tim, wait=False, last=True)
    if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
        pass
        #print 'Sim Time = ', tim.sim[0]
    else:
        raise ach.AchException( v.result_string(status) )

#-----------------------------------------------------
#--------[ Do not edit above ]------------------------
#-----------------------------------------------------
    # Main Loop
    # Def:
    # tim.sim[0] = Sim Time
    
    [status, framesize] = t.get(tim, wait=False, last=True)
    tic = tim.sim[0]
    
    [statuss, framesizes] = c.get(controller, wait=False, last=True)
    
    if (i == 0):
		i = i + 1
		#[status, framesize] = t.get(tim, wait=False, last=True)
		start_time_s = tic
		start_time_r = timeit.default_timer()
		
    
    key = stdscr.getch()
    
    if (controller.direction == ci.FORWARD): 
        stdscr.addstr(3, 10, ">> Forward")
        s = s + 10
        if (s > 114):
			s = 114
        buff = setVelocity(0, 1, s)
        ref = ser.serial_sim(r,ref,buff)
        buff = setVelocity(1, 1, s)
        ref = ser.serial_sim(r,ref,buff)
        d0 = 1
        d1 = 1
        		
    elif (controller.direction == ci.REVERSE): 
        stdscr.addstr(4, 10, ">> Reverse")
        s = s + 2
        if (s > 114):
			s = 114
        buff = setVelocity(0, 0, s)
        ref = ser.serial_sim(r,ref,buff)
        buff = setVelocity(1, 0, s)
        ref = ser.serial_sim(r,ref,buff)
        d0 = 0
        d1 = 0
        
    elif (controller.direction == ci.RIGHT): 
        stdscr.addstr(5, 10, ">> Right")
        s = s + 10
        if (s > 114):
			s = 114
        buff = setVelocity(0, 0, s)
        ref = ser.serial_sim(r,ref,buff)
        buff = setVelocity(1, 1, s)
        ref = ser.serial_sim(r,ref,buff)
        d0 = 0
        d1 = 1
        
    elif (controller.direction == ci.LEFT): 
        stdscr.addstr(6, 10, ">> Left")
        s = s + 10
        if (s > 114):
			s = 114
        buff = setVelocity(0, 1, s)
        ref = ser.serial_sim(r,ref,buff)
        buff = setVelocity(1, 0, s)
        ref = ser.serial_sim(r,ref,buff)
        d0 = 1
        d1 = 0
        
    elif key == ord('q'): 
        curses.endwin()
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()
        sys.exit("Done!")
        
    elif True:
		s = s - 2
		if (s < 0):
			s = 0
		buff = setVelocity(0, d0, s)
		ref = ser.serial_sim(r,ref,buff)
		buff = setVelocity(1, d1, s)
		ref = ser.serial_sim(r,ref,buff)
		stdscr.addstr(3, 10, "   Forward")
		stdscr.addstr(4, 10, "   Reverse")
		stdscr.addstr(5, 10, "   Right")
		stdscr.addstr(6, 10, "   Left")
        
    
    
    sWait(delT, tic)    
    time_r = timeit.default_timer() - start_time_r
    [status, framesize] = t.get(tim, wait=False, last=True)
    time_s = tim.sim[0] - start_time_s    
    stdscr.addstr(8,2,"R-time: " + str(time_r) + "\tS-time: " + str(time_s) + "\tSpeed: " + str(s) + "\t")
    stdscr.refresh() 
#-----------------------------------------------------
#--------[ Do not edit below ]------------------------
#-----------------------------------------------------
