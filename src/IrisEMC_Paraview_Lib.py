#
# -*- coding: UTF-8 -*-
#
################################################################################################
#
# NAME: IrisEMC_Paraview-Lib.py - EMC ParaView scripts mmain library
#
#       http://ds.iris.edu/ds/products/emc/
#
# DESCRIPTION: Thefunctions in this library are for support of EMC ParaView Python scripts
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
# HISTORY:
#    2018-09-13 Manoch: R.0.2018.256 added support for 3D geoCSV files
#    2018-05-09 Manoch: R.0.2018.129 added support for 2D netCDF files
#    2018-04-30 Manoch: R.0.2018.120 modified query2fileName to accepth optional url argument
#                       and add a simplified version of it to the begining of the file name.
#                       This would allow the code to distinguish between files created from
#                       two different sites but using the same query
#    2018-04-23 Manoch: R.0.2018.113 update lat and lon loops logic to avoid gaps at region 
#                       boundaries due to selected step (inc)
#    2018-03-21 Manoch: R.0.2018.080 release
#
#
# -*- coding: UTF-8 -*-
#
################################################################################################
#
import sys,os
from paraview.simple import *
import IrisEMC_Paraview_Param as param
import IrisEMC_Paraview_Utils as utils

#
# parameters
#
depthFactor   = 1
irisEMC_Files_URL = param.irisEMC_Files_URL
usgsEvent_URL     = param.usgsEvent_URL
usgsSlab_URL      = param.usgsSlab_URL
pathDict          = param.pathDict
columnKeys        = param.columnKeys
filesDict         = param.filesDict
etopo5File        = filesDict['ETOPO5']

#
# USGS Slab 1.0
#
usgsSlab_URL      = param.usgsSlab_URL
usgsSlabDict      = param.usgsSlabDict
usgsSlabKeys      = param.usgsSlabKeys
usgsSlabValues    = param.usgsSlabValues
usgsSlabRangeDict = param.usgsSlabRangeDict

#
# boundaries
#
boundariesDict = param.boundariesDict
boundaryKeys   = param.boundaryKeys
boundaryValues = param.boundaryValues

#
# areas
#
areaDict       = param.areaDict
areaRangeDict  = param.areaRangeDict
areaKeys       = param.areaKeys
areaValues     = param.areaValues

#
# earthquake catalogs
#
earthquakeCatalogDict = param.earthquakeCatalogDict
earthquakeQuery       = param.earthquakeQuery
earthquakeKeys        = param.earthquakeKeys
earthquakeValues      = param.earthquakeValues

#
# volcano
#
volcanoLocationsQuery   = param.volcanoLocationsQuery
volcanoLocationsKeys    = param.volcanoLocationsKeys
volcanoLocationsValues  = param.volcanoLocationsValues
volcanoLocationsDict    = param.volcanoLocationsDict  


################################################################################################
#
# getArea
#
################################################################################################
def getArea(Area,Latitude_Begin,Latitude_End,Longitude_Begin,Longitude_End):
    """
    provide latitude, longitude ranges for the area selected. The provided latitude, longitudes,
    if any, will override the corresponding values for the selected area.

    Parameters
     ----------
       Area: int
          drop down Area index
       Latitude_Begin: float
          start latitude
       Latitude_End: float
          end latitude
       Longitude_Begin: float
          start longitude
       Longitude_End: float
          range longitude

    Returns
    -------
    lat0: float
       start latitude
    lat1: float
       end latitude
    lon0: float
       start longitude
    lon1: float
       end longitude

    """
    lat0, lat1 = areaRangeDict[str(Area)]['lat']
    lon0, lon1 = areaRangeDict[str(Area)]['lon']
   
    try:
        lat0  = float(Latitude_Begin)
    except:
        pass
    try:
        lat1    = float(Latitude_End)
    except:
        pass
    try:
        lon0 = float(Longitude_Begin)
    except:
        pass
    try:
        lon1   = float(Longitude_End)
    except:
        pass

    return lat0, lat1, lon0, lon1

################################################################################################
#
# eqHeader
#
################################################################################################
def eqHeader(url):
    """
    generate a GeoCSV style header for FDSN style event service output

    Parameters
     ----------
       url: str
          event service URL

    Returns
    -------
    header: str
         GeoCSV file header

    """
    header  = "# dataset: Earthquake catalog\n"
    header += "# source: " + url + "\n"
    header += "# delimiter: |\n"
    header += "# latitude_column: Latitude\n"
    header += "# longitude_column: Longitude\n"
    header += "# depth_column: Depth/km\n"
    header += "# magnitude_column: Magnitude\n"
    header += "EventID|Time|Latitude|Longitude|Depth/km|Author|Catalog|Contributor|ContributorID"
    header += "|MagType|Magnitude|MagAuthor|EventLocationName\n"
    return header

################################################################################################
#
# WOVOHeader
#
################################################################################################
def wovoHeader(url):
    """
    generate a GeoCSV style header for the WOVOdata volcano locations

    Parameters
     ----------
    url: str
       WOVOdata volcano locationsURL

    Returns
    -------
    header: str
        GeoCSV file header

    """
    header  = "# dataset: Volcano Locations\n"
    header += "# source: " + url + "\n"
    header += "# delimiter: |\n"
    header += "# latitude_column: lat\n"
    header += "# longitude_column: long\n"
    header += "# elevation_column: elevation\n"
    return header

################################################################################################
#
# isClose
#
################################################################################################
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    """
    compare two values to see if they are close (within the given tolerance)

    Parameters
    ----------
    a: float
       first value
    b: float
       second value
    rel_tol: float
       relative tolerance
    abs_tol: float
       absolute tolerance

    Returns
    -------
    boolean 
      a flag  indicating if the two values are close
    """
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def readGcsv(file_name):
    """
    read a given GeoCSV file and output a dictionary of the header keys along with a text
    block of the date body

    Parameters
    ----------
    file_name: str
       the GeoCSV file to read

    Returns
    -------
    params: dict
       a dictionary of the key-value pairs found in the header
    data: str
       a text block of the body
    """
    fp = open(file_name, 'r')
    content = fp.read()
    lines = content.split('\n')
    fp.close()
    params = {}
    data = []
    for i in range(len(lines)):
        if len(lines[i].strip()) <= 0:
                continue
        elif lines[i].strip()[0] == '#':
            this_line = lines[i].strip()[1:]
            if len(this_line.strip()) <= 0:
                continue
            if ':' not in this_line:
                if params['latitude_column'] in this_line and params['longitude_column'] in this_line:
                    params['header'] = this_line.strip().split(params['delimiter'])
                continue
            values = this_line.split(':')
            key = values[0].strip().lower()
            params[key] = this_line.replace(key+':', '').strip()
        else:
            data.append(lines[i].strip())
    if 'latitude_column' not in params.keys():
        params['latitude_column'] = 'latitude'
    if 'longitude_column' not in params.keys():
        params['longitude_column'] = 'longitude'
    if 'elevation_column' not in params.keys():
        params['elevation_column'] = 'elevation'
    if 'depth_column' not in params.keys():
        params['depth_column'] = 'depth'
    return params, data


