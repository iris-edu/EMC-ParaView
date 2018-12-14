"""
 NAME: IrisEMC_Paraview-Lib.py - EMC ParaView scripts mmain library

       http://ds.iris.edu/ds/products/emc/

 DESCRIPTION: Thefunctions in this library are for support of EMC ParaView Python scripts

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

 HISTORY:
    2018-12-13 Manoch: R.1.2018.347 CSV file is now uses open rU to open for input as a text file with universal
                       newline interpretation. We are now using splitlines() to regardless of line ending
                       Fixed the issue with GeoCSV slab legend that displayed negative depths.
    2018-12-12 Manoch: R.1.2018.346 resolved an issue were for GeoCSV files a factor of zero was included that
                       would mask the slab depth
    2018-12-06 Manoch: R.1.2018.340 R1 release supports OS X, Linux, and Windows
    2018-11-12 Manoch: now find_file checks the OS to make sure .nc files are not requested on Windows platform
    2018-10-17 Manoch: R.1.2018.290 updates for R1
    2018-09-13 Manoch: R.0.2018.256 added support for 3D geoCSV files
    2018-05-09 Manoch: R.0.2018.129 added support for 2D netCDF files
    2018-04-30 Manoch: R.0.2018.120 modified query2file_name to accepth optional url argument
                       and add a simplified version of it to the begining of the file name.
                       This would allow the code to distinguish between files created from
                       two different sites but using the same query
    2018-04-23 Manoch: R.0.2018.113 update lat and lon loops logic to avoid gaps at region
                       boundaries due to selected step (inc)
    2018-03-21 Manoch: R.0.2018.080 release
"""

import sys
import os
from paraview.simple import *
import IrisEMC_Paraview_Param as param
import IrisEMC_Paraview_Utils as utils

# parameters
depthFactor = 1
irisEMC_Files_URL = param.irisEMC_Files_URL
usgsSlab_URL = param.usgsSlab_URL
pathDict = param.pathDict
columnKeys = param.columnKeys
filesDict = param.filesDict

# USGS Slab 1.0
usgsSlab_URL = param.usgsSlab_URL
usgsSlabDict = param.usgsSlabDict
usgsSlabKeys = param.usgsSlabKeys
usgsSlabValues = param.usgsSlabValues
usgsSlabRangeDict = param.usgsSlabRangeDict

# boundaries
boundariesDict = param.boundariesDict
boundaryKeys = param.boundaryKeys
boundaryValues = param.boundaryValues

# topo
topoDict = param.topoDict
topoKeys = param.topoKeys
topoValues = param.topoValues

# areas
areaDict = param.areaDict
areaRangeDict = param.areaRangeDict
areaKeys = param.areaKeys
areaValues = param.areaValues

# earthquake catalogs
earthquakeCatalogDict = param.earthquakeCatalogDict
earthquakeQuery = param.earthquakeQuery
earthquakeKeys = param.earthquakeKeys
earthquakeValues = param.earthquakeValues

# volcano
volcanoLocationsQuery = param.volcanoLocationsQuery
volcanoLocationsKeys = param.volcanoLocationsKeys
volcanoLocationsValues = param.volcanoLocationsValues
volcanoLocationsDict = param.volcanoLocationsDict


def get_points_in_volume(lat, lon, dep, ll, ur, inc, depth_min, depth_max):
    """find points that fall with in a volume

    Keyword arguments:
    lat: latitude list to check
    lon: longitude list to check
    dep: depth list to check
    ll: lower-left coordinate
    ur: upper-right coordinate
    depth_min: minimum depth of volume
    depth_max: maximum depth of volume

    Return values:
    latitude: list of latitudes that are in the volume
    longitude: list of longitude that are in the volume
    depth: list of depths that are in the volume
    """
    latitude = []
    longitude = []
    depth = []
    last_i = -1
    for i, lon_val in enumerate(lon):
        if i != 0 and i != len(lon) - 1 and i != last_i + inc:
            continue
        last_i = i
        for j, depth_val in enumerate(dep):
            last_k = -1
            for k, lat_val in enumerate(lat):
                if k != 0 and k != len(lat) - 1 and k != last_k + inc:
                    continue
                last_k = k
                if utils.isValueIn(lat_val, ll[0], ur[0]) and utils.isLongitudeIn(lon_val, ll[1], ur[1]) and \
                        utils.isValueIn(float(depth_val), depth_min, depth_max):
                    if lon_val not in longitude:
                        longitude.append(lon_val)
                    if depth_val not in depth:
                        depth.append(depth_val)
                    if lat_val not in latitude:
                        latitude.append(lat_val)
    return latitude, longitude, depth


