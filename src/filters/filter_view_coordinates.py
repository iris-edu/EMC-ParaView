Name = 'viewCoordinates'
Label = 'View Coordinates'
FilterCategory = 'IRIS EMC'
Help = 'Display coordinate information of the input in terms of lat, lon, depth'

NumberOfInputs = 1
OutputDataType = 'vtkTable'

Properties = dict(
    Label=''
)

PropertiesHelp = dict(
    view_coordinates='',
)

def RequestData():
    # R.1.2018.352
    import sys
    sys.path.insert(0, "EMC_SRC_PATH")
    from datetime import datetime
    import numpy as np
    from vtk.numpy_interface import dataset_adapter as dsa
    from vtk.util import numpy_support
    import IrisEMC_Paraview_Lib as lib
    import paraview.simple as simple

    views = simple.GetViews(viewtype="SpreadSheetView")
    print len(views)
    if len(views) > 0:
        # set active view
        view = simple.SetActiveView(views[0])
    else:
        view = simple.GetActiveView()
        layout = simple.GetLayout(view)
        location_id = layout.SplitViewVertical(view=view, fraction=0.7)

    myId = simple.GetActiveSource().Input.GetGlobalIDAsString()

    proxies = simple.GetSources()
    proxyList = []
    for key in proxies:
        list_elt = dict()
        list_elt['name'] = key[0]
        list_elt['id'] = key[1]
        proxy = proxies[key]
        parent_id = '0'
        if hasattr(proxy, 'Input'):
            parent_id = proxy.Input.GetGlobalIDAsString()
        list_elt['parent'] = parent_id
        proxyList.append(list_elt)
 
    pdi = self.GetInput()  # VTK PolyData Type
    np = pdi.GetNumberOfPoints()
    latitude = {}
    longitude = {}
    depth = []

    pdo = self.GetOutput()  # VTK Table Type
    poly_data = vtk.vtkPolyData()
    data_points = vtk.vtkPoints()

    if len(Label.strip()) <= 0:
        pid = simple.GetActiveSource().Input.GetGlobalIDAsString()
        proxies = simple.GetSources()
        for key in proxies:
            if key[1] == pid:
                Label = " ".join(["Coordinates:", key[0]])
                break

    for i in range(np):
        point = pdi.GetPoints().GetPoint(i)
        (lat, lon, this_depth) = lib.xyz2llz(point[0], point[1], point[2])
        data_points.InsertNextPoint((lat, lon, this_depth))

        key = "%0.4f" % this_depth
        if key not in latitude.keys():
            latitude[key] = []
            longitude[key] = []
            depth.append(float(this_depth))
        latitude[key].append(float(lat))
        longitude[key].append(float(lon))

    # store boundary metadata
    field_data = poly_data.GetFieldData()
    field_data.AllocateArrays(4)  # number of fields

    depth_data = vtk.vtkFloatArray()
    depth_data.SetName('Depth\n(km)')

    lat_data = vtk.vtkFloatArray()
    lat_data.SetName('Latitude\n(degrees)')

    lon_data = vtk.vtkFloatArray()
    lon_data.SetName('Longitude\n(degrees)')

    depth_keys = latitude.keys()

    for i in range(len(depth_keys)):
        depth_key = depth_keys[i]
        lon_list = longitude[depth_key]
        lat_list = latitude[depth_key]
        point_list = zip(lat_list, lon_list)
        point_list.sort()
        for j in range(len(point_list)):
            depth_data.InsertNextValue(depth[i])
            lat_data.InsertNextValue(float(point_list[j][0]))
            lon_data.InsertNextValue(float(point_list[j][1]))

    field_data.AddArray(lat_data)
    field_data.AddArray(lon_data)
    field_data.AddArray(depth_data)

    if len(Label.strip()) > 0:
        simple.RenameSource(Label)

    pdo.SetFieldData(field_data)
