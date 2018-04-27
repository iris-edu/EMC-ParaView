#
# -*- coding: UTF-8 -*-
#
################################################################################################
#
# NAME: IrisEMC_Paraview-Param.py - EMC ParaView Support parameters
#
#       http://ds.iris.edu/ds/products/emc/
#
# DESCRIPTION: These parameters are the default values for the IRIS EMC Paraview Python scripts
#
# Copyright (C) 2018  Product Team, IRIS Data Management Center
#
#    This is a free software; you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation; either version 3 of the
#    License, or (at your option) any later version.
#
#    This script is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License (GNU-LGPL) for more details.  The
#    GNU-LGPL and further information can be found here:
#    http://www.gnu.org/
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# HISTORY:
#    2018-04-27 Manoch: R.0.2018.117 updateid irisEMC_Files_URL
#    2018-04-23 Manoch: R.0.2018.113 updateid lat and lon limits for the world
#                       added very low resolution coastline data file
#    2018-03-21 Manoch: R.0.2018.080 release
#
#
# -*- coding: UTF-8 -*-
#
################################################################################################
#

import os
import IrisEMC_Paraview_Utils as utils 

################################################################################################
#
# sortDictByValue
#
################################################################################################
def sortDictByValue(thisDict):
    """
    Splits a Python dictionary to two lists containing keys and values sorted by values.

    Parameters
    ----------
    thisDict : dict
       a Python dictionary

    Returns
    -------
    keys: list
       list of keys in the distionary
    values: list
       list of values in the dictionary

    """
    from operator import itemgetter
    keys   = []
    values = []
    if len(thisDict.keys()) == 1:
       return thisDict.keys(), thisDict.values()

    for key, value in sorted(thisDict.items(), key = itemgetter(1)):
       keys.append(key)
       values.append(value)
    return keys, values


################################################################################################
#
# URLs
#
irisEMC_Files_URL   = "https://ds.iris.edu/files/products/emc/emc-files/"
usgsEvent_URL       = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=text"
usgsSlab_URL        = "https://earthquake.usgs.gov/static/lfs/data/slab/models/"

################################################################################################
#
# earthquake catalogue sources
#
earthquakeCatalogDict = {'https://earthquake.usgs.gov/fdsnws/event/1/query':'USGS Earthquake Hazards Program'}
earthquakeQuery       = "format=text&starttime=%s&minmag=%0.1f&maxmag=%0.1f&orderby=magnitude&mindepth=%0.1f&maxdepth=%0.1f&minlat=%0.2f&maxlat=%0.2f&minlon=%0.2f&maxlon=%0.2f&limit=%0i&nodata=404"

#
# sort the earthquake dictionary based on the values (organization)
#
(earthquakeKeys, earthquakeValues) = sortDictByValue(earthquakeCatalogDict)

################################################################################################
#
# volcano locations sources
#
volcanoLocationsDict  = {'http://geows.ds.iris.edu/geows-uf/wovodat/1/query':'WOVOdat'}
volcanoLocationsQuery = "getVolcanoLocations=true"

#
# sort volcano location sources  dictionary based on the values (organization)
#
(volcanoLocationsKeys, volcanoLocationsValues) = sortDictByValue(volcanoLocationsDict)

################################################################################################
#
# Paths
#
topDir          = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))

pathDict        = {'EMC_MAIN_PATH':topDir,
                   'EMC_PLUGINS_PATH':os.path.join(topDir,'plugins'),
                   'EMC_MACROS_PATH':os.path.join(topDir,'macros'),
                   'EMC_SRC_PATH':os.path.join(topDir,'src'),
                   'EMC_DATA_PATH':os.path.join(topDir,'data'),
                   'EMC_SCRATCH_PATH':os.path.join(topDir,'data','scratch'),
                   'EMC_SLABS_PATH':os.path.join(topDir,'data','slabs'),
                   'EMC_MODELS_PATH':os.path.join(topDir,'data','models'),
                   'EMC_BOUNDARIES_PATH':os.path.join(topDir,'data','boundaries'),
                   'EMC_VOLCANOES_PATH':os.path.join(topDir,'data','volcanoes'),
                   'EMC_EARTHQUAKES_PATH':os.path.join(topDir,'data','earthquakes')}

for key in pathDict.keys():
    utils.makePath(pathDict[key])

#
# default files
#
filesDict       = {'ETOPO5':'etopo5.nc', 'EMC_DEFAULT_MODEL':'wUS-SH-2010_percent.nc'}

#
# default column names for GeoCSV files. User can redefine these in the GeoCSV header
#
columnKeys      = {'latitude_column':'latitude','longitude_column':'longitude','depth_column':'depth','elevation_column':'elevation','magnitude_column':'magnitude'}

