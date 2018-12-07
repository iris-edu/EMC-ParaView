"""NAME: IrisEMC_Paraview-Utils.py - library of various functions in support of EMC

       http://ds.iris.edu/ds/products/emc-earthmodels/

 Copyright (C) 2018  Product Team, IRIS Data Management Center

    This is a free software; you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as
    published by the Free Software Foundation; either version 3 of the
    License, or (at your option) any later version.

    This script is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License (GNU-LGPL) for more details.  The
    GNU-LGPL and further information can be found here:
    http://www.gnu.org/

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

 History:
    2018-11-12 Manoch: added check_system to check OS
    2018-10-17 Manoch: R.1.2018.290 updates for R1
    2018-09-13 Manoch: R.0.2018.256 updated the isValueIn to ensure values are float
    2018-03-21 Manoch: R.0.2018.080 release for ParaView support
    2015-06-08 Manoch: updated the parameter file message based on the changes
               in the main script
    2015-01-17 Manoch: created
"""

import os
import platform
import numpy as np
from time import time


def do_https():
    """finds if secure HHTP is possible
    Keyword arguments:
        none

    Return values:
       bool
    """

    try:
        import ssl
        return True
    except ImportError:
        return False


def support_nc():
    """finds if scipy is available for reading netCDF file
    Keyword arguments:
        none

    Return values:
       bool
    """

    try:
        import scipy
        return True
    except ImportError:
        return False


def check_system():
    """find which OS the package is running under, so we can check for valid file types
    Keyword arguments:
        none

    Return values:
       operating system
    """

    return platform.system()


def min_max(these_values):
    """find min and max of a list or numpy array

    Keyword arguments:
        these_values: values to search

    Return values:
        this_min: minimum value
        this_max: maximum value
    """
    if type(these_values) is list:
        this_min = min(these_values)
        this_max = max(these_values)
    else:
        this_min = np.min(these_values)
        this_max = np.max(these_values)
    return this_min, this_max


def float_key(this_float, this_format='%0.4f'):
    """" creates a key for a dictionary based on a given value

    Keyword arguments:
        this_float: given float number
        this_format: format to use to construct the key

    Return values:
        the corresponding depth_key string
    """
    return this_format % float(this_float)


def str2float(sequence):
    """convert content of a sequence to float, otherwise leave them
    as string

    Keyword arguments:
        sequence: a sequence of values to convert

    Return values:
        a generator of the converted sequence
    """

    for item in sequence:
        try:
            yield float(item)
        except ValueError as e:
            yield item


def lon_is_360(lon):
    """checks longitude values to determine if they represent 0/360 range

    Keyword arguments:
        lon: list of longitudes to check

    Return values:
        boolean: True or False
    """
    if isinstance(lon, float) or isinstance(lon, int) or isinstance(lon, np.float64):
        if float(lon) > 180.0:
            return True
        else:
            return False
    else:
        lon_min, lon_max = min_max(lon)
        if lon_min >= 0.0 and lon_max > 180.0:
            return True
        else:
            return False


def lon_180(lon, fix_gap=False):
    """convert longitude values from 0/360 to -180/180

    Keyword arguments:
        lon: list of longitudes to check and convert

    Return values:
        lon: updated longitudes
        lon_map: mapping between old and new longitudes
    """

    lon_360 = lon_is_360(lon)
    lon_map = {}

    lon_start, lon_end = min_max(lon)
    lon_start_index = np.argmin(lon)
    lon_end_index = np.argmax(lon)

    if isinstance(lon, float) or isinstance(lon, int) or isinstance(lon, np.float64):
        if float(lon) > 180.0:
            this_lon = float(lon) - 360.0
            lon_map[float_key(lon)] = this_lon
            lon = this_lon

    else:

        grid = abs(sorted(lon)[1] - sorted(lon)[0])

        for lon_val in lon:
            lon_map[float_key(lon_val)] = float(lon_val)

        if lon_360:
            for i, lon_value in enumerate(lon):
                this_lon = float(lon_value)
                if this_lon > 180.0:
                    lon[i] = this_lon - 360.0
                    lon_map[float_key(lon_value)] = lon[i]
                    lon_map[float_key(lon[i])] = lon[i]
                else:
                    lon[i] = this_lon
                    lon_map[float_key(lon_value)] = lon[i]

        # this logic tries to address the gap at -180/180  or 0/360 longitudes. If the start and end longitudes
        # are within one grid away from each other they are moved closer to closed the gap.
        if fix_gap:
            if 360.0 - abs(lon_end - lon_start) <= grid:
                if lon_360:
                    lon_0 = -0.0009
                    lon_1 = 0.0
                else:
                   lon_0 = -179.9999
                   lon_1 = 179.9999
                lon_map[float_key(lon[lon_start_index])] = lon_0
                lon_map[float_key(lon[lon_end_index])] = lon_1
                lon_map[float_key(lon_start)] = lon_0
                lon_map[float_key(lon_end)] = lon_1
                lon_map[float_key(lon_0)] = lon_0
                lon_map[float_key(lon_1)] = lon_1
                lon[lon_start_index] = lon_0
                lon[lon_end_index] = lon_1
    if fix_gap:
        return lon, lon_map
    else:
        return lon