def get_points_in_area(lat, lon, dep, ll, ur, inc):
    """find points that fall with in an area

    Keyword arguments:
    lat: latitude list to check
    lon: longitude list to check
    dep: depth to use
    ll: lower-left coordinate
    ur: upper-right coordinate

    Return values:
    latitude: list of latitudes that are in the area
    longitude: list of longitude that are in the area
    depth: list of depths that are in the volume
    """

    use_dep = dep
    if type(dep) is list:
        use_dep = [dep[0]]
    latitude = []
    longitude = []
    depth = []
    last_i = -1
    for i, lon_val in enumerate(lon):
        if i != 0 and i != len(lon) - 1 and i != last_i + inc:
            continue
        last_i = i
        for j, depth_val in enumerate(use_dep):
            last_k = -1
            for k, lat_val in enumerate(lat):
                if k != 0 and k != len(lat) - 1 and k != last_k + inc:
                    continue
                last_k = k
                if utils.isValueIn(lat_val, ll[0], ur[0]) and utils.isLongitudeIn(lon_val, ll[1], ur[1]):
                    if lon_val not in longitude:
                        longitude.append(lon_val)
                    if depth_val not in depth:
                        depth.append(depth_val)
                    if lat_val not in latitude:
                        latitude.append(lat_val)
    return latitude, longitude, depth


def get_area(area, latitude_begin, latitude_end, longitude_begin, longitude_end):
    """provide latitude, longitude ranges for the area selected. The provided latitude, longitudes,
    if any, will override the corresponding values for the selected area.

    Keyword arguments:
       area: drop down Area index
       latitude_begin: start latitude
       latitude_end: end latitude
       longitude_begin: start longitude
       longitude_end: range longitude

    Return values:
    lat0: start latitude
    lat1: end latitude
    lon0: start longitude
    lon1: end longitude
    """
    lat0, lat1 = areaRangeDict[str(area)]['lat']
    lon0, lon1 = areaRangeDict[str(area)]['lon']

    try:
        lat0 = float(latitude_begin)
    except:
        pass
    try:
        lat1 = float(latitude_end)
    except:
        pass
    try:
        lon0 = float(longitude_begin)
    except:
        pass
    try:
        lon1 = float(longitude_end)
    except:
        pass

    return lat0, lat1, lon0, lon1


def eq_header(url):
    """generate a GeoCSV style header for FDSN style event service output

    Keyword arguments:
       url: event service URL

    Return values:
    header: GeoCSV file header
    """
    header = ("# dataset: GeoCSV 2.0\n"
              "# title: Earthquake catalog\n"
              "# source: " + url + "\n"
              "# delimiter: |\n"
              "# latitude_column: Latitude\n"
              "# longitude_column: Longitude\n"
              "# depth_column: Depth/km\n"
              "# magnitude_column: Magnitude\n"
              "EventID|Time|Latitude|Longitude|Depth/km|Author|Catalog|Contributor|ContributorID"
              "|MagType|Magnitude|MagAuthor|EventLocationName\n")
    return header


def wovo_header(url):
    """generate a GeoCSV style header for the WOVOdata volcano locations

    Keyword arguments:
    url: WOVOdata volcano locationsURL

    Return values:
    header: GeoCSV file header
    """
    header = ("# title: Volcano Locations\n"
              "# source: %s\n"
              "# latitude_column: lat\n"
              "# longitude_column: long\n"
              "# elevation_column: elevation\n") % url
    return header


def is_close(a, b, rel_tol=1e-09, abs_tol=0.0):
    """compare two values to see if they are close (within the given tolerance)

    Keyword arguments:
    a: first value
    b: second value
    rel_tol: relative tolerance
    abs_tol: absolute tolerance

    Return values:
    boolean: a flag  indicating if the two values are close
    """
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def read_geocsv(gfile_name, is_2d=False):
    """read a given GeoCSV file and output a dictionary of the header keys along with a text
    block of the data body

    Keyword arguments:
    gfile_name: the GeoCSV file to read

    Return values:
    params: a dictionary of the key-value pairs found in the header
    data: a text block of the body
    """
    # open the CSV file
    # rU: open for input as a text file with universal newline interpretation
    fp = open(gfile_name, 'ru')
    content = fp.read()
    lines = content.splitlines()
    fp.close()
    params = {}
    data = []
    found_header = False
    for i in range(len(lines)):
        if len(lines[i].strip()) <= 0:
                continue
        elif lines[i].strip()[0] == '#':
            this_line = lines[i].strip()[1:]
            if len(this_line.strip()) <= 0:
                continue
            values = this_line.split(':')
            key = values[0].strip()
            params[key] = this_line.replace(key+':', '').strip()
        else:
            # the first data line is the header
            this_line = lines[i].strip()
            if not found_header:
                params['header'] = this_line.split(params['delimiter'])
                found_header = True
                continue
            data.append(this_line)

    # set the default columns
    if 'latitude_column' not in params.keys():
        params['latitude_column'] = 'latitude'
    if 'longitude_column' not in params.keys():
        params['longitude_column'] = 'longitude'
    if not is_2d:
        if 'elevation_column' not in params.keys():
            params['elevation_column'] = 'elevation'
        if 'depth_column' not in params.keys():
            params['depth_column'] = 'depth'
        
    return params, data


def file_name(full_file_name):
    """for a given full file name, extract and return a file name without extension and path

    Keyword arguments:
    full_file_name: a full file name

    Return values:
    filename: file name without extension and path
    """
    filename_w_ext = os.path.basename(full_file_name)
    filename, file_extension = os.path.splitext(filename_w_ext)
    return filename


