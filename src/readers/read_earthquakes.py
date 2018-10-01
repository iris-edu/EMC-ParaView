Name = 'ReadEarthquakes'
Label = 'Show Earthquake Locations'
FilterCategory = 'IRIS EMC'
Help = 'Get and display earthquake locations from USGS.'

ExtraXml = '''\
<IntVectorProperty
    name="Data_Source"
    command="SetParameter"
    number_of_elements="1"
    initial_string="drop_down_menu"
    default_values="0">
    <EnumerationDomain name="enum">
          EARTHQUAKE_DROP_DOWN
    </EnumerationDomain>
    <Documentation>
        Choose earthquake catalogue service
    </Documentation>
</IntVectorProperty>
<IntVectorProperty
    name="Area"
    command="SetParameter"
    number_of_elements="1"
    initial_string="area_drop_down_menu"
    default_values="1">
    <EnumerationDomain name="enum">
          AREA_DROP_DOWN
    </EnumerationDomain>
    <Documentation>
        Choose the area to draw in.
    </Documentation>
</IntVectorProperty>
'''

NumberOfInputs = 0
OutputDataType = 'vtkPolyData'

Properties = dict(
    Area=1,
    Data_Source=0,
    Alternate_FileName="",
    Latitude_Begin='',
    Latitude_End='',
    Longitude_Begin='',
    Longitude_End='',
    Depth_Begin=0,
    Depth_End=200,
    Magnitude_Begin=6,
    Magnitude_End=10,
    Start_Time='2000-01-01',
    Max_Count=200
)

