Name = 'DrawGrids'
Label = 'Draw Grids'
FilterCategory = 'IRIS EMC'
Help = 'Draw the latitude and longitude grid lines.'

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
    Area=1,
    Latitude_Begin='',
    Latitude_End='',
    Longitude_Begin='',
    Longitude_End='',
    Depth_Bias='0.0',
    Grid_Resolution_degrees=1,
    Grid_Spacing='20.0'
)

def RequestData():
    # R.0.2018.080
    import sys
    import numpy as np
    import os
    import paraview.simple as simple
    sys.path.insert(0, r'EMC_SRC_PATH')
    import IrisEMC_Paraview_Lib as lib

    grid_depth = float(Depth_Bias)
    spacing = float(Grid_Spacing)

    pdo = self.GetOutput()  # vtkPolyData

    Latitude_Begin, Latitude_End, Longitude_Begin, Longitude_End = lib.get_area(Area, Latitude_Begin, Latitude_End,
                                                                                Longitude_Begin, Longitude_End)
    Label2 = " - %s (lat:%0.1f,%0.1f, lon:%0.1f,%0.1f) with grid spacing of %0.1f degrees" % (lib.areaValues[Area],
                                                                                              Latitude_Begin,
                                                                                              Latitude_End,
                                                                                              Longitude_Begin,
                                                                                              Longitude_End,
                                                                                              spacing)

    x = []
    y = []
    z = []
    segments = []

    # create grid points along latitudes
    nLat = int((Latitude_End - Latitude_Begin) / spacing) + 1
    mLat = int((Latitude_End - Latitude_Begin) / Grid_Resolution_degrees) + 1
    nLon = int((Longitude_End - Longitude_Begin) / spacing) + 1
    mLon = int((Longitude_End - Longitude_Begin) / Grid_Resolution_degrees) + 1

    lat = Latitude_Begin - spacing
    for i in range(nLat):
        lat += spacing
        this_segment = []
        point_index = 0
        lon = Longitude_Begin - Grid_Resolution_degrees
        for j in range(mLon):
            lon += Grid_Resolution_degrees
            X, Y, Z = lib.llz2xyz(lat, lon, grid_depth)
            x.append(X)
            y.append(Y)
            z.append(Z)
            point_index += 1

            # store point index for this segment
            this_segment.append(len(x) - 1)
        segments.append(this_segment)

    # create grid points along longitudes
    lon = Longitude_Begin - spacing
    for j in range(nLon):
        lon += spacing
        this_segment = []
        point_index = 0
        lat = Latitude_Begin - Grid_Resolution_degrees
        for i in range(mLat):
            lat += Grid_Resolution_degrees
            X, Y, Z = lib.llz2xyz(lat, lon, grid_depth)
            x.append(X)
            y.append(Y)
            z.append(Z)
            point_index += 1

            # store point index for this segment
            this_segment.append(len(x) - 1)
        segments.append(this_segment)

    # this vtk object will store all the points
    new_points = vtk.vtkPoints()
    npoints = len(x)
    for i in range(npoints):
       new_points.InsertPoint(i, x[i], y[i], z[i])

    # add the points to the vtkPolyData object
    pdo.SetPoints(new_points)

    # initialize storage for line segments
    nSegments = len(segments)
    pdo.Allocate(nSegments, 1)

    # make a vtkPolyLine object to hold each segment data
    for i in range(0, nSegments):
        a_polyLine = vtk.vtkPolyLine()

        # indicate the number of points along the line
        a_polyLine.GetPointIds().SetNumberOfIds(len(segments[i]))
        for j in range(len(segments[i])):
            a_polyLine.GetPointIds().SetId(j, segments[i][j])
        pdo.InsertNextCell(a_polyLine.GetCellType(), a_polyLine.GetPointIds())

    # store grid metadata
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
    data.SetName('Grid Elevation (km),\nResolution & Spacing (deg)')
    data.InsertNextValue(grid_depth)
    data.InsertNextValue(Grid_Resolution_degrees)
    data.InsertNextValue(spacing)
    fieldData.AddArray(data)

    pdo.SetFieldData(fieldData)
    simple.RenameSource(' '.join(['Grid',Label2.strip()]))

def RequestInformation():
    pass