def read_info_file(data_file):
    """find an info file for a data file and return the origin information
    if info file not found, return the file name

    Keyword arguments:
    data_file: data file name

    Return values:
    origin: origin information
    """
    info_file = os.path.splitext(data_file)[0] + '.inf'
    origin = file_name(data_file)
    if os.path.isfile(info_file):
            fp = open(info_file, 'r')
            lines = fp.read().splitlines()
            fp.close()
            origin = data_file
            for line in lines:
                if 'source:' in line:
                    origin = line.replace('source:', '')[1:].strip()
                    import urlparse
                    origin = urlparse.urlparse(origin).netloc
                    break
    return origin


def query2filename(query, url=''):
    """convert a query to a potential file name by removing some characters

    Keyword arguments:
    query: the query portion of a URL

    Return values:
    filename: the file name without path
    """
    import urlparse

    if len(url) > 0:
        urlinfo = urlparse.urlparse(url)
        site = urlinfo[1]
        query = '_'.join([site, query])
    filename = query.replace("&", '').replace("=", "").replace(".", '').replace("formattext", "")
    filename = filename.replace("nodata404", "").replace("max", "").replace("min", "")
    filename = filename.replace("-", "") + ".csv"

    return filename


def is_url_valid(url):
    """Checks if a given URL is reachable

    Keyword arguments:
    url: URL to check

    Return values:
    bool: a flag indicating if the  URL is reachable
    """
    import urllib

    conn = urllib.urlopen(url)
    code = conn.getcode()
    if code == 200:
        return True
    else:
        return False


def get_file_from_url(url, path, filename=''):
    """get a file from the given URL and save it locally under a given file name

    Keyword arguments:
    url: URL of the file to retrieve
    path: location where the file should be saved
    filename: name to save the file under (this overrides the default file name)

    Return values:
    bool: indicating if the operation was a success
    destination: full address of the local file
    url: URL where the file came from (se to destination if not retrieved)
    """

    import urllib
    import urlparse
    from datetime import datetime

    try:
        if len(filename.strip()) <= 0:
            url_info = urlparse.urlparse(url)
            filename = url_info[2].strip()
            filename = os.path.basename(filename)
        destination = os.path.join(path, filename)
        urllib.urlretrieve(url, destination)
        if os.path.isfile(destination):
            info_file = os.path.splitext(destination)[0] + '.inf'
            fp = open(info_file, 'w')
            fp.write('# date: %s\n' % str(datetime.now()))
            fp.write('# file: %s\n' % destination)
            fp.write('# source: %s\n' % url)
            fp.close()
            return True, destination, url
    except:
        pass
    url = destination
    return False, destination, url


def find_file(address, loc, query='', ext=None):
    """find a file either locally or via a URL

    Keyword arguments:
    address: file address, path, url, etc.
    loc: location of the file
    query: URL query string

    Return values:
    found: indicating if the operation was a success
    address: full address of the local file
    source: where the file came from
    """
    import urllib

    found = False

    # for default files, the calling script sends the proper extension to use depending on the OS support
    if ext is not None:
        address = ''.join([address, ext])

    if address.lower().endswith('.nc') and not utils.support_nc():
        print "[ERROR] Cannot read netCDF files on this platform, try GeoCSV format!"
        return False, address, address
    elif address.lower().endswith('.nc'):
        from scipy.io import netcdf

    # it is a full path to a file?
    source = address
    if os.path.isfile(address):
        origin = read_info_file(source)
        return True, address, origin

    # it is a file under the data directory?
    elif os.path.isfile(os.path.join(loc, address)):
        source = os.path.join(loc, address)
        origin = read_info_file(source)
        return True, source, origin

    # Other possibilities, URL?
    else:
        # check the DMC URL
        if loc in (pathDict['EMC_BOUNDARIES_PATH'], pathDict['EMC_MODELS_PATH']):
            source = irisEMC_Files_URL + address
            if is_url_valid(source):
                found, destination, origin = get_file_from_url(source, loc, filename=os.path.join(loc, address))

        # USGS Slab 1.0
        elif loc == pathDict['EMC_SLABS_PATH']:
            source = usgsSlab_URL + address
            if is_url_valid(source):
                found, destination, origin = get_file_from_url(source, loc, filename=os.path.join(loc, address))

        # earthquakes
        elif loc == pathDict['EMC_EARTHQUAKES_PATH']:
            source = query
            if is_url_valid(source):
                found, destination, origin = get_file_from_url(source, loc, filename=os.path.join(loc, address))
                if found:
                    fp = open(destination, 'r+')
                    catalog = fp.read()
                    fp.seek(0, 0)
                    fp.write(eq_header(source))
                    fp.write(catalog)
                    fp.close()

        # Volcano locations
        elif loc == pathDict['EMC_VOLCANOES_PATH']:
            source = query
            if is_url_valid(source):
                found, destination, origin = get_file_from_url(source, loc, filename=os.path.join(loc, address))
                if found:
                    fp = open(destination, 'r+')
                    catalog = fp.read()
                    lines = catalog.splitlines()
                    fp.seek(0, 0)
                    fp.write("%s\n%s" % (lines[0], wovo_header(source)))
                    for line in lines[1:]:
                        fp.write("%s\n" % line)
                    fp.close()

        # did we find the file?
        if found:
            return found, destination, origin

        # did user provide a URL
        else:
            found, destination, origin = get_file_from_url(address, loc, query)
            return found, destination, origin


