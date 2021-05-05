from abaqus import *
from abaqusConstants import *
from viewerModules import *

ModelName='weave_1_220'
def ExtractData(threadNumber, ModelName):

	o2 = session.openOdb(ModelName + '.odb')
	#: Number of Assemblies:         1
	#: Number of Assembly instances: 0
	#: Number of Part instances:     1
	#: Number of Meshes:             1
	#: Number of Element Sets:       38
	#: Number of Node Sets:          71
	#: Number of Steps:              1
	session.viewports['Viewport: 1'].setValues(displayedObject=o2)
	odb = session.odbs[str(ModelName) + '.odb']
	xy0 = xyPlot.XYDataFromHistory(odb=odb, 
		outputVariableName='Spatial displacement: U3 at Node 3998775 in NSET CONSTRAINTSDRIVER0', 
		steps=('Step-1', ), suppressQuery=True, __linkedVpName__='Viewport: 1')
	xy1 = xyPlot.XYDataFromHistory(odb=odb, 
		outputVariableName='Reaction force: RF3 at Node 3998775 in NSET CONSTRAINTSDRIVER0', 
		steps=('Step-1', ), suppressQuery=True, __linkedVpName__='Viewport: 1')
	xy2 = combine(xy0, xy1, )
	print(max(xy1[1]))
	print(max(xy1))
	ReactionForce=[]
	for i in xy1:
		ReactionForce.append(i[1])
	OFV=max(ReactionForce)
	print(OFV)
	xy_result = session.XYData(name='XYData-1', objectToCopy=xy2, 
		sourceDescription='combine(XYData-1, XYData-1, )')
	del session.xyDataObjects[xy0.name]
	del session.xyDataObjects[xy1.name]
	del session.xyDataObjects[xy2.name]
	c1 = session.Curve(xyData=xy_result)
	xyp = session.XYPlot('XYTESTPLOT')
	chartName = xyp.charts.keys()[0]
	chart = xyp.charts[chartName]
	chart.setValues(curvesToPlot=(c1, ), )
	session.viewports['Viewport: 1'].setValues(displayedObject=xyp)

	file=open("MeshConvergence.dat", "a")
	file.write(str(-OFV) + "\n")
	file.close()

	# from SubmitJobElastic import *
	# SubmitJob(ModelName, path1cell_offset, path2cell_offset, path3cell_offset, nbl, 4, 6)
	return

#FlatCohesiveSubmit(1, "weave_1_160")
ExtractData(1, ModelName)
