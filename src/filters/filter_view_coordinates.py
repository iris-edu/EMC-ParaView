Name = 'viewCoordinates'
Label = 'View Coordinates'
FilterCategory = 'IRIS EMC'
Help = 'Display boundary coordinate information of the input in terms of lat, lon, depth'

NumberOfInputs = 1
OutputDataType = 'vtkTable'

Properties = dict(
    Label = ''
)

PropertiesHelp = dict(
    view_coordinates = "",
)

def RequestData():
    # R.0.2018.080
    import sys
    sys.path.insert(0, "EMC_SRC_PATH")
    from datetime import datetime
    import numpy as np
    from vtk.numpy_interface import dataset_adapter as dsa
    from vtk.util import numpy_support
    import IrisEMC_Paraview_Lib as lib
    import paraview.simple as simple

    views = simple.GetViews(viewtype="SpreadSheetView")
    if len(views) > 0:
       simple.Delete(views[0])
    else:
       view = simple.GetActiveView()
       layout = simple.GetLayout(view)
       locationId = layout.SplitViewVertical(view=view ,fraction=0.7)

    myId    = simple.GetActiveSource().Input.GetGlobalIDAsString()
    proxies = simple.GetSources()
    proxyList = []
    for key in proxies:
       listElt = {}
       listElt['name'] = key[0]
       listElt['id'] = key[1]
       proxy = proxies[key]
       parentId = '0'
       if hasattr(proxy, 'Input'):
           parentId = proxy.Input.GetGlobalIDAsString()
       listElt['parent'] = parentId
       proxyList.append(listElt)


    pdi = self.GetInput() # VTK PolyData Type
    np = pdi.GetNumberOfPoints()
    depthMin = 9999999999999.0
    depthMax = -9999999999999.0
    latitude  = {}
    longitude = {}

    pdo = self.GetOutput() # VTK Table Type
    polyData  = vtk.vtkPolyData()
    dataPoints = vtk.vtkPoints()

    if len(Label.strip()) <= 0:
         pid = simple.GetActiveSource().Input.GetGlobalIDAsString()
         proxies = simple.GetSources()
         for key in proxies:
             if key[1] == pid:
                 Label = " ".join(["Coordinates View:",key[0]])
                 break
    for i in range(np):
        point = pdi.GetPoints().GetPoint(i)
        (lat,lon,depth) = lib.xyz2llz(point[0],point[1],point[2])
        dataPoints.InsertNextPoint((lat,lon,depth))
        key = "%0.1f"%(depth)
        if depthMin >= float(key):
           depthMin = float(key)
           depthMinKey = key
        if depthMax <= float(key):
           depthMax = float(key)
           depthMaxKey = key
        if key not in latitude.keys():
            latitude[key] =[]
            longitude[key] = []
        latitude[key].append(float("%0.1f"%(lat)))
        longitude[key].append(float("%0.1f"%(lon)))

    # store boundary metadata

    fieldData = polyData.GetFieldData()
    fieldData.AllocateArrays(3) # number of fields

    depthData = vtk.vtkStringArray()
    depthData.SetName('Depth\n(km)')

    data = vtk.vtkStringArray()
    data.SetName('Corners (lat,lon)\n(degrees)')

    depthKeys = [depthMinKey,depthMaxKey]
    if depthMinKey == depthMaxKey:
        depthKeys = [depthMinKey]
    for i in range(len(depthKeys)):
       depthKey = depthKeys[i]
       borderLat = []
       borderLon = []
       oldMin = 999999999.0
       oldMax = -99999999.0
       lonList = list(set(sorted(longitude[depthKey])))
       for j in range(len(lonList)):
          lon = lonList[j]
          minVal = 999999999.0
          maxVal = -99999999.0
          for i in range(len(longitude[depthKey])):
             if longitude[depthKey][i] == lon:
                if latitude[depthKey][i] > maxVal:
                  maxVal = latitude[depthKey][i]
                if latitude[depthKey][i] < minVal:
                  minVal = latitude[depthKey][i]
          if oldMin != minVal or j==len(lonList)-1:
             if abs(oldMin) < 9999.0:
                borderLat.append(oldMin)
                borderLon.append(lon)
             borderLat.append(minVal)
             borderLon.append(lon)
             oldMin = minVal
          if oldMax != maxVal or j==len(lonList)-1:
             if abs(oldMax) < 9999.0:
                borderLat.append(oldMax)
                borderLon.append(lon)
             borderLat.append(maxVal)
             borderLon.append(lon)
             oldMax = maxVal
       borderList = zip(borderLat, borderLon)
       borderList.sort()
       borderList = list(set(borderList))
       min1 = borderList[0][0]
       max1 = borderList[0][0]
       for i in range(len(borderList)):
          if borderList[i][0] < min1:
             min1 = borderList[i][0]
          if borderList[i][0] > max1:
             max1 = borderList[i][0]
       minList = []
       maxList = []
       for i in range(len(borderList)):
          if borderList[i][0] ==  min1:
             minList.append(borderList[i][1])
          if borderList[i][0] ==  max1:
             maxList.append(borderList[i][1])
       depthData.InsertNextValue(depthKey)
       data.InsertNextValue("%0.1f, %0.1f"%(min1,min(minList)))
       if min(minList) != max(minList):
          depthData.InsertNextValue(" ")
          data.InsertNextValue("%0.1f, %0.1f"%(min1,max(minList)))
       depthData.InsertNextValue(" ")
       data.InsertNextValue("%0.1f, %0.1f"%(max1,max(maxList)))
       if min(maxList) != max(maxList):
         depthData.InsertNextValue(" ")
         data.InsertNextValue("%0.1f, %0.1f"%(max1,min(maxList)))
    fieldData.AddArray(data)
    fieldData.AddArray(depthData)

    if len(Label.strip()) > 0:
        simple.RenameSource(Label)

    pdo.SetFieldData(fieldData)