def llz2xyz(lat, lon, depth):
    """ convert latitude, longitude, and altitude to earth-centered, earth-fixed (ECEF) cartesian
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

    Keyword arguments:
    lat: latitude (deg)
    lon: longitude (deg)
    depth: depth (km)

    Return values:
    x: x-coordinate  normalized to the radius of Earh
    y: y-coordinate  normalized to the radius of Earh
    z: z-coordinate  normalized to the radius of Earh
    """
    import numpy as np

    alt = -1.0 * 1000.0 * depth  # height above WGS84 ellipsoid (m)
    lat = np.deg2rad(lat)
    cos_lat = np.cos(lat)
    sin_lat = np.sin(lat)

    # World Geodetic System 1984, WGS 84
    erad = np.float64(6378137.0)  # Radius of the Earth in meters (equatorial radius, WGS84)
    rad = 1  # sphere radius
    e = np.float64(8.1819190842622e-2)
    n = erad / np.sqrt(1.0 - e * e * sin_lat * sin_lat)  # prime vertical radius of curvature

    lon = np.deg2rad(lon)
    cos_lon = np.cos(lon)
    sin_lon = np.sin(lon)

    x = (n + alt) * cos_lat * cos_lon  # meters
    y = (n + alt) * cos_lat * sin_lon  # meters
    z = ((1 - e * e) * n + alt) * sin_lat  # meters

    x = x * rad / erad  # normalize to radius of rad
    y = y * rad / erad  # normalize to radius of rad
    z = z * rad / erad  # normalize to radius of rad
    return x, y, z


def xyz2llz(x, y, z):
    """convert earth-centered, earth-fixed (ECEF) cartesian x, y, z to latitude, longitude, and altitude

    code is based on:

    https://www.mathworks.com/matlabcentral/fileexchange/7941-convert-cartesian--ecef--coordinates-to-lat--lon--alt?
                 focused=5062924&tab=function

     Keyword arguments:
     x: x-coordinate  normalized to the radius of Earh
     y: y-coordinate  normalized to the radius of Earh
     z: z-coordinate  normalized to the radius of Earh

     Return values:
     lat: latitude (deg)
     lon: longitude (deg)
     depth: depth (km)
    """
    import numpy as np
    import math

    # World Geodetic System 1984, WGS 84
    erad = np.float64(6378137.0)  # Radius of the Earth in meters (equatorial radius, WGS84)
    rad = 1  # sphere radius
    e = np.float64(8.1819190842622e-2)

    # convert to radius
    x = x * erad / rad
    y = y * erad / rad
    z = z * erad / rad

    b = np.sqrt(erad * erad * (1 - e * e))
    ep = np.sqrt((erad * erad - b * b) / (b * b))
    p = np.sqrt(x * x + y * y)
    th = np.arctan2(erad * z, b * p)
    lon = np.arctan2(y, x)
    lat = np.arctan2((z + ep * ep * b * np.sin(th) * np.sin(th) * np.sin(th)),
                     (p - e * e * erad * np.cos(th) * np.cos(th) * np.cos(th)))
    N = erad / np.sqrt(1.0 - e * e * np.sin(lat) * np.sin(lat))
    alt = p / np.cos(lat) - N

    lon = lon % (math.pi * 2.0)
    lon = utils.lon_180(lon)
    lat = np.rad2deg(lat)
    alt = -1 * alt / 1000.0  # depth as negative alt

    return lat, lon, alt


def get_column(matrix, column_index):
    """Read in a matrix and return a selected column.

    Keyword arguments:
    matrix: the matrix to process
    column_index: index of the column to extract

    Return values:
    list of values in column_index of matrix
     """
    return [row[column_index] for row in matrix]


