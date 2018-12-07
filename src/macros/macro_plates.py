# trace generated using paraview version 5.6.0-RC2
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Draw Boundaries'
drawBoundaries1 = DrawBoundaries(AlternateFileName='')

# Properties modified on drawBoundaries1
drawBoundaries1.DataFile = 5

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [876, 884]

# show data in view
drawBoundaries1Display = Show(drawBoundaries1, renderView1)

# trace defaults for the display properties.
drawBoundaries1Display.Representation = 'Surface'
drawBoundaries1Display.ColorArrayName = [None, '']
drawBoundaries1Display.OSPRayScaleFunction = 'PiecewiseFunction'
drawBoundaries1Display.SelectOrientationVectors = 'None'
drawBoundaries1Display.ScaleFactor = 0.17204684615135193
drawBoundaries1Display.SelectScaleArray = 'None'
drawBoundaries1Display.GlyphType = 'Arrow'
drawBoundaries1Display.GlyphTableIndexArray = 'None'
drawBoundaries1Display.GaussianRadius = 0.008602342307567597
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
# renderView1.ResetCamera()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

# change solid color
drawBoundaries1Display.DiffuseColor = [1.0, 0.0, 0.0]

# Properties modified on drawBoundaries1Display
drawBoundaries1Display.LineWidth = 3.0

# create a new 'Draw Boundaries'
drawBoundaries1_1 = DrawBoundaries(AlternateFileName='')

# Properties modified on drawBoundaries1_1
drawBoundaries1_1.DataFile = 6

# show data in view
drawBoundaries1_1Display = Show(drawBoundaries1_1, renderView1)

# trace defaults for the display properties.
drawBoundaries1_1Display.Representation = 'Surface'
drawBoundaries1_1Display.ColorArrayName = [None, '']
drawBoundaries1_1Display.OSPRayScaleFunction = 'PiecewiseFunction'
drawBoundaries1_1Display.SelectOrientationVectors = 'None'
drawBoundaries1_1Display.ScaleFactor = 0.15049939155578615
drawBoundaries1_1Display.SelectScaleArray = 'None'
drawBoundaries1_1Display.GlyphType = 'Arrow'
drawBoundaries1_1Display.GlyphTableIndexArray = 'None'
drawBoundaries1_1Display.GaussianRadius = 0.007524969577789307
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
# renderView1.Update()

# change solid color
drawBoundaries1_1Display.DiffuseColor = [0.0, 0.3333333333333333, 1.0]

# Properties modified on drawBoundaries1_1Display
drawBoundaries1_1Display.LineWidth = 3.0

# create a new 'Draw Boundaries'
drawBoundaries1_2 = DrawBoundaries(AlternateFileName='')

# Properties modified on drawBoundaries1_2
drawBoundaries1_2.DataFile = 4

# show data in view
drawBoundaries1_2Display = Show(drawBoundaries1_2, renderView1)

# trace defaults for the display properties.
drawBoundaries1_2Display.Representation = 'Surface'
drawBoundaries1_2Display.ColorArrayName = [None, '']
drawBoundaries1_2Display.OSPRayScaleFunction = 'PiecewiseFunction'
drawBoundaries1_2Display.SelectOrientationVectors = 'None'
drawBoundaries1_2Display.ScaleFactor = 0.1697576344013214
drawBoundaries1_2Display.SelectScaleArray = 'None'
drawBoundaries1_2Display.GlyphType = 'Arrow'
drawBoundaries1_2Display.GlyphTableIndexArray = 'None'
drawBoundaries1_2Display.GaussianRadius = 0.00848788172006607
drawBoundaries1_2Display.SetScaleArray = [None, '']
drawBoundaries1_2Display.ScaleTransferFunction = 'PiecewiseFunction'
drawBoundaries1_2Display.OpacityArray = [None, '']
drawBoundaries1_2Display.OpacityTransferFunction = 'PiecewiseFunction'
drawBoundaries1_2Display.DataAxesGrid = 'GridAxesRepresentation'
drawBoundaries1_2Display.SelectionCellLabelFontFile = ''
drawBoundaries1_2Display.SelectionPointLabelFontFile = ''
drawBoundaries1_2Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
drawBoundaries1_2Display.DataAxesGrid.XTitleFontFile = ''
drawBoundaries1_2Display.DataAxesGrid.YTitleFontFile = ''
drawBoundaries1_2Display.DataAxesGrid.ZTitleFontFile = ''
drawBoundaries1_2Display.DataAxesGrid.XLabelFontFile = ''
drawBoundaries1_2Display.DataAxesGrid.YLabelFontFile = ''
drawBoundaries1_2Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
drawBoundaries1_2Display.PolarAxes.PolarAxisTitleFontFile = ''
drawBoundaries1_2Display.PolarAxes.PolarAxisLabelFontFile = ''
drawBoundaries1_2Display.PolarAxes.LastRadialAxisTextFontFile = ''
drawBoundaries1_2Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# update the view to ensure updated data information
# renderView1.Update()

# Properties modified on drawBoundaries1_2Display
drawBoundaries1_2Display.LineWidth = 3.0

# change solid color
drawBoundaries1_2Display.DiffuseColor = [1.0, 1.0, 0.0]

#### saving camera placements for all active views

# current camera placement for renderView1
# renderView1.CameraPosition = [0.2002662718296051, -0.6179858967661858, 4.4899332103098555]
# renderView1.CameraFocalPoint = [0.2002662718296051, -0.6179858967661858, -0.0011411607265472412]
# renderView1.CameraParallelScale = 1.1630776825277929

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).