from paraview.simple import *

"""Trace generated using paraview version 5.6.0-RC2
 To ensure correct image size when batch processing, please search 
 for and uncomment the line `# renderView*.ViewSize = [*,*]`
"""
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Draw Grids'
drawGrids1 = DrawGrids()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1174, 944]

# show data in view
drawGrids1Display = Show(drawGrids1, renderView1)

# trace defaults for the display properties.
drawGrids1Display.Representation = 'Surface'
drawGrids1Display.ColorArrayName = [None, '']
drawGrids1Display.OSPRayScaleFunction = 'PiecewiseFunction'
drawGrids1Display.SelectOrientationVectors = 'None'
drawGrids1Display.ScaleFactor = 0.18508331179618837
drawGrids1Display.SelectScaleArray = 'None'
drawGrids1Display.GlyphType = 'Arrow'
drawGrids1Display.GlyphTableIndexArray = 'None'
drawGrids1Display.GaussianRadius = 0.009254165589809418
drawGrids1Display.SetScaleArray = [None, '']
drawGrids1Display.ScaleTransferFunction = 'PiecewiseFunction'
drawGrids1Display.OpacityArray = [None, '']
drawGrids1Display.OpacityTransferFunction = 'PiecewiseFunction'
drawGrids1Display.DataAxesGrid = 'GridAxesRepresentation'
drawGrids1Display.SelectionCellLabelFontFile = ''
drawGrids1Display.SelectionPointLabelFontFile = ''
drawGrids1Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
drawGrids1Display.DataAxesGrid.XTitleFontFile = ''
drawGrids1Display.DataAxesGrid.YTitleFontFile = ''
drawGrids1Display.DataAxesGrid.ZTitleFontFile = ''
drawGrids1Display.DataAxesGrid.XLabelFontFile = ''
drawGrids1Display.DataAxesGrid.YLabelFontFile = ''
drawGrids1Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
drawGrids1Display.PolarAxes.PolarAxisTitleFontFile = ''
drawGrids1Display.PolarAxes.PolarAxisLabelFontFile = ''
drawGrids1Display.PolarAxes.LastRadialAxisTextFontFile = ''
drawGrids1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# reset view to fit data
#renderView1.ResetCamera()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on drawGrids1Display
drawGrids1Display.Opacity = 0.5

#### saving camera placements for all active views

# current camera placement for renderView1
#renderView1.CameraPosition = [-0.059391170740127563, -0.515126028098166, 5.442962405261595]
#renderView1.CameraFocalPoint = [-0.059391170740127563, -0.515126028098166, 0.05950528383255005]
#renderView1.CameraParallelScale = 1.3933412315186304

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