################################################################################################
#
# fileName
#
################################################################################################
def fileName(fullFileName): 
    """
    for a given full file name, extract and return a file name without extension and path

    Parameters
    ----------
    fullFileName: str
       a full file name

    Returns
    -------
    filename: str
       file name without extension and path
    """
    filename_w_ext = os.path.basename(fullFileName)
    filename, file_extension = os.path.splitext(filename_w_ext)
    return filename

################################################################################################
#
# readInfoFile
#
################################################################################################
def readInfoFile(dataFile):
    """
    find an info file for a data file and return the origin information
    if info file not found, return the file name

    Parameters
    ----------
    dataFile: str
       data file name

    Returns
    -------
    origin: str
       origin information
    """
    infoFile = os.path.splitext(dataFile)[0]+'.inf'
    origin = fileName(dataFile)
    if os.path.isfile(infoFile):
            fp = open(infoFile,'r')
            lines = fp.read().split('\n')
            fp.close()
            origin = dataFile
            for line in lines:
                if 'source:' in line:
                    origin = line.replace('source:','')[1:].strip()
                    import urlparse
                    origin = urlparse.urlparse(origin).netloc
                    break
    return origin

################################################################################################
#
# query2fileName
#
################################################################################################
def query2fileName(query,url=''):
    """
    convert a query to a potential file name by removing some characters

    Parameters
    ----------
    query: str
       the query portion of a URL

    Returns
    -------
    filename: str
       the file name without path
    """
    if len(url) > 0:
       import urlparse
       urlinfo  = urlparse.urlparse(url)
       site     = urlinfo[1]
       query    = '_'.join([site,query])
    filename = query.replace("&",'').replace("=","").replace(".",'').replace("formattext","")
    filename = filename.replace("nodata404","").replace("max","").replace("min","")
    filename = filename.replace("-","")+".csv"

    return filename

################################################################################################
#
# isUrlValid
#
################################################################################################
def isUrlValid(url):
    """
    Checks if a given URL is reachable

    Parameters
    ----------
    url: str
        URL to check

    Returns
    -------
    bool
       a flag indicating if the  URL is reachable
    """

    import urllib
    conn = urllib.urlopen(url)
    code = conn.getcode()
    if code == 200:
       return True
    else:
        return False

################################################################################################
#
# getFileFromUrl
#
################################################################################################
def getFileFromUrl(url,path, filename=''):
    """
   get a file from the given URL and save it locally under a given file name

    Parameters
    ----------
    url: str
       URL of the file to retrieve
    path: str
       location where the file should be saved
    filename: str
       name to save the file under (this overrides the default file name)

    Returns
    -------
    bool 
       indicating if the operation was a success
    destination: str
       full address of the local file
    url: str
       URL where the file came from (se to destination if not retrieved)
    """
    try:
       import urllib
       import urlparse
       from datetime import datetime
       if len(filename.strip()) <= 0:
          urlinfo     = urlparse.urlparse(url)
          filename    = urlinfo[2].strip()
          filename    = os.path.basename(filename)
       destination    = os.path.join(path,filename)
       urllib.urlretrieve(url, destination)
       if os.path.isfile(destination):
           infoFile = os.path.splitext(destination)[0]+'.inf'
           fp = open(infoFile,'w')
           fp.write('# date: %s\n'%(str(datetime.now())))
           fp.write('# file: %s\n'%(destination))
           fp.write('# source: %s\n'%(url))
           fp.close()
           return True, destination, url
    except:
        pass
    url = destination
    return False, destination, url

################################################################################################
#
# findFile
#
################################################################################################
def findFile(address,loc,query=''):
    """
    find a file either locally or via a URL

    Parameters
    ----------
    address: str
       file address, path, url, etc.
    loc: str
       location of the file
    query: str
       URL query string

    Returns
    -------
    found: boo
       indicating if the operation was a success
    address: str
       full address of the local file
    source: str
       where the file came from
    """
    import urllib

    found = False

    #
    # it is a full path to a file?
    #
    source = address
    if os.path.isfile(address):
        origin = readInfoFile(source)
        return True, address, origin
    #
    # it is a file under the data directory?
    #
    elif os.path.isfile(os.path.join(loc,address)):
        source = os.path.join(loc,address)
        origin = readInfoFile(source)
        return True, source, origin
    #
    # Other posibilities, URL?
    #
    else:
        #
        # check the DMC URL
        #
        if loc in(pathDict['EMC_BOUNDARIES_PATH'],pathDict['EMC_MODELS_PATH']):
           source = irisEMC_Files_URL + address
           if isUrlValid(source):
              found,destination,origin = getFileFromUrl(source,loc,filename=os.path.join(loc,address))
        #
        # USGS Slab 1.0
        #
        elif loc == pathDict['EMC_SLABS_PATH']:
           source = usgsSlab_URL + address
           if isUrlValid(source):
              found,destination,origin = getFileFromUrl(source,loc,filename=os.path.join(loc,address))
        #
        # earthquakes
        #
        elif(loc == pathDict['EMC_EARTHQUAKES_PATH']):
           source = query
           if isUrlValid(source):
              found,destination,origin = getFileFromUrl(source,loc,filename=os.path.join(loc,address))
              if found:
                 fp = open(destination,'r+')
                 catalog = fp.read()
                 fp.seek(0, 0)
                 fp.write(eqHeader(source))
                 fp.write(catalog)
                 fp.close()
        #
        # Volcano locations
        #
        elif(loc == pathDict['EMC_VOLCANOES_PATH']):
           source = query
           if isUrlValid(source):
              found,destination,origin = getFileFromUrl(source,loc,filename=os.path.join(loc,address))
              if found:
                 fp = open(destination,'r+')
                 catalog = fp.read()
                 fp.seek(0, 0)
                 fp.write(wovoHeader(source))
                 fp.write(catalog)
                 fp.close()
        #
        # did we find the file?
        #
        if found:
            return found,destination, origin
        #
        # did user provide a URL
        #
        else:
            source = address
            found,destination,origin = getFileFromUrl(address,loc,query)
            return found,destination, origin
    return False, address,source

