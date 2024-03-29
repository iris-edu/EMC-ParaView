Name = 'Read2DEarthModel'
Label = 'Read 2D Models'
FilterCategory = 'IRIS EMC'
Help = 'Read and display 2D Earth models.'

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
OutputDataType = 'vtkStructuredGrid'

Properties = dict(
    File_name="EMC_DEFAULT_2DMODEL",
    Area=1,
    Roughness='1',
    Depth_Bias='0.0',
    Label='',
    Latitude_Begin='',
    Latitude_End='',
    Latitude_Variable='latitude',
    Longitude_Begin='',
    Longitude_End='',
    Longitude_Variable='longitude',
    Variable='thickness',
    Sampling=2,
)


def RequestData():
    # V.2019.112
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

    File_name = File_name.strip()
    ext = None
    if File_name in list(param.filesDict.values()) or not (File_name.lower().endswith(param.filesExtDict['ssl'].lower()) or
                                                     File_name.lower().endswith(param.filesExtDict['geo'].lower())):
        if utils.support_nc():
            ext = param.filesExtDict['ssl']
        else:
            ext = param.filesExtDict['geo']

    baseline = float(Depth_Bias)
    roughness_factor = float(Roughness)

    Latitude_Begin, Latitude_End, Longitude_Begin, Longitude_End = lib.get_area(Area, Latitude_Begin, Latitude_End,
                                                                                Longitude_Begin, Longitude_End)
    if len(Latitude_Variable.strip()) <= 0 or len(Longitude_Variable.strip()) <= 0 or len(Variable.strip()) <= 0:
        raise Exception('Latitude, Longitude and Variable are required')

    # make sure we have input files
    fileFound, address, source = lib.find_file(File_name, loc=r'EMC_MODELS_PATH', ext=ext)
    if not fileFound:
        raise Exception('model file "' + address + '" not found! Aborting.')

    filename = lib.file_name(File_name)
    if len(Label.strip()) <= 0:
        if source == filename:
           Label = "%s " % filename
        else:
           Label = "%s from %s " % (filename, source)

    sg = self.GetOutput()  # vtkPolyData

    this_filename, extension = splitext(address)
    if extension.lower() in ['.nc', '.grd']:
        X, Y, Z, V, meta = lib.read_2d_netcdf_file(address, Latitude_Variable, Longitude_Variable, Variable,
                                                   (Latitude_Begin, Longitude_Begin), (Latitude_End, Longitude_End),
                                                   Sampling, roughness_factor, base=baseline, extent=False)
    else:
        try:
            X, Y, Z, V, meta = lib.read_geocsv_model_2d(address,
                                                        (Latitude_Begin, Longitude_Begin), (Latitude_End,
                                                                                            Longitude_End),
                                                        Sampling, roughness_factor, base=baseline, extent=False)
        except Exception as e:
            raise Exception('cannot recognize model file "' + address + '"! Aborting.\n' + str(e))

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
    for var in list(V.keys()):
        scalars = vtk.vtkFloatArray()
        scalars.SetNumberOfComponents(1)
        scalars.SetName(var)
        for k in range(nz):
            for j in range(ny):
                for i in range(nx):
                    if V[var][i, j, k] is float('nan'):
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
    data.InsertNextValue(File_name)
    fieldData.AddArray(data)

    Label2 = " - %s (lat:%0.1f,%0.1f, lon:%0.1f,%0.1f)" % (lib.areaValues[Area], meta['lat'][0], meta['lat'][1],
                                                           meta['lon'][0], meta['lon'][1])
    RenameSource(' '.join([Label.strip(),Label2.strip()]))
    sg.SetFieldData(fieldData)

def RequestInformation():
    sys.path.insert(0, r'EMC_SRC_PATH')
    import IrisEMC_Paraview_Lib as lib
    from os.path import splitext
    from paraview import util
    import IrisEMC_Paraview_Utils as utils
    import IrisEMC_Paraview_Param as param

    File_name = File_name.strip()
    ext = None
    if File_name in list(param.filesDict.values()) or not (File_name.lower().endswith(param.filesExtDict['ssl'].lower()) or
                                                     File_name.lower().endswith(param.filesExtDict['geo'].lower())):
        if utils.support_nc():
            ext = param.filesExtDict['ssl']
        else:
            ext = param.filesExtDict['geo']

    fileFound, address, source = lib.find_file(File_name, loc=r'EMC_MODELS_PATH', ext=ext)
    if not fileFound:
        raise Exception('model file "'+address+'" not found! Aborting.')
    Latitude_Begin, Latitude_End, Longitude_Begin, Longitude_End = lib.get_area(Area,
                                                                                Latitude_Begin, Latitude_End,
                                                                                Longitude_Begin, Longitude_End)
    this_filename, extension = splitext(address)
    if extension.lower() == '.nc':
        nx, ny, nz = lib.read_2d_netcdf_file(address, Latitude_Variable, Longitude_Variable, Variable,
                                             (Latitude_Begin, Longitude_Begin), (Latitude_End, Longitude_End),
                                             Sampling, 1.0, extent=True)
    else:
        try:
            nx, ny, nz = lib.read_geocsv_model_2d(address,
                                                  (Latitude_Begin, Longitude_Begin), (Latitude_End, Longitude_End),
                                                  Sampling, 1.0, extent=True)
        except Exception:
            raise Exception('cannot recognize model file "' + address + '"! Aborting.')

    # ABSOLUTELY NECESSARY FOR THE READER TO WORK:
    util.SetOutputWholeExtent(self, [0,nx, 0,ny, 0,nz+1])
