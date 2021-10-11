from paraview.simple import *

"""Trace generated using paraview version 5.6.0-RC2
 To ensure correct image size when batch processing, please search 
 for and uncomment the line `# renderView*.ViewSize = [*,*]`
"""
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Draw Boundaries'
drawBoundaries1 = DrawBoundaries(AlternateFileName='')

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1174, 944]

# show data in view
drawBoundaries1Display = Show(drawBoundaries1, renderView1)

# trace defaults for the display properties.
drawBoundaries1Display.Representation = 'Surface'
drawBoundaries1Display.ColorArrayName = [None, '']
drawBoundaries1Display.OSPRayScaleFunction = 'PiecewiseFunction'
drawBoundaries1Display.SelectOrientationVectors = 'None'
drawBoundaries1Display.ScaleFactor = 0.1801776885986328
drawBoundaries1Display.SelectScaleArray = 'None'
drawBoundaries1Display.GlyphType = 'Arrow'
drawBoundaries1Display.GlyphTableIndexArray = 'None'
drawBoundaries1Display.GaussianRadius = 0.00900888442993164
drawBoundaries1Display.SetScaleArray = [None, '']
drawBoundaries1Display.ScaleTransferFunction = 'PiecewiseFunction'
drawBoundaries1Display.OpacityArray = [None, '']
drawBoundaries1Display.OpacityTransferFunction = 'PiecewiseFunction'
drawBoundaries1Display.DataAxesGrid = 'GridAxesRepresentation'
drawBoundaries1Display.SelectionCellLabelFontFile = ''
drawBoundaries1Display.SelectionPointLabelFontFile = ''
drawBoundaries1Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
drawBoundaries1Display.DataAxesGrid.XTitleFontFile = ''
drawBoundaries1Display.DataAxesGrid.YTitleFontFile = ''
drawBoundaries1Display.DataAxesGrid.ZTitleFontFile = ''
drawBoundaries1Display.DataAxesGrid.XLabelFontFile = ''
drawBoundaries1Display.DataAxesGrid.YLabelFontFile = ''
drawBoundaries1Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
drawBoundaries1Display.PolarAxes.PolarAxisTitleFontFile = ''
drawBoundaries1Display.PolarAxes.PolarAxisLabelFontFile = ''
drawBoundaries1Display.PolarAxes.LastRadialAxisTextFontFile = ''
drawBoundaries1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# reset view to fit data
renderView1.ResetCamera()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Draw Boundaries'
drawBoundaries1_1 = DrawBoundaries(AlternateFileName='')

# Properties modified on drawBoundaries1_1
drawBoundaries1_1.DataFile = 3

# show data in view
drawBoundaries1_1Display = Show(drawBoundaries1_1, renderView1)

# trace defaults for the display properties.
drawBoundaries1_1Display.Representation = 'Surface'
drawBoundaries1_1Display.ColorArrayName = [None, '']
drawBoundaries1_1Display.OSPRayScaleFunction = 'PiecewiseFunction'
drawBoundaries1_1Display.SelectOrientationVectors = 'None'
drawBoundaries1_1Display.ScaleFactor = 0.1755068302154541
drawBoundaries1_1Display.SelectScaleArray = 'None'
drawBoundaries1_1Display.GlyphType = 'Arrow'
drawBoundaries1_1Display.GlyphTableIndexArray = 'None'
drawBoundaries1_1Display.GaussianRadius = 0.008775341510772706
drawBoundaries1_1Display.SetScaleArray = [None, '']
drawBoundaries1_1Display.ScaleTransferFunction = 'PiecewiseFunction'
drawBoundaries1_1Display.OpacityArray = [None, '']
drawBoundaries1_1Display.OpacityTransferFunction = 'PiecewiseFunction'
drawBoundaries1_1Display.DataAxesGrid = 'GridAxesRepresentation'
drawBoundaries1_1Display.SelectionCellLabelFontFile = ''
drawBoundaries1_1Display.SelectionPointLabelFontFile = ''
drawBoundaries1_1Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
drawBoundaries1_1Display.DataAxesGrid.XTitleFontFile = ''
drawBoundaries1_1Display.DataAxesGrid.YTitleFontFile = ''
drawBoundaries1_1Display.DataAxesGrid.ZTitleFontFile = ''
drawBoundaries1_1Display.DataAxesGrid.XLabelFontFile = ''
drawBoundaries1_1Display.DataAxesGrid.YLabelFontFile = ''
drawBoundaries1_1Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
drawBoundaries1_1Display.PolarAxes.PolarAxisTitleFontFile = ''
drawBoundaries1_1Display.PolarAxes.PolarAxisLabelFontFile = ''
drawBoundaries1_1Display.PolarAxes.LastRadialAxisTextFontFile = ''
drawBoundaries1_1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# update the view to ensure updated data information
renderView1.Update()

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [0.11119141983865279, -3.8275503734247405, 3.9364893346743184]
renderView1.CameraFocalPoint = [-0.023228138685226413, -0.5428674146533012, 0.08051764965057373]
renderView1.CameraViewUp = [0.002323043049074252, 0.7612844311872383, 0.6484139251303255]
renderView1.CameraParallelScale = 1.31146775484586

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).