def checkPath(path):
    """check path to see if it exists

    Keyword arguments:
        path: directory path to check

    Return values:
        bool: True or False
    """
    if os.path.exists(path):
        return path
    else:
        return None


def isValueIn(value, value_min, value_max):
    """"check a value to see if it is within limits

    Keyword arguments:
        value: value to check
        value_min: minimum acceptable value
        value_max: maximum acceptable value

    Return values:
        bool: True or False
    """
    if float(value) < float(value_min) or float(value) > float(value_max):
        return False
    else:
        return True


def isLongitudeIn(longitude, lon_min, lon_max):
    """check a longitude to see if it is within the box

    Keyword arguments:
        longitude: longitude to check
        lon_min: minimum acceptable longitude
        lon_max: maximum acceptable longitude

    Return values:
        bool: True or False
    """

    # validate based on min and max if regular

    if lon_min < lon_max:
        if lon_min <= longitude <= lon_max:
            return True
        else:
            return False

    # move to 0-360 to avoid zero crossing and 180 crossing issues
    if lon_min <= 0:
        lon_min += 360
    if lon_max <= 0:
        lon_max += 360
    if longitude <= 0:
        longitude += 360

    if longitude < lon_min or longitude > lon_max:
        return False
    return True


def getLons(lon_start, lon_end, inc):
    """create a list of longitudes from start to end

    Keyword arguments:
        lon_start: starting longitude
        lon_end: end longitude
        inc: longitude increment

    Return values:
        lon_list: longitude list
    """

    # move to 0-360 to avoid zero crossing and 180 crossing issues
    lon = lon_start - inc
    lon_list = []
    if lonStart < lonEnd:
        while lon <= lonEnd - inc:
            lon += inc
            lon_list.append(float(lon))
    else:
        while lon <= 180 - inc:
            lon += inc
            lon_list.append(float(lon))
        lon = -180.0
        while lon <= lon_end - inc:
            lon += inc
            lon_list.append(float(lon))
    return lon_list


def makePath(directory):
    """Checks a directory for existance and if it does not exist,
       create it. If needed, create all parent directories.

    Keyword arguments:
        directory: directory to check

    Return values:
        bool if directory does not exist
        thisPath --- the path if exists
    """

    # the path must be an absolute path (start with "/")
    if not os.path.isabs(directory):
        print ('ERR [checkMakePath]: pat must be an absolute path')
        return None

    # create directories
    this_path = os.path.abspath(directory)
    if checkPath(this_path) is None:
        os.makedirs(this_path)
    return this_path


def error(message, code=1, sender=None):
    """write an error message out in block format and return an exit code

     Keyword arguments:
      message: message to write
      code: code to return
      sender: sender of the message

    Return values:
      code: error code
    """
    line = "\n" + 100 * "*" + "\n"
    if sender:
        lab = "[ERROR from " + sender + "]"
    else:
        lab = "[ERROR]"
    print (line, lab, message, line)
    return code


def isLatValid(value, sender=None):
    """validate latitude value (must be between +/-90 degrees
    returns True if the latitude value is valid

    Keyword arguments:
       value: latitude to check
       sender: sender

    Return values:
      bool: True or False
    """
    if abs(float(value)) > 90.0:
        if sender:
            error(sender + ": Bad latitude (" + str(value) + "), must be between +/-90.0", 1)
        else:
            error("Bad latitude (" + str(value) + "), must be between +/-90.0", 1)
        return False
    else:
        return True


def isLonValid(value, sender=None):
    """validate longitude value (must be between +/-180 degrees
    returns True if the longitude value is valid

      Keyword arguments:
         value: longitude to check
         sender: sender

      Return values:
        bool: True or False
      """
    if abs(float(value)) > 180.0:
        if sender:
            error(sender + ": Bad longitude (" + str(value) + "), must be between +/-180.0", 1)
        else:
            error("Bad longitude (" + str(value) + "), must be between +/-180.0", 1)
        return False
    else:
        return True


def warning(message, sender=None):
    """write a warning message out

    Keyword arguments:
        message: message to write
        sender: sender of the message

    Return values:
        code: error code
        message: message
        line: separator line
      """
    line = "\n" + 100 * "-" + "\n"
    if sender:
        code = "[WARNING from " + sender + "]"
    else:
        code = "[WARNING]"
    print (code, message, line)


def usage(script, paramPath):
    """usage message for the 3D viewer
         Keyword arguments:
               script: sending script
               paramPath: path to the parameter file
    """
    print ("\n\nUSAGE:\n\n")
    print ("%50s\n" % "user defined parameter file name")
    print ("%40s\n" % "|")
    print ("%10s %20s %10s\n" % ("python", script, "paramFile"))
    print (" ")
    print ("\n\nNOTE:\n\n")
    print (" The shared parameter file, 'common.par', must reside under:", paramPath)
    print (" ")
    print ("\n\n\n\n")


def timeIt(new, who, t0):
    """compute elapsed time since the last call (t0)

     Keyword arguments:
         new: tag
         who: timing sender
         t0: initial time
    """
    t1 = time()
    dt = t1 - t0
    t = t0
    line = 50 * '.'
    print ("%s%s\n[TIME] %s %0.5f s\n%s\n" % (new, line, who, dt, line))

