# R.0.2018.080
#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Show Volcano Locations'
showVolcanoLocations1 = ShowVolcanoLocations(AlternateFileName='')
showVolcanoLocations1.Data_Source = 'WOVOdat'

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1501, 958]

# show data in view
showVolcanoLocations1Display = Show(showVolcanoLocations1, renderView1)

# trace defaults for the display properties.
showVolcanoLocations1Display.Representation = 'Surface'
showVolcanoLocations1Display.ColorArrayName = [None, '']
showVolcanoLocations1Display.OSPRayScaleArray = 'Latitude\nRange (deg)'
showVolcanoLocations1Display.OSPRayScaleFunction = 'PiecewiseFunction'
showVolcanoLocations1Display.SelectOrientationVectors = 'None'
showVolcanoLocations1Display.ScaleFactor = 0.17350171804428102
showVolcanoLocations1Display.SelectScaleArray = 'None'
showVolcanoLocations1Display.GlyphType = 'Arrow'
showVolcanoLocations1Display.GlyphTableIndexArray = 'None'
showVolcanoLocations1Display.DataAxesGrid = 'GridAxesRepresentation'
showVolcanoLocations1Display.PolarAxes = 'PolarAxesRepresentation'
showVolcanoLocations1Display.GaussianRadius = 0.08675085902214051
showVolcanoLocations1Display.SetScaleArray = [None, '']
showVolcanoLocations1Display.ScaleTransferFunction = 'PiecewiseFunction'
showVolcanoLocations1Display.OpacityArray = [None, '']
showVolcanoLocations1Display.OpacityTransferFunction = 'PiecewiseFunction'

# reset view to fit data
#renderView1.ResetCamera()

# update the view to ensure updated data information
renderView1.Update()

# change representation type
showVolcanoLocations1Display.SetRepresentationType('Point Gaussian')

# change solid color
showVolcanoLocations1Display.DiffuseColor = [1.0, 0.0, 0.0]

# Properties modified on showVolcanoLocations1Display
showVolcanoLocations1Display.GaussianRadius = 0.005

# Properties modified on showVolcanoLocations1Display
showVolcanoLocations1Display.ShaderPreset = 'Triangle'

#### saving camera placements for all active views

# current camera placement for renderView1
# renderView1.CameraPosition = [-0.1463538408279419, -0.5529114790260792, 4.934178739291951]
# renderView1.CameraFocalPoint = [-0.1463538408279419, -0.5529114790260792, 0.03968733549118042]
# renderView1.CameraParallelScale = 1.2667875913942117

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
