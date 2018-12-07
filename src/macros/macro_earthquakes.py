# trace generated using paraview version 5.6.0-RC2
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Show Earthquake Locations'
showEarthquakeLocations1 = ShowEarthquakeLocations(AlternateFileName='')

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [876, 884]

# show data in view
showEarthquakeLocations1Display = Show(showEarthquakeLocations1, renderView1)

# trace defaults for the display properties.
showEarthquakeLocations1Display.Representation = 'Surface'
showEarthquakeLocations1Display.ColorArrayName = [None, '']
showEarthquakeLocations1Display.OSPRayScaleArray = 'magnitude'
showEarthquakeLocations1Display.OSPRayScaleFunction = 'PiecewiseFunction'
showEarthquakeLocations1Display.SelectOrientationVectors = 'None'
showEarthquakeLocations1Display.ScaleFactor = 0.1821804702281952
showEarthquakeLocations1Display.SelectScaleArray = 'None'
showEarthquakeLocations1Display.GlyphType = 'Arrow'
showEarthquakeLocations1Display.GlyphTableIndexArray = 'None'
showEarthquakeLocations1Display.GaussianRadius = 0.009109023511409759
showEarthquakeLocations1Display.SetScaleArray = ['POINTS', 'magnitude']
showEarthquakeLocations1Display.ScaleTransferFunction = 'PiecewiseFunction'
showEarthquakeLocations1Display.OpacityArray = ['POINTS', 'magnitude']
showEarthquakeLocations1Display.OpacityTransferFunction = 'PiecewiseFunction'
showEarthquakeLocations1Display.DataAxesGrid = 'GridAxesRepresentation'
showEarthquakeLocations1Display.SelectionCellLabelFontFile = ''
showEarthquakeLocations1Display.SelectionPointLabelFontFile = ''
showEarthquakeLocations1Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
showEarthquakeLocations1Display.DataAxesGrid.XTitleFontFile = ''
showEarthquakeLocations1Display.DataAxesGrid.YTitleFontFile = ''
showEarthquakeLocations1Display.DataAxesGrid.ZTitleFontFile = ''
showEarthquakeLocations1Display.DataAxesGrid.XLabelFontFile = ''
showEarthquakeLocations1Display.DataAxesGrid.YLabelFontFile = ''
showEarthquakeLocations1Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
showEarthquakeLocations1Display.PolarAxes.PolarAxisTitleFontFile = ''
showEarthquakeLocations1Display.PolarAxes.PolarAxisLabelFontFile = ''
showEarthquakeLocations1Display.PolarAxes.LastRadialAxisTextFontFile = ''
showEarthquakeLocations1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# reset view to fit data
# renderView1.ResetCamera()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

# change representation type
showEarthquakeLocations1Display.SetRepresentationType('Point Gaussian')

# set scalar coloring
ColorBy(showEarthquakeLocations1Display, ('POINTS', 'magnitude'))

# rescale color and/or opacity maps used to include current data range
showEarthquakeLocations1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
showEarthquakeLocations1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'magnitude'
magnitudeLUT = GetColorTransferFunction('magnitude')

# get opacity transfer function/opacity map for 'magnitude'
magnitudePWF = GetOpacityTransferFunction('magnitude')

# Properties modified on showEarthquakeLocations1Display
showEarthquakeLocations1Display.GaussianRadius = 0.005920865282416344

#### saving camera placements for all active views

# current camera placement for renderView1
# renderView1.CameraPosition = [0.0033947527408599854, -0.5507959313690662, 5.226825777325647]
# renderView1.CameraFocalPoint = [0.0033947527408599854, -0.5507959313690662, 0.05025723576545715]
# renderView1.CameraParallelScale = 1.3406037944044775

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).