# R.0.2018.080 
#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1863, 958]

# get layout
layout1 = GetLayout()

# split cell
layout1.SplitVertical(0, 0.5)

# set active view
SetActiveView(None)

# create a new 'Convert Coordinates'
convertCoordinates1 = ConvertCoordinates()

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024L
# uncomment following to set a specific view size
# spreadSheetView1.ViewSize = [400, 400]

# place view in the layout
layout1.AssignView(2, spreadSheetView1)

# show data in view
convertCoordinates1Display = Show(convertCoordinates1, spreadSheetView1)

# trace defaults for the display properties.
convertCoordinates1Display.FieldAssociation = 'Field Data'

# update the view to ensure updated data information
spreadSheetView1.Update()

#### saving camera placements for all active views

# current camera placement for renderView1

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).