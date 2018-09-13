#
# -*- coding: UTF-8 -*-
#
################################################################################################
#
# NAME: IrisEMC_Paraview-Utils.py - library of various functions in support of EMC
#
#       http://ds.iris.edu/ds/products/emc-earthmodels/
#
# Copyright (C) 2018  Product Team, IRIS Data Management Center
#
#    This is a free software; you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation; either version 3 of the
#    License, or (at your option) any later version.
#
#    This script is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License (GNU-LGPL) for more details.  The
#    GNU-LGPL and further information can be found here:
#    http://www.gnu.org/
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# History:
#    2018-09-13 Manoch: R.0.2018.256 updated the isValueIn to ensure values are float
#    2018-03-21 Manoch: R.0.2018.080 release for ParaView support
#    2015-06-08 Manoch: updated the parameter file message based on the changes
#               in the main script
#    2015-01-17 Manoch: created
#

import os
from   time import time

################################################################################################
#
# check path
#
################################################################################################
#
def checkPath(path):
   "check path to see if it exists"
   if os.path.exists(path):
    return path
   else:
    return None

################################################################################################
#
# isValueIn
#
################################################################################################
#
def isValueIn(value,valueMin,valueMax):
   "check a value to see if it is within limits"
   if float(value) < float(valueMin) or float(value) > float(valueMax):
       return False
   else:
      return True

################################################################################################
#
# isPointIn
#
################################################################################################
#
def isLongitudeIn(longitude,lonMin,lonMax):
   "check a longitude to see if it is within the box"

   #
   # validate based on min and max if regular
   #
   if lonMin < lonMax:
       if longitude >= lonMin and longitude <= lonMax:
           return True
       else:
          return False
   #
   # move to 0-360 to avoid zero crossing and 180 crossing issues
   #
   if lonMin <= 0:
       lonMin += 360
   if lonMax <= 0:
        lonMax +=360
   if longitude <= 0:
        longitude += 360

   if longitude < lonMin and longitude > lonMax:
           return False
   return True

################################################################################################
#
# get longitudes
#
################################################################################################
#
def getLons(lonStart,lonEnd,inc):
   "create a list of longitudes from start to end"

   #
   # move to 0-360 to avoid zero crossing and 180 crossing issues
   #
   lon = lonStart - inc
   lonList = []
   if lonStart < lonEnd:
      while lon <= lonEnd-inc:
         lon += inc
         lonList.append(float(lon ))
   else:
      while lon <= 180-inc:
        lon += inc
        lonList.append(float(lon ))
      lon = -180.0
      while lon <= lonEnd-inc:
        lon += inc
        lonList.append(float(lon ))
   return lonList

################################################################################################
#
# makePath
#
################################################################################################
#
def makePath(directory):
    "Checks a directory for existance and if it does not exist, "
    "create it. If needed, create all parent directories."

    #
    # the path must be an absolute path (start with "/")
    #
    if not os.path.isabs(directory):
        print ('ERR [checkMakePath]: pat must be an absolute path')
        return None

    #
    # create directories
    #
    thisPath = os.path.abspath(directory)
    if checkPath(thisPath) is None:
            os.makedirs(thisPath)
    return thisPath

################################################################################################
#
# error message
#
################################################################################################
#
def error(message,code=1,sender=None):
  "write an error message out in block format and return an exit code"
  line = "\n"+100*"*"+"\n"
  if sender:
    lab = "[ERROR from " + sender + "]"
  else:
    lab = "[ERROR]"
  print (line,lab,message,line)
  return(code)

################################################################################################
#
# check latitude
#
################################################################################################
#
def isLatValid(value,sender=None):
  "validate latitude value (must be between +/-90 degrees"
  "returns True if the latitude value is valid"
  if abs(float(value)) > 90.0:
    if sender:
      error(sender+": Bad latitude ("+str(value)+"), must be between +/-90.0",1)
    else:
      error("Bad latitude ("+str(value)+"), must be between +/-90.0",1)
    return False
  else:
      return True

################################################################################################
#
# check longitude
#
################################################################################################
#
def isLonValid(value,sender=None):
  "validate longitude value (must be between +/-180 degrees"
  "returns True if the longitude value is valid"
  if abs(float(value))  > 180.0:
    if sender:
      error(sender+": Bad longitude ("+str(value)+"), must be between +/-180.0",1)
    else:
      error("Bad longitude ("+str(value)+"), must be between +/-180.0",1)
    return False
  else:
      return True

################################################################################################
#
# warning message
#
################################################################################################
#
def warning(message,sender=None):
  "write a warning message out"
  line = "\n"+100*"-"+"\n"
  if sender:
    code = "[WARNING from " + sender + "]"
  else:
    code = "[WARNING]"
  print (code,message,line)

################################################################################################
#
# outout usage message
#
################################################################################################
#
def usage(script,paramPath):
   "usage message for the 3D viewer"
   print ("\n\nUSAGE:\n\n")
   print ("%50s\n"%("user defined parameter file name"))
   print ("%40s\n"%("|"))
   print ("%10s %20s %10s\n"%("python",script,"paramFile"))
   print (" ")
   print ("\n\nNOTE:\n\n")
   print (" The shared parameter file, 'common.par', must reside under:",paramPath)
   print (" ")
   print ("\n\n\n\n")


################################################################################################
#
# timeIt 
#
################################################################################################
#
def timeIt(new,who,t0):
   "compute elapsed time since the last call (t0)"
   t1 = time()
   dt = t1 - t0
   t = t0
   line = 50*'.'
   print ("%s%s\n[TIME] %s %0.5f s\n%s\n"%(new,line,who,dt,line))

   return 
