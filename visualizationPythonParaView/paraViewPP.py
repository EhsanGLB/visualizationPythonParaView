#------------------------------- nanoFluid4Foam project -------------------------------#
#Author
    #Ehsan Golab, SUT. All rights reserved.
    #Ehsan1996Golab@gmail.com

#--------------------------------------------------------------------------------------#

import os, shutil, sys
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()
# get the current working directory
currentDir = os.getcwd()

DIRDATA = currentDir + '/case'
DIRSAVE = currentDir
print ("post processing by paraview in path: " + str(DIRSAVE) )


#-------------------------------------------------------------- Initial setting --------------------------------------------------------------#
# create a new 'OpenFOAMReader'
Casefoam = OpenFOAMReader(FileName = DIRDATA + '/Data.foam')
Casefoam.MeshRegions = ['internalMesh']
Casefoam.CellArrays = ['p', 'U', 'T', 'streamFunction']
times = Casefoam.TimestepValues
maxt = max(times)

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
renderView1.ViewTime = maxt

# uncomment following to set a specific view size
# renderView1.ViewSize = [546, 496]

# show data in view
CasefoamDisplay = Show(Casefoam, renderView1)

# Hide orientation axes
renderView1.OrientationAxesVisibility = 0

#change interaction mode for render view
renderView1.InteractionMode = '2D'

# update the view to ensure updated data information
renderView1.Update()

# reset view to fit data
renderView1.ResetCamera()

# get display properties
testOpenFOAMDisplay = GetDisplayProperties(Casefoam, view=renderView1)

# Properties modified on testOpenFOAMDisplay
testOpenFOAMDisplay.SpecularPower = 32.0
testOpenFOAMDisplay.Specular = 1.0
testOpenFOAMDisplay.Ambient = 0.0
testOpenFOAMDisplay.Diffuse = 1.0

# current camera placement for renderView1
#renderView1.CameraPosition = [0.15, 0.0, 0.0]
#renderView1.CameraFocalPoint = [0.0, 0.0, 0.0]
#renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 0.1



#-------------------------------------------------------------- Pressure distribution --------------------------------------------------------------#
ColorBy(CasefoamDisplay, ('POINTS', 'p'))

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')

# get opacity transfer function/opacity map for 'p'
pPWF = GetOpacityTransferFunction('p')

# show color bar/color legend
CasefoamDisplay.SetScalarBarVisibility(renderView1, True)

# get color legend/bar for pLUT in view renderView1
pLUTColorBar = GetScalarBar(pLUT, renderView1)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
pLUT.ApplyPreset('jet', True)

# change scalar bar placement
pLUTColorBar.Title = ''
pLUTColorBar.LabelFontFamily = 'Times'
pLUTColorBar.LabelFontSize = 8
pLUTColorBar.LabelBold = 1
pLUTColorBar.LabelItalic = 1
pLUTColorBar.Orientation = 'Horizontal'
pLUTColorBar.WindowLocation = 'AnyLocation'
pLUTColorBar.Position = [0.25, 0.78]
pLUTColorBar.ScalarBarLength = 0.5
pLUTColorBar.ScalarBarThickness = 8
pLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
pLUTColorBar.AutomaticLabelFormat = 0
pLUTColorBar.LabelFormat = '%-#6.20e'
pLUTColorBar.RangeLabelFormat = '%-#6.2e' #'%-#4.4f'

# save screenshot
SaveScreenshot(DIRSAVE + '/pDis.png', renderView1, ImageResolution=[1100, 1000], OverrideColorPalette='PrintBackground')



