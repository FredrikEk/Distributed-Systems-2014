# -*- coding: utf-8 -*-
### Automatically generated by repyhelper.py ### C:\Users\Fredrik\Documents\Distributed systems\demokit\time.repy

### THIS FILE WILL BE OVERWRITTEN!
### DO NOT MAKE CHANGES HERE, INSTEAD EDIT THE ORIGINAL SOURCE FILE
###
### If changes to the src aren't propagating here, try manually deleting this file. 
### Deleting this file forces regeneration of a repy translation


from repyportability import *
import repyhelper
mycontext = repyhelper.get_shared_context()
callfunc = 'import'
callargs = []

"""
<Program Name>
  time.repy

<Author>
  Eric Kimbrel

<Started>
  Jul 2, 2009

<Purpose>
 replaces the previous time.repy by use of the active interface 
 time_interface.repy and the implementors ntp_time.repy and tcp_time.repy

 see time_interface.repy for details

"""


repyhelper.translate_and_import('ntp_time.repy')
repyhelper.translate_and_import('tcp_time.repy')


### Automatically generated by repyhelper.py ### C:\Users\Fredrik\Documents\Distributed systems\demokit\time.repy
