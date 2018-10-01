Name = 'Read2DEarthModels'
Label = 'Read 2D Earth Models'
FilterCategory = 'IRIS EMC'
Help = 'Read and display 2D netCDF Earth models.'

ExtraXml = '''\
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
OutputDataType = 'vtkStructuredGrid'

Properties = dict(
    FileName="EMC_DEFAULT_2DMODEL",
    Area=1,
    Depth=-1,
    Label='',
    Latitude_Begin='',
    Latitude_End='',
    Latitude_Variable='latitude',
    Longitude_Begin='',
    Longitude_End='',
    Longitude_Variable='longitude',
    Variable='thickness',
    Sampling=2
)

def RequestData():
    # R.0.2018.129
    import sys
    sys.path.insert(0, "EMC_SRC_PATH")
    from paraview.simple import RenameSource, GetActiveViewOrCreate, ColorBy, GetDisplayProperties, GetActiveSource
    import numpy as np
    import csv
    import os
    from vtk.util import numpy_support as nps
    import IrisEMC_Paraview_Lib as lib

    Latitude_Begin, Latitude_End, Longitude_Begin, Longitude_End = lib.get_area(Area, Latitude_Begin, Latitude_End,
                                                                                Longitude_Begin, Longitude_End)
    if len(Latitude_Variable.strip()) <= 0 or len(Longitude_Variable.strip()) <= 0 or len(Variable.strip()) <= 0:
        raise Exception('Latitude, Longitude and Variable are required')

    # make sure we have input files
    fileFound, address, source = lib.find_file(FileName, loc='EMC_MODELS_PATH')
    if not fileFound:
        raise Exception('model file "' + address + '" not found! Aborting.')

    filename = lib.file_name(FileName)
    if len(Label.strip()) <= 0:
        if source == filename:
           Label = "%s " % filename
        else:
           Label = "%s from %s " % (filename, source)

    sg = self.GetOutput()  # vtkPolyData

    if Depth < 0:
       X, Y, Z, V, meta = lib.read_2d_netcdf_file(address, Latitude_Variable, Longitude_Variable, Variable,
                                                  (Latitude_Begin, Longitude_Begin), (Latitude_End, Longitude_End),
                                                  Sampling, None, False)
    else:
       X, Y, Z, V, meta = lib.read_2d_netcdf_file(address, Latitude_Variable, Longitude_Variable, Variable,
                                                  (Latitude_Begin, Longitude_Begin), (Latitude_End, Longitude_End),
                                                  Sampling, Depth, False)
    nx = len(X)
    if nx <= 0:
        raise Exception('No data found!')
    ny = len(X[0])
    nz = len(X[0][0])
    sg.SetDimensions(nx, ny, nz)

    # make geometry
    points = vtk.vtkPoints()
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                points.InsertNextPoint((X[i, j, k], Y[i, j, k], Z[i, j, k]))
    sg.SetPoints(points)

    # make geometry
    count = 0
    for var in V.keys():
        scalars = vtk.vtkFloatArray()
        scalars.SetNumberOfComponents(1)
        scalars.SetName(var)
        for k in range(nz):
            for j in range(ny):
                for i in range(nx):
                    if V[var][i, j, k] == 9999.0 or V[var][i, j, k] is float('nan'):
                        scalars.InsertNextValue(float('nan'))
                    else:
                        scalars.InsertNextValue(V[var][i, j, k])
        if count == 0:
            sg.GetPointData().SetScalars(scalars)
        else:
            sg.GetPointData().AddArray(scalars)
        count += 1

    # store boundary metadata
    fieldData = sg.GetFieldData()
    fieldData.AllocateArrays(3)  # number of fields

    data = vtk.vtkFloatArray()
    data.SetName('Latitude\nRange (deg)')
    data.InsertNextValue(meta['lat'][0])
    data.InsertNextValue(meta['lat'][1])
    fieldData.AddArray(data)

    data = vtk.vtkFloatArray()
    data.SetName('Longitude\nRange (deg)')
    data.InsertNextValue(meta['lon'][0])
    data.InsertNextValue(meta['lon'][1])
    fieldData.AddArray(data)

    data = vtk.vtkStringArray()
    data.SetName('Source')
    data.InsertNextValue(FileName)
    fieldData.AddArray(data)

    Label2 = " - %s (lat:%0.1f,%0.1f, lon:%0.1f,%0.1f)" % (lib.areaValues[Area], meta['lat'][0], meta['lat'][1],
                                                           meta['lon'][0], meta['lon'][1])
    RenameSource(' '.join([Label.strip(),Label2.strip()]))
    sg.SetFieldData(fieldData)

def RequestInformation():
    sys.path.insert(0, "EMC_SRC_PATH")
    import IrisEMC_Paraview_Lib as lib
    from paraview import util

    fileFound, address, source = lib.find_file(FileName, loc='EMC_MODELS_PATH')
    if not fileFound:
        raise Exception('model file "'+address+'" not found! Aborting.')
    Latitude_Begin, Latitude_End, Longitude_Begin, Longitude_End = lib.get_area(Area,
                                                                                Latitude_Begin, Latitude_End,
                                                                                Longitude_Begin, Longitude_End)
    nx, ny, nz = lib.read_2d_netcdf_file(address, Latitude_Variable, Longitude_Variable, Variable,
                                         (Latitude_Begin, Longitude_Begin), (Latitude_End, Longitude_End),
                                         Sampling, None, True)

    # ABSOLUTELY NECESSARY FOR THE READER TO WORK:
    util.SetOutputWholeExtent(self, [0,nx, 0,ny, 0,nz+1])