def read_geocsv_model_3d(model_file, ll, ur, depth_min, depth_max, roughness, inc, extent=False):
    """Read in a 3-D Earth model in the GeoCSV format.

      Keyword arguments:
      model_file: model file
      ll: lower-left coordinate
      ur: upper-right coordinate
      depth_min: minimum depth
      depth_max: maximum depth
      inc: grid sampling interval
      extent: provide model extent only (True or False)

      Return values:
      x: x-coordinate  normalized to the radius of the Earth
      y: y-coordinate  normalized to the radius of the Earth
      z: z-coordinate  normalized to the radius of the Earth
      meta: file metadata information
     """

    # model data and metadata
    import numpy as np
    from operator import itemgetter

    (params, lines) = read_geocsv(model_file)

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

    lat = np.array(list(set(get_column(data, lat_index))), dtype=float)
    lon = np.array(list(set(get_column(data, lon_index))), dtype=float)

    # -180/180 models are the norm, so we convert 0/360 models to -180/180 first to unify
    # the rest of the code for all models
    data = np.ndarray.tolist(np.asfarray(data))
    if utils.lon_is_360(lon):
        for i, values in enumerate(data):
            if float(values[lon_index]) > 180.0:
                data[i][lon_index] = float(values[lon_index]) - 360.0
        lon = np.array(list(set(get_column(data, lon_index))), dtype=float)

    # we want the grid to be in x, y z order (longitude, depth, latitude)
    data.sort(key=itemgetter(lon_index, depth_index, lat_index))

    lon.sort()
    lon, lon_map = utils.lon_180(lon, fix_gap=True)
    depth = np.array(list(set(get_column(data, depth_index))), dtype=float)

    # get coordinates sorted one last time
    lat.sort()
    lon.sort()
    depth.sort()

    # select the coordinates within the ranges (this is to get a count only)
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

                if utils.isValueIn(float(lat_val), ll[0], ur[0]) and utils.isLongitudeIn(
                        float(lon_val), ll[1], ur[1]) and \
                        utils.isValueIn(float(depth_val), depth_min, depth_max):
                    if float(lon_map[utils.float_key(lon_val)]) not in longitude:
                        longitude.append(float(lon_map[utils.float_key(lon_val)]))
                    if float(depth_val) not in depth2:
                        depth2.append(float(depth_val))
                    if float(lat_val) not in latitude:
                        latitude.append(float(lat_val))

    # model data grid definition
    V = {}
    nx = len(longitude)
    ny = len(depth2)
    nz = len(latitude)
    if extent:
        return nx - 1, ny - 1, nz - 1

    meta = {'depth': [], 'lat': [100, -100], 'lon': [400, -400], 'source': model_file}

    X = np.zeros((nx, ny, nz))
    Y = np.zeros((nx, ny, nz))
    Z = np.zeros((nx, ny, nz))

    for i, values in enumerate(data):
        lon_val = float(lon_map[utils.float_key(values[lon_index])])
        lat_val = float(values[lat_index])
        depth_val = float(values[depth_index])

        if lon_val in longitude and lat_val in latitude and depth_val in depth2:
            meta['lon'] = [min(meta['lon'][0], lon_val),
                           max(meta['lon'][0], lon_val)]
            meta['lat'] = [min(meta['lat'][0], lat_val), max(meta['lat'][0], lat_val)]
            if depth_val not in meta['depth']:
                meta['depth'].append(depth_val)
            x, y, z = llz2xyz(lat_val, lon_val, depth_val * roughness)

            ii = longitude.index(lon_val)
            jj = depth2.index(depth_val)
            kk = latitude.index(lat_val)
            X[ii, jj, kk] = x
            Y[ii, jj, kk] = y
            Z[ii, jj, kk] = z

            for l, var_val in enumerate(variables):
                if var_val not in V.keys():
                    V[var_val] = np.zeros((nx, ny, nz))
                V[var_val][ii, jj, kk] = float(values[var_index[var_val]])

    return X, Y, Z, V, meta


def read_netcdf_model(model_file, lat_variable, lon_variable, depth_variable, ll, ur, depth_min, depth_max,
                      roughness, inc, extent=False):
    """read in an EMC Earth model in the netCDF format

      Keyword arguments:
      model_file: model file
      ll: lower-left coordinate
      ur: upper-right coordinate
      depth_min: minimum depth
      depth_max: maximum depth
      inc: grid sampling interval

      Return values:
      x: x-coordinate  normalized to the radius of the Earth
      y: y-coordinate  normalized to the radius of the Earth
      z: z-coordinate  normalized to the radius of the Earth
      meta: file metadata information
    """

    import numpy as np
    # ParaView on some platforms does not have SciPy module
    if not utils.support_nc():
        print "[ERROR] Cannot read netCDF files on this platform, try GeoCSV format!"
        return [], [], [], [], {}
    elif model_file.lower().endswith('.nc'):
        from scipy.io import netcdf

    # NetCDF files, when opened read-only, return arrays that refer directly to memory-mapped data on disk:
    data = netcdf.netcdf_file(model_file, 'r')
    variables = []
    for name in data.variables.keys():
        if name not in (depth_variable, lon_variable, lat_variable):
            variables.append(name)

    # expects variables be a function of latitude, longitude and depth, find the order
    var = variables[0]
    for i, value in enumerate(data.variables[var].dimensions):
        if value == depth_variable:
            depth_index = i
        elif value == lon_variable:
            lon_index = i
        else:
            lat_index = i

    lat = data.variables[lat_variable][:].copy()
    lon = data.variables[lon_variable][:].copy()
    lon, lon_map = utils.lon_180(lon, fix_gap=True)

    depth = data.variables[depth_variable][:].copy()

    # select the values within the ranges (this is to get a count only)
    latitude, longitude, depth2 = get_points_in_volume(lat, lon, depth, ll, ur, inc, depth_min, depth_max)

    # model data grid definition
    V = {}
    nx = len(longitude)
    ny = len(depth2)
    nz = len(latitude)
    if extent:
        return nx - 1, ny - 1, nz - 1
    index = [-1, -1, -1]
    meta = {'depth': [], 'lat': [100, -100], 'lon': [400, -400], 'source': model_file}
    for l, var_val in enumerate(variables):
        X = np.zeros((nx, ny, nz))
        Y = np.zeros((nx, ny, nz))
        Z = np.zeros((nx, ny, nz))
        v = np.zeros((nx, ny, nz))
        data_in = data.variables[var_val][:].copy()

        # increment longitudes, we want to keep the first and last longitude regardless of inc
        for i, lon_val in enumerate(lon):
            for j, depth_val in enumerate(depth):
                for k, lat_val in enumerate(lat):
                    if lon_val in longitude and lat_val in latitude and depth_val in depth2:
                        meta['lon'] = [min(meta['lon'][0], lon_val), max(meta['lon'][0], lon_val)]
                        meta['lat'] = [min(meta['lat'][0], lat_val), max(meta['lat'][0], lat_val)]
                        if depth_val not in meta['depth']:
                            meta['depth'].append(depth_val)
                        x, y, z = llz2xyz(lat_val, lon_val, depth_val * roughness)
                        ii = longitude.index(lon_val)
                        jj = depth2.index(depth_val)
                        kk = latitude.index(lat_val)

                        X[ii, jj, kk] = x
                        Y[ii, jj, kk] = y
                        Z[ii, jj, kk] = z

                        index[depth_index] = j
                        index[lat_index] = k
                        index[lon_index] = i

                        v[ii, jj, kk] = data_in[index[0]][index[1]][index[2]]

        V[var_val] = v
    data.close()
    return X, Y, Z, V, meta


