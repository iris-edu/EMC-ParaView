# R.0.2018.080
#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Draw Boundaries'
drawBoundaries1 = DrawBoundaries(AlternateFileName='')

# Properties modified on drawBoundaries1
drawBoundaries1.DataFile = 'Present-day plate boundaries: divergent margins'

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1501, 958]

# show data in view
drawBoundaries1Display = Show(drawBoundaries1, renderView1)

# trace defaults for the display properties.
drawBoundaries1Display.Representation = 'Surface'
drawBoundaries1Display.ColorArrayName = [None, '']
drawBoundaries1Display.OSPRayScaleArray = 'Boundary Elevation (km)'
drawBoundaries1Display.OSPRayScaleFunction = 'PiecewiseFunction'
drawBoundaries1Display.SelectOrientationVectors = 'None'
drawBoundaries1Display.ScaleFactor = 0.17231773138046266
drawBoundaries1Display.SelectScaleArray = 'None'
drawBoundaries1Display.GlyphType = 'Arrow'
drawBoundaries1Display.GlyphTableIndexArray = 'None'
drawBoundaries1Display.DataAxesGrid = 'GridAxesRepresentation'
drawBoundaries1Display.PolarAxes = 'PolarAxesRepresentation'
drawBoundaries1Display.GaussianRadius = 0.08615886569023133
drawBoundaries1Display.SetScaleArray = [None, '']
drawBoundaries1Display.ScaleTransferFunction = 'PiecewiseFunction'
drawBoundaries1Display.OpacityArray = [None, '']
drawBoundaries1Display.OpacityTransferFunction = 'PiecewiseFunction'

# reset view to fit data
#renderView1.ResetCamera()

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on drawBoundaries1Display
drawBoundaries1Display.LineWidth = 2.0

# change solid color
drawBoundaries1Display.DiffuseColor = [1.0, 0.0, 0.0]

# create a new 'Draw Boundaries'
drawBoundaries1_1 = DrawBoundaries(AlternateFileName='')

# Properties modified on drawBoundaries1_1
drawBoundaries1_1.DataFile = 'Present-day plate boundaries: transform margins'

# show data in view
drawBoundaries1_1Display = Show(drawBoundaries1_1, renderView1)

# trace defaults for the display properties.
drawBoundaries1_1Display.Representation = 'Surface'
drawBoundaries1_1Display.ColorArrayName = [None, '']
drawBoundaries1_1Display.OSPRayScaleArray = 'Boundary Elevation (km)'
drawBoundaries1_1Display.OSPRayScaleFunction = 'PiecewiseFunction'
drawBoundaries1_1Display.SelectOrientationVectors = 'None'
drawBoundaries1_1Display.ScaleFactor = 0.15073646306991578
drawBoundaries1_1Display.SelectScaleArray = 'None'
drawBoundaries1_1Display.GlyphType = 'Arrow'
drawBoundaries1_1Display.GlyphTableIndexArray = 'None'
drawBoundaries1_1Display.DataAxesGrid = 'GridAxesRepresentation'
drawBoundaries1_1Display.PolarAxes = 'PolarAxesRepresentation'
drawBoundaries1_1Display.GaussianRadius = 0.07536823153495789
drawBoundaries1_1Display.SetScaleArray = [None, '']
drawBoundaries1_1Display.ScaleTransferFunction = 'PiecewiseFunction'
drawBoundaries1_1Display.OpacityArray = [None, '']
drawBoundaries1_1Display.OpacityTransferFunction = 'PiecewiseFunction'

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on drawBoundaries1_1Display
drawBoundaries1_1Display.LineWidth = 2.0

# change solid color
drawBoundaries1_1Display.DiffuseColor = [0.0, 0.3333333333333333, 1.0]

# create a new 'Draw Boundaries'
drawBoundaries1_2 = DrawBoundaries(AlternateFileName='')

# Properties modified on drawBoundaries1_2
drawBoundaries1_2.DataFile = 'Present-day plate boundaries: convergent margins'

# show data in view
drawBoundaries1_2Display = Show(drawBoundaries1_2, renderView1)

# trace defaults for the display properties.
drawBoundaries1_2Display.Representation = 'Surface'
drawBoundaries1_2Display.ColorArrayName = [None, '']
drawBoundaries1_2Display.OSPRayScaleArray = 'Boundary Elevation (km)'
drawBoundaries1_2Display.OSPRayScaleFunction = 'PiecewiseFunction'
drawBoundaries1_2Display.SelectOrientationVectors = 'None'
drawBoundaries1_2Display.ScaleFactor = 0.1700249254703522
drawBoundaries1_2Display.SelectScaleArray = 'None'
drawBoundaries1_2Display.GlyphType = 'Arrow'
drawBoundaries1_2Display.GlyphTableIndexArray = 'None'
drawBoundaries1_2Display.DataAxesGrid = 'GridAxesRepresentation'
drawBoundaries1_2Display.PolarAxes = 'PolarAxesRepresentation'
drawBoundaries1_2Display.GaussianRadius = 0.0850124627351761
drawBoundaries1_2Display.SetScaleArray = [None, '']
drawBoundaries1_2Display.ScaleTransferFunction = 'PiecewiseFunction'
drawBoundaries1_2Display.OpacityArray = [None, '']
drawBoundaries1_2Display.OpacityTransferFunction = 'PiecewiseFunction'

# update the view to ensure updated data information
renderView1.Update()

# change solid color
drawBoundaries1_2Display.DiffuseColor = [1.0, 1.0, 0.0]

# Properties modified on drawBoundaries1_2Display
drawBoundaries1_2Display.LineWidth = 2.0

#### saving camera placements for all active views

# current camera placement for renderView1
# renderView1.CameraPosition = [0.20058076083660126, -0.6189543306827545, 4.458974120393207]
# renderView1.CameraFocalPoint = [0.20058076083660126, -0.6189543306827545, -0.0011429786682128906]
# renderView1.CameraParallelScale = 1.1543632486245017

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
