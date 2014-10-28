#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
# /*
# Copyright (c) 2014, Daniel M. Lofaro
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



import controller_include as ci
import ach
import sys
import time
import numpy as np
from ctypes import *

import curses
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)
stdscr.nodelay(1)

stdscr.addstr(0,2,"Hit 'q' to quit")
stdscr.addstr(1,5,"Use 'Arrow keys' to move the robot!")
stdscr.refresh()

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
c = ach.Channel(ci.CONTROLLER_REF_NAME)
controller = ci.CONTROLLER_REF()

controller.direction = ci.STOP
c.put(controller)


key = ''
while key != ord('q'):
	key = stdscr.getch()

	time.sleep(0.05)
	
	if (key == curses.KEY_UP) | (key == ord('w')):
		stdscr.addstr(3, 10, ">> Forward")
		controller.direction = ci.FORWARD
		
	elif (key == curses.KEY_DOWN) | (key == ord('s')):
		stdscr.addstr(4, 10, ">> Reverse")
		controller.direction = ci.REVERSE
		
	elif (key == curses.KEY_RIGHT) | (key == ord('d')): 
		stdscr.addstr(5, 10, ">> Right")
		controller.direction = ci.RIGHT
	
	elif (key == curses.KEY_LEFT) | (key == ord('a')):
		stdscr.addstr(6, 10, ">> Left")
		controller.direction = ci.LEFT		
		
	elif True:	
		controller.direction = ci.STOP
		stdscr.addstr(3, 10, "   Forward")
		stdscr.addstr(4, 10, "   Reverse")
		stdscr.addstr(5, 10, "   Right")
		stdscr.addstr(6, 10, "   Left")
		
	
	c.put(controller)
	stdscr.refresh()

# Close the connection to the channels

#r.close()
#s.close()


curses.endwin()
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
sys.exit("Done!")