################################################################################################
#
# llz2xyz 
#
################################################################################################
def llz2xyz(lat,lon,depth):
   """
   convert latitude, longitude, and altitude to earth-centered, earth-fixed (ECEF) cartesian
   the output coordinates will be normalized to the radius of interest for the
   displayed sphere as defined by the rad parameter above

   code is based on:

   http://www.mathworks.com/matlabcentral/fileexchange/7942-covert-lat--lon--alt-to-ecef-cartesian/content/lla2ecef.m
   latitude, longitude, altitude to ECEF ("Earth-Centered, Earth-Fixed")
   http://www.gmat.unsw.edu.au/snap/gps/clynch_pdfs/coordcvt.pdf

   calculations based on: 

   http://rbrundritt.wordpress.com/2008/10/14/conversion-between-spherical-and-cartesian-coordinates-systems/
   http://stackoverflow.com/questions/10473852/convert-latitude-and-longitude-to-point-in-3d-space
   http://www.oosa.unvienna.org/pdf/icg/2012/template/WGS_84.pdf

   computation verified using:

   http://www.sysense.com/products/ecef_lla_converter/index.html

   Parameters
   ----------
   lat: float
      latitude (deg)
   lon: float
      longitude (deg)
   depth: float
      depth (km)

   Returns
   -------
   x: float
      x-coordinate  normalized to the radius of Earh
   y: float
      y-coordinate  normalized to the radius of Earh
   z: float
      z-coordinate  normalized to the radius of Earh
   """
   import numpy as np
   from scipy import deg2rad,rad2deg

   alt     = -1.0 * 1000.0 * depth # height above WGS84 ellipsoid (m)
   lat     = deg2rad(lat)
   cosLat  = np.cos(lat)
   sinLat  = np.sin(lat)

   #
   # World Geodetic System 1984
   # WGS 84
   #
   erad    = np.float64(6378137.0)      # Radius of the Earth in meters (equatorial radius, WGS84)
   rad     = 1    # sphere radius
   e       = np.float64(8.1819190842622e-2)
   n       = erad / np.sqrt(1.0 - e * e * sinLat * sinLat) # prime vertical radius of curvature

   lon     = deg2rad(lon)
   cosLon  = np.cos(lon)
   sinLon  = np.sin(lon)

   x    = (n + alt) * cosLat * cosLon      # meters
   y    = (n + alt) * cosLat * sinLon      # meters
   z    = ((1 - e * e) * n + alt) * sinLat # meters

   x    = x * rad / erad # normalize to radius of rad
   y    = y * rad / erad # normalize to radius of rad
   z    = z * rad / erad # normalize to radius of rad
   return x,y,z

################################################################################################
#
# xyz2llz 
#
################################################################################################
def xyz2llz(x,y,z):
   """
   convert earth-centered, earth-fixed (ECEF) cartesian x, y, z to latitude, longitude, and altitude 

   code is based on:

   https://www.mathworks.com/matlabcentral/fileexchange/7941-convert-cartesian--ecef--coordinates-to-lat--lon--alt?focused=5062924&tab=function

    Parameters
    ----------
    x: float
       x-coordinate  normalized to the radius of Earh
    y: float
       y-coordinate  normalized to the radius of Earh
    z: float
       z-coordinate  normalized to the radius of Earh

    Returns
    -------
    lat: float
       latitude (deg)
    lon: float
       longitude (deg)
    depth: float
       depth (km)
   """
   import numpy as np
   import math
   from scipy import deg2rad,rad2deg

   # World Geodetic System 1984
   # WGS 84
   #
   erad    = np.float64(6378137.0)      # Radius of the Earth in meters (equatorial radius, WGS84)
   rad     = 1    # sphere radius
   e       = np.float64(8.1819190842622e-2)

   # convert to radius 
   x       = x * erad /rad
   y       = y * erad /rad
   z       = z * erad /rad

   b       = np.sqrt(erad*erad*(1-e*e))
   ep      = np.sqrt((erad*erad-b*b)/(b*b));
   p       = np.sqrt(x*x+y*y)
   th      = np.arctan2(erad*z,b*p)
   lon     = np.arctan2(y,x)
   lat     = np.arctan2((z+ep*ep*b*np.sin(th)*np.sin(th)*np.sin(th)),(p-e*e*erad*np.cos(th)*np.cos(th)*np.cos(th)))
   N       = erad /np.sqrt(1.0-e*e*np.sin(lat)*np.sin(lat))
   alt     = p/np.cos(lat)-N

   lon     = lon % (math.pi*2.0)
   lon     = rad2deg(lon)
   if lon > 180.0:
      lon -= 360.0
   lat     = rad2deg(lat)
   alt     = -1 * (alt) / 1000.0  # depth as negative alt
   
   return lat,lon,alt


def get_column(matrix, column_index):
    """Read in a matrix and return a selected column.

    Keyword arguments:
    matrix -- the matrix to process
    column_index -- index of the column to extract

    Return values:
    list of values in column_index of matrix
     """
    return [row[column_index] for row in matrix]


