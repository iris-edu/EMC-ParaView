# R.0.2018.080
#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Show Earthquake Locations'
showEarthquakeLocations1 = ShowEarthquakeLocations(AlternateFileName='')

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1501, 958]

# show data in view
showEarthquakeLocations1Display = Show(showEarthquakeLocations1, renderView1)

# trace defaults for the display properties.
showEarthquakeLocations1Display.Representation = 'Surface'
showEarthquakeLocations1Display.ColorArrayName = [None, '']
showEarthquakeLocations1Display.OSPRayScaleArray = 'magnitude'
showEarthquakeLocations1Display.OSPRayScaleFunction = 'PiecewiseFunction'
showEarthquakeLocations1Display.SelectOrientationVectors = 'None'
showEarthquakeLocations1Display.ScaleFactor = 0.1728173553943634
showEarthquakeLocations1Display.SelectScaleArray = 'None'
showEarthquakeLocations1Display.GlyphType = 'Arrow'
showEarthquakeLocations1Display.GlyphTableIndexArray = 'None'
showEarthquakeLocations1Display.DataAxesGrid = 'GridAxesRepresentation'
showEarthquakeLocations1Display.PolarAxes = 'PolarAxesRepresentation'
showEarthquakeLocations1Display.GaussianRadius = 0.0864086776971817
showEarthquakeLocations1Display.SetScaleArray = ['POINTS', 'magnitude']
showEarthquakeLocations1Display.ScaleTransferFunction = 'PiecewiseFunction'
showEarthquakeLocations1Display.OpacityArray = ['POINTS', 'magnitude']
showEarthquakeLocations1Display.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
showEarthquakeLocations1Display.ScaleTransferFunction.Points = [6.400000095367432, 0.0, 0.5, 0.0, 8.800000190734863, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
showEarthquakeLocations1Display.OpacityTransferFunction.Points = [6.400000095367432, 0.0, 0.5, 0.0, 8.800000190734863, 1.0, 0.5, 0.0]

# reset view to fit data
#renderView1.ResetCamera()

# update the view to ensure updated data information
renderView1.Update()

# change representation type
showEarthquakeLocations1Display.SetRepresentationType('Point Gaussian')

# change solid color
showEarthquakeLocations1Display.DiffuseColor = [1.0, 1.0, 0.0]

# Properties modified on showEarthquakeLocations1Display
showEarthquakeLocations1Display.GaussianRadius = 0.01

#### saving camera placements for all active views

# current camera placement for renderView1
# renderView1.CameraPosition = [-0.020621180534362793, -0.5458549745380878, 4.965568518458476]
# renderView1.CameraFocalPoint = [-0.020621180534362793, -0.5458549745380878, 0.026769012212753296]
# renderView1.CameraParallelScale = 1.278255372159319

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
