# Credits:
#
#  This code closely follows build_plugins.sh script developed by  Bane Sullivan (http://banesullivan.com/)
#  see:
#       https://github.com/banesullivan/ParaViewGeophysics
#
# Description:
#
# This script builds all server manager XML plugins .py macros from the .py files that describe plugins and macros.
# There are 3 stages to this process:
#    1. build the readers
#    2. build the filters
#    3. update the macros
#
# NOTE: plugins and macros are created from files with specific prefixex as follows:
# 
#           Filters     ->      './filters/filter_*.py'
#           Readers     ->      './readers/read_*.py'
#           Macros      ->      './macros/macro_*.py'
#
# History:
#
#     2018-03-21 Manoch:  R.0.2018.080
#
import sys
import os
import subprocess 
import IrisEMC_Paraview_Param as param
import IrisEMC_Paraview_Utils as utils

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

################################################################################################
#
# fileName
#
################################################################################################
def fileName(fullFileName):
    """
    for a given full file name, extract and return a file name without extension and path

    Parameters
    ----------
    fullFileName: str
       a full file name

    Returns
    -------
    filename: str
       file name without extension and path
    """
    filename_w_ext = os.path.basename(fullFileName)
    filename, file_extension = os.path.splitext(filename_w_ext)
    return filename

print "\n\n installing under %s OS\n\n" % utils.check_system()
#
#  wrap READERS in XML
#
print "\n\n.... Attempting to wrap READERS in XML...\n"
for file in os.listdir("readers"):
    if not file.startswith("read_"):
        print '**** WARNING ....skipped',file
        continue
    print '....trying',file

    inputFile = os.path.join('readers',file)
    filename = fileName(file)
    outputFile = os.path.join(param.pathDict['EMC_PLUGINS_PATH'],filename+'.xml')
    try:
      subprocess.check_output([sys.executable ,"python_filter_generator.py",inputFile,outputFile])
      print "++++ SUCCESS:",inputFile,"--->",outputFile
    except:
      print "---- FAILED:",inputFile,"--->",outputFile
      pass

#
#  wrap FILTERS in XML
#
print "\n\n.... Attempting to wrap FILTERS in XML...\n"
for file in os.listdir("filters"):
    if not file.startswith("filter_"):
        print '**** WARNING ....skipped',file
        continue
    print '....trying',file

    inputFile = os.path.join('filters',file)
    filename = fileName(file)
    outputFile = os.path.join(param.pathDict['EMC_PLUGINS_PATH'],filename+'.xml')
    try:
      subprocess.check_output([sys.executable ,"python_filter_generator.py",inputFile,outputFile])
      print "++++ SUCCESS:",inputFile,"--->",outputFile
    except:
      print "---- FAILED:",inputFile,"--->",outputFile
      pass

#
#  update MACROS
#
print "\n\n.... Attempting to update MACROS ...\n"
for file in os.listdir("macros"):
    if not file.startswith("macro_"):
        print '**** WARNING ....skipped',file
        continue
    print '....trying',file

    inputFile = os.path.join('macros',file)
    filename = fileName(file)
    outputFile = os.path.join('..','macros',filename.replace('macro_','')+'.py')
    try:
      subprocess.check_output([sys.executable ,"python_macro_generator.py",inputFile,outputFile])
      print "++++ SUCCESS:",inputFile,"--->",outputFile
    except:
      print "---- FAILED:",inputFile,"--->",outputFile
      pass