def read_geocsv_model_3d(model_file, ll, ur, depth_min, depth_max, inc):
    """Read in a 3-D Earth model in the GeoCSV format.

      Keyword arguments:
      model_file -- model file
      ll -- lower-left coordinate
      ur -- upper-right coordinate
      depth_min -- minimum depth
      depth_max -- maximum depth
      inc -- grid sampling interval

      Return values:
      x -- x-coordinate  normalized to the radius of the Earth
      y -- y-coordinate  normalized to the radius of the Earth
      z -- z-coordinate  normalized to the radius of the Earth
      meta -- file metadata information
     """

    # model data and metadata
    import numpy as np
    import csv
    (params, lines) = readGcsv(model_file)

    # model data
    data = []
    for line in lines:
        data.append(line.split(params['delimiter']))

    # model variables
    depth_variable = params['depth_column']
    lat_variable = params['latitude_column']
    lon_variable = params['longitude_column']
    elev_variable = params['elevation_column']
    variables = []
    for this_param in params.keys():
        if params[this_param] not in (depth_variable, lon_variable, lat_variable, elev_variable
                                      ) and '_column' in this_param:
            variables.append(params[this_param])

    # index to the variables
    var_index = {}
    for i, val in enumerate(params['header']):
        if val == depth_variable:
            depth_index = i
        elif val == lon_variable:
            lon_index = i
        elif val == lat_variable:
            lat_index = i
        else:
            var_index[val] = i

    lat = list(set(get_column(data, lat_index)))
    lon = list(set(get_column(data, lon_index)))
    for i, lon_val in enumerate(lon):
        if float(lon_val) > 180.0:
            lon[i] = float(lon_val) - 360.0

    depth = list(set(get_column(data, depth_index)))

    # select the values within the ranges (this is to get a count only)
    latitude = []
    longitude = []
    depth2 = []
    last_i = -1
    for i, lon_val in enumerate(lon):
        if i != 0 and i != len(lon) - 1 and i != last_i + inc:
            continue
        last_i = i

        for j, depth_val in enumerate(depth):
            last_k = -1
            for k, lat_val in enumerate(lat):
                if k != 0 and k != len(lat) - 1 and k != last_k + inc:
                    continue
                last_k = k

                if utils.isValueIn(float(lat_val), ll[0], ur[0]) and utils.isLongitudeIn(float(lon_val),
                                                                                         ll[1],
                                                                                         ur[1]) and \
                        utils.isValueIn(float(depth_val), depth_min, depth_max):
                    if float(lon_val) not in longitude:
                        longitude.append(float(lon_val))
                    if float(depth_val) not in depth2:
                        depth2.append(float(depth_val))
                    if float(lat_val) not in latitude:
                        latitude.append(float(lat_val))

    # model data grid definition
    V = {}
    longitude.sort()
    latitude.sort()
    depth2.sort()
    nx = len(longitude)
    ny = len(depth2)
    nz = len(latitude)

    index = [-1, -1, -1]
    meta = {'depth': [], 'lat': [100, -100], 'lon': [400, -400], 'source': model_file}

    X = np.zeros((nx, ny, nz))
    Y = np.zeros((nx, ny, nz))
    Z = np.zeros((nx, ny, nz))

    for i, values in enumerate(data):
        lon_val = float(values[lon_index])
        lat_val = float(values[lat_index])
        depth_val = float(values[depth_index])
        if lon_val in longitude and lat_val in latitude and depth_val in depth2:
            meta['lon'] = [min(meta['lon'][0], float(lon_val)), max(meta['lon'][0], float(lon_val))]
            ii = longitude.index(lon_val)
            jj = depth2.index(depth_val)
            kk = latitude.index(lat_val)
            if depth_val not in meta['depth']:
                meta['depth'].append(float(depth_val))
            meta['lat'] = [min(meta['lat'][0], float(lat_val)), max(meta['lat'][0], float(lat_val))]
            x, y, z = llz2xyz(float(lat_val), float(lon_val), float(depth_val) * depthFactor)
            print(ii, jj, kk)
            X[ii, jj, kk] = x
            Y[ii, jj, kk] = y
            Z[ii, jj, kk] = z
            index[depth_index] = j
            index[lat_index] = k
            index[lon_index] = i
            for l, var_val in enumerate(variables):
                if var_val not in V.keys():
                    V[var_val] = np.zeros((nx, ny, nz))
                V[var_val][ii, jj, kk] = float(values[var_index[var_val]])

    return X, Y, Z, V, meta


def read_geocsv_model_3d_extent(model_file, ll, ur, depth_min, depth_max, inc):
    """Read in an Earth model in the GeoCSV format and compute the display grid size needed.

      Keyword arguments:
      model_file -- model file
      ll -- lower-left coordinate
      ur -- upper-right coordinate
      depth_min -- minimum depth
      depth_max -- maximum depth
      inc -- grid sampling interval

      Return values:
      nx -- number of grid points in the x-coordinate
      ny -- number of grid points in the y-coordinate
      nz -- number of grid points in the z-coordinate
     """

    # model data and metadata
    import numpy as np
    import csv
    (params, lines) = readGcsv(model_file)

    # model data
    data = []
    for line in lines:
        data.append(line.split(params['delimiter']))

    # model variables
    depth_variable = params['depth_column']
    lat_variable = params['latitude_column']
    lon_variable = params['longitude_column']
    elev_variable = params['elevation_column']
    variables = []
    for this_param in params.keys():
        if params[this_param] not in (depth_variable, lon_variable, lat_variable, elev_variable
                                      ) and '_column' in this_param:
            variables.append(params[this_param])

    # index to the variables
    var_index = {}
    for i, val in enumerate(params['header']):
        if val == depth_variable:
            depth_index = i
        elif val == lon_variable:
            lon_index = i
        elif val == lat_variable:
            lat_index = i
        else:
            var_index[val] = i

    lat = list(set(get_column(data, lat_index)))
    lon = list(set(get_column(data, lon_index)))
    for i, lon_val in enumerate(lon):
        if float(lon_val) > 180.0:
            lon[i] = float(lon_val) - 360.0

    depth = list(set(get_column(data, depth_index)))

    # select the values within the ranges (this is to get a count only)
    latitude = []
    longitude = []
    depth2 = []
    last_i = -1
    for i, lon_val in enumerate(lon):
        if i != 0 and i != len(lon) - 1 and i != last_i + inc:
            continue
        last_i = i

        for j, depth_val in enumerate(depth):
            last_k = -1
            for k, lat_val in enumerate(lat):
                if k != 0 and k != len(lat) - 1 and k != last_k + inc:
                    continue
                last_k = k

                if utils.isValueIn(float(lat_val), ll[0], ur[0]) and utils.isLongitudeIn(float(lon_val),
                                                                                         ll[1],
                                                                                         ur[1]) and \
                        utils.isValueIn(float(depth_val), depth_min, depth_max):
                    if float(lon_val) not in longitude:
                        longitude.append(float(lon_val))
                    if float(depth_val) not in depth2:
                        depth2.append(float(depth_val))
                    if float(lat_val) not in latitude:
                        latitude.append(float(lat_val))

    # model data grid definition
    nx = len(sorted(longitude))
    ny = len(sorted(depth2))
    nz = len(sorted(latitude))

    return nx, ny, nz


