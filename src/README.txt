2018-12-06

IRIS_EMC_Paraview/src:
----------------------
   Directory of all the installation and plugin scripts


- src/IrisEMC_Paraview_Lib.py
    IRIS EMC ParaView support Python library of functions called by the plugins

- src/IrisEMC_Paraview_Param.py
    IRIS EMC ParaView support Python parameter file that contains parameters accessed by the plugins
    User may change these parameters to change the default startup values.

- src/IrisEMC_Paraview_Utils.py
    IRIS EMC ParaView support Python library of utility functions called by the plugins

- src/build_plugins_macros.py
    A Python script to build the plugins. Anytime user modifies any of the python scripts, this script must be executed
    to update the plugins and macros

- src/python_filter_generator.py
   A python script to wrap the existing Python scripts into an XML plugin

- src/python_macro_generator.py
   A python script to prepare Python macros for installation