################################################################################################
#
# USGS Slab 1.0 files, will populate the drop down menu
#
usgsSlabDict = {'alu_slab1.0_clip.grd':'Alaska-Aleutians',
                'cas_slab1.0_clip.grd':'Cascadia',
                'izu_slab1.0_clip.grd':'Izu-Bonin',
                'ker_slab1.0_clip.grd':'Kermadec-Tonga',
                'kur_slab1.0_clip.grd':'Kamchatka/Kurils/Japan',
                'mex_slab1.0_clip.grd':'Central America',
                'phi_slab1.0_clip.grd':'Philippines',
                'ryu_slab1.0_clip.grd':'Ryukyu',
                'sam_slab1.0_clip.grd':'South America',
                'sco_slab1.0_clip.grd':'Scotia',
                'sol_slab1.0_clip.grd':'Solomon Islands',
                'van_slab1.0_clip.grd':'Santa Cruz Islands/Vanuatu/Loyalty Islands'}

#
# sort the SLAB dictionary based on the values (regions)
#
(usgsSlabKeys, usgsSlabValues) = sortDictByValue(usgsSlabDict)

#
# extent of the slab regions
#
usgsSlabRangeDict = {'alu_slab1.0_clip.grd':{'X':(167., 216),'Y':(50., 65.),'Z':(-278.8,-6.264)},
                     'cas_slab1.0_clip.grd':{'X':( -128.5, -120.5),'Y':(39., 52. ),'Z':(100.18,-4.99)},
                     'izu_slab1.0_clip.grd':{'X':(129., 148.),'Y':(11., 40.),'Z':(-686.764,-1.002)},
                     'ker_slab1.0_clip.grd':{'X':(174., 188.),'Y':(-39., -14.),'Z':(-700.35,-2.81)},
                     'kur_slab1.0_clip.grd':{'X':(129., 164.),'Y':(32., 56.5),'Z':(-724.18, -5.85)},
                     'mex_slab1.0_clip.grd':{'X':(254., 279.),'Y':(7., 21),'Z':(-294.83,0.402)},
                     'phi_slab1.0_clip.grd':{'X':(122., 128.),'Y':(7,15),'Z':(-224.68,-6.42)},
                     'ryu_slab1.0_clip.grd':{'X':(122., 139),'Y':(22., 38),'Z':(-287.93,0.78)},
                     'sam_slab1.0_clip.grd':{'X':(278., 300.),'Y':(-45., 5.),'Z':(-742.32,1.83)},
                     'sco_slab1.0_clip.grd':{'X':(328., 337. ),'Y':(-61., -55.),'Z':(-260.69, -4.88)},
                     'sol_slab1.0_clip.grd':{'X':(145., 165.),'Y':(-12., -2.),'Z':(-616.65,-1.81)},
                     'van_slab1.0_clip.grd':{'X':(164., 173.),'Y':(-23.5, -9.),'Z':(-331.3,-3.89)}}

################################################################################################
#
# Area   
#
areaDict = {'0':'Africa',
            '1':'Americas',
            '2':'Asia',
            '3':'Europe',
            '4':'Japan',
            '5':'North America',
            '6':'South America',
            '7':'Taiwan',
            '8':'USA',
            '9':'World'}

#
# sort the Area dictionary based on the values (regions)
#
(areaKeys, areaValues) = sortDictByValue(areaDict)

#
# extent of the areas
#
areaRangeDict = {'0':{'lat':(-35.,40.),'lon':(-20,55)},
                 '1':{'lat':(-60.,80.),'lon':(-170.,-30.)},
                 '2':{'lat':(0.,80.),'lon':(55.,179.9)},
                 '3':{'lat':(35.,75.),'lon':(-20.,50.)},
                 '4':{'lat':(24.,46.),'lon':(120.,150.)},
                 '5':{'lat':(10.,80.),'lon':(-170.,-50.)},
                 '6':{'lat':(-60.,20.),'lon':(-85.,-30)},
                 '7':{'lat':(21.5,25.5),'lon':(120.0,122.5)},
                 '8':{'lat':(25.,57.),'lon':(-125.,-66.5)},
                 '9':{'lat':(-90.,90.),'lon':(-180.,180.)}}

################################################################################################
#
# Boundary files that will appear in the drop down menu
#
boundariesDict = {'coastline_data_int.csv':'Coastline data: intermediate resolution',
                  'coastline_data_low.csv':'Coastline data: low resolution',
                  'coastline_data_very_low.csv':'Coastline data: very low resolution',
                  'national_boundaries_data.csv':'National boundaries + US state + Canadian province boundaries',
                  'plate_boundaries_divergent.csv':'Present-day plate boundaries: divergent margins',
                  'plate_boundaries_transform.csv':'Present-day plate boundaries: transform margins',
                  'plate_boundaries_convergent.csv':'Present-day plate boundaries: convergent margins'}
boundariesColor= {'coastline_data_int.csv':'1,1,1',
                  'coastline_data_low.csv':'1,1,1',
                  'coastline_data_very_low.csv':'1,1,1',
                  'national_boundaries_data.csv':'1,1,1',
                  'plate_boundaries_divergent.csv':'0.0, 0.3333333333333333, 1.0',
                  'plate_boundaries_transform.csv':'1.0, 0.0, 0.0',
                  'plate_boundaries_convergent.csv':'1.0, 1.0, 0.0'}

#
# sorted list of the boundary files based on values
#
(boundaryKeys, boundaryValues) = sortDictByValue(boundariesDict)
