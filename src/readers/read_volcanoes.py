Name = 'ReadVolcalnoes'
Label = 'Show Volcano Locations'
FilterCategory = 'IRIS EMC'
Help = 'Read and display volcano locations.'

ExtraXml = '''\

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
    File_name="EMC_DEFAULT_VOLCANO",
    Area=1,
    Latitude_Begin='',
    Latitude_End='',
    Longitude_Begin='',
    Longitude_End=''
)

def RequestData():
    # V.2019.014
    import sys
    sys.path.insert(0, r'EMC_SRC_PATH')
    import paraview.simple as simple
    import numpy as np
    import csv
    import os
    from vtk.util import numpy_support as nps
    import IrisEMC_Paraview_Lib as lib
    import urlparse

    Label = ''

    pts = vtk.vtkPoints()

    # make sure we have input files
    if len(File_name.strip()) <= 0:
        fileFound = False
        address = ''
    else:
       fileFound, address, source = lib.find_file(File_name.strip(), loc=r'EMC_VOLCANOES_PATH')

    if not fileFound:
        raise Exception('volcano file "' + address +
                        '" not found! Please provide the full path or UR for the file. Aborting.')
    (params, lines) = lib.read_geocsv(address)

    Latitude_Begin, Latitude_End, Longitude_Begin, Longitude_End = lib.get_area(Area,
                                                                                Latitude_Begin, Latitude_End,
                                                                                Longitude_Begin, Longitude_End)
    Label2 = " - %s (lat:%0.1f,%0.1f, lon:%0.1f,%0.1f)" % (lib.areaValues[Area], Latitude_Begin, Latitude_End,
                                                           Longitude_Begin, Longitude_End)

    pdo = self.GetOutput()  # vtkPoints
    lat_index = 0
    lon_index = 1

    column_keys = lib.columnKeys
    for key in lib.columnKeys.keys():
        if key in params.keys():
            column_keys[key] = params[key]

    delimiter = params['delimiter'].strip()
    
    origin = None
    if 'source' in params:
        origin = params['source']
        if len(Label.strip()) <= 0:
            Label = origin

    fields = params['header']
    for i in range(len(fields)):
        if fields[i].strip().lower() == column_keys['longitude_column'].lower():
            lon_index = i
        elif fields[i].strip().lower() == column_keys['latitude_column'].lower():
            lat_index = i
        elif fields[i].strip().lower() == column_keys['elevation_column'].lower():
            elev_index = i

    for i, line in enumerate(lines):
        line = line.strip()
        values = line.split(delimiter)
        try:
            lat = float(values[lat_index])
            lon = float(values[lon_index])
        except:
            continue
        if len(values[elev_index].strip()) <= 0:
            depth = 0.0
        else:
            try:
                depth = -1 * float(values[elev_index]) / 1000.0
            except:
                continue
        if Latitude_Begin <= lat <= Latitude_End and Longitude_Begin <= lon <= Longitude_End:
            x, y, z = lib.llz2xyz(lat, lon, depth)
            pts.InsertNextPoint(x, y, z)
    pdo.SetPoints(pts)

    simple.RenameSource(' '.join(['Volcano locations:', Label.strip(), Label2.strip()]))

    view = simple.GetActiveView()

    # store metadata
    fieldData = pdo.GetFieldData()
    fieldData.AllocateArrays(3)  # number of fields

    data = vtk.vtkFloatArray()
    data.SetName('Latitude\nRange (deg)')
    data.InsertNextValue(Latitude_Begin)
    data.InsertNextValue(Latitude_End)
    fieldData.AddArray(data)

    data = vtk.vtkFloatArray()
    data.SetName('Longitude\nRange (deg)')
    data.InsertNextValue(Longitude_Begin)
    data.InsertNextValue(Longitude_End)
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

    if len(File_name.strip()) <= 0:
        fileFound = False
        address = ''
    else:
        fileFound, address, source = lib.find_file(File_name.strip(), loc=r'EMC_VOLCANOES_PATH')

    if not fileFound:
        raise Exception('volcano file "' + address +
                        '" not found! Please provide the full path or UR for the file. Aborting.')
    (params, lines) = lib.read_geocsv(address)
    num = len(lines)

    # ABSOLUTELY NECESSARY FOR THE READER TO WORK:
    util.SetOutputWholeExtent(self, [0, num - 1, 0, num - 1, 0, num - 1])
