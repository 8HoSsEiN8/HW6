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

dd = diff_drive
ref = dd.H_REF()
tim = dd.H_TIME()

ROBOT_DIFF_DRIVE_CHAN   = 'robot-diff-drive'
ROBOT_CHAN_VIEW_R   = 'robot-vid-chan-r'
ROBOT_CHAN_VIEW_L   = 'robot-vid-chan-l'
ROBOT_TIME_CHAN  = 'robot-time'
# CV setup 
cv.NamedWindow("wctrl_L", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("wctrl_R", cv.CV_WINDOW_AUTOSIZE)
#capture = cv.CaptureFromCAM(0)
#capture = cv2.VideoCapture(0)

# added
##sock.connect((MCAST_GRP, MCAST_PORT))
newx = 320
newy = 240

nx = 320
ny = 240

r = ach.Channel(ROBOT_DIFF_DRIVE_CHAN)
r.flush()
vl = ach.Channel(ROBOT_CHAN_VIEW_L)
vl.flush()
vr = ach.Channel(ROBOT_CHAN_VIEW_R)
vr.flush()
t = ach.Channel(ROBOT_TIME_CHAN)
t.flush()

i=0


print '======================================'
print '============= Robot-View ============='
print '========== Daniel M. Lofaro =========='
print '========= dan@danLofaro.com =========='
print '======================================'
while True:
    # Get Frame
    imgL = np.zeros((newx,newy,3), np.uint8)
    imgR = np.zeros((newx,newy,3), np.uint8)
    c_image = imgL.copy()
    c_image = imgR.copy()
    vidL = cv2.resize(c_image,(newx,newy))
    vidR = cv2.resize(c_image,(newx,newy))
    [status, framesize] = vl.get(vidL, wait=False, last=True)
    if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
        vid2 = cv2.resize(vidL,(nx,ny))
        imgL = cv2.cvtColor(vid2,cv2.COLOR_BGR2RGB)
        cv2.imshow("wctrl_L", imgL)
        cv2.waitKey(10)
    else:
        raise ach.AchException( v.result_string(status) )
    [status, framesize] = vr.get(vidR, wait=False, last=True)
    if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
        vid2 = cv2.resize(vidR,(nx,ny))
        imgR = cv2.cvtColor(vid2,cv2.COLOR_BGR2RGB)
        cv2.imshow("wctrl_R", imgR)
        cv2.waitKey(10)
    else:
        raise ach.AchException( v.result_string(status) )


    [status, framesize] = t.get(tim, wait=False, last=True)
    if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
        pass
        #print 'Sim Time = ', tim.sim[0]
    else:
        raise ach.AchException( v.result_string(status) )

#-----------------------------------------------------
#-----------------------------------------------------
#-----------------------------------------------------
    # Def:
    # ref.ref[0] = Right Wheel Velos
    # ref.ref[1] = Left Wheel Velos
    # tim.sim[0] = Sim Time
    # imgL       = cv image in BGR format (Left Camera)
    # imgR       = cv image in BGR format (Right Camera)
    
    xL = yL = xR = yR = -1
    # Define upper and lower range of green color in HSV
    lower_green = np.array([50,0,0], dtype=np.uint8)
    upper_green = np.array([70,255,255], dtype=np.uint8)
    
    
    # ##### Right Image:    
    # Convert RGB to HSV
    hsvR = cv2.cvtColor(imgR, cv2.COLOR_RGB2HSV)

    # Threshold the HSV image to get only green colors
    maskR = cv2.inRange(hsvR, lower_green, upper_green)
    
    # Use findContours to get the boundry of the green blob
    contours,hierarchy = cv2.findContours(maskR,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # Look through all the seperate contours and highlight the boundry and centroid
    for cnt in contours:
		# Calculate moments
        moments = cv2.moments(cnt)                
        if moments['m00']!=0:
            xR = int(moments['m10']/moments['m00'])
            yR = int(moments['m01']/moments['m00'])
            print 'Center of Mass (Right) = ', '(', xR, ', ', yR, ')'
            
            # draw contours 
            cv2.drawContours(imgR,[cnt],0,(0,0,255),1)   
            # draw centroids in red
            cv2.circle(imgR,(xR,yR),5,(0,0,255),-1)      

    
    
    # ##### Left Image:    
    # Convert RGB to HSV
    hsvL = cv2.cvtColor(imgL, cv2.COLOR_RGB2HSV)

    # Threshold the HSV image to get only green colors
    maskL = cv2.inRange(hsvL, lower_green, upper_green)
    
    # Use findContours to get the boundry of the green blob
    contours,hierarchy = cv2.findContours(maskL,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # Look through all the seperate contours and highlight the boundry and centroid
    for cnt in contours:
		# Calculate moments
        moments = cv2.moments(cnt)                
        if moments['m00']!=0:
            xL = int(moments['m10']/moments['m00'])
            yL = int(moments['m01']/moments['m00'])
            print 'Center of Mass (Left) = ', '(', xL, ', ', yL, ')'
            
            # draw contours 
            cv2.drawContours(imgL,[cnt],0,(0,0,255),1)   
            # draw centroids in red
            cv2.circle(imgL,(xL,yL),5,(0,0,255),-1)      

    
    
    
    
    LR_combo = np.zeros((newy, (2*newx)+5 ,3), np.uint8)
    LR_combo[:newy, :newx, :3] = imgL   
    LR_combo[:newy, (newx+5):(2*newx)+5, :3] = imgR
    
    # ###### Depth Calculation:
    f = 85.0e-3 		# Focal length
    b = 0.4				# Baseline
    p = 280.0e-6		# Pixel size
    
    d = abs(xR - xL)	# Disparity
    
    if( (xR > 0) & (xL > 0) ):	# Stereo vision available
		Depth = (f * b) / (d * p)
		print 'Distance is ', Depth, ' m'
		depth = '%.4f m' % Depth
		cv2.putText(LR_combo, depth, (10, 230), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255),2)	
    else:
		print 'No Stereo Vision!'
		cv2.putText(LR_combo, 'No Stereo Vision!', (10, 230), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255),2)
		
    cv2.imshow('Left | Right    -     Stereo Vision', LR_combo)
    cv2.waitKey(10)

    # Sleeps
    time.sleep(0.1)   
#-----------------------------------------------------
#-----------------------------------------------------
#-----------------------------------------------------
