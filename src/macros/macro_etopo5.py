# R.0.218.080
#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'NOAA Etopo5 elevation data'
nOAAEtopo5elevationdata1 = NOAAEtopo5elevationdata()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1863, 958]

# show data in view
nOAAEtopo5elevationdata1Display = Show(nOAAEtopo5elevationdata1, renderView1)

# get color transfer function/color map for 'elev'
elevLUT = GetColorTransferFunction('elev')

# get opacity transfer function/opacity map for 'elev'
elevPWF = GetOpacityTransferFunction('elev')

# trace defaults for the display properties.
nOAAEtopo5elevationdata1Display.Representation = 'Surface'
nOAAEtopo5elevationdata1Display.ColorArrayName = ['POINTS', 'elev']
nOAAEtopo5elevationdata1Display.LookupTable = elevLUT
nOAAEtopo5elevationdata1Display.OSPRayScaleArray = 'elev'
nOAAEtopo5elevationdata1Display.OSPRayScaleFunction = 'PiecewiseFunction'
nOAAEtopo5elevationdata1Display.SelectOrientationVectors = 'None'
nOAAEtopo5elevationdata1Display.ScaleFactor = 0.18522241711616516
nOAAEtopo5elevationdata1Display.SelectScaleArray = 'elev'
nOAAEtopo5elevationdata1Display.GlyphType = 'Arrow'
nOAAEtopo5elevationdata1Display.GlyphTableIndexArray = 'elev'
nOAAEtopo5elevationdata1Display.DataAxesGrid = 'GridAxesRepresentation'
nOAAEtopo5elevationdata1Display.PolarAxes = 'PolarAxesRepresentation'
nOAAEtopo5elevationdata1Display.ScalarOpacityFunction = elevPWF
nOAAEtopo5elevationdata1Display.ScalarOpacityUnitDistance = 0.09158854695375834
nOAAEtopo5elevationdata1Display.GaussianRadius = 0.09261120855808258
nOAAEtopo5elevationdata1Display.SetScaleArray = ['POINTS', 'elev']
nOAAEtopo5elevationdata1Display.ScaleTransferFunction = 'PiecewiseFunction'
nOAAEtopo5elevationdata1Display.OpacityArray = ['POINTS', 'elev']
nOAAEtopo5elevationdata1Display.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
nOAAEtopo5elevationdata1Display.ScaleTransferFunction.Points = [-7814.0, 0.0, 0.5, 0.0, 5029.0, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
nOAAEtopo5elevationdata1Display.OpacityTransferFunction.Points = [-7814.0, 0.0, 0.5, 0.0, 5029.0, 1.0, 0.5, 0.0]

# reset view to fit data
renderView1.ResetCamera()

# show color bar/color legend
nOAAEtopo5elevationdata1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on nOAAEtopo5elevationdata1Display
nOAAEtopo5elevationdata1Display.Opacity = 0.6

# get color legend/bar for elevLUT in view renderView1
elevLUTColorBar = GetScalarBar(elevLUT, renderView1)

# Properties modified on elevLUTColorBar
elevLUTColorBar.Title = 'Elevation (m)'

#### saving camera placements for all active views

# current camera placement for renderView1
# renderView1.CameraPosition = [-0.059544533491134644, -0.5152373211458325, 5.440815881684258]
# renderView1.CameraFocalPoint = [-0.059544533491134644, -0.5152373211458325, 0.06312963366508484]
# renderView1.CameraParallelScale = 1.3918476195732798

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).