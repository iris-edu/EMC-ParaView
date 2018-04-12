Name = 'ReadEtopo5'
Label = 'NOAA Etopo5 elevation data'
FilterCategory = 'IRIS EMC'
Help = 'Read and display surface elevation changes, using ETOPO5 elevation data file.'

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
    Area            = 1,
    Latitude_Begin  = '',
    Latitude_End    = '',
    Longitude_Begin = '',
    Longitude_End   = '',
    Sampling        = 10
)

def RequestData():
    # R.0.2018.080
    import sys
    sys.path.insert(0, "EMC_SRC_PATH")
    from paraview.simple import RenameSource, GetActiveViewOrCreate, ColorBy, GetDisplayProperties, GetActiveSource
    import numpy as np
    import csv
    import os
    from vtk.util import numpy_support as nps
    import IrisEMC_Paraview_Lib as lib

    FileName = lib.etopo5File

    # make sure we have input files
    fileFound,address,source = lib.findFile(FileName,loc='EMC_MODELS_PATH')
    if not fileFound:
        raise Exception('Etopo5 file "'+address+'" not found! Aborting.')

    filename = lib.fileName(FileName)

    sg = self.GetOutput() # vtkPolyData

    Latitude_Begin,Latitude_End,Longitude_Begin,Longitude_End = lib.getArea(Area,Latitude_Begin,Latitude_End,Longitude_Begin,Longitude_End)
    Label2 = " - %s (%0.1f,%0.1f,%0.1f,%0.1f)"%(lib.areaValues[Area],Latitude_Begin,Latitude_End,Longitude_Begin,Longitude_End)

    X,Y,Z,V,label = lib.readTopoFile(address,(Latitude_Begin,Longitude_Begin),(Latitude_End,Longitude_End),Sampling)
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
                scalars.InsertNextValue(V[var][i,j,k])
       if count == 0:
          sg.GetPointData().SetScalars(scalars)
       else:
          sg.GetPointData().AddArray(scalars)
       count += 1

    # store metadata
    fieldData = sg.GetFieldData()
    fieldData.AllocateArrays(3) # number of fields

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

    
    RenameSource(' '.join([label.strip(),'from',source.strip(),Label2.strip()]))

def RequestInformation():
    sys.path.insert(0, "EMC_SRC_PATH")
    import IrisEMC_Paraview_Lib as lib
    from paraview import util
    fileFound,address,source = lib.findFile(lib.etopo5File,loc='EMC_MODELS_PATH')
    Latitude_Begin,Latitude_End,Longitude_Begin,Longitude_End = lib.getArea(Area,Latitude_Begin,Latitude_End,Longitude_Begin,Longitude_End)

    nx,ny,nz = lib.findTopoExtent(address,(Latitude_Begin,Longitude_Begin),(Latitude_End,Longitude_End),Sampling)
    # ABSOLUTELY NECESSARY FOR THE READER TO WORK:
    util.SetOutputWholeExtent(self, [0,nx-1, 0,ny-1, 0,nz-1])