################################################################################################
#
# read_netCdfEarthModel 
#
################################################################################################
def read_netCdfEarthModel(modelFile,latVariable,lonVariable,depthVariable,LL,UR,depthMin,depthMax,inc):
   """
   read in an EMC Earth model in the netCDF format

    Parameters
    ----------
    modelFile: str
       model file
    latVariable: str
      latitude variable
   lonVariable: str
      longitude variable
   depthVar: str
      depthVariable
    LL: list
       lower-left coordinate
    UR: list
       upper-right coordinate
    depthMin: float
       minimum depth
    depthMax: float
       maximum depth
    inc: int
       grid sampling interval

    Returns
    -------
    X: float
       x-coordinate  normalized to the radius of Earh
    Y: float
       y-coordinate  normalized to the radius of Earh
    Z: float
       z-coordinate  normalized to the radius of Earh
    meta: dict
       file metadata information
   """
   #depthVariable = 'depth'
   #lonVariable   = 'longitude'
   #latVariable   = 'latitude'

   #
   # model data
   # NetCDF files, when opened read-only, return arrays that refer directly to memory-mapped data on disk:
   #
   import numpy as np
   from scipy.io import netcdf
   emcdata     = netcdf.netcdf_file(modelFile, 'r')
   variables   = []
   for name in emcdata.variables.keys():
       if name not in (depthVariable,lonVariable,latVariable):
          variables.append(name)

   #
   # I assume all variables are defined with uniform order of latitude, longitude and depth
   #
   var = variables[0]
   for i in range(len(emcdata.variables[var].dimensions)):
      if emcdata.variables[var].dimensions[i] == depthVariable:
         depthIndex = i
      elif emcdata.variables[var].dimensions[i] == lonVariable:
         lonIndex = i
      else:
         latIndex = i

   lat         = emcdata.variables[latVariable][:].copy()
   lon         = emcdata.variables[lonVariable][:].copy()
   for i in range(len(lon)):
      if lon[i]> 180.0: lon[i] -= 360.0;

   depth       = emcdata.variables[depthVariable][:].copy()

   #
   # select the values within the ranges (this is to get a count only)
   #
   depth2    = []
   latitude  = []
   longitude = []
   depth2    = []
   lastI     = -1
   for i in range(len(lon)):
      if i != 0 and i != len(lon)-1 and i != lastI+inc:
             continue
      lastI = i 
      for j in range(len(depth)):
         lastK = -1
         for k in range(len(lat)):
            if k != 0 and k != len(lat)-1 and k != lastK+inc:
                  continue
            lastK = k
            if utils.isValueIn(lat[k],LL[0],UR[0]) and utils.isLongitudeIn(lon[i],LL[1],UR[1]) and utils.isValueIn(float(depth[j]), depthMin, depthMax):
              if lon[i] not in longitude:
                 longitude.append(lon[i])
              if depth[j] not in depth2:
                 depth2.append(depth[j])
              if lat[k] not in latitude:
                 latitude.append(lat[k])

   #
   # model data grid definition
   #
   V  = {}
   nx = len(longitude)
   ny = len(depth2)
   nz = len(latitude)
   index     = [-1,-1,-1]
   meta      = {'depth':[],'lat':[100,-100],'lon':[400,-400],'source':modelFile}
   for l in range(len(variables)):
      X      = np.zeros((nx, ny, nz))
      Y      = np.zeros((nx, ny, nz))
      Z      = np.zeros((nx, ny, nz))
      v      = np.zeros((nx, ny, nz))
      var    = variables[l]
      emcin  = emcdata.variables[var][:].copy()
      latitude  = []
      longitude = []
      depth2    = []
      ii     = -1
      jj     = -1
      kk     = -1
      oldI   = -1
      oldJ   = -1
      oldK   = -1
      lastI  = -1
      for i in range(len(lon)):
         if i != 0 and i != len(lon)-1 and i != lastI+inc:
             continue
         lastI = i  
         for j in range(len(depth)):
            lastK = -1
            for k in range(len(lat)):
              if k != 0 and k != len(lat)-1 and k != lastK+inc:
                  continue
              lastK = k
              if utils.isValueIn(lat[k],LL[0],UR[0]) and utils.isLongitudeIn(lon[i],LL[1],UR[1]) and utils.isValueIn(float(depth[j]), depthMin, depthMax):
                 if i != oldI:
                    meta['lon'] = [min(meta['lon'][0],lon[i]),max(meta['lon'][0],lon[i])]
                    oldI = i
                    ii  +=1
                    jj   = -1
                    oldJ = -1
                    kk   = -1
                    oldK = -1
                 if j != oldJ:
                    if depth[j] not in meta['depth']:
                       meta['depth'].append(depth[j])
                    oldJ = j
                    jj  +=1
                    kk   = -1
                    oldK = -1
                 if k != oldK:
                    meta['lat'] = [min(meta['lat'][0],lat[k]),max(meta['lat'][0],lat[k])]
                    oldK = k
                    kk  +=1
                 x,y,z = llz2xyz(lat[k],lon[i],depth[j]*depthFactor)
                 X[ii,jj,kk]=x
                 Y[ii,jj,kk]=y
                 Z[ii,jj,kk]=z
                 index[depthIndex] = j
                 index[latIndex]   = k
                 index[lonIndex]   = i

                 v[ii,jj,kk] = emcin[index[0]][index[1]][index[2]]

      V[var] = v
   emcdata.close()
   return X,Y,Z,V,meta

