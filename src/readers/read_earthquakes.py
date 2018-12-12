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
    <EnumerationDomain name="enum_source">
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
    <EnumerationDomain name="enum_area">
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
    Vertical_Scaling=1,
    Start_Time='2000-01-01'
)


def RequestData():
    # R.1.2018.346
    import sys
    sys.path.insert(0, r'EMC_SRC_PATH')
    import paraview.simple as simple
    import numpy as np
    import csv
    import os
    from vtk.util import numpy_support as nps
    import IrisEMC_Paraview_Lib as Lib
    import urlparse

    pts = vtk.vtkPoints()
    Latitude_Begin, Latitude_End, Longitude_Begin, Longitude_End = Lib.get_area(Area, Latitude_Begin, Latitude_End,
                                                                                Longitude_Begin, Longitude_End)
    label2 = " - %s (lat:%0.1f,%0.1f, lon:%0.1f,%0.1f, depth:%0.1f-%0.1f)" % (Lib.areaValues[Area], Latitude_Begin,
                                                                              Latitude_End, Longitude_Begin,
                                                                              Longitude_End, Depth_Begin, Depth_End)

    # make sure we have input files
    query = Lib.earthquakeQuery % (Start_Time, Magnitude_Begin, Magnitude_End, Depth_Begin, Depth_End, Latitude_Begin,
                                   Latitude_End, Longitude_Begin, Longitude_End)
    Alternate_FileName = Alternate_FileName.strip()
    if len(Alternate_FileName) <= 0:
        eqFile = Lib.query2filename(query, url=Lib.earthquakeKeys[Data_Source])
        query = '?'.join([Lib.earthquakeKeys[Data_Source], query])
        fileFound, address, source = Lib.find_file(eqFile, loc=r'EMC_EARTHQUAKES_PATH', query=query)
    else:
        fileFound, address, source = Lib.find_file(Alternate_FileName, loc=r'EMC_EARTHQUAKES_PATH')
    if not fileFound:
        raise Exception('earthquake catalog file "' + address +
                        '" not found! Please provide the full path or UR for the file. Aborting.')
    (params, lines) = Lib.read_geocsv(address)

    pdo = self.GetOutput()  # vtkPoints
    column_keys = Lib.columnKeys
    for key in Lib.columnKeys.keys():
        if key in params.keys():
            column_keys[key] = params[key]

    origin = None
    if 'source' in params:
        origin = params['source']
        this_label = urlparse.urlparse(origin).netloc
    else:
        try:
            this_label = urlparse.urlparse(Alternate_FileName).netloc
        except:
            this_label = Alternate_FileName

    header = params['header']
    lat_index = None
    lon_index = None
    depth_index = None
    mag_index = None
    for index, value in enumerate(header):
        if value.strip().lower() == column_keys['longitude_column'].lower():
            lon_index = index
        elif value.strip().lower() == column_keys['latitude_column'].lower():
            lat_index = index
        elif value.strip().lower() == column_keys['depth_column'].lower():
            depth_index = index
        elif value.strip().lower() == column_keys['magnitude_column'].lower():
            mag_index = index

    scalar_m = vtk.vtkFloatArray()
    scalar_m.SetNumberOfComponents(1)
    scalar_m.SetName("magnitude")
    scalar_d = vtk.vtkFloatArray()
    scalar_d.SetNumberOfComponents(1)
    scalar_d.SetName("depth")
    lat = []
    lon = []
    depth = []
    mag = []

    for i in range(1, len(lines)):
        line = lines[i].strip()
        values = line.strip().split(params['delimiter'].strip())
        lat.append(float(values[lat_index]))
        lon.append(float(values[lon_index]))
        depth.append(float(values[depth_index]))
        mag.append(float(values[mag_index]))
        if Latitude_Begin <= lat[-1] <= Latitude_End and Longitude_Begin <= lon[-1] <= Longitude_End:
            x, y, z = Lib.llz2xyz(lat[-1], lon[-1], depth[-1])
            pts.InsertNextPoint(x, y, z)
            scalar_m.InsertNextValue(mag[-1])
            scalar_d.InsertNextValue(depth[-1])
    pdo.SetPoints(pts)
    pdo.GetPointData().AddArray(scalar_m)
    pdo.GetPointData().AddArray(scalar_d)

    if len(this_label.strip()) > 0:
        simple.RenameSource(' '.join(['Earthquake locations:', 'from', this_label.strip(), label2.strip()]))

    # store metadata
    field_data = pdo.GetFieldData()
    field_data.AllocateArrays(3)  # number of fields

    data = vtk.vtkFloatArray()
    data.SetName('Latitude\nRange (deg)')
    data.InsertNextValue(min(lat))
    data.InsertNextValue(max(lat))
    field_data.AddArray(data)

    data = vtk.vtkFloatArray()
    data.SetName('Longitude\nRange (deg)')
    data.InsertNextValue(min(lon))
    data.InsertNextValue(max(lon))
    field_data.AddArray(data)

    data = vtk.vtkFloatArray()
    data.SetName('Depth\nRange (km)')
    data.InsertNextValue(min(depth))
    data.InsertNextValue(max(depth))
    field_data.AddArray(data)

    data = vtk.vtkFloatArray()
    data.SetName('Magnitude\nRange')
    data.InsertNextValue(min(mag))
    data.InsertNextValue(max(mag))
    field_data.AddArray(data)

    data = vtk.vtkIntArray()
    data.SetName('Max. Event\nCount')
    data.InsertNextValue(len(mag))
    field_data.AddArray(data)

    data = vtk.vtkStringArray()
    data.SetName('Start Date')
    data.InsertNextValue(Start_Time)
    field_data.AddArray(data)

    data = vtk.vtkStringArray()
    data.SetName('Source')
    if origin is not None:
        data.InsertNextValue(origin)

    data.InsertNextValue(source)
    field_data.AddArray(data)

    pdo.SetFieldData(field_data)


def RequestInformation():
    from paraview import util
    sys.path.insert(0, r'EMC_SRC_PATH')
    import IrisEMC_Paraview_Lib as Lib

    Latitude_Begin, Latitude_End, Longitude_Begin, Longitude_End = Lib.get_area(Area, Latitude_Begin, Latitude_End,
                                                                                Longitude_Begin, Longitude_End)
    query = Lib.earthquakeQuery % (Start_Time, Magnitude_Begin, Magnitude_End, Depth_Begin, Depth_End, Latitude_Begin,
                                   Latitude_End, Longitude_Begin, Longitude_End)

    Alternate_FileName = Alternate_FileName.strip()
    if len(Alternate_FileName) <= 0:
        eq_file = Lib.query2filename(query, url=Lib.earthquakeKeys[Data_Source])
        query = '?'.join([Lib.earthquakeKeys[Data_Source], query])
        file_found, address, source = Lib.find_file(eq_file, loc=r'EMC_EARTHQUAKES_PATH', query=query)
    else:
        file_found, address, source = Lib.find_file(Alternate_FileName, loc=r'EMC_EARTHQUAKES_PATH')
    if not file_found:
        raise Exception('earthquake catalog file "' + address +
                        '" not found! Please provide the full path or UR for the file. Aborting.')
    (params, lines) = Lib.read_geocsv(address)
    num = len(lines)
    # ABSOLUTELY NECESSARY FOR THE READER TO WORK:
    util.SetOutputWholeExtent(self, [0, num - 1, 0, num - 1, 0, num - 1])