def RequestData():
    # R.0.2018.120
    import sys
    sys.path.insert(0, "EMC_SRC_PATH")
    import paraview.simple as simple
    import numpy as np
    import csv
    import os
    from vtk.util import numpy_support as nps
    import IrisEMC_Paraview_Lib as lib
    import urlparse

    Label = ''

    pts = vtk.vtkPoints()
    Latitude_Begin, Latitude_End, Longitude_Begin, Longitude_End = lib.get_area(Area, Latitude_Begin, Latitude_End,
                                                                                Longitude_Begin, Longitude_End)
    Label2 = " - %s (lat:%0.1f,%0.1f, lon:%0.1f,%0.1f, depth:%0.1f-%0.1f)" % (lib.areaValues[Area], Latitude_Begin,
                                                                              Latitude_End, Longitude_Begin,
                                                                              Longitude_End, Depth_Begin, Depth_End)

    # make sure we have input files
    query = lib.earthquakeQuery % (Start_Time, Magnitude_Begin, Magnitude_End, Depth_Begin, Depth_End, Latitude_Begin,
                                   Latitude_End, Longitude_Begin, Longitude_End, Max_Count)
    if len(Alternate_FileName) <= 0:
        eqFile = lib.query2filename(query, url=lib.earthquakeKeys[Data_Source])
        query = '?'.join([lib.earthquakeKeys[Data_Source], query])
        fileFound, address, source = lib.find_file(eqFile, loc='EMC_EARTHQUAKES_PATH', query=query)
    else:
       fileFound, address, source = lib.find_file(Alternate_FileName, loc='EMC_EARTHQUAKES_PATH')
    if not fileFound:
        raise Exception('earthquake catalog file "' + address +
                        '" not found! Please provide the full path or UR for the file. Aborting.')
    (params, lines) = lib.read_geocsv(address)

    pdo = self.GetOutput()  # vtkPoints
    column_keys = lib.columnKeys
    for key in lib.columnKeys.keys():
        if key in params.keys():
            column_keys[key] = params[key]

    delimiter = params['delimiter'].strip()
    origin = None
    if 'source' in params:
        origin = params['source']
        Label = urlparse.urlparse(origin).netloc
    else:
        try:
            Label = urlparse.urlparse(Alternate_FileName).netloc
        except:
            Label = Alternate_FileName

    header = lines[0].strip()
    fields = header.split(delimiter)
    for i in range(len(fields)):
          if fields[i].strip().lower() == column_keys['longitude_column'].lower():
             lonIndex = i
          elif fields[i].strip().lower() == column_keys['latitude_column'].lower():
             latIndex = i
          elif fields[i].strip().lower() == column_keys['depth_column'].lower():
             depthIndex = i
          elif fields[i].strip().lower() == column_keys['magnitude_column'].lower():
             magIndex = i

    scalars = vtk.vtkFloatArray()
    scalars.SetNumberOfComponents(1)
    scalars.SetName("magnitude")
    lat = []
    lon = []
    depth = []
    mag = []

    for i in range(1,len(lines)):
       line = lines[i].strip()
       values = line.strip().split(params['delimiter'].strip())
       lat.append(float(values[latIndex]))
       lon.append(float(values[lonIndex]))
       depth.append(float(values[depthIndex]))
       mag.append(float(values[magIndex]))
       if Latitude_Begin <= lat[-1] <= Latitude_End and Longitude_Begin <= lon[-1] <= Longitude_End:
          x, y, z = lib.llz2xyz(lat[-1], lon[-1], depth[-1])
          pts.InsertNextPoint(x, y, z)
          scalars.InsertNextValue(mag[-1])
    pdo.SetPoints(pts)
    pdo.GetPointData().AddArray(scalars)

    if len(Label.strip()) > 0:
        simple.RenameSource(' '.join(['Earthquake locations:', 'from', Label.strip(), Label2.strip()]))

    view = simple.GetActiveView()

    # store metadata
    fieldData = pdo.GetFieldData()
    fieldData.AllocateArrays(3)  # number of fields

    data = vtk.vtkFloatArray()
    data.SetName('Latitude\nRange (deg)')
    data.InsertNextValue(min(lat))
    data.InsertNextValue(max(lat))
    fieldData.AddArray(data)

    data = vtk.vtkFloatArray()
    data.SetName('Longitude\nRange (deg)')
    data.InsertNextValue(min(lon))
    data.InsertNextValue(max(lon))
    fieldData.AddArray(data)

    data = vtk.vtkFloatArray()
    data.SetName('Depth\nRange (km)')
    data.InsertNextValue(min(depth))
    data.InsertNextValue(max(depth))
    fieldData.AddArray(data)

    data = vtk.vtkFloatArray()
    data.SetName('Magnitude\nRange')
    data.InsertNextValue(min(mag))
    data.InsertNextValue(max(mag))
    fieldData.AddArray(data)

    data = vtk.vtkIntArray()
    data.SetName('Max. Event\nCount')
    data.InsertNextValue(len(mag))
    fieldData.AddArray(data)

    data = vtk.vtkStringArray()
    data.SetName('Start Date')
    data.InsertNextValue(Start_Time)
    fieldData.AddArray(data)

    data = vtk.vtkStringArray()
    data.SetName('Source')
    if origin is not None:
       data.InsertNextValue(origin)

    data.InsertNextValue(source)
    fieldData.AddArray(data)

    pdo.SetFieldData(fieldData)

def RequestInformation():
    from paraview import util
    sys.path.insert(0, "EMC_SRC_PATH")
    import IrisEMC_Paraview_Lib as lib

    Latitude_Begin, Latitude_End, Longitude_Begin, Longitude_End = lib.get_area(Area, Latitude_Begin, Latitude_End,
                                                                                Longitude_Begin, Longitude_End)
    query = lib.earthquakeQuery % (Start_Time, Magnitude_Begin, Magnitude_End, Depth_Begin, Depth_End, Latitude_Begin,
                                   Latitude_End, Longitude_Begin, Longitude_End, Max_Count)
    if len(Alternate_FileName) <= 0:
        eqFile = lib.query2filename(query, url=lib.earthquakeKeys[Data_Source])
        query = '?'.join([lib.earthquakeKeys[Data_Source], query])
        fileFound, address, source = lib.find_file(eqFile, loc='EMC_EARTHQUAKES_PATH', query=query)
    else:
       fileFound, address, source = lib.find_file(Alternate_FileName, loc='EMC_EARTHQUAKES_PATH')
    if not fileFound:
       raise Exception('earthquake catalog file "' + address +
                       '" not found! Please provide the full path or UR for the file. Aborting.')
    (params, lines) = lib.read_geocsv(address)
    num = len(lines)
    # ABSOLUTELY NECESSARY FOR THE READER TO WORK:
    util.SetOutputWholeExtent(self, [0, num - 1, 0, num - 1, 0, num - 1])