################################################################################################
#
# find_netCDFModelExtent 
#
################################################################################################
def find_netCDFModelExtent(modelFile,latVariable,lonVariable,depthVariable,LL,UR,depthMin,depthMax,inc):
   """
   find the extent of the model as the number of grid points in each direction

   Parameters
   ----------
   modelFile: str
      model file
   latVariable: str
      latitude variable
   lonVariable: str
      longitude variable
   depthVar: str
      depthVariable
   LL: list
      lower-left coordinate
   UR: list
      upper-right coordinate
   depthMin: float
      minimum depth
   depthMax: float
      maximum depth
   inc: int
      grid sampling interval

   Returns
   -------
   ii: int
      number of element in the x-direction
   jj: int
      number of element in the y-direction
   kk: int
      number of element in the z-direction
   """
   #depthVariable = 'depth'
   #lonVariable   = 'longitude'
   #latVariable   = 'latitude'

   #
   # model data
   #
   import numpy as np
   from scipy.io import netcdf
   emcdata     = netcdf.netcdf_file(modelFile, 'r')
   variables   = []
   for name in emcdata.variables.keys():
       if name not in (depthVariable,lonVariable,latVariable):
          variables.append(name)

   #
   # I assume all variables are defined with uniform order of latitude, longitude and depth
   #
   var = variables[0]
   for i in range(len(emcdata.variables[var].dimensions)):
      if emcdata.variables[var].dimensions[i] == depthVariable:
         depthIndex = i
      elif emcdata.variables[var].dimensions[i] == lonVariable:
         lonIndex = i
      else:
         latIndex = i

   lat         = emcdata.variables[latVariable][:].copy()
   lon         = emcdata.variables[lonVariable][:].copy()
   for i in range(len(lon)):
      if lon[i]> 180.0: lon[i] -= 360.0;

   depth       = emcdata.variables[depthVariable][:].copy()
   emcdata.close()

   #
   # model data grid definition
   #
   for l in range(len(variables)):
      ii     = -1
      jj     = -1
      kk     = -1
      oldI   = -1
      oldJ   = -1
      oldK   = -1
      lastI  = -1
      for i in range(len(lon)):
         if i != 0 and i != len(lon)-1 and i != lastI+inc:
             continue
         lastI = i 
         for j in range(len(depth)):
            lastK = -1
            for k in range(len(lat)):
              if k != 0 and k != len(lat)-1 and k != lastK+inc:
                  continue
              lastK = k
              if utils.isValueIn(lat[k],LL[0],UR[0]) and utils.isLongitudeIn(lon[i],LL[1],UR[1]) and utils.isValueIn(float(depth[j]), depthMin, depthMax):
                 if i != oldI:
                    oldI = i
                    ii  +=1
                    jj   = -1
                    oldJ = -1
                    kk   = -1
                    oldK = -1
                 if j != oldJ:
                    oldJ = j
                    jj  +=1
                    kk   = -1
                    oldK = -1
                 if k != oldK:
                    oldK = k
                    kk  +=1
   return ii,jj,kk

################################################################################################
#
# read2DnetCDFFile
#
################################################################################################
def read2DnetCDFFile(modelFile,latVariable,lonVariable,variable,LL,UR,inc,setDepth=None):
   """
   read in a 2-D netCDF file

   Parameters
   ----------
   modelFile: str
      model file
   latVar: str
      latitude variable
   lonVar: str
      longitude variable
   var: str
      variable to plot  
   LL: list
      lower-left coordinate
   UR: list
      upper-right coordinate
   inc: int
      grid sampling interval
   depth: float
       depth to plot var at. If None, use var also as depth

    Returns
    -------
    X: float
       x-coordinate  normalized to the radius of Earh
    Y: float
       y-coordinate  normalized to the radius of Earh
    Z: float
       z-coordinate  normalized to the radius of Earh
    meta: dict
       file metadata information
   """
   #
   # model data
   # NetCDF files, when opened read-only, return arrays that refer directly to memory-mapped data on disk:
   #
   import numpy as np
   from scipy.io import netcdf
   emcdata     = netcdf.netcdf_file(modelFile, 'r')
   variables   = []
   for name in emcdata.variables.keys():
       if name not in (lonVariable,latVariable):
          variables.append(name)

   #
   # I assume all variables are defined with uniform order of latitude and longitude
   #
   var = variables[0]
   for i in range(len(emcdata.variables[var].dimensions)):
      if emcdata.variables[var].dimensions[i] == lonVariable:
         lonIndex = i
      else:
         latIndex = i

   lat         = emcdata.variables[latVariable][:].copy()
   lon         = emcdata.variables[lonVariable][:].copy()
   for i in range(len(lon)):
      if lon[i]> 180.0: lon[i] -= 360.0;

   depth       = [0,1]

   #
   # select the values within the ranges (this is to get a count only)
   #
   depth2    = []
   latitude  = []
   longitude = []
   depth2    = []
   lastI     = -1
   for i in range(len(lon)):
      if i != 0 and i != len(lon)-1 and i != lastI+inc:
             continue
      lastI = i 
      for j in range(len(depth)):
         lastK = -1
         for k in range(len(lat)):
            if k != 0 and k != len(lat)-1 and k != lastK+inc:
                  continue
            lastK = k
            if utils.isValueIn(lat[k],LL[0],UR[0]) and utils.isLongitudeIn(lon[i],LL[1],UR[1]):
              if lon[i] not in longitude:
                 longitude.append(lon[i])
              if depth[j] not in depth2:
                 depth2.append(depth[j])
              if lat[k] not in latitude:
                 latitude.append(lat[k])

   #
   # model data grid definition
   #
   V  = {}
   nx = len(longitude)
   ny = len(depth2)
   nz = len(latitude)
   index     = [-1,-1,-1]
   meta      = {'depth':[],'lat':[100,-100],'lon':[400,-400],'source':modelFile}
   for l in range(len(variables)):
      X      = np.zeros((nx, ny, nz))
      Y      = np.zeros((nx, ny, nz))
      Z      = np.zeros((nx, ny, nz))
      v      = np.zeros((nx, ny, nz))
      var    = variables[l]
      emcin  = emcdata.variables[var][:].copy()
      latitude  = []
      longitude = []
      depth2    = []
      ii     = -1
      jj     = -1
      kk     = -1
      oldI   = -1
      oldJ   = -1
      oldK   = -1
      lastI  = -1
      for i in range(len(lon)):
         if i != 0 and i != len(lon)-1 and i != lastI+inc:
             continue
         lastI = i  
         for j in range(len(depth)):
            lastK = -1
            for k in range(len(lat)):
              if k != 0 and k != len(lat)-1 and k != lastK+inc:
                  continue
              lastK = k
              if utils.isValueIn(lat[k],LL[0],UR[0]) and utils.isLongitudeIn(lon[i],LL[1],UR[1]):
                 if i != oldI:
                    meta['lon'] = [min(meta['lon'][0],lon[i]),max(meta['lon'][0],lon[i])]
                    oldI = i
                    ii  +=1
                    jj   = -1
                    oldJ = -1
                    kk   = -1
                    oldK = -1
                 if j != oldJ:
                    if depth[j] not in meta['depth']:
                       meta['depth'].append(depth[j])
                    oldJ = j
                    jj  +=1
                    kk   = -1
                    oldK = -1
                 if k != oldK:
                    meta['lat'] = [min(meta['lat'][0],lat[k]),max(meta['lat'][0],lat[k])]
                    oldK = k
                    kk  +=1

                 index[latIndex]   = k
                 index[lonIndex]   = i
                 thisValue = emcin[index[0]][index[1]]
                 if thisValue <= -990 or thisValue > 9999:
                 	thisValue = None
                 if thisValue is None:
                     v[ii,jj,kk] = None
                 else:
                     v[ii,jj,kk] = float(thisValue)
                 if setDepth is None:
                 	if thisValue is None:
                 		thisDepth = 0
                 	else:
                 		thisDepth = float(thisValue)
                 else:
                 		thisDepth = float(thisValue)
                 x,y,z = llz2xyz(lat[k],lon[i],thisDepth)
                 X[ii,jj,kk]=x
                 Y[ii,jj,kk]=y
                 Z[ii,jj,kk]=z

                 

      V[var] = v
   emcdata.close()
   return X,Y,Z,V,meta


