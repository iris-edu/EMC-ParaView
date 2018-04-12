Name = 'ReadUSGSSlabModel'
Label = 'Show USGS Slab 1.0'
FilterCategory = 'IRIS EMC'
Help = 'Get/Read and display USGS Slab 1.0 models.'

ExtraXml = '''\
<IntVectorProperty
    name="Slab"
    command="SetParameter"
    number_of_elements="1"
    initial_string="slab_drop_down_menu"
    default_values="0">
    <EnumerationDomain name="enum">
          USGS_SLAB_DROP_DOWN
    </EnumerationDomain>
    <Documentation>
        Choose what slab to plot
    </Documentation>
</IntVectorProperty>
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
    Alternate_FileName  = '' ,
    Latitude_Begin      = '',
    Latitude_End        = '',
    Longitude_Begin     = '',
    Longitude_End       = '',
    Sampling            = 5,
    Slab                = 0,
    Area                = 1
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
    import urlparse
    USGS = True
    if len(Alternate_FileName.strip()) > 0:
         FileName        = Alternate_FileName
         Label           = ' '.join(['SLAB',lib.fileName(Alternate_FileName).strip()])
         USGS            = False
    else:
         FileName        = lib.usgsSlabKeys[Slab]

    depthFactor = -1

    Latitude_Begin,Latitude_End,Longitude_Begin,Longitude_End = lib.getArea(Area,Latitude_Begin,Latitude_End,Longitude_Begin,Longitude_End)
    Label2 = " - %s (lat:%0.1f,%0.1f, lon:%0.1f,%0.1f)"%(lib.areaValues[Area],Latitude_Begin,Latitude_End,Longitude_Begin,Longitude_End)

    # Make sure we have input files
    fileFound,address,source = lib.findFile(FileName,loc='EMC_SLABS_PATH')
    if not fileFound:
        raise Exception('model file "'+address+'" not found! Aborting.')

    sg = self.GetOutput() # vtkPolyData

    X,Y,Z,V,label = lib.readSlabFile(address,(Latitude_Begin,Longitude_Begin),(Latitude_End,Longitude_End),inc=Sampling)
    
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
                scalars.InsertNextValue(depthFactor * V[var][i,j,k])
       if count == 0:
          sg.GetPointData().SetScalars(scalars)
       else:
          sg.GetPointData().AddArray(scalars)
       count += 1

    # store USGS metadata
    if USGS:
       fieldData = sg.GetFieldData()
       fieldData.AllocateArrays(3) # number of fields

       data = vtk.vtkFloatArray()
       data.SetName('Latitude\nRange (deg)')
       data.InsertNextValue(lib.usgsSlabRangeDict[lib.usgsSlabKeys[Slab]]['Y'][0])
       data.InsertNextValue(lib.usgsSlabRangeDict[lib.usgsSlabKeys[Slab]]['Y'][1])
       fieldData.AddArray(data)

       data = vtk.vtkFloatArray()
       data.SetName('Longitude\nRange (deg)')
       minX = lib.usgsSlabRangeDict[lib.usgsSlabKeys[Slab]]['X'][0]
       if minX > 180:
           minX -= 360
       maxX = lib.usgsSlabRangeDict[lib.usgsSlabKeys[Slab]]['X'][1]
       if maxX > 180:
           maxX -= 360
       xMin = min([minX,maxX])
       xMax = max([minX,maxX])
       data.InsertNextValue(xMin)
       data.InsertNextValue(xMax)
       fieldData.AddArray(data)

       data = vtk.vtkFloatArray()
       data.SetName('Depth to Slab\nRange (km)')
       data.InsertNextValue(abs(lib.usgsSlabRangeDict[lib.usgsSlabKeys[Slab]]['Z'][1]))
       data.InsertNextValue(abs(lib.usgsSlabRangeDict[lib.usgsSlabKeys[Slab]]['Z'][0]))
       fieldData.AddArray(data)

       data = vtk.vtkStringArray()
       data.SetName('Source')
       data.InsertNextValue(lib.usgsSlab_URL)
       Label = ' '.join(['USGS Slab 1.0:',lib.usgsSlabValues[Slab].strip(),'from',urlparse.urlparse(lib.usgsSlab_URL).netloc.strip()])
       data.InsertNextValue(lib.usgsSlabKeys[Slab])
       fieldData.AddArray(data)

    RenameSource(' '.join([Label.strip(),Label2.strip()]))

def RequestInformation():
    sys.path.insert(0, "EMC_SRC_PATH")
    import IrisEMC_Paraview_Lib as lib
    from paraview import util

    Latitude_Begin,Latitude_End,Longitude_Begin,Longitude_End = lib.getArea(Area,Latitude_Begin,Latitude_End,Longitude_Begin,Longitude_End)

    if len(Alternate_FileName.strip()) > 0:
         FileName        = Alternate_FileName
         Label           = ' '.join(['SLAB',lib.fileName(Alternate_FileName).strip()])
    else:
         FileName        = lib.usgsSlabKeys[Slab]
         Label           = ' '.join(['USGS Slab 1.0 -',lib.usgsSlabValues[Slab].strip()])
    
    fileFound,address,source = lib.findFile(FileName,loc='EMC_SLABS_PATH')
    if not fileFound:
        raise Exception('model file "'+address+'" not found! Aborting.')

    nx,ny,nz = lib.getSlabExtent(address,(Latitude_Begin,Longitude_Begin),(Latitude_End,Longitude_End),inc=Sampling)
    # ABSOLUTELY NECESSARY FOR THE READER TO WORK:
    util.SetOutputWholeExtent(self, [0,nx-1, 0,ny-1, 0,nz-1])
