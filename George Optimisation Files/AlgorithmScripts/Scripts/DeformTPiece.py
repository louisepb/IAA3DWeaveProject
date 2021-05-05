from math import *
from TexGen.Core import *

def TransformPoint( Point, Origin ):
	print 'Point.y = ', Point.y, 'Point.z', Point.z
	
	OffsetPoint = Point - Origin
	print 'Offset.y = ', OffsetPoint.y, 'Offset.z = ', OffsetPoint.z
	Angle = 0.0
	dy = 0.0
	dz = 0.0
	HalfPi = PI / 2.0
	
	if (OffsetPoint.y < 0.0) & (fabs(OffsetPoint.y) <= HalfPi*OffsetPoint.z) :
		print 'Fillet'
		Angle = -OffsetPoint.y / OffsetPoint.z
		dy = OffsetPoint.z * sin(Angle) + OffsetPoint.y
		dz = OffsetPoint.z * cos(Angle) - OffsetPoint.z
	else:
		print 'Flange'
		Angle = -HalfPi
		dy = OffsetPoint.z + OffsetPoint.y
		dz = ( HalfPi * OffsetPoint.z + OffsetPoint.y ) - OffsetPoint.z
	
	OffsetPoint.y = OffsetPoint.y - dy + Origin.y
	OffsetPoint.z = OffsetPoint.z + dz + Origin.z
	print 'Angle =', Angle, 'Point y = ', OffsetPoint.y, 'Point.z = ', OffsetPoint.z 
	return OffsetPoint, -Angle

	
def TransformPointUp( Point, Origin ):
	print 'Point.y = ', Point.y, 'Point.z', Point.z
	
	OffsetPoint = Point - Origin
	print 'UpOffset.y = ', OffsetPoint.y, 'Offset.z = ', OffsetPoint.z
	Angle = 0.0
	dy = 0.0
	dz = 0.0
	HalfPi = PI / 2.0
	
	if (OffsetPoint.y < 0.0) & (fabs(OffsetPoint.y) <= fabs(HalfPi*OffsetPoint.z)) :
		print 'Fillet'
		Angle = -OffsetPoint.y / fabs(OffsetPoint.z)
		dy = fabs(OffsetPoint.z) * sin(Angle) + OffsetPoint.y
		dz = OffsetPoint.z * cos(Angle) - OffsetPoint.z
	else:
		print 'Flange'
		Angle = -HalfPi
		dy = fabs(OffsetPoint.z) + OffsetPoint.y
		dz = (-(HalfPi * fabs(OffsetPoint.z)) - OffsetPoint.y) - OffsetPoint.z
		print 'dy = ', dy, 'dz = ', dz
	
	OffsetPoint.y = OffsetPoint.y - dy + Origin.y
	OffsetPoint.z = OffsetPoint.z + dz + Origin.z
	print 'Angle =', Angle, 'Point y = ', OffsetPoint.y, 'Point.z = ', OffsetPoint.z 
	return OffsetPoint, Angle

def TransformYarn( Yarn, Origin, Up ):
	
	YarnSection = Yarn.GetYarnSection()
	SectionConstant = YarnSection.GetSectionConstant()
	Section = SectionConstant.GetSection()
	
	Nodes = Yarn.GetMasterNodes()
	i = 0
	for Node in Nodes:
		Point = Node.GetPosition()
		if Up == True:
			Point,Angle = TransformPointUp( Point, Origin )
		else:
			Point,Angle = TransformPoint( Point, Origin )
		if i == 0:
			RotatedSection = CSectionRotated( Section, Angle )
		Node.SetPosition( Point )
		Yarn.ReplaceNode( i, Node )
		i += 1
	NewSection = CYarnSectionConstant( RotatedSection )
	Yarn.AssignSection( NewSection )
	
def TransformYarnSection( Yarn, Origin, MaxIndex, Up ):
	Nodes = Yarn.GetMasterNodes()
	i = 0
	for i in range(0, MaxIndex+1):
		Point = Nodes[i].GetPosition()
		if Up == True:
			Point,Angle = TransformPointUp( Point, Origin )
		else:
			Point,Angle = TransformPoint( Point, Origin )
		Nodes[i].SetPosition( Point )
		Yarn.ReplaceNode( i, Nodes[i] )
		i += 1
		


# Create bifurcation from flat woven textile
Textile = GetTextile()
Weave = Textile.GetOrthogonalWeave()
Yarns = Textile.GetYarns()
MaxWeftIndex = 7  # Need to transform from node 0 to max index on weft yarns
# y value of origin corresponds to position of last binder yarn which spans the whole textile
# Differernce between z value and z coordinate of bottom binder node gives effective radius
# Origin for lower yarns
Origin = XYZ(0, 11.5175, -2.21)
#Origin = XYZ(0, 8.5, -3)

# Binder yarns 9, 27
LowerWarpYarns = [1,2,3,4,9,10,11,12,13,19,20,21,22,27,28,29,30,31]
for x in LowerWarpYarns:
	Yarn = Yarns[x]
	TransformYarn( Yarn, Origin, False )

LowerWeftYarns = [54,55,56,57,58,64,65,66,67,68]
for x in LowerWeftYarns:
	Yarn = Yarns[x]
	TransformYarnSection( Yarn, Origin, MaxWeftIndex, False )
	Yarn.AssignInterpolation( CInterpolationCubic( False ) )
	Weave.CheckUpVectors(x, PATTERN3D_YYARN, True )

#Origin for upper yarns	
Origin = XYZ(0, 11.5175, 6)
#Origin = XYZ(0, 8.5, 6.5)

# Binder yarns 0,18
UpperWarpYarns = [0,5,6,7,8,14,15,16,17,18,23,24,25,26,32,33,34,35]
for x in UpperWarpYarns:
	Yarn = Yarns[x]
	TransformYarn( Yarn, Origin, True )

UpperWeftYarns = [59,60,61,62,63,69,70,71,72,73]
for x in UpperWeftYarns:
	Yarn = Yarns[x]
	TransformYarnSection( Yarn, Origin, MaxWeftIndex, True )
	Yarn.AssignInterpolation( CInterpolationCubic( False ) )
	Weave.CheckUpVectors(x, PATTERN3D_YYARN, True )

