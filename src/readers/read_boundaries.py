Name = 'DrawBoundaries'
Label = 'Draw Boundaries'
FilterCategory = 'IRIS EMC'
Help = 'Draw boundaries by reading a selected boundary file based on the lat,lon limits.'

ExtraXml = '''\
<IntVectorProperty
    name="DataFile"
    command="SetParameter"
    number_of_elements="1"
    initial_string="boundary_drop_down_menu"
    default_values="2">
    <EnumerationDomain name="enum_data">
          BOUNDARY_DROP_DOWN
    </EnumerationDomain>
    <Documentation>
        Choose what type of boundary to draw.
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
    Alternate_FileName='',
    Latitude_Begin='',
    Latitude_End='',
    Longitude_Begin='',
    Longitude_End='',
    Depth_Bias='0.0',
    DataFile=2
)

def RequestData():
    # R.0.2018.080
    import sys
    import paraview.simple as simple
    import numpy as np
    import csv
    import os
    sys.path.insert(0, r'EMC_SRC_PATH')
    import IrisEMC_Paraview_Lib as lib
    import urlparse

    if len(Alternate_FileName.strip()) > 0:
         FileName = Alternate_FileName.strip()
         Label = ' '.join(['Boundary', lib.file_name(Alternate_FileName).strip()])
    else:
         FileName = lib.boundaryKeys[DataFile]
         Label = lib.boundaryValues[DataFile]

    # make sure we have input files
    fileFound, address, source = lib.find_file(FileName, loc=r'EMC_BOUNDARIES_PATH')
    if not fileFound:
        raise Exception('boundary file "' + address +
                        '" not found! Please provide the full path or UR for the file. Aborting.')
    (params, lines) = lib.read_geocsv(address)
    
    pdo = self.GetOutput()  # vtkPolyData
    
    Latitude_Begin, Latitude_End, Longitude_Begin, Longitude_End = lib.get_area(Area, Latitude_Begin, Latitude_End,
                                                                                Longitude_Begin, Longitude_End)
    Label2 = " - %s (lat:%0.1f,%0.1f, lon:%0.1f,%0.1f)" % (lib.areaValues[Area], Latitude_Begin, Latitude_End,
                                                           Longitude_Begin, Longitude_End)

    x = []
    y = []
    z = []
    segments = []
    pointIndex  = -1
    thisSegment = []
    Boundary_Elevation = float(Depth_Bias)

    column_keys = lib.columnKeys
    for key in lib.columnKeys.keys():
        if key in params.keys():
            column_keys[key] = params[key].strip()
    delimiter = params['delimiter'].strip()
    gaps = params['gaps'].strip()
    latIndex = 0
    lonIndex = 1
    if 'source' in params.keys():
        try:
           netloc = urlparse.urlparse(params['source']).netloc
        except:
           netloc = params['source']

        if len(netloc.strip()) <= 0:
           netloc = params['source']

        Label = ' '.join([Label.strip(), 'from', netloc.strip()])
    
    fields = params['header']
    if fields[0].strip() == column_keys['longitude_column']:
       latIndex = 1
       lonIndex = 0

    for l in range(len(lines)):
        line = lines[l].strip()
        # segment break
        if gaps in line:
            # file start
            if pointIndex <= 0:
               continue

            # finished one segment, store the number of points
            else:
                 segments.append(thisSegment)
                 thisSegment = []
                 pointIndex  = 0
        else:
             values = line.strip().split(delimiter)
             lat,lon = values[latIndex], values[lonIndex]
             if float(lat) < Latitude_Begin or float(lat) > Latitude_End or float(lon) < Longitude_Begin or \
                     float(lon) > Longitude_End:
                 continue
            
             # convert to spherical coordinates
             X, Y, Z =lib.llz2xyz(float(lat), float(lon), Boundary_Elevation)
             x.append(X)
             y.append(Y)
             z.append(Z)
             pointIndex += 1

             # store point index for this segment
             thisSegment.append(len(x) - 1)

    # This vtk object will store all the points
    newPts = vtk.vtkPoints()
    nPoints = len(x)
    for i in range(nPoints):
       newPts.InsertPoint(i, x[i], y[i], z[i])

    # Add the points to the vtkPolyData object
    pdo.SetPoints(newPts)

    # storage for the line segments
    nSegments = len(segments)
    pdo.Allocate(nSegments, 1)

    # Make a vtkPolyLine object to hold each segment data
    for i in range(0, nSegments):
       aPolyLine = vtk.vtkPolyLine()

       # Indicate the number of points along the line
       aPolyLine.GetPointIds().SetNumberOfIds(len(segments[i]))
       for j in range(len(segments[i])):
           aPolyLine.GetPointIds().SetId(j, segments[i][j])
       pdo.InsertNextCell(aPolyLine.GetCellType(), aPolyLine.GetPointIds())

    simple.RenameSource(Label+Label2)

    # store boundary metadata
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

    data = vtk.vtkFloatArray()
    data.SetName('Boundary Elevation (km)')
    data.InsertNextValue(-1*Boundary_Elevation)
    fieldData.AddArray(data)

    data = vtk.vtkStringArray()
    data.SetName('Source')
    data.InsertNextValue(source)
    fieldData.AddArray(data)

    pdo.SetFieldData(fieldData)

def RequestInformation():
    from paraview import util
    import csv
    pass
