# -*- coding: utf-8 -*-
### Automatically generated by repyhelper.py ### C:\Users\Fredrik\Documents\Distributed systems\Lab\udpcentralizedadvertise.repy

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
Author: Justin Cappos

Start Date: Oct 30, 2011

Description:
Advertisements to a central server (similar to openDHT)

This uses UDP and is conceptually quite similar to the centralized advertise
service
"""

repyhelper.translate_and_import('serialize.repy')
repyhelper.translate_and_import('uniqueid.repy')


# Hmm, perhaps I should make an initialization call instead of hardcoding this?
# I suppose it doesn't matter since one can always override these values
udpservername = "udpadvertiseserver.poly.edu"
udpserverport = 10102

# how long to wait for timeouts...
udpcentralizedservertimeouts = [1,2,4,8]

# If a query times out or if we decide to abandon it, put the ID here. That way, 
# the communicate function can reject it if the server responds belatedly.
failed_querylist = []

# Need this for receiving over UDP. The Repy v1 API forces us to use 
# a callback, which requires this roundabout solution.
mycontext['advertise_response'] = []

mycontext['udprequestport'] = 0

class UDPCentralAdvertiseError(Exception):
  """Error when advertising a value to the central advertise service."""

class UDPNoResponseError(Exception):
  """Error when advertising a value to the central advertise service."""




def _getusableport():
  """
  <Purpose>
    Discover which port the server can use for announcements.

  <Arguments>
    None

  <Exceptions>
    None

  <Side Effects>
    None

  <Returns>
    An integer port
  """
  port_found = False
  port_min = 63000
  port_max = 63150
  port_iter = port_min
  local_addr = getmyip()

  while not port_found:
    if port_iter > port_max:
      raise Exception("Network restriction error! Unable to find a free port!")
    try:
      udp_test_socket = recvmess(local_addr, port_iter, _dummy_function)
      stopcomm(udp_test_socket)
      port_found = True
    except Exception, e:
      port_iter += 1

  return port_iter




# This helper function handles communications with the server
def _udpcentralizedadvertise_communicate(datastringtosend, timeout, queryid):
  if mycontext['udprequestport'] == 0:
    mycontext['udprequestport'] = _getusableport()

  udprequestport = mycontext['udprequestport']

  if udprequestport is None:
    udprequestport = _getusableport()
    mycontext['udprequestport'] = udprequestport

  starttime = getruntime()

  # Let's get ready to receive a response...
  # NOTE: This is a roundabout solution to deal with the fact that the 
  #       V1 API requires use of callbacks when using UDP.
  udpresponsesocket = recvmess(getmyip(), udprequestport, _listenformessage)

  # but always close the response socket...
  try:
    # send the request over UDP...
    sendmess(udpservername, udpserverport, datastringtosend, getmyip(), udprequestport)

    while getruntime() < starttime + timeout:

      for entry in mycontext['advertise_response']:
        if entry[len(entry) - 1] == queryid:
          return_value = mycontext['advertise_response'].pop(mycontext['advertise_response'].index(entry))
          return return_value

      # Since there's nothing here for us, why not do some spring cleaning?
      for entry in mycontext['advertise_response']:
        if queryid - entry[len(entry) - 1] > 100:
          mycontext['advertise_response'].pop(mycontext['advertise_response'].index(entry))

      # Already done? Let's play nice with the other threads.
      sleep(0.01) # Strongly recommend NOT to set this any higher.
      
    raise UDPNoResponseError("Did not receive a response from UDP advertise server")

  finally:
    # always close the response socket...
    stopcomm(udpresponsesocket)




# This is our roundabout solution for a UDP callback.
# Could crash. Probably should if something bad happens.
def _listenformessage(remoteIP, remoteport, message, commhandle):
  mycontext['advertise_response'].append(serialize_deserializedata(message))

  stopcomm(commhandle)
  return




# A dummy function for getusableport.
def _dummy_function(remoteIP, remoteport, message, commhandle):
  return




def udpcentralizedadvertise_announce(key, value, ttlval):
  """
   <Purpose>
     Announce a key / value pair into the CHT.

   <Arguments>
     key: the key to put the value under. This will be converted to a string.

     value: the value to store at the key. This is also converted to a string.

     ttlval: the amount of time until the value expires.   Must be an integer

   <Exceptions>
     TypeError if ttlval is of the wrong type.

     ValueError if ttlval is not positive 

     UDPCentralAdvertiseError is raised the server response is corrupted

     Various network and timeout exceptions are raised by udp messages

   <Side Effects>
     The CHT will store the key / value pair.

   <Returns>
     None
  """
  # do basic argument checking / munging
  key = str(key)
  value = str(value)

  if not type(ttlval) is int and not type(ttlval) is long:
    raise TypeError("Invalid type '"+str(type(ttlval))+"' for ttlval.")

  if ttlval < 1:
    raise ValueError("The argument ttlval must be positive, not '"+str(ttlval)+"'")

  # myrequestport = getusableport()

  unique_request_id = uniqueid_getid()

  # We'll loop through and send a request, increasing the timeout upon failure
  for thistimeout in udpcentralizedservertimeouts:

    # build the tuple to send, then convert to a string because only strings
    # (bytes) can be transmitted over the network...
    datatosend = ('PUT',key,value,ttlval, unique_request_id)
    datastringtosend = serialize_serializedata(datatosend)
  
    rawresponse = None

    try:
    # send the request over UDP...
      rawresponse = _udpcentralizedadvertise_communicate(datastringtosend, thistimeout, unique_request_id)

    except UDPNoResponseError:
      # let's increase the timeout...
      continue
    
    if not rawresponse == None:
      # We should check that the response is 'OK'
      try:
        response = rawresponse
      except ValueError, e:
        raise UDPCentralAdvertiseError("Received unknown response from server '"+rawresponse+"'")

      if type(response) is not tuple or len(response) != 2:
        raise UDPCentralAdvertiseError("UDP Centralized announce received invalid response type '"+str(response)+"'")
      if type(response[0]) is not str:
        raise UDPCentralAdvertiseError("UDP Centralized announce received response with invalid first parameter '"+str(response)+"'")
  
      if response[1] != unique_request_id:
        raise UDPCentralAdvertiseError("UDP Centralized announce received different request id '"+str(response)+"'")

      if response[0] != 'OK':
        raise UDPCentralAdvertiseError("UDP Centralized announce failed with '"+response[0]+"'")

      else:
        # else all is well!   Let's return success
        return
      
  failed_querylist.append(unique_request_id)

  # fell through all of the timeout values...
  raise UDPCentralAdvertiseError("UDP Centralized announce timed out!")



def udpcentralizedadvertise_lookup(key, maxvals=100):
  """
   <Purpose>
     Returns a list of valid values stored under a key

   <Arguments>
     key: the key to put the value under. This will be converted to a string.

     maxvals: the maximum number of values to return.   Must be an integer

   <Exceptions>
     TypeError if maxvals is of the wrong type.

     ValueError if maxvals is not a positive number

     UDPCentralAdvertiseError is raised the server response is corrupted

     Various network and timeout exceptions are raised by timeout_openconn
     and session_sendmessage / session_recvmessage

   <Side Effects>
     None

   <Returns>
     The list of values
  """

  # do basic argument checking / munging
  key = str(key)

  if not type(maxvals) is int and not type(maxvals) is long:
    raise TypeError("Invalid type '"+str(type(maxvals))+"' for ttlval.")

  if maxvals < 1:
    raise ValueError("The argument ttlval must be positive, not '"+str(ttlval)+"'")


  # We'll loop through and send a request, increasing the timeout upon failure
  for thistimeout in udpcentralizedservertimeouts:

    # get a unique request id
    unique_request_id = uniqueid_getid()
  
    # build the tuple to send, then convert to a string because only strings
    # (bytes) can be transmitted over the network...
    messagetosend = ('GET',key,maxvals,unique_request_id)
    messagestringtosend = serialize_serializedata(messagetosend)

  
    try:
    # send the request over UDP...
      responsetuple = _udpcentralizedadvertise_communicate(messagestringtosend, thistimeout, unique_request_id)

    except UDPNoResponseError:
      # let's increase the timeout...
      continue
  

    # try:
    #   responsetuple = serialize_deserializedata(rawreceiveddata[2])
    # except ValueError, e:
    #   raise UDPCentralAdvertiseError("Received unknown response from server '"+rawresponse+"'")

    # For a set of values, 'a','b','c',  I should see the response: 
    # ('OK', ['a','b','c'])    Anything else is WRONG!!!
  
    if not type(responsetuple) is tuple:
      raise UDPCentralAdvertiseError("Received data is not a tuple '"+str(responsetuple)+"'")


    if len(responsetuple) != 3:
      raise UDPCentralAdvertiseError("Response tuple did not have exactly three elements '"+str(responsetuple)+"'")

    if responsetuple[2] != unique_request_id:
      raise UDPCentralAdvertiseError("UDP Centralized announce received different request id '"+str(responsetuple)+"'")

    if responsetuple[0] != 'OK':
      raise UDPCentralAdvertiseError("Central server returns error '"+str(responsetuple[:-1])+"'")


  
    if not type(responsetuple[1]) is list:
      raise UDPCentralAdvertiseError("Received item is not a list '"+responsetuple+"'")

    for responseitem in responsetuple[1]:
      if not type(responseitem) is str:
        raise UDPCentralAdvertiseError("Received item '"+str(responseitem)+"' is not a string in '"+responsetuple+"'")

    # okay, we *finally* seem to have what we expect...

    return responsetuple[1]
      

### Automatically generated by repyhelper.py ### C:\Users\Fredrik\Documents\Distributed systems\Lab\udpcentralizedadvertise.repy