#-------------------------------------------------------------- Velocity distribution --------------------------------------------------------------#
# set scalar coloring
ColorBy(CasefoamDisplay, ('POINTS', 'U', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(pLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
CasefoamDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
CasefoamDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'U'
uLUT = GetColorTransferFunction('U')

# get opacity transfer function/opacity map for 'U'
uPWF = GetOpacityTransferFunction('U')

# get color legend/bar for uLUT in view renderView1
uLUTColorBar = GetScalarBar(uLUT, renderView1)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
uLUT.ApplyPreset('jet', True)

# change scalar bar placement
uLUTColorBar.Title = ''
uLUTColorBar.ComponentTitle = ''
uLUTColorBar.LabelFontFamily = 'Times'
uLUTColorBar.LabelFontSize = 8
uLUTColorBar.LabelBold = 1
uLUTColorBar.LabelItalic = 1
uLUTColorBar.Orientation = 'Horizontal'
uLUTColorBar.WindowLocation = 'AnyLocation'
uLUTColorBar.Position = [0.25, 0.78]
uLUTColorBar.ScalarBarLength = 0.5
uLUTColorBar.ScalarBarThickness = 8
uLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
uLUTColorBar.AutomaticLabelFormat = 0
uLUTColorBar.LabelFormat = '%-#6.50f'
uLUTColorBar.RangeLabelFormat = '%-#6.2e' #'%-#4.4f'

# save screenshot
SaveScreenshot(DIRSAVE + '/UDis.png', renderView1, ImageResolution=[1100, 1000], OverrideColorPalette='PrintBackground')



#-------------------------------------------------------------- Temperature distribution --------------------------------------------------------------#
# set scalar coloring
ColorBy(CasefoamDisplay, ('POINTS', 'T'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(uLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
CasefoamDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
CasefoamDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'T'
tLUT = GetColorTransferFunction('T')

# get opacity transfer function/opacity map for 'T'
tPWF = GetOpacityTransferFunction('T')

# get color legend/bar for tLUT in view renderView1
tLUTColorBar = GetScalarBar(tLUT, renderView1)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
tLUT.ApplyPreset('jet', True)

# change scalar bar placement
tLUTColorBar.Title = ''
tLUTColorBar.LabelFontFamily = 'Times'
tLUTColorBar.LabelFontSize = 8
tLUTColorBar.LabelBold = 1
tLUTColorBar.LabelItalic = 1
tLUTColorBar.Orientation = 'Horizontal'
tLUTColorBar.WindowLocation = 'AnyLocation'
tLUTColorBar.Position = [0.25, 0.78]
tLUTColorBar.ScalarBarLength = 0.5
tLUTColorBar.ScalarBarThickness = 8
tLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
tLUTColorBar.AutomaticLabelFormat = 0
tLUTColorBar.LabelFormat = '%-#4.50f'
tLUTColorBar.RangeLabelFormat = '%-#4.1f'

# save screenshot
SaveScreenshot(DIRSAVE + '/TDis.png', renderView1, ImageResolution=[1100, 1000], OverrideColorPalette='PrintBackground')

#++++++++++++++++++++++++++++++++++++++++++ Temperature slice ++++++++++++++++++++++++++++++++++++++++++#
HideScalarBarIfNotNeeded(tLUT, renderView1)

# create a new 'Slice'
slice1 = Slice(Input=Casefoam)
slice1.SliceType = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [0.05, 0.05, 0.0]

# Properties modified on slice1.SliceType
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

# show data in view
slice1Display = Show(slice1, renderView1)

# trace defaults for the display properties.
slice1Display.Representation = 'Surface'
slice1Display.ColorArrayName = ['POINTS', 'T']
slice1Display.LookupTable = tLUT

slice1Display.SetScalarBarVisibility(renderView1, True)
tLUTColorBar = GetScalarBar(tLUT, renderView1)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
tLUT.ApplyPreset('jet', True)

# change scalar bar placement
tLUTColorBar.Title = ''
tLUTColorBar.LabelFontFamily = 'Times'
tLUTColorBar.LabelFontSize = 8
tLUTColorBar.LabelBold = 1
tLUTColorBar.LabelItalic = 1
tLUTColorBar.Orientation = 'Horizontal'
tLUTColorBar.WindowLocation = 'AnyLocation'
tLUTColorBar.Position = [0.25, 0.78]
tLUTColorBar.ScalarBarLength = 0.5
tLUTColorBar.ScalarBarThickness = 8
tLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
tLUTColorBar.AutomaticLabelFormat = 0
tLUTColorBar.LabelFormat = '%-#4.70f'
tLUTColorBar.RangeLabelFormat = '%-#4.1f'

#++++++++++++++++++++++++++++++++++++++++++ Temperature contour ++++++++++++++++++++++++++++++++++++++++++#
# create a new 'Contour'
contour1 = Contour(Input=Casefoam)

# Properties modified on contour1
contour1.ContourBy = ['POINTS', 'T']
#contour1.ContourBy = 'T'

num_Tcntr = 10
minT = min( Casefoam.PointData.GetArray("T").GetRange() )
maxT = max( Casefoam.PointData.GetArray("T").GetRange() )
stepT = (maxT-minT)/num_Tcntr
Tcntr = [minT + i*stepT for i in range(0, (num_Tcntr+1), 1)]
contour1.Isosurfaces = Tcntr

#RenameSource('Tcnt', contour1)
#print (T.GetRange())

# show data in view
contour1Display = Show(contour1, renderView1)

# change representation type
contour1Display.SetRepresentationType('Surface With Edges')

# Properties modified on contour1Display
contour1Display.EdgeColor = [0.0, 0.0, 0.0]

# Properties modified on tLUT
tLUT.NumberOfTableValues = 10


# save screenshot
SaveScreenshot(DIRSAVE + '/TCont.png', renderView1, ImageResolution=[1100, 1000], OverrideColorPalette='PrintBackground')



#-------------------------------------------------------------- StreamLine distribution --------------------------------------------------------------#
slice1Display = Hide(slice1, renderView1)
contour1Display = Hide(contour1, renderView1)

# set scalar coloring
ColorBy(CasefoamDisplay, ('POINTS', 'streamFunction'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(tLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
CasefoamDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
CasefoamDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'ST'
STLUT = GetColorTransferFunction('streamFunction')

# get opacity transfer function/opacity map for 'ST'
STPWF = GetOpacityTransferFunction('streamFunction')

# get color legend/bar for tLUT in view renderView1
STLUTColorBar = GetScalarBar(STLUT, renderView1)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
STLUT.ApplyPreset('jet', True)

# change scalar bar placement
STLUTColorBar.Title = ''
STLUTColorBar.LabelFontFamily = 'Times'
STLUTColorBar.LabelFontSize = 8
STLUTColorBar.LabelBold = 1
STLUTColorBar.LabelItalic = 1
STLUTColorBar.Orientation = 'Horizontal'
STLUTColorBar.WindowLocation = 'AnyLocation'
STLUTColorBar.Position = [0.25, 0.78]
STLUTColorBar.ScalarBarLength = 0.5
STLUTColorBar.ScalarBarThickness = 8
STLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
STLUTColorBar.AutomaticLabelFormat = 0
STLUTColorBar.LabelFormat = '%-#6.50f'
STLUTColorBar.RangeLabelFormat = '%-#6.2e'

# save screenshot
SaveScreenshot(DIRSAVE + '/SLDis.png', renderView1, ImageResolution=[1100, 1000], OverrideColorPalette='PrintBackground')

#++++++++++++++++++++++++++++++++++++++++++ streamLine slice ++++++++++++++++++++++++++++++++++++++++++#
HideScalarBarIfNotNeeded(STLUT, renderView1)

# create a new 'Slice'
slice2 = Slice(Input=Casefoam)
slice2.SliceType = 'Plane'
slice2.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice2.SliceType.Origin = [0.5, 0.5, 0.0]

# Properties modified on slice1.SliceType
slice2.SliceType.Normal = [0.0, 0.0, 1.0]

# show data in view
slice2Display = Show(slice2, renderView1)

# trace defaults for the display properties.
slice2Display.Representation = 'Surface'
slice2Display.ColorArrayName = ['POINTS', 'streamFunction']
slice2Display.LookupTable = STLUT

slice2Display.SetScalarBarVisibility(renderView1, True)
STLUTColorBar = GetScalarBar(STLUT, renderView1)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
STLUT.ApplyPreset('jet', True)

# change scalar bar placement
STLUTColorBar.Title = ''
STLUTColorBar.LabelFontFamily = 'Times'
STLUTColorBar.LabelFontSize = 8
STLUTColorBar.LabelBold = 1
STLUTColorBar.LabelItalic = 1
STLUTColorBar.Orientation = 'Horizontal'
STLUTColorBar.WindowLocation = 'AnyLocation'
STLUTColorBar.Position = [0.25, 0.78]
STLUTColorBar.ScalarBarLength = 0.5
STLUTColorBar.ScalarBarThickness = 8
STLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
STLUTColorBar.AutomaticLabelFormat = 0
STLUTColorBar.LabelFormat = '%-#6.50f'
STLUTColorBar.RangeLabelFormat = '%-#6.2e'

#++++++++++++++++++++++++++++++++++++++++++ streamLine contour ++++++++++++++++++++++++++++++++++++++++++#
# create a new 'Contour'
contour2 = Contour(Input=Casefoam)

# Properties modified on contour1
contour2.ContourBy = ['POINTS', 'streamFunction']
#contour1.ContourBy = 'streamFunction'

num_STcntr = 19
minST = min( Casefoam.PointData.GetArray("streamFunction").GetRange() )
maxST = max( Casefoam.PointData.GetArray("streamFunction").GetRange() )
stepST = (maxST-minST)/num_STcntr
STcntr = [minST + i*stepST for i in range(0, (num_STcntr+1), 1)]
contour2.Isosurfaces = STcntr

#RenameSource('streamFunctioncnt', contour2)


# show data in view
contour2Display = Show(contour2, renderView1)

# change representation type
contour2Display.SetRepresentationType('Surface With Edges')

# Properties modified on contour1Display
contour2Display.EdgeColor = [0.0, 0.0, 0.0]

# Properties modified on tLUT
STLUT.NumberOfTableValues = 19

# save screenshot
SaveScreenshot(DIRSAVE + '/SLcont.png', renderView1, ImageResolution=[1100, 1000], OverrideColorPalette='PrintBackground')


#-------------------------------------------------------------- End-of-file --------------------------------------------------------------#