def read_geocsv_model_2d(model_file, ll, ur, inc, roughness, unit_factor=1, base=0, extent=False):
    """Read in a 3-D Earth model in the GeoCSV format.

      Keyword arguments:
      model_file: model file
      ll: lower-left coordinate
      ur: upper-right coordinate
      inc: grid sampling interval
      roughness: set the variable as depth and use this for exaggeration
      extent: should only compute model extent? (True or False)

      Return values:
      x: x-coordinate  normalized to the radius of the Earth
      y: y-coordinate  normalized to the radius of the Earth
      z: z-coordinate  normalized to the radius of the Earth
      meta: file metadata information
     """

    # model data and metadata
    import numpy as np
    from operator import itemgetter

    (params, lines) = read_geocsv(model_file, is_2d=True)

    # model data
    raw_data = []
    for line in lines:
        raw_data.append(line.split(params['delimiter']))
    data = [list(utils.str2float(sublist)) for sublist in raw_data]

    # model variables
    variables = []
    for this_param in params.keys():
        if params[this_param] not in (params['longitude_column'], params['latitude_column']
                                      ) and '_column' in this_param:
            variables.append(params[this_param])

    # index to the variables
    var_index = {}
    for i, val in enumerate(params['header']):
        if val == params['longitude_column']:
            lon_index = i
        elif val == params['latitude_column']:
            lat_index = i
        else:
            for this_var in variables:
                if val == params[this_var + '_column']:
                    var_index[this_var] = i
                    break

    lat = list(set(get_column(data, lat_index)))
    lon = list(set(get_column(data, lon_index)))
    lon.sort(key=float)
    lon, lon_map = utils.lon_180(lon, fix_gap=True)
    depth = [base]

    # get coordinates sorted otherwise inc will not function properly
    lat.sort(key=float)
    lon.sort(key=float)

    # select the values within the ranges (this is to get a count only)
    latitude, longitude, depth2 = get_points_in_area(lat, lon, depth, ll, ur, inc)

    # model data grid definition
    V = {}
    nx = len(longitude)
    ny = len(depth2)
    nz = len(latitude)
    if extent:
        return nx - 1, ny - 1, nz - 1

    meta = {'depth': [], 'lat': [100, -100], 'lon': [400, -400], 'source': model_file}

    for l, var_val in enumerate(variables):
        X = np.zeros((nx, ny, nz))
        Y = np.zeros((nx, ny, nz))
        Z = np.zeros((nx, ny, nz))

        # we want the grid to be in x, y z order (longitude, depth, latitude)
        data.sort(key=itemgetter(lat_index, lon_index))
        for i, values in enumerate(data):
            lon_val = float(lon_map[utils.float_key(values[lon_index])])
            lat_val = float(values[lat_index])
            this_value = float(values[var_index[var_val]])
            if this_value is None:
                depth_val = base
            else:
                depth_val = base + float(this_value) * float(roughness) * float(unit_factor)

            if lon_val in longitude and lat_val in latitude:
                meta['lon'] = [min(meta['lon'][0], lon_val), max(meta['lon'][0], lon_val)]
                meta['lat'] = [min(meta['lat'][0], lat_val), max(meta['lat'][0], lat_val)]
                if depth_val not in meta['depth']:
                    meta['depth'].append(depth_val)
                x, y, z = llz2xyz(lat_val, lon_val, depth_val)

                ii = longitude.index(lon_val)
                jj = 0
                kk = latitude.index(lat_val)
                X[ii, jj, kk] = x
                Y[ii, jj, kk] = y
                Z[ii, jj, kk] = z

                if var_val not in V.keys():
                    V[var_val] = np.zeros((nx, ny, nz))
                # V[var_val][ii, jj, kk] = float(this_value) * float(unit_factor)
                V[var_val][ii, jj, kk] = float(this_value)

    return X, Y, Z, V, meta


