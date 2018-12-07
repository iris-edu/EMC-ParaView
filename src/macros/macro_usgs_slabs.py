# trace generated using paraview version 5.6.0-RC2
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Show USGS Slab 1.0'
showUSGSSlab101 = ShowUSGSSlab10(AlternateFileName='')

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1174, 944]

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
showUSGSSlab101Display.ScaleFactor = 0.0243834525346756
showUSGSSlab101Display.SelectScaleArray = 'z'
showUSGSSlab101Display.GlyphType = 'Arrow'
showUSGSSlab101Display.GlyphTableIndexArray = 'z'
showUSGSSlab101Display.GaussianRadius = 0.00121917262673378
showUSGSSlab101Display.SetScaleArray = ['POINTS', 'z']
showUSGSSlab101Display.ScaleTransferFunction = 'PiecewiseFunction'
showUSGSSlab101Display.OpacityArray = ['POINTS', 'z']
showUSGSSlab101Display.OpacityTransferFunction = 'PiecewiseFunction'
showUSGSSlab101Display.DataAxesGrid = 'GridAxesRepresentation'
showUSGSSlab101Display.SelectionCellLabelFontFile = ''
showUSGSSlab101Display.SelectionPointLabelFontFile = ''
showUSGSSlab101Display.PolarAxes = 'PolarAxesRepresentation'
showUSGSSlab101Display.ScalarOpacityFunction = zPWF
showUSGSSlab101Display.ScalarOpacityUnitDistance = 0.009885280278558792

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
showUSGSSlab101Display.DataAxesGrid.XTitleFontFile = ''
showUSGSSlab101Display.DataAxesGrid.YTitleFontFile = ''
showUSGSSlab101Display.DataAxesGrid.ZTitleFontFile = ''
showUSGSSlab101Display.DataAxesGrid.XLabelFontFile = ''
showUSGSSlab101Display.DataAxesGrid.YLabelFontFile = ''
showUSGSSlab101Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
showUSGSSlab101Display.PolarAxes.PolarAxisTitleFontFile = ''
showUSGSSlab101Display.PolarAxes.PolarAxisLabelFontFile = ''
showUSGSSlab101Display.PolarAxes.LastRadialAxisTextFontFile = ''
showUSGSSlab101Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# reset view to fit data
#renderView1.ResetCamera()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# show color bar/color legend
showUSGSSlab101Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Show USGS Slab 1.0'
showUSGSSlab101_1 = ShowUSGSSlab10(AlternateFileName='')

# Properties modified on showUSGSSlab101_1
showUSGSSlab101_1.Slab = 1

# show data in view
showUSGSSlab101_1Display = Show(showUSGSSlab101_1, renderView1)

# trace defaults for the display properties.
showUSGSSlab101_1Display.Representation = 'Surface'
showUSGSSlab101_1Display.ColorArrayName = ['POINTS', 'z']
showUSGSSlab101_1Display.LookupTable = zLUT
showUSGSSlab101_1Display.OSPRayScaleArray = 'z'
showUSGSSlab101_1Display.OSPRayScaleFunction = 'PiecewiseFunction'
showUSGSSlab101_1Display.SelectOrientationVectors = 'None'
showUSGSSlab101_1Display.ScaleFactor = 0.015397274494171144
showUSGSSlab101_1Display.SelectScaleArray = 'z'
showUSGSSlab101_1Display.GlyphType = 'Arrow'
showUSGSSlab101_1Display.GlyphTableIndexArray = 'z'
showUSGSSlab101_1Display.GaussianRadius = 0.0007698637247085571
showUSGSSlab101_1Display.SetScaleArray = ['POINTS', 'z']
showUSGSSlab101_1Display.ScaleTransferFunction = 'PiecewiseFunction'
showUSGSSlab101_1Display.OpacityArray = ['POINTS', 'z']
showUSGSSlab101_1Display.OpacityTransferFunction = 'PiecewiseFunction'
showUSGSSlab101_1Display.DataAxesGrid = 'GridAxesRepresentation'
showUSGSSlab101_1Display.SelectionCellLabelFontFile = ''
showUSGSSlab101_1Display.SelectionPointLabelFontFile = ''
showUSGSSlab101_1Display.PolarAxes = 'PolarAxesRepresentation'
showUSGSSlab101_1Display.ScalarOpacityFunction = zPWF
showUSGSSlab101_1Display.ScalarOpacityUnitDistance = 0.010813655393003241

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
showUSGSSlab101_1Display.DataAxesGrid.XTitleFontFile = ''
showUSGSSlab101_1Display.DataAxesGrid.YTitleFontFile = ''
showUSGSSlab101_1Display.DataAxesGrid.ZTitleFontFile = ''
showUSGSSlab101_1Display.DataAxesGrid.XLabelFontFile = ''
showUSGSSlab101_1Display.DataAxesGrid.YLabelFontFile = ''
showUSGSSlab101_1Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
showUSGSSlab101_1Display.PolarAxes.PolarAxisTitleFontFile = ''
showUSGSSlab101_1Display.PolarAxes.PolarAxisLabelFontFile = ''
showUSGSSlab101_1Display.PolarAxes.LastRadialAxisTextFontFile = ''
showUSGSSlab101_1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# show color bar/color legend
showUSGSSlab101_1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Show USGS Slab 1.0'
showUSGSSlab101_2 = ShowUSGSSlab10(AlternateFileName='')