################################################################################################
#
# find2DnetCDFExtent
#
################################################################################################
def find2DnetCDFExtent(modelFile,latVar,lonVar,LL,UR,inc=1):
   """
   find the  extent of a 2-D netCDF  as the number of grid points in each direction

   Parameters
   ----------
   modelFile: str
      model file
   LL: list
      lower-left coordinate
   UR: list
      upper-right coordinate
   inc: int
      grid sampling interval

   Returns
   -------
   ii: int
      number of element in the x-direction
   jj: int
      number of element in the y-direction
   kk: int
      number of element in the z-direction
   """
   lonVariable   = lonVar
   latVariable   = latVar

   #
   # select the values within the ranges (this is to get a count only)
   #
   import numpy as np
   from scipy.io import netcdf
   twoDnetCDFdata     = netcdf.netcdf_file(modelFile, 'r')
   lat      = twoDnetCDFdata.variables[latVariable][:].copy()
   lon      = twoDnetCDFdata.variables[lonVariable][:].copy()
   for i in range(len(lon)):
      if lon[i]> 180.0: lon[i] -= 360.0;
   twoDnetCDFdata.close()

   #
   # model data grid definition
   #
   for l in range(1):
      ii     = 0
      jj     = 1
      kk     = 0
      oldI   = -1
      oldJ   = -1
      oldK   = -1
      lastI  = -1
      lastK  = -1
      for i in range(len(lon)):
            if i != 0 and i != len(lon)-1 and i != lastI+inc:
               continue
            lastI = i
            for k in range(len(lat)):
                if k != 0 and k != len(lat)-1 and k != lastK+inc:
                     continue
                lastK = k
                if utils.isValueIn(lat[k],LL[0],UR[0]) and utils.isLongitudeIn(lon[i],LL[1],UR[1]):
                 if i != oldI:
                    oldI = i
                    ii  +=1
                    oldJ = -1
                    kk   = -1
                    oldK = -1
                 if k != oldK:
                    oldK = k
                    kk  +=1
   return ii,jj,kk

################################################################################################
#
# readTopoFile
#
################################################################################################
def readTopoFile(modelFile,LL,UR,inc):
   """
   read in etopo5, a 2-D netCDF topo file

   Parameters
   ----------
   modelFile: str
      model file
   LL: list
      lower-left coordinate
   UR: list
      upper-right coordinate
   inc: int
      grid sampling interval

   Returns
   -------
   X: float
      x-coordinate  normalized to the radius of Earh
   Y: float
      y-coordinate  normalized to the radius of Earh
   Z: float
      z-coordinate  normalized to the radius of Earh
   label: str
      file label
   """
   zVariable     = 'elev'
   lonVariable   = 'X'
   latVariable   = 'Y'
   #
   # model data
   #
   import numpy as np
   from scipy.io import netcdf
   topodata     = netcdf.netcdf_file(modelFile, 'r')
   lat      = topodata.variables[latVariable][:].copy()
   lon      = topodata.variables[lonVariable][:].copy()
   for i in range(len(lon)):
      if lon[i]> 180.0: lon[i] -= 360.0;
   elevData    = topodata.variables[zVariable][:].copy()

   topodata.close()

   #
   # select the values within the ranges (this is to get a count only)
   #
   depth2    = [0]
   latitude  = []
   longitude = []

   #
   # the loop is intended to include that last lat and lon regardless of inc
   #
   lastI = -1
   for i in range(len(lon)):
         if i != 0 and i != len(lon)-1 and i != lastI+inc: 
             continue
         lastI = i
         lastK = -1
         for k in range(len(lat)):
             if k != 0 and k != len(lat)-1 and k != lastK+inc: 
                  continue
             lastK = k
             if utils.isValueIn(lat[k],LL[0],UR[0]) and utils.isLongitudeIn(lon[i],LL[1],UR[1]):
                 if lon[i] not in longitude:
                    longitude.append(lon[i])
                 if lat[k] not in latitude:
                    latitude.append(lat[k])
   #
   # model data grid definition
   #
   V  = {}
   nx = len(longitude)
   ny = len(depth2)
   nz = len(latitude)
   index     = [-1,-1,-1]
   label     = topodata.description
   for l in range(1):
      X      = np.zeros((nx, ny, nz))
      Y      = np.zeros((nx, ny, nz))
      Z      = np.zeros((nx, ny, nz))
      v      = np.zeros((nx, ny, nz))
      latitude  = []
      longitude = []
      depth2    = []
      ii     = -1
      jj     = -1
      kk     = -1
      oldI   = -1
      oldJ   = -1
      oldK   = -1
      lastI = -1
      for i in range(len(lon)):
          if i != 0 and i != len(lon)-1 and i != lastI+inc:
             continue
          lastI = i
          for j in range(1):
            lastK = -1
            for k in range(len(lat)):
                if k != 0 and k != len(lat)-1 and k != lastK+inc:
                   continue
                lastK = k
                if utils.isValueIn(lat[k],LL[0],UR[0]) and utils.isLongitudeIn(lon[i],LL[1],UR[1]):
                 if i != oldI:
                    oldI = i
                    ii  +=1
                    oldJ = -1
                    kk   = -1
                    oldK = -1
                 if k != oldK:
                    oldK = k
                    kk  +=1
                 x,y,z = llz2xyz(lat[k],lon[i],elevData[k][i]*depthFactor/1000.0)
                 X[ii,j,kk]=x
                 Y[ii,j,kk]=y
                 Z[ii,j,kk]=z

                 v[ii,j,kk] = elevData[k][i]

      V[zVariable] = v
   return X,Y,Z,V,label