def read_2d_netcdf_file(model_file, lat_variable, lon_variable, variable, ll, ur, inc, roughness, base=0,
                        extent=False):
    """read in an EMC 2D in the netCDF format

      Keyword arguments:
      model_file: model file
      ll: lower-left coordinate
      ur: upper-right coordinate
      depth_min: minimum depth
      depth_max: maximum depth
      inc: grid sampling interval
      roughness: set the variable as depth and use this for exaggeration
      extent: should only compute model extent? (True or False)

      Return values:
      x: x-coordinate  normalized to the radius of the Earth
      y: y-coordinate  normalized to the radius of the Earth
      z: z-coordinate  normalized to the radius of the Earth
      meta: file metadata information
    """

    import numpy as np

    # ParaView on some platforms does not have SciPy module
    if not utils.support_nc:
        print "[ERROR] Cannot read netCDF files on this platform, try GeoCSV format!"
        return [], [], [], [], {}
    elif model_file.lower().endswith('.nc'):
        from scipy.io import netcdf

    # NetCDF files, when opened read-only, return arrays that refer directly to memory-mapped data on disk:
    data = netcdf.netcdf_file(model_file, 'r')
    variables = []
    for name in data.variables.keys():
        if name not in (lon_variable, lat_variable):
            variables.append(name)

    # expects variables be a function of latitude, longitude and depth, find the order
    var = variables[0]
    for i, value in enumerate(data.variables[var].dimensions):
        if value == lon_variable:
            lon_index = i
        else:
            lat_index = i
    lat = data.variables[lat_variable][:].copy()
    lon = data.variables[lon_variable][:].copy()
    lon, lon_map = utils.lon_180(lon, fix_gap=True)

    depth = [base]

    # select the values within the ranges (this is to get a count only)
    latitude, longitude, depth2 = get_points_in_area(lat, lon, depth, ll, ur, inc)

    # model data grid definition
    V = {}
    nx = len(longitude)
    ny = len(depth2)
    nz = len(latitude)
    if extent:
        return nx - 1, ny - 1, nz - 1

    index = [-1, -1, -1]
    meta = {'depth': [], 'lat': [100, -100], 'lon': [400, -400], 'source': model_file}
    for l, var_val in enumerate(variables):
        missing_value = None
        if hasattr(data.variables[var], 'missing_value'):
            missing_value = float(data.variables[var].missing_value)

        X = np.zeros((nx, ny, nz))
        Y = np.zeros((nx, ny, nz))
        Z = np.zeros((nx, ny, nz))
        v = np.zeros((nx, ny, nz))
        data_in = data.variables[var_val][:].copy()

        # increment longitudes, we want to keep the first and last longitude regardless of inc
        for i, lon_val in enumerate(lon):
            for j, depth_val in enumerate(depth):
                for k, lat_val in enumerate(lat):
                    if lon_val in longitude and lat_val in latitude:
                        meta['lon'] = [min(meta['lon'][0], lon_val), max(meta['lon'][0], lon_val)]
                        meta['lat'] = [min(meta['lat'][0], lat_val), max(meta['lat'][0], lat_val)]
                        if depth_val not in meta['depth']:
                            meta['depth'].append(depth_val)

                        index[lat_index] = k
                        index[lon_index] = i

                        ii = longitude.index(lon_val)
                        jj = j
                        kk = latitude.index(lat_val)

                        this_value = data_in[index[0]][index[1]]

                        if this_value is None:
                            v[ii, jj, kk] = None
                        elif this_value is not None:
                            if this_value == missing_value:
                                v[ii, jj, kk] = None
                                this_value = None
                            else:
                                v[ii, jj, kk] = this_value
                        else:
                            v[ii, jj, kk] = this_value

                        if this_value is None:
                            depth_val = base + 0
                        else:
                            depth_val = base + float(this_value) * float(roughness)
                        x, y, z = llz2xyz(lat_val, lon_val, depth_val)

                        X[ii, jj, kk] = x
                        Y[ii, jj, kk] = y
                        Z[ii, jj, kk] = z
        V[var_val] = v
    data.close()
    return X, Y, Z, V, meta


