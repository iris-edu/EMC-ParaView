 
Incorporated Research Institutions for Seismology (IRIS)
Data Management Center (DMC)
Data Products Team
IRIS Earth Model Collaboration (EMC) - ParaView support bundle

COMMENTS/QUESTIONS:

    Please contact manoch@iris.washington.edu

Python 3
2021-10-04
------------------------------------------------------------------------------------------------------------------------

 DESCRIPTION:

 This package provides a set of Python 3 programmable filters/sources to allow ParaView open-source, multi-platform data 
 analysis and visualization application (on macOS®, Linux®, and Windows® platforms) to display EMC netCDF/GeoCSV models 
 along with other auxiliary Earth data.  After installing this package (see INSTALL.txt) the plugins/macros in the 
 package will allow you to:

    - Draw Boundaries of:
        + very low-resolution, low-resolution or intermediate resolution coastlines
        + national, US states and Canadian provinces 
        + present-day plates (divergent, transform or convergent margins)
        + your own GeoCSV boundary files

    - Show Volcano Locations:
        + plot location of volcanoes using WOVOdat location data from ds.iris.edu
        + plot location of volcanoes using your GeoCSV volcano location or other data-point files

    - Show Earthquake Locations:
        + plot earthquake locations based on the FDSN event services
        + plot earthquake locations based on your local GeoCSV earthquake location file
 
    NOTE: For information on GeoCSV files, visit: http://geows.ds.iris.edu/documents/GeoCSV.pdf
    NOTE: We also offer Python scripts for converting model files from/to netCDF and GeoCSV formats.
          For more information, please visit: https://github.com/iris-edu/emc-tools
    NOTE: Unless data files are available locally, an Internet connection is required for data download
  
    - Show USGS Slab 1.0 - Display USGS Slab 1.0 models 
    - Draw grids - Draw latitude/longitude grid lines
    - Elevation data - Plot surface elevation changes using elevation data files 
    - Read Earth Models - Read and plot 2D and 3D Earth model files in netCDF and GeoCSV file format. 
                          The available EMC model files are at https://ds.iris.edu/files/products/emc/emc-files/
                          The model descriptions are available at http://ds.iris.edu/ds/products/emc-earthmodels/
      NOTE: You do not need to download the model files. Just insert the name of the file into the "FileName" 
            property box
    - Convert latitude, longitude and, depth to X, Y, and Z (Or Vice Versa) 
    - Display the coordinates (latitude, longitude, and depth) of an object in the Pipeline Browser.


 USAGE:
    You can work with plugins directly, or you can work with macros. Macros are wrappers for plugins that include 
    additional steps needed to tune the display. 

    PLUGINS:
    - From the "Sources --> IRIS EMC" menu, select the plugin of interest
    - The Area drop-down allows you to limit the plot to a particular geographic area, or you can define your region 
      by specifying the lat/lon limits

      NOTE: by populating any of the latitude or longitude limit boxes, you are modifying the corresponding limit of 
      the selected area

    - Click on Apply button to run the plugin. 
         + The following plugins will provide a display that you can tune by changing line, color, etc.:
              Draw Boundaries, Draw grids, Show USGS Slab 1.0 and Topo elevation data

         + The following plugins are of point type, and you need to instruct ParaView how to display them before you can 
            tune them by changing line, color, etc.:
              Show Earthquake Locations - set Representation to "Point Gaussian," and set Gaussian Radius to a smaller 
                number like 0.01
              Show Volcano Locations - set Representation to "Point Gaussian," Shared Preset to "Triangle," and set 
                Gaussian Radius to a smaller number like 0.005
              
         + The following plugin is of surface type, and you need to instruct ParaView how to display it before you can 
               tune them by changing line, color, etc.:
                   Read 2D Model and Read 3D Model - set Representation "Surface" and select the variable for coloring 
                   using the drop-down that shows "Solid Color"

    - Two additional plugins serve as convenience tools to obtain the coordinate information:
        + Convert Coordinates - a coordinate conversion tool that allows you to convert ParaView's Cartesian coordinates 
            to latitude, longitude, and depth
        + View Coordinates - to display coordinates (latitude, longitude, and depth) of a pipeline object 
            The objects created in the PipelineBrowser via the EMC plugins preserve the coordinate information. You may 
            review the coordinates under a SpreadSheetView using the drop-down menu. For objects in the PipelineBrowser 
            that are created from EMC objects using one of the ParaView tools like "Slice," select the object in the 
            PipelineBrowser, then in paraview menu select "Filters --> IRIS EMC" that will open a SpreadSheetView and 
            display coordinate information of that object.

    MACROS:
    - From ParaView's Macros menu, select "Add new macro..." and browse to the  IRIS_EMC_Paraview/macros directory and 
        add the macros you want.
    - From ParaView's Macros menu or ParaView's toolbar, click on the macro you want to run
    - Like plugins, adjust the display using the property panel

      NOTE: You can create your macros as described here: https://www.paraview.org/Wiki/Python_GUI_Tools
 
