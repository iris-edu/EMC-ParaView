Name = 'ReadTopo'
Label = 'Topo Elevation Data'
FilterCategory = 'IRIS EMC'
Help = 'Read and display surface elevation changes, using elevation data file.'

ExtraXml = '''\
<IntVectorProperty
    name="TopoFile"
    command="SetParameter"
    number_of_elements="1"
    initial_string="topo_drop_down_menu"
    default_values="1">
    <EnumerationDomain name="enum_topo">
          TOPO_DROP_DOWN
    </EnumerationDomain>
    <Documentation>
        Choose elevation data to use.
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
OutputDataType = 'vtkStructuredGrid'

Properties = dict(
    Area=1,
    Alternate_FileName='',
    Depth_Bias='0.0',
    Latitude_Begin='',
    Latitude_End='',
    Latitude_Variable='latitude',
    Longitude_Begin='',
    Longitude_End='',
    Longitude_Variable='longitude',
    Elevation_Variable='elevation',
    Roughness='1',
    Sampling=10,
    Unit_Factor='0.001',
    TopoFile=1
)

def RequestData():
    # V.2019.030
    import sys
    sys.path.insert(0, r'EMC_SRC_PATH')
    from paraview.simple import RenameSource, GetActiveViewOrCreate, ColorBy, GetDisplayProperties, GetActiveSource
    import numpy as np
    import csv
    import os
    from os.path import splitext
    from vtk.util import numpy_support as nps
    import IrisEMC_Paraview_Lib as lib
    import IrisEMC_Paraview_Utils as utils
    import IrisEMC_Paraview_Param as param

    # elevation units in meters
    Roughness = -1 * float(Roughness)

    baseline = float(Depth_Bias)

    if len(Alternate_FileName.strip()) > 0:
        file_name = Alternate_FileName.strip()
        label = ' '.join(['Topo', lib.file_name(Alternate_FileName).strip()])
    else:
        file_name = lib.topoKeys[TopoFile]
        label = lib.topoValues[TopoFile]

    file_name = file_name.strip()
    ext = None
    if file_name in param.topoDict.keys():
        if utils.support_nc():
            ext = param.topoExtDict['ssl']
        else:
            ext = param.topoExtDict['geo']

    # make sure we have input files
    file_found, address, source = lib.find_file(file_name, loc=r'EMC_MODELS_PATH', ext=ext)

    if not file_found:
        raise Exception('Topo file "' + address + '" not found! Aborting.')

    this_filename, extension = splitext(address)

    sg = self.GetOutput()  # vtkPolyData

    Latitude_Begin, Latitude_End, Longitude_Begin, Longitude_End = lib.get_area(Area, Latitude_Begin, Latitude_End,
                                                                                   Longitude_Begin, Longitude_End)

    label2 = " - %s (%0.1f,%0.1f,%0.1f,%0.1f)" % (lib.areaValues[Area], Latitude_Begin, Latitude_End, Longitude_Begin,
                                                  Longitude_End)

    if extension.lower() in ['.nc', '.grd']:

        X, Y, Z, V, label = lib.read_netcdf_topo_file(address, (Latitude_Begin, Longitude_Begin), (Latitude_End,
                                                                                                   Longitude_End),
                                                      Sampling, Roughness,  base=baseline, lon_var=Longitude_Variable,
                                                      lat_var=Latitude_Variable, elev_var=Elevation_Variable,
                                                      unit_factor=float(Unit_Factor),
                                                      extent=False)

    else:
        try:
            X, Y, Z, V, meta = lib.read_geocsv_model_2d(address, (Latitude_Begin, Longitude_Begin), (Latitude_End,
                                                                                                     Longitude_End),
                                                        Sampling, Roughness, base=baseline,
                                                        unit_factor=float(Unit_Factor),
                                                        extent=False)

        except Exception:
            raise Exception('cannot recognize model file "' + address + '"! Aborting.')

    nx = len(X)
    ny = len(X[0])
    nz = len(X[0][0])
    sg.SetDimensions(nx,ny,nz)

    #
    # make geometry
    #
    points = vtk.vtkPoints()
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                points.InsertNextPoint((X[i, j, k], Y[i, j, k], Z[i, j, k]))
    sg.SetPoints(points)

    #
    # make geometry
    #
    count = 0
    for var in V.keys():
        scalars = vtk.vtkFloatArray()
        scalars.SetNumberOfComponents(1)
        scalars.SetName(var)
        for k in range(nz):
            for j in range(ny):
                for i in range(nx):
                    scalars.InsertNextValue(V[var][i, j, k])
        if count == 0:
            sg.GetPointData().SetScalars(scalars)
        else:
            sg.GetPointData().AddArray(scalars)
        count += 1

    # store metadata
    fieldData = sg.GetFieldData()
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
    data.InsertNextValue(source)
    fieldData.AddArray(data)
    RenameSource(' '.join([label.strip(), 'from', source.strip(), label2.strip()]))

def RequestInformation():
    sys.path.insert(0, r'EMC_SRC_PATH')
    from os.path import splitext
    import IrisEMC_Paraview_Lib as lib
    from paraview import util
    import IrisEMC_Paraview_Utils as utils
    import IrisEMC_Paraview_Param as param

    if len(Alternate_FileName.strip()) > 0:
        file_name = Alternate_FileName.strip()
    else:
        file_name = lib.topoKeys[TopoFile]

    file_name = file_name.strip()
    ext = None
    if file_name in param.topoDict.keys():
        if utils.support_nc():
            ext = param.topoExtDict['ssl']
        else:
            ext = param.topoExtDict['geo']

    fileFound, address, source = lib.find_file(file_name, loc=r'EMC_MODELS_PATH', ext=ext)
    Latitude_Begin, Latitude_End, Longitude_Begin, Longitude_End = lib.get_area(Area, Latitude_Begin, Latitude_End,
                                                                               Longitude_Begin, Longitude_End)

    this_filename, extension = splitext(address)
    if extension.lower() in ['.nc', '.grd']:
        nx, ny, nz = lib.read_netcdf_topo_file(address, (Latitude_Begin, Longitude_Begin), (Latitude_End,
                                                                                            Longitude_End),
                                               Sampling, Roughness, lon_var=Longitude_Variable,
                                               lat_var=Latitude_Variable, elev_var=Elevation_Variable,
                                               extent=True)
    else:
        try:
            nx, ny, nz = lib.read_geocsv_model_2d(address, (Latitude_Begin, Longitude_Begin), (Latitude_End,
                                                                                           Longitude_End),
                                                  Sampling, Roughness, extent=True)
        except Exception:
            raise Exception('cannot recognize model file "' + address + '"! Aborting.')

    # ABSOLUTELY NECESSARY FOR THE READER TO WORK:
    util.SetOutputWholeExtent(self, [0, nx, 0, ny, 0, nz])