def read_netcdf_topo_file(model_file, ll, ur, inc, roughness, lon_var='longitude', lat_var='latitude',
                          elev_var='elevation', base=0, unit_factor=1, extent=False):
    """read in etopo, a 2-D netCDF topo file

    Keyword arguments:
    model_file: model file
    ll: lower-left coordinate
    ur: upper-right coordinate
    inc: grid sampling interval
    roughness: set the variable as depth and use this for exaggeration
    extent: should only compute model extent? (True or False)

    RReturn values:
    X: x-coordinate  normalized to the radius of Earh
    Y: y-coordinate  normalized to the radius of Earh
    Z: z-coordinate  normalized to the radius of Earh
    label: file label
    """

    import numpy as np
    # ParaView on some platforms does not have SciPy module

    if not utils.support_nc():
        print "[ERROR] Sorry, cannot read netCDF files on this platform!"
        return 0, 0, 0
    elif model_file.lower().endswith('.nc'):
        from scipy.io import netcdf

    z_variable = elev_var
    lon_variable = lon_var
    lat_variable = lat_var
    depth = base
    # model data
    data = netcdf.netcdf_file(model_file, 'r')
    lat = data.variables[lat_variable][:].copy()
    lon = data.variables[lon_variable][:].copy()
    lon = utils.lon_180(lon)
    elevation_data = data.variables[z_variable][:].copy()

    data.close()
    dep = [depth]
    variables = [z_variable]

    # select the values within the ranges (this is to get a count only)
    latitude, longitude, depth2 = get_points_in_area(lat, lon, dep, ll, ur, inc)

    # model data grid definition
    V = {}
    nx = len(longitude)
    ny = len(depth2)
    nz = len(latitude)

    if extent:
        return nx - 1, ny - 1, nz - 1

    label = ''
    if hasattr(data, 'description'):
        label = data.description
    elif hasattr(data, 'title'):
        label = data.title

    for l, var_value in enumerate(variables):
        X = np.zeros((nx, ny, nz))
        Y = np.zeros((nx, ny, nz))
        Z = np.zeros((nx, ny, nz))
        v = np.zeros((nx, ny, nz))

        for i, lon_val in enumerate(lon):
            for j, depth_val in enumerate(dep):
                for k, lat_val in enumerate(lat):
                    if lon_val in longitude and lat_val in latitude and depth_val in depth2:

                        ii = longitude.index(lon_val)
                        jj = depth2.index(depth_val)
                        kk = latitude.index(lat_val)
                        # "+" since it is elevation but we already making roughness negative to make it positive up
                        x, y, z = llz2xyz(lat_val, lon_val, depth_val + (
                                elevation_data[k][i] * roughness * unit_factor))
                        X[ii, jj, kk] = x
                        Y[ii, jj, kk] = y
                        Z[ii, jj, kk] = z

                        v[ii, jj, kk] = elevation_data[k][i] * float(unit_factor)

    V[z_variable] = v
    return X, Y, Z, V, label


def read_slab_file(model_file, ll, ur, inc=1, depth_factor=-1, extent=False):
    """read in a 2-D netCDF Slab file

    Keyword arguments:
    model_file: model file
    ll: lower-left coordinate
    ur: upper-right coordinate
    inc: grid sampling interval

    RReturn values:
    X: x-coordinate  normalized to the radius of Earh
    Y: y-coordinate  normalized to the radius of Earh
    Z: z-coordinate  normalized to the radius of Earh
    label: file label
    """

    import numpy as np
    # ParaView on some systems does not have SciPy module
    if not utils.support_nc():
        print "[ERROR] Cannot read netCDF files on this platform, try GeoCSV format!"
        return [], [], [], [], ''
    elif model_file.lower().endswith('.nc') or model_file.lower().endswith('.grd'):
        from scipy.io import netcdf

    z_variable = 'z'
    lon_variable = 'x'
    lat_variable = 'y'
    depth = 0

    # model data
    data = netcdf.netcdf_file(model_file, 'r')
    lat = data.variables[lat_variable][:].copy()
    lon = data.variables[lon_variable][:].copy()
    lon = utils.lon_180(lon)
    elevation_data = data.variables[z_variable][:].copy()

    data.close()
    dep = [depth]
    variables = [z_variable]

    # select the values within the ranges (this is to get a count only)
    latitude, longitude, depth2 = get_points_in_area(lat, lon, dep, ll, ur, inc)

    # model data grid definition
    V = {}
    nx = len(longitude)
    ny = len(depth2)
    nz = len(latitude)

    if extent:
        return nx - 1, ny - 1, nz - 1

    label = ''
    if len(depth2):
        label = "%0.1f-%0.1fkm" % (min(depth2), max(depth2))

    for l, var_value in enumerate(variables):
        X = np.zeros((nx, ny, nz))
        Y = np.zeros((nx, ny, nz))
        Z = np.zeros((nx, ny, nz))
        v = np.zeros((nx, ny, nz))

        for i, lon_val in enumerate(lon):
            for j, depth_val in enumerate(dep):
                for k, lat_val in enumerate(lat):
                    if lon_val in longitude and lat_val in latitude and depth_val in depth2:
                        ii = longitude.index(lon_val)
                        jj = depth2.index(depth_val)
                        kk = latitude.index(lat_val)
                        x, y, z = llz2xyz(lat[k], lon[i], elevation_data[k][i] * depth_factor)
                        X[ii, jj, kk] = x
                        Y[ii, jj, kk] = y
                        Z[ii, jj, kk] = z

                        v[ii, jj, kk] = elevation_data[k][i]

    V[z_variable] = v
    return X, Y, Z, V, label