################################################################################################
#
# findEmcModelExtent 
#
################################################################################################
def findTopoExtent(modelFile,LL,UR,inc):
   """
   find the  extent of a 2-D top model file in netCDF format as the number of grid points in 
   each direction

   Parameters
   ----------
   modelFile: str
      model file
   LL: list
      lower-left coordinate
   UR: list
      upper-right coordinate
   inc: int
      grid sampling interval

   Returns
   -------
   ii: int
      number of element in the x-direction
   jj: int
      number of element in the y-direction
   kk: int
      number of element in the z-direction
   """
   depthVariable = 'elev'
   lonVariable   = 'X'
   latVariable   = 'Y'

   #
   # select the values within the ranges (this is to get a count only)
   #
   import numpy as np
   from scipy.io import netcdf
   topodata     = netcdf.netcdf_file(modelFile, 'r')
   lat      = topodata.variables[latVariable][:].copy()
   lon      = topodata.variables[lonVariable][:].copy()
   for i in range(len(lon)):
      if lon[i]> 180.0: lon[i] -= 360.0;
   depth    = topodata.variables[depthVariable][:].copy()
   topodata.close()

   #
   # model data grid definition
   #
   for l in range(1):
      ii     = 0
      jj     = 1
      kk     = 0
      oldI   = -1
      oldJ   = -1
      oldK   = -1
      lastI  = -1
      lastK  = -1
      for i in range(len(lon)):
            if i != 0 and i != len(lon)-1 and i != lastI+inc:
               continue
            lastI = i
            for k in range(len(lat)):
                if k != 0 and k != len(lat)-1 and k != lastK+inc:
                     continue
                lastK = k
                if utils.isValueIn(lat[k],LL[0],UR[0]) and utils.isLongitudeIn(lon[i],LL[1],UR[1]):
                 if i != oldI:
                    oldI = i
                    ii  +=1
                    oldJ = -1
                    kk   = -1
                    oldK = -1
                 if k != oldK:
                    oldK = k
                    kk  +=1
   return ii,jj,kk

################################################################################################
#
# readSlabFile
#
################################################################################################
def readSlabFile(modelFile,LL,UR,inc=5):
   """
   read in a 2-D netCDF topo file

   Parameters
   ----------
   modelFile: str
      model file
   LL: list
      lower-left coordinate
   UR: list
      upper-right coordinate
   inc: int
      grid sampling interval

   Returns
   -------
   X: float
      x-coordinate  normalized to the radius of Earh
   Y: float
      y-coordinate  normalized to the radius of Earh
   Z: float
      z-coordinate  normalized to the radius of Earh
   label: str
      file label
   """
   zVariable     = 'z'
   lonVariable   = 'x'
   latVariable   = 'y'
   depthFactor   = -1

   #
   # model data
   #
   import numpy as np
   from scipy.io import netcdf
   topodata     = netcdf.netcdf_file(modelFile, 'r')
   lat      = topodata.variables[latVariable][:].copy()
   lon      = topodata.variables[lonVariable][:].copy()
   for i in range(len(lon)):
      if lon[i]> 180.0: lon[i] -= 360.0;
   elevData    = topodata.variables[zVariable][:].copy()

   topodata.close()

   #
   # select the values within the ranges (this is to get a count only)
   #
   depth2    = [0]
   latitude  = []
   longitude = []
   for i in range(0,len(lon),inc):
         for k in range(0,len(lat),inc):
             if utils.isValueIn(lat[k],LL[0],UR[0]) and utils.isLongitudeIn(lon[i],LL[1],UR[1]):
              if lon[i] not in longitude:
                 longitude.append(lon[i])
              if lat[k] not in latitude:
                 latitude.append(lat[k])
   #
   # model data grid definition
   #
   V  = {}
   nx = len(longitude)
   ny = len(depth2)
   nz = len(latitude)
   index     = [-1,-1,-1]
   label     = "%0.1f-%0.1fkm"%(min(depth2),max(depth2))
   for l in range(1):
      X      = np.zeros((nx, ny, nz))
      Y      = np.zeros((nx, ny, nz))
      Z      = np.zeros((nx, ny, nz))
      v      = np.zeros((nx, ny, nz))
      latitude  = []
      longitude = []
      depth2    = []
      ii     = -1
      jj     = -1
      kk     = -1
      oldI   = -1
      oldJ   = -1
      oldK   = -1
      for i in range(0,len(lon),inc):
          for j in range(1):
            for k in range(0,len(lat),inc):
                if utils.isValueIn(lat[k],LL[0],UR[0]) and utils.isLongitudeIn(lon[i],LL[1],UR[1]):
                 if i != oldI:
                    oldI = i
                    ii  +=1
                    oldJ = -1
                    kk   = -1
                    oldK = -1
                 if k != oldK:
                    oldK = k
                    kk  +=1
                 x,y,z = llz2xyz(lat[k],lon[i],elevData[k][i]*depthFactor)
                 X[ii,j,kk]=x
                 Y[ii,j,kk]=y
                 Z[ii,j,kk]=z

                 v[ii,j,kk] = elevData[k][i]

      V[zVariable] = v
   return X,Y,Z,V,label

################################################################################################
#
# getSlabExtent
#
################################################################################################
def getSlabExtent(modelFile,LL,UR,inc=5):
   """
   find the  extent of a 2-D top model file in netCDF format as the number of grid points in each direction

   Parameters
   ----------
   modelFile: str
      model file
   LL: list
      lower-left coordinate
   UR: list
      upper-right coordinate
   inc: int
      grid sampling interval

   Returns
   -------
   ii: int
      number of element in the x-direction
   jj: int
      number of element in the y-direction
   kk: int
      number of element in the z-direction
   """
   depthVariable = 'z'
   lonVariable   = 'x'
   latVariable   = 'y'

   #
   # select the values within the ranges (this is to get a count only)
   #
   import numpy as np
   from scipy.io import netcdf
   topodata     = netcdf.netcdf_file(modelFile, 'r')
   lat      = topodata.variables[latVariable][:].copy()
   lon      = topodata.variables[lonVariable][:].copy()
   for i in range(len(lon)):
      if lon[i]> 180.0: lon[i] -= 360.0;
   depth    = topodata.variables[depthVariable][:].copy()
   topodata.close()

   #
   # model data grid definition
   #
   for l in range(1):
      ii     = 0
      jj     = 1
      kk     = 0
      oldI   = -1
      oldJ   = -1
      oldK   = -1
      for i in range(0,len(lon),inc):
            for k in range(0,len(lat),inc):
                if utils.isValueIn(lat[k],LL[0],UR[0]) and utils.isLongitudeIn(lon[i],LL[1],UR[1]):
                 if i != oldI:
                    oldI = i
                    ii  +=1
                    oldJ = -1
                    kk   = -1
                    oldK = -1
                 if k != oldK:
                    oldK = k
                    kk  +=1
   return ii,jj,kk

