# R.0.2018.080
#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Draw Grids'
drawGrids1 = DrawGrids()

# Properties modified on drawGrids1
drawGrids1.GridSpacing = 10.0

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1501, 958]

# show data in view
drawGrids1Display = Show(drawGrids1, renderView1)

# trace defaults for the display properties.
drawGrids1Display.Representation = 'Surface'
drawGrids1Display.ColorArrayName = [None, '']
drawGrids1Display.OSPRayScaleArray = 'Grid Elevation (km),\nResolution & Spacing (deg)'
drawGrids1Display.OSPRayScaleFunction = 'PiecewiseFunction'
drawGrids1Display.SelectOrientationVectors = 'None'
drawGrids1Display.ScaleFactor = 0.18537349700927735
drawGrids1Display.SelectScaleArray = 'None'
drawGrids1Display.GlyphType = 'Arrow'
drawGrids1Display.GlyphTableIndexArray = 'None'
drawGrids1Display.DataAxesGrid = 'GridAxesRepresentation'
drawGrids1Display.PolarAxes = 'PolarAxesRepresentation'
drawGrids1Display.GaussianRadius = 0.09268674850463868
drawGrids1Display.SetScaleArray = [None, '']
drawGrids1Display.ScaleTransferFunction = 'PiecewiseFunction'
drawGrids1Display.OpacityArray = [None, '']
drawGrids1Display.OpacityTransferFunction = 'PiecewiseFunction'

# reset view to fit data
#renderView1.ResetCamera()

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on drawGrids1Display
drawGrids1Display.Opacity = 0.3

#### saving camera placements for all active views

# current camera placement for renderView1
# renderView1.CameraPosition = [-0.05948430299758911, -0.5159335862845182, 5.451510239710665]
# renderView1.CameraFocalPoint = [-0.05948430299758911, -0.5159335862845182, 0.0595984160900116]
# renderView1.CameraParallelScale = 1.3955294694664888

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
