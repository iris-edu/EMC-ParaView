Name = 'Lat-Lon-Depth_X-Y-Z'
Label = 'Convert Coordinates'
FilterCategory = 'IRIS EMC'
Help = 'Converts latitude, longitude and ,depth to X, Y and Z (Or Vice Versa)'

ExtraXml = '''\
<IntVectorProperty
    name="Coordinate_Type"
    command="SetParameter"
    number_of_elements="1"
    initial_string="coordinate_drop_down_menu"
    default_values="0">
    <EnumerationDomain name="enum_type">
          <Entry value="0" text="Latitude, Longitude, Depth"/>
          <Entry value="1" text="X, Y, Z"/>
    </EnumerationDomain>
    <Documentation>
        Choose type of coordinates provided
    </Documentation>
</IntVectorProperty>
'''

NumberOfInputs = 0
OutputDataType = 'vtkTable'

Properties = dict(
    Coordinate_Type=0,
    X_or_Longitude=-113.0,
    Y_or_Latitude=20.0,
    Z_or_Depth=50.0
)

def RequestData():
    # R.0.2018.080
    import sys
    import numpy as np
    import os
    import paraview.simple as simple
    sys.path.insert(0, r'EMC_SRC_PATH')
    import IrisEMC_Paraview_Lib as lib

    views = simple.GetViews(viewtype="SpreadSheetView")
    if len(views) > 0:
       simple.Delete(views[0])
    else:
       view = simple.GetActiveView()
       layout = simple.GetLayout(view)

    pdo = self.GetOutput()  # vtkTable

    if Coordinate_Type == 0:
       lon = X_or_Longitude
       lat = Y_or_Latitude
       depth = Z_or_Depth
       x, y, z = lib.llz2xyz(lat, lon, depth)
    else:
       x = X_or_Longitude
       y = Y_or_Latitude
       z = Z_or_Depth
       lat, lon, depth = lib.xyz2llz(x, y, z)

    # store metadata
    fieldData = pdo.GetFieldData()
    fieldData.AllocateArrays(3)  # number of fields

    fieldData = pdo.GetFieldData()
    data = vtk.vtkFloatArray()
    data.SetName('Longitude, Latitude, Depth')
    data.InsertNextValue(lon)
    data.InsertNextValue(lat)
    data.InsertNextValue(depth)
    fieldData.AddArray(data)

    data = vtk.vtkFloatArray()
    data.SetName('X, Y, Z')
    data.InsertNextValue(x)
    data.InsertNextValue(y)
    data.InsertNextValue(z)
    fieldData.AddArray(data)

    pdo.SetFieldData(fieldData)

def RequestInformation():
    pass
