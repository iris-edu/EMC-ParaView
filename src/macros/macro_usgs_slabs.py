# R.0.2018.080
#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Show USGS Slab 1.0'
showUSGSSlab101 = ShowUSGSSlab10(AlternateFileName='')

# Properties modified on showUSGSSlab101
showUSGSSlab101.Slab = 'Central America'

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1501, 958]

# show data in view
showUSGSSlab101Display = Show(showUSGSSlab101, renderView1)

# get color transfer function/color map for 'z'
zLUT = GetColorTransferFunction('z')

# get opacity transfer function/opacity map for 'z'
zPWF = GetOpacityTransferFunction('z')

# trace defaults for the display properties.
showUSGSSlab101Display.Representation = 'Surface'
showUSGSSlab101Display.ColorArrayName = ['POINTS', 'z']
showUSGSSlab101Display.LookupTable = zLUT
showUSGSSlab101Display.OSPRayScaleArray = 'z'
showUSGSSlab101Display.OSPRayScaleFunction = 'PiecewiseFunction'
showUSGSSlab101Display.SelectOrientationVectors = 'None'
showUSGSSlab101Display.ScaleFactor = 0.03669944405555725
showUSGSSlab101Display.SelectScaleArray = 'z'
showUSGSSlab101Display.GlyphType = 'Arrow'
showUSGSSlab101Display.GlyphTableIndexArray = 'z'
showUSGSSlab101Display.DataAxesGrid = 'GridAxesRepresentation'
showUSGSSlab101Display.PolarAxes = 'PolarAxesRepresentation'
showUSGSSlab101Display.ScalarOpacityFunction = zPWF
showUSGSSlab101Display.ScalarOpacityUnitDistance = 0.012927825008836259
showUSGSSlab101Display.GaussianRadius = 0.018349722027778625
showUSGSSlab101Display.SetScaleArray = ['POINTS', 'z']
showUSGSSlab101Display.ScaleTransferFunction = 'PiecewiseFunction'
showUSGSSlab101Display.OpacityArray = ['POINTS', 'z']
showUSGSSlab101Display.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
showUSGSSlab101Display.ScaleTransferFunction.Points = [-0.26796382665634155, 0.0, 0.5, 0.0, 290.0155944824219, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
showUSGSSlab101Display.OpacityTransferFunction.Points = [-0.26796382665634155, 0.0, 0.5, 0.0, 290.0155944824219, 1.0, 0.5, 0.0]

# reset view to fit data
#renderView1.ResetCamera()

# show color bar/color legend
showUSGSSlab101Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

#### saving camera placements for all active views

# current camera placement for renderView1
# renderView1.CameraPosition = [-0.06311893463134766, -0.9411111772060394, 1.0526660028588413]
# renderView1.CameraFocalPoint = [-0.06311893463134766, -0.9411111772060394, 0.23572896420955658]
# renderView1.CameraParallelScale = 0.21143886425208894

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
