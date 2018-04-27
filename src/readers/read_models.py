Name = 'ReadEarthModels'
Label = 'Read Earth Models'
FilterCategory = 'IRIS EMC'
Help = 'Read and display netCDF Earth models.'

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
    FileName           = "EMC_DEFAULT_MODEL",
    Area               = 1,
    Label              = '',
    Latitude_Begin     = '',
    Latitude_End       = '',
    Latitude_Variable  = 'latitude',
    Longitude_Begin    = '',
    Longitude_End      = '',
    Longitude_Variable = 'longitude',
    Depth_Begin        = 0,
    Depth_End          = 200,
    Depth_Variable     = 'depth',
    Sampling           = 5
)

def RequestData():
    # R.0.2018.117
    import sys
    sys.path.insert(0, "EMC_SRC_PATH")
    from paraview.simple import RenameSource, GetActiveViewOrCreate, ColorBy, GetDisplayProperties, GetActiveSource
    import numpy as np
    import csv
    import os
    from vtk.util import numpy_support as nps
    import IrisEMC_Paraview_Lib as lib

    if Depth_Begin > Depth_End:
         raise Exception('Begin Depth < End Depth! Aborting.')

    Latitude_Begin,Latitude_End,Longitude_Begin,Longitude_End = lib.getArea(Area,Latitude_Begin,Latitude_End,Longitude_Begin,Longitude_End)

    if len(Latitude_Variable.strip()) <= 0 or len(Longitude_Variable.strip()) <= 0 or len(Depth_Variable.strip()) <=0:
        raise Exception('Latitude, Longitude and Depth variable are required')

    # make sure we have input files
    fileFound,address,source = lib.findFile(FileName,loc='EMC_MODELS_PATH')
    if not fileFound:
        raise Exception('model file "'+address+'" not found! Aborting.')

    filename = lib.fileName(FileName)
    if len(Label.strip()) <= 0:
        if source == filename:
           Label = "%s "%(filename)
        else:
           Label = "%s from %s "%(filename,source)

    sg = self.GetOutput() # vtkPolyData

    X,Y,Z,V,meta = lib.read_netCdfEarthModel(address,Latitude_Variable,Longitude_Variable,Depth_Variable,(Latitude_Begin,Longitude_Begin),(Latitude_End,Longitude_End),Depth_Begin,Depth_End,inc=Sampling) 
    nx = len(X)
    if nx <= 0:
        raise Exception('No data found!')
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
             points.InsertNextPoint((X[i,j,k],Y[i,j,k],Z[i,j,k]))
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
                if V[var][i,j,k] > 999.0:
                   scalars.InsertNextValue(float('nan'))
                else:
                   scalars.InsertNextValue(V[var][i,j,k])
       if count == 0:
          sg.GetPointData().SetScalars(scalars)
       else:
          sg.GetPointData().AddArray(scalars)
       count += 1

    # store boundary metadata
    fieldData = sg.GetFieldData()
    fieldData.AllocateArrays(3) # number of fields

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

    data = vtk.vtkFloatArray()
    data.SetName('Depths (km)')
    for d in sorted(meta['depth']):
       data.InsertNextValue(d)
    fieldData.AddArray(data)

    data = vtk.vtkStringArray()
    data.SetName('Source')
    data.InsertNextValue(FileName)
    fieldData.AddArray(data)

    Label2 = " - %s (lat:%0.1f,%0.1f, lon:%0.1f,%0.1f, depth:%0.1f - %0.1f)"%(lib.areaValues[Area],meta['lat'][0],meta['lat'][1],meta['lon'][0],meta['lon'][1],meta['depth'][0],meta['depth'][-1])
    RenameSource(' '.join([Label.strip(),Label2.strip()]))
    sg.SetFieldData(fieldData)

def RequestInformation():
    sys.path.insert(0, "EMC_SRC_PATH")
    import IrisEMC_Paraview_Lib as lib
    from paraview import util
    fileFound,address,source = lib.findFile(FileName,loc='EMC_MODELS_PATH')
    if not fileFound:
        raise Exception('model file "'+address+'" not found! Aborting.')
    Latitude_Begin,Latitude_End,Longitude_Begin,Longitude_End = lib.getArea(Area,Latitude_Begin,Latitude_End,Longitude_Begin,Longitude_End)
    nx,ny,nz = lib.find_netCDFModelExtent(address,Latitude_Variable,Longitude_Variable,Depth_Variable,(Latitude_Begin,Longitude_Begin),(Latitude_End,Longitude_End),Depth_Begin,Depth_End,inc=Sampling)
    # ABSOLUTELY NECESSARY FOR THE READER TO WORK:
    util.SetOutputWholeExtent(self, [0,nx, 0,ny, 0,nz])
