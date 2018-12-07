# trace generated using paraview version 5.6.0-RC2
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Topo elevation data'
topoelevationdata1 = Topoelevationdata(AlternateFileName='')

# Properties modified on topoelevationdata1
topoelevationdata1.DepthBias = '100'
topoelevationdata1.Roughness = '50'
topoelevationdata1.Sampling = 1

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [876, 884]

# show data in view
topoelevationdata1Display = Show(topoelevationdata1, renderView1)

# get color transfer function/color map for 'elevation'
elevationLUT = GetColorTransferFunction('elevation')

# get opacity transfer function/opacity map for 'elevation'
elevationPWF = GetOpacityTransferFunction('elevation')

# trace defaults for the display properties.
topoelevationdata1Display.Representation = 'Surface'
topoelevationdata1Display.ColorArrayName = ['POINTS', 'elevation']
topoelevationdata1Display.LookupTable = elevationLUT
topoelevationdata1Display.OSPRayScaleArray = 'elevation'
topoelevationdata1Display.OSPRayScaleFunction = 'PiecewiseFunction'
topoelevationdata1Display.SelectOrientationVectors = 'None'
topoelevationdata1Display.ScaleFactor = 0.1855192244052887
topoelevationdata1Display.SelectScaleArray = 'elevation'
topoelevationdata1Display.GlyphType = 'Arrow'
topoelevationdata1Display.GlyphTableIndexArray = 'elevation'
topoelevationdata1Display.GaussianRadius = 0.009275961220264434
topoelevationdata1Display.SetScaleArray = ['POINTS', 'elevation']
topoelevationdata1Display.ScaleTransferFunction = 'PiecewiseFunction'
topoelevationdata1Display.OpacityArray = ['POINTS', 'elevation']
topoelevationdata1Display.OpacityTransferFunction = 'PiecewiseFunction'
topoelevationdata1Display.DataAxesGrid = 'GridAxesRepresentation'
topoelevationdata1Display.SelectionCellLabelFontFile = ''
topoelevationdata1Display.SelectionPointLabelFontFile = ''
topoelevationdata1Display.PolarAxes = 'PolarAxesRepresentation'
topoelevationdata1Display.ScalarOpacityFunction = elevationPWF
topoelevationdata1Display.ScalarOpacityUnitDistance = 0.06538854428036935

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
topoelevationdata1Display.DataAxesGrid.XTitleFontFile = ''
topoelevationdata1Display.DataAxesGrid.YTitleFontFile = ''
topoelevationdata1Display.DataAxesGrid.ZTitleFontFile = ''
topoelevationdata1Display.DataAxesGrid.XLabelFontFile = ''
topoelevationdata1Display.DataAxesGrid.YLabelFontFile = ''
topoelevationdata1Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
topoelevationdata1Display.PolarAxes.PolarAxisTitleFontFile = ''
topoelevationdata1Display.PolarAxes.PolarAxisLabelFontFile = ''
topoelevationdata1Display.PolarAxes.LastRadialAxisTextFontFile = ''
topoelevationdata1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# reset view to fit data
# renderView1.ResetCamera()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# show color bar/color legend
topoelevationdata1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

#### saving camera placements for all active views

# current camera placement for renderView1
# renderView1.CameraPosition = [-0.06000778079032898, -0.5188647452741861, 5.508311506836358]
# renderView1.CameraFocalPoint = [-0.06000778079032898, -0.5188647452741861, 0.0687466561794281]
# renderView1.CameraParallelScale = 1.408713362945648

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).