Name = 'Read3DGeoCSV'
Label = 'Read 3-D GeoCSV'
FilterCategory = 'IRIS EMC'
Help = 'Read and display 3-D netCDF Earth models.'

ExtraXml = '''\
<IntVectorProperty
    name="Area"
    command="SetParameter"
    number_of_elements="1"
    initial_string="Area_drop_down_menu"
    default_values="1">
    <EnumerationDomain name="enum">
          AREA_DROP_DOWN
    </EnumerationDomain>
    <Documentation>
        Choose the Area to draw in.
    </Documentation>
</IntVectorProperty>
'''

NumberOfInputs = 0
OutputDataType = 'vtkStructuredGrid'

Properties = dict(
    File_name="EMC_DEFAULT_GSV_MODEL",
    Area=1,
    Label='',
    Latitude_begin='',
    Latitude_end='',
    Longitude_begin='',
    Longitude_end='',
    Depth_begin=0,
    Depth_end=200,
    Sampling=5
)


def RequestData():
    # R.0.2018.256
    import sys
    sys.path.insert(0, "EMC_SRC_PATH")
    from paraview.simple import RenameSource, GetActiveViewOrCreate, ColorBy, GetDisplayProperties, GetActiveSource
    import numpy as np
    import csv
    import os
    from vtk.util import numpy_support as nps
    import IrisEMC_Paraview_Lib as lib

    if Depth_begin > Depth_end:
        raise Exception('Begin Depth < End Depth! Aborting.')

    Latitude_begin, Latitude_end, Longitude_begin, Longitude_end = lib.get_area(Area, Latitude_begin, Latitude_end,
                                                                               Longitude_begin, Longitude_end)

    # make sure we have input files
    file_found, address, source = lib.find_file(File_name, loc='EMC_MODELS_PATH')
    if not file_found:
        raise Exception('model file "' + address + '" not found! Aborting.')

    filename = lib.file_name(File_name)
    if len(Label.strip()) <= 0:
        if source == filename:
           Label = "%s " % filename
        else:
           Label = "%s from %s " % (filename, source)

    sg = self.GetOutput()  # vtkPolyData

    x, y, z, v, meta = lib.read_geocsv_model_3d(address,
                                                (Latitude_begin, Longitude_begin), (Latitude_end, Longitude_end),
                                                Depth_begin, Depth_end, Sampling, False)
    nx = len(x)
    if nx <= 0:
        raise Exception('No data found!')
    ny = len(x[0])
    nz = len(x[0][0])
    sg.SetDimensions(nx, ny, nz)

    # make geometry
    points = vtk.vtkPoints()
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                points.InsertNextPoint((x[i, j, k], y[i, j, k], z[i, j, k]))
    sg.SetPoints(points)

    # make geometry
    count = 0
    for var in v.keys():
        scalars = vtk.vtkFloatArray()
        scalars.SetNumberOfComponents(1)
        scalars.SetName(var)
        for k in range(nz):
            for j in range(ny):
                for i in range(nx):
                    if v[var][i, j, k] > 999.0 or v[var][i, j, k] == float('nan'):
                        scalars.InsertNextValue(float('nan'))
                    else:
                        scalars.InsertNextValue(v[var][i, j, k])
        if count == 0:
            sg.GetPointData().SetScalars(scalars)
        else:
            sg.GetPointData().AddArray(scalars)
        count += 1

    # store boundary metadata
    field_data = sg.GetFieldData()
    field_data.AllocateArrays(3)  # number of fields

    data = vtk.vtkFloatArray()
    data.SetName('Latitude\nRange (deg)')
    data.InsertNextValue(meta['lat'][0])
    data.InsertNextValue(meta['lat'][1])
    field_data.AddArray(data)

    data = vtk.vtkFloatArray()
    data.SetName('Longitude\nRange (deg)')
    data.InsertNextValue(meta['lon'][0])
    data.InsertNextValue(meta['lon'][1])
    field_data.AddArray(data)

    data = vtk.vtkFloatArray()
    data.SetName('Depths (km)')
    for d in sorted(meta['depth']):
        data.InsertNextValue(d)
    field_data.AddArray(data)

    data = vtk.vtkStringArray()
    data.SetName('Source')
    data.InsertNextValue(File_name)
    field_data.AddArray(data)

    label_2 = ' - %s (lat:%0.1f,%0.1f, lon:%0.1f,%0.1f, depth:%0.1f - %0.1f)'%(lib.areaValues[Area], meta['lat'][0],
                                                                               meta['lat'][1], meta['lon'][0],
                                                                               meta['lon'][1], meta['depth'][0],
                                                                               meta['depth'][-1])
    RenameSource(' '.join([Label.strip(), label_2.strip()]))
    sg.SetFieldData(field_data)


def RequestInformation():
    sys.path.insert(0, "EMC_SRC_PATH")
    import IrisEMC_Paraview_Lib as lib
    from paraview import util

    file_found, address, source = lib.find_file(File_name, loc='EMC_MODELS_PATH')

    if not file_found:
        raise Exception('model file "' + address + '" not found! Aborting.')
    Latitude_begin, Latitude_end, Longitude_begin, Longitude_end = lib.get_area(Area, Latitude_begin, Latitude_end,
                                                                               Longitude_begin, Longitude_end)
    nx, ny, nz = lib.read_geocsv_model_3d(address,
                                          (Latitude_begin, Longitude_begin), (Latitude_end, Longitude_end),
                                          Depth_begin, Depth_end, Sampling, True)

    # ABSOLUTELY NECESSARY FOR THE READER TO WORK:
    util.SetOutputWholeExtent(self, [0, nx, 0, ny, 0, nz])