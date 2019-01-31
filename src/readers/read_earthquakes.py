Name = 'ReadEarthquakes'
Label = 'Show Earthquake Locations'
FilterCategory = 'IRIS EMC'
Help = 'Get and display earthquake locations from USGS.'

ExtraXml = '''\
<IntVectorProperty
    name="Data_Source"
    command="SetParameter"
    number_of_elements="1"
    initial_string="drop_down_menu"
    default_values="0">
    <EnumerationDomain name="enum_source">
          EARTHQUAKE_DROP_DOWN
    </EnumerationDomain>
    <Documentation>
        Choose earthquake catalogue service
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
OutputDataType = 'vtkPolyData'

Properties = dict(
    Area=1,
    Data_Source=0,
    Alternate_FileName="",
    Latitude_Begin='',
    Latitude_End='',
    Longitude_Begin='',
    Longitude_End='',
    Depth_Begin=0,
    Depth_End=200,
    Magnitude_Begin=6,
    Magnitude_End=10,
    Vertical_Scaling=1,
    Frame_Length_sec=3600,
    Frame_Tag='',
    Time_Begin='2000-01-01',
    Time_End=''
)


def RequestData():
    # V.2019.030
    import sys
    sys.path.insert(0, r'EMC_SRC_PATH')
    import paraview.simple as simple
    import numpy as np
    import csv
    import os
    import datetime
    from vtk.util import numpy_support as nps
    import IrisEMC_Paraview_Lib as Lib
    import IrisEMC_Paraview_Utils as Utils
    import urlparse

    pts = vtk.vtkPoints()
    Latitude_Begin, Latitude_End, Longitude_Begin, Longitude_End = Lib.get_area(Area, Latitude_Begin, Latitude_End,
                                                                                Longitude_Begin, Longitude_End)
    label2 = " - %s (lat:%0.1f,%0.1f, lon:%0.1f,%0.1f, depth:%0.1f-%0.1f)" % (Lib.areaValues[Area], Latitude_Begin,
                                                                              Latitude_End, Longitude_Begin,
                                                                              Longitude_End, Depth_Begin, Depth_End)

    # make sure we have input files
    if not Time_End.strip():
        Time_End = datetime.datetime.today().strftime('%Y-%m-%d')
    query = Lib.earthquakeQuery % (Time_Begin, Time_End, Magnitude_Begin, Magnitude_End, Depth_Begin, Depth_End,
                                   Latitude_Begin, Latitude_End, Longitude_Begin, Longitude_End)
    Alternate_FileName = Alternate_FileName.strip()
    if len(Alternate_FileName) <= 0:
        eqFile = Lib.query2filename(query, url=Lib.earthquakeKeys[Data_Source])
        query = '?'.join([Lib.earthquakeKeys[Data_Source], query])
        fileFound, address, source = Lib.find_file(eqFile, loc=r'EMC_EARTHQUAKES_PATH', query=query)
    else:
        fileFound, address, source = Lib.find_file(Alternate_FileName, loc=r'EMC_EARTHQUAKES_PATH')
    if not fileFound:
        raise Exception('earthquake catalog file "' + address +
                        '" not found! Please provide the full path or UR for the file. Aborting.')
    (params, lines) = Lib.read_geocsv(address)

    pdo = self.GetOutput()  # vtkPoints
    column_keys = Lib.columnKeys
    for key in Lib.columnKeys.keys():
        if key in params.keys():
            column_keys[key] = params[key]

    origin = None
    if 'source' in params:
        origin = params['source']
        this_label = urlparse.urlparse(origin).netloc
    else:
        try:
            this_label = urlparse.urlparse(Alternate_FileName).netloc
        except:
            this_label = Alternate_FileName

    header = params['header']
    lat_index = None
    lon_index = None
    depth_index = None
    mag_index = None
    time_index = None
    for index, value in enumerate(header):
        if value.strip().lower() == column_keys['longitude_column'].lower():
            lon_index = index
        elif value.strip().lower() == column_keys['latitude_column'].lower():
            lat_index = index
        elif value.strip().lower() == column_keys['depth_column'].lower():
            depth_index = index
        elif value.strip().lower() == column_keys['magnitude_column'].lower():
            mag_index = index
        elif value.strip().lower() == column_keys['time_column'].lower():
            time_index = index

    scalar_m = vtk.vtkFloatArray()
    scalar_m.SetNumberOfComponents(1)
    scalar_m.SetName("magnitude")
    scalar_d = vtk.vtkFloatArray()
    scalar_d.SetNumberOfComponents(1)
    scalar_d.SetName("depth")
    scalar_t = vtk.vtkLongArray()
    scalar_t.SetNumberOfComponents(1)
    scalar_t.SetName("year-month")
    lat = []
    lon = []
    depth = []
    mag = []
    time = []
    frame_tag = Frame_Tag.strip()
    frame = dict()
    frame_key = Frame_Length_sec

    for i in range(len(lines)):
        line = lines[i].strip()
        values = line.strip().split(params['delimiter'].strip())
        lat_value = float(values[lat_index])
        lat.append(lat_value)
        lon_value = float(values[lon_index])
        lon.append(lon_value)
        depth_value = float(values[depth_index])
        depth.append(depth_value)
        mag_value = float(values[mag_index])
        mag.append(mag_value)
        time_value = values[time_index]
        time.append(time_value)

        # check conditions again in case data came from a file
        if not (float(Latitude_Begin) <= lat_value <= float(Latitude_End) and
                float(Longitude_Begin) <= lon_value <= float(Longitude_End) and
                float(Depth_Begin) <= depth_value <= float(Depth_End) and
                float(Magnitude_Begin) <= mag_value <= float(Magnitude_End)):
            continue

        if Latitude_Begin <= lat[-1] <= Latitude_End and Longitude_Begin <= lon[-1] <= Longitude_End:
            x, y, z = Lib.llz2xyz(lat[-1], lon[-1], depth[-1])
            pts.InsertNextPoint(x, y, z)
            scalar_m.InsertNextValue(mag[-1])
            scalar_d.InsertNextValue(depth[-1])
            day_value = Utils.datetime_to_int(time[-1], level='day')
            scalar_t.InsertNextValue(day_value)
            if frame_tag:
                frame_time = int(Utils.datetime_to_float(time_value) - Utils.datetime_to_float(Time_Begin))
                if frame_time <= frame_key:
                    frame[str(frame_key)] = '%s\n%f,%f,%f,%0.2f,%0.1f,%d' % (
                        frame[str(frame_key)], x, y, z, depth[-1], mag[-1], day_value)
                else:
                    frame_key += Frame_Length_sec
                    frame[str(frame_key)] = '%f,%f,%f,%0.2f,%0.1f,%d' % (x, y, z, depth[-1], mag[-1], day_value)

    # save animation frames
    if frame_tag:
        Utils.remove_files(os.path.join('EMC_EQ_ANIMATION_PATH', '%s_*.txt') % frame_tag)
        key_list = [int(x) for x in frame.keys()]
        key_list.sort()
        key0 = key_list[0]
        eq_list = 'X,Y,Z,Depth,Mag,Year-Month'
        for i, key in enumerate(key_list):
            eq_list = '%s\n%s' % (eq_list, frame[str(key)])
            with open(os.path.join('EMC_EQ_ANIMATION_PATH', '%s_%012d.txt' % (frame_tag, key - key0)), 'w') as fp:
                fp.write('%s' % eq_list)
    pdo.SetPoints(pts)
    pdo.GetPointData().AddArray(scalar_m)
    pdo.GetPointData().AddArray(scalar_d)
    pdo.GetPointData().AddArray(scalar_t)

    if len(this_label.strip()) > 0:
        simple.RenameSource(' '.join(['Earthquake locations:', 'from', this_label.strip(), label2.strip()]))

    # store metadata
    field_data = pdo.GetFieldData()
    field_data.AllocateArrays(3)  # number of fields

    data = vtk.vtkFloatArray()
    data.SetName('Latitude\nRange (deg)')
    data.InsertNextValue(min(lat))
    data.InsertNextValue(max(lat))
    field_data.AddArray(data)

    data = vtk.vtkFloatArray()
    data.SetName('Longitude\nRange (deg)')
    data.InsertNextValue(min(lon))
    data.InsertNextValue(max(lon))
    field_data.AddArray(data)

    data = vtk.vtkFloatArray()
    data.SetName('Depth\nRange (km)')
    data.InsertNextValue(min(depth))
    data.InsertNextValue(max(depth))
    field_data.AddArray(data)

    data = vtk.vtkFloatArray()
    data.SetName('Magnitude\nRange')
    data.InsertNextValue(min(mag))
    data.InsertNextValue(max(mag))
    field_data.AddArray(data)

    data = vtk.vtkIntArray()
    data.SetName('Max. Event\nCount')
    data.InsertNextValue(len(mag))
    field_data.AddArray(data)

    data = vtk.vtkStringArray()
    data.SetName('Start Date')
    data.InsertNextValue(Time_Begin)
    field_data.AddArray(data)

    data = vtk.vtkStringArray()
    data.SetName('End Date')
    data.InsertNextValue(Time_End)
    field_data.AddArray(data)

    data = vtk.vtkStringArray()
    data.SetName('Source')
    if origin is not None:
        data.InsertNextValue(origin)

    data.InsertNextValue(source)
    field_data.AddArray(data)

    pdo.SetFieldData(field_data)


def RequestInformation():
    import datetime
    from paraview import util
    sys.path.insert(0, r'EMC_SRC_PATH')
    import IrisEMC_Paraview_Lib as Lib

    Latitude_Begin, Latitude_End, Longitude_Begin, Longitude_End = Lib.get_area(Area, Latitude_Begin, Latitude_End,
                                                                                Longitude_Begin, Longitude_End)
    if not Time_End.strip():
        Time_End = datetime.datetime.today().strftime('%Y-%m-%d')
    query = Lib.earthquakeQuery % (Time_Begin, Time_End, Magnitude_Begin, Magnitude_End, Depth_Begin, Depth_End,
                                   Latitude_Begin, Latitude_End, Longitude_Begin, Longitude_End)

    Alternate_FileName = Alternate_FileName.strip()
    if len(Alternate_FileName) <= 0:
        eq_file = Lib.query2filename(query, url=Lib.earthquakeKeys[Data_Source])
        query = '?'.join([Lib.earthquakeKeys[Data_Source], query])
        file_found, address, source = Lib.find_file(eq_file, loc=r'EMC_EARTHQUAKES_PATH', query=query)
    else:
        file_found, address, source = Lib.find_file(Alternate_FileName, loc=r'EMC_EARTHQUAKES_PATH')
    if not file_found:
        raise Exception('earthquake catalog file "' + address +
                        '" not found! Please provide the full path or UR for the file. Aborting.')
    (params, lines) = Lib.read_geocsv(address)
    num = len(lines)
    # ABSOLUTELY NECESSARY FOR THE READER TO WORK:
    util.SetOutputWholeExtent(self, [0, num - 1, 0, num - 1, 0, num - 1])
