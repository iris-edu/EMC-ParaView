import sys
import os
import subprocess
import IrisEMC_Paraview_Param as param
import IrisEMC_Paraview_Utils as utils

"""
 Credits:

  This code closely follows build_plugins.sh script developed by  Bane Sullivan (http://banesullivan.com/)
  see:
       https://github.com/banesullivan/ParaViewGeophysics

 Description:

 This script builds all server manager XML plugins .py macros from the .py files that describe plugins and macros.
 There are 3 stages to this process:
    1. build the readers
    2. build the filters
    3. update the macros

 NOTE: plugins and macros are created from files with specific prefixex as follows:

           Filters     ->      './filters/filter_*.py'
           Readers     ->      './readers/read_*.py'
           Macros      ->      './macros/macro_*.py'

 History:
     2021-10-03 Manoch: v.2021.276 Python 3 r2
     2018-03-21 Manoch: v.2018.080
"""


class bcolors:
    def __init__(self):
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'


def extract_file_name(full_file_name):
    """
    for a given full file name, extract and return a file name without extension and path

    Parameters
    ----------
    full_file_name: str
       a full file name

    Returns
    -------
    filename: str
       file name without extension and path
    """
    file_name_w_ext = os.path.basename(full_file_name)
    file_name, file_extension = os.path.splitext(file_name_w_ext)
    return file_name


print(f"\n\n[INFO] installing under {utils.check_system()} OS\n\n")

#  Wrap READERS in XML.
print("\n\n[INFO] .... Attempting to wrap READERS in XML...\n")
for _file in os.listdir("readers"):
    if not _file.startswith("read_"):
        print(f'[WARN] ....skipped file: {_file}')
        continue
    print(f'[INFO] ....trying file: {_file}')

    input_file = os.path.join('readers', _file)
    filename = extract_file_name(_file)
    output_file = os.path.join(param.pathDict['EMC_PLUGINS_PATH'], f'{filename}.xml')
    try:
        subprocess.check_output([sys.executable, "python_filter_generator.py", input_file, output_file])
        print(f"[INFO] SUCCESS: {input_file} ---> {output_file}")
    except Exception as ex:
        print(f"[ERR] FAILED: {input_file} ---> {output_file}\n{ex}")
        pass

#  Wrap FILTERS in XML.
print("\n\n[INFO] .... Attempting to wrap FILTERS in XML...\n")
for _file in os.listdir("filters"):
    if not _file.startswith("filter_"):
        print(f'[WARN] ....skipped file: {_file}')
        continue
    print(f'[INFO]....trying file: {_file}')

    input_file = os.path.join('filters', _file)
    filename = extract_file_name(_file)
    output_file = os.path.join(param.pathDict['EMC_PLUGINS_PATH'], f"{filename}.xml")
    try:
        subprocess.check_output([sys.executable, "python_filter_generator.py", input_file, output_file])
        print(f"[INFO] SUCCESS: {input_file} ---> {output_file}")
    except Exception as ex:
        print(f"[ERR] FAILED: {input_file} ---> {output_file}\n{ex}")
        pass

#  Update MACRO.
print(f"\n\n[INFO].... Attempting to update MACROS ...\n")
for _file in os.listdir("macros"):
    if not _file.startswith("macro_"):
        print(f'[WARN] ....skipped file:{_file}')
        continue
    print(f'[INFO] ....trying file: {_file}')

    input_file = os.path.join('macros', _file)
    filename = extract_file_name(_file)
    output_file = os.path.join('..', 'macros', f"{filename.replace('macro_', '')}.py")
    try:
        subprocess.check_output([sys.executable, "python_macro_generator.py", input_file, output_file])
        print(f"[INFO] SUCCESS: {input_file} ---> {output_file}")
    except Exception as ex:
        print(f"[ERR] FAILED: {input_file} ---> {output_file}\n{ex}")
        pass
