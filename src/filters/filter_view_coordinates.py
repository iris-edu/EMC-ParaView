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
    # R.1.2018.354
    import sys
    sys.path.insert(0, "EMC_SRC_PATH")
    from operator import itemgetter
    from datetime import datetime
    import numpy as np
    from vtk.numpy_interface import dataset_adapter as dsa
    from vtk.util import numpy_support
    import IrisEMC_Paraview_Lib as lib
    import paraview.simple as simple

    views = simple.GetViews(viewtype="SpreadSheetView")
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
    try:
        np = pdi.GetNumberOfPoints()
    except Exception:
        raise Exception('Invalid input!')

    na = pdi.GetPointData().GetNumberOfArrays()
    val_arrays = []
    for i in range(na):
        val_arrays.append(pdi.GetPointData().GetArray(i))

    latitude = {}
    longitude = {}
    value = {}
    depth = {}
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
        key = "%0.2f" % this_depth
        if key not in list(latitude.keys()):
            latitude[key] = []
            longitude[key] = []
            value[key] = []

        # need to control precision to have a reasonable sort order
        # note that these coordinates are recomputed
        if key not in list(depth.keys()):
            depth[key] = float('%0.4f' % this_depth)
        latitude[key].append(float('%0.4f' % lat))
        longitude[key].append(float('%0.4f' % lon))
        value_array = []
        for j in range(na):
            value_array.append(float(val_arrays[j].GetTuple1(i)))
        value[key].append(value_array)

    # store boundary metadata
    field_data = poly_data.GetFieldData()
    field_data.AllocateArrays(5)  # number of fields

    depth_data = vtk.vtkFloatArray()
    depth_data.SetName('depth')

    lat_data = vtk.vtkFloatArray()
    lat_data.SetName('latitude')

    lon_data = vtk.vtkFloatArray()
    lon_data.SetName('longitude')

    val_data = []
    for j in range(na):
        val_data.append(vtk.vtkFloatArray())
        val_data[j].SetName('value(%s)' % pdi.GetPointData().GetArray(j).GetName())

    depth_keys = list(latitude.keys())

    for i in range(len(depth_keys)):
        depth_key = depth_keys[i]
        lon_list = longitude[depth_key]
        lat_list = latitude[depth_key]
        val_list = value[depth_key]
        point_list = list(zip(lat_list, lon_list, val_list))
        point_list.sort(key=itemgetter(0, 1))

        for index, data in enumerate(point_list):
            depth_data.InsertNextValue(float(depth[depth_key]))
            lat_data.InsertNextValue(float(data[0]))
            lon_data.InsertNextValue(float(data[1]))
            for k in range(na):
                point_data = data[2]
                val_data[k].InsertNextValue(point_data[k])

    field_data.AddArray(lat_data)
    field_data.AddArray(lon_data)
    field_data.AddArray(depth_data)
    for j in range(na):
        field_data.AddArray(val_data[j])

    if len(Label.strip()) > 0:
        simple.RenameSource(Label)

    pdo.SetFieldData(field_data)

