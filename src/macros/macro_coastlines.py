# R.0.2018.080
#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Draw Boundaries'
drawBoundaries1 = DrawBoundaries(AlternateFileName='')

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
drawBoundaries1Display.ScaleFactor = 0.18068044781684878
drawBoundaries1Display.SelectScaleArray = 'None'
drawBoundaries1Display.GlyphType = 'Arrow'
drawBoundaries1Display.GlyphTableIndexArray = 'None'
drawBoundaries1Display.DataAxesGrid = 'GridAxesRepresentation'
drawBoundaries1Display.PolarAxes = 'PolarAxesRepresentation'
drawBoundaries1Display.GaussianRadius = 0.09034022390842439
drawBoundaries1Display.SetScaleArray = [None, '']
drawBoundaries1Display.ScaleTransferFunction = 'PiecewiseFunction'
drawBoundaries1Display.OpacityArray = [None, '']
drawBoundaries1Display.OpacityTransferFunction = 'PiecewiseFunction'

# reset view to fit data
renderView1.ResetCamera()

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Draw Boundaries'
drawBoundaries1_1 = DrawBoundaries(AlternateFileName='')

# Properties modified on drawBoundaries1_1
drawBoundaries1_1.DataFile = 'National boundaries + US state + Canadian province boundaries'

# show data in view
drawBoundaries1_1Display = Show(drawBoundaries1_1, renderView1)

# trace defaults for the display properties.
drawBoundaries1_1Display.Representation = 'Surface'
drawBoundaries1_1Display.ColorArrayName = [None, '']
drawBoundaries1_1Display.OSPRayScaleArray = 'Boundary Elevation (km)'
drawBoundaries1_1Display.OSPRayScaleFunction = 'PiecewiseFunction'
drawBoundaries1_1Display.SelectOrientationVectors = 'None'
drawBoundaries1_1Display.ScaleFactor = 0.17578312754631042
drawBoundaries1_1Display.SelectScaleArray = 'None'
drawBoundaries1_1Display.GlyphType = 'Arrow'
drawBoundaries1_1Display.GlyphTableIndexArray = 'None'
drawBoundaries1_1Display.DataAxesGrid = 'GridAxesRepresentation'
drawBoundaries1_1Display.PolarAxes = 'PolarAxesRepresentation'
drawBoundaries1_1Display.GaussianRadius = 0.08789156377315521
drawBoundaries1_1Display.SetScaleArray = [None, '']
drawBoundaries1_1Display.ScaleTransferFunction = 'PiecewiseFunction'
drawBoundaries1_1Display.OpacityArray = [None, '']
drawBoundaries1_1Display.OpacityTransferFunction = 'PiecewiseFunction'

# update the view to ensure updated data information
renderView1.Update()

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [-0.009587253218760135, -4.99167809286439, 2.7575719641428345]
renderView1.CameraFocalPoint = [-0.06604686379432678, -0.5362660102546215, 0.07954463362693787]
renderView1.CameraViewUp = [-0.00574014327974261, 0.5151098074736402, 0.8571049743173805]
renderView1.CameraParallelScale = 1.345503482101207

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