# Properties modified on showUSGSSlab101_2
showUSGSSlab101_2.Slab = 2

# show data in view
showUSGSSlab101_2Display = Show(showUSGSSlab101_2, renderView1)

# trace defaults for the display properties.
showUSGSSlab101_2Display.Representation = 'Surface'
showUSGSSlab101_2Display.ColorArrayName = ['POINTS', 'z']
showUSGSSlab101_2Display.LookupTable = zLUT
showUSGSSlab101_2Display.OSPRayScaleArray = 'z'
showUSGSSlab101_2Display.OSPRayScaleFunction = 'PiecewiseFunction'
showUSGSSlab101_2Display.SelectOrientationVectors = 'None'
showUSGSSlab101_2Display.ScaleFactor = 0.036885755509138106
showUSGSSlab101_2Display.SelectScaleArray = 'z'
showUSGSSlab101_2Display.GlyphType = 'Arrow'
showUSGSSlab101_2Display.GlyphTableIndexArray = 'z'
showUSGSSlab101_2Display.GaussianRadius = 0.0018442877754569053
showUSGSSlab101_2Display.SetScaleArray = ['POINTS', 'z']
showUSGSSlab101_2Display.ScaleTransferFunction = 'PiecewiseFunction'
showUSGSSlab101_2Display.OpacityArray = ['POINTS', 'z']
showUSGSSlab101_2Display.OpacityTransferFunction = 'PiecewiseFunction'
showUSGSSlab101_2Display.DataAxesGrid = 'GridAxesRepresentation'
showUSGSSlab101_2Display.SelectionCellLabelFontFile = ''
showUSGSSlab101_2Display.SelectionPointLabelFontFile = ''
showUSGSSlab101_2Display.PolarAxes = 'PolarAxesRepresentation'
showUSGSSlab101_2Display.ScalarOpacityFunction = zPWF
showUSGSSlab101_2Display.ScalarOpacityUnitDistance = 0.012967980524272487

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
showUSGSSlab101_2Display.DataAxesGrid.XTitleFontFile = ''
showUSGSSlab101_2Display.DataAxesGrid.YTitleFontFile = ''
showUSGSSlab101_2Display.DataAxesGrid.ZTitleFontFile = ''
showUSGSSlab101_2Display.DataAxesGrid.XLabelFontFile = ''
showUSGSSlab101_2Display.DataAxesGrid.YLabelFontFile = ''
showUSGSSlab101_2Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
showUSGSSlab101_2Display.PolarAxes.PolarAxisTitleFontFile = ''
showUSGSSlab101_2Display.PolarAxes.PolarAxisLabelFontFile = ''
showUSGSSlab101_2Display.PolarAxes.LastRadialAxisTextFontFile = ''
showUSGSSlab101_2Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# show color bar/color legend
showUSGSSlab101_2Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

#### saving camera placements for all active views

# current camera placement for renderView1
#renderView1.CameraPosition = [-0.49508480727672577, -0.2009134478867054, 1.483602525349324]
#renderView1.CameraFocalPoint = [-0.49508480727672577, -0.2009134478867054, 0.8359864354133606]
#renderView1.CameraParallelScale = 0.1676153779902542

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
