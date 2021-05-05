import sys
sys.path.append("C:\SIMULIA\CAE\2018\win_b64\tools\SMApy\python2.7\Lib\site-packages")
sys.path.append("F:\\")
from TexGen.Core import *


def WriteToInputTJoint(FileName):

	t=GetTextile()
    NumYarns=t.GetNumYarns()
	
    file=open(FileName, 'a+')
	
	#overwrite mat props
    file.write("*Material, Name=Mat0" + "\n")
    file.write("*Elastic" + "\n")
    file.write("3.5e+003, 0.35" + "\n")
    file.write("*Expansion" + "\n")
    file.write("5.27e-005" + "\n")
    file.write("*Density" + "\n")
    file.write("1000." + "\n")
    file.write("*Material, Name=Mat1" + "\n")
    file.write("*Elastic, type=ENGINEERING CONSTANTS" + "\n")
    file.write("1.744e+005, 8.9e+003, 8.9e+003, 0.3, 0.3, 0.3, 4.2e+003, 4.2e+003" + "\n")
    file.write("3e+003" + "\n")
    file.write("*Expansion, type=ORTHO" + "\n")
    file.write("5.4, 5.4, 5.4" + "\n")
    file.write("*Density" + "\n")
    file.write("1200" + "\n")
    file.write("*Solid Section, ElSet=Matrix, Material=Mat0" + "\n")
    file.write("1.0," + "\n")
    for i in range(2, NumYarns+2):
        file.write("*Solid Section, ElSet=Yarn" + str(i-2) + ", Material=Mat1, Orientation=TexGenOrientations" + "\n")
        file.write("1.0," + "\n")
	
	#linear constraints
    file.write("** Constraint: Eqn-1" + "\n")
    file.write("*Equation" + "\n")
    file.write("2" + "\n")
    file.write("WEBNODES, 3, 1." + "\n")
    file.write("CONSTRAINTSDRIVER0, 3, -1." + "\n")
    file.write("** Constraint: Eqn-2" + "\n")
    file.write("*Equation" + "\n")
    file.write("2" + "\n")
    file.write("FLANGEANODES, 3, 1." + "\n")
    file.write("CONSTRAINTSDRIVER1, 3, -1." + "\n")
	file.write("** Constraint: Eqn-3" + "\n")
    file.write("*Equation" + "\n")
    file.write("2" + "\n")
    file.write("FLANGEBNODES, 3, 1." + "\n")
    file.write("CONSTRAINTSDRIVER2, 3, -1." + "\n")
	
    #Amplitude
    file.write("*Amplitude, name=AMP-1, time=TOTAL TIME" + "\n")
    file.write("         0.,              0.,           100.,              1." + "\n")
    file.write("*Contact Clearance, name=clear1, adjust=YES" + "\n")
	
	
	#interaction properties
    file.write("** " + "\n")
    file.write("** INTERACTION PROPERTIES" + "\n")
    file.write("** " + "\n")
    file.write("*Surface Interaction, name=INTPROP-1" + "\n")
    file.write("*Cohesive Behavior, eligibility=ORIGINAL CONTACTS" + "\n")
    file.write("1e+06.,1e+06.,1e+06." + "\n")
    file.write("*Damage Initiation, criterion=MAXS" + "\n")
    file.write("60.,60.,60." + "\n")
    file.write("*Damage Evolution, type=ENERGY, mixed mode behavior=POWER LAW, power=2." + "\n")
    file.write("2.2, 8.4, 8.4" + "\n")
    file.write("*Surface Interaction, name=INTPROP-2" + "\n")
    file.write("*Surface Behavior, pressure-overclosure=HARD" + "\n")
    file.write("*Distribution Table, name=PART-1_PART-1_TEXGENORIENTATIONVECTORS_Table" + "\n")
    file.write("coord3d, coord3d" + "\n")
	
	#step
    file.write("** ----------------------------------------------------------------" + "\n")
    file.write("** " + "\n")
    file.write("** STEP: Step-1" + "\n")
    file.write("** " + "\n")
    file.write("*Step, name=Step-1, nlgeom=YES" + "\n")
    file.write("*Dynamic, Explicit" + "\n")
    file.write(", 100." + "\n")
    file.write("*Bulk Viscosity" + "\n")
    file.write("0.06, 1.2" + "\n")
    file.write("** Mass Scaling: Semi-Automatic" + "\n")
    file.write("** Whole Model" + "\n")
    file.write("*Variable Mass Scaling, dt=1., type=below min, frequency=1" + "\n")
    file.write("** " + "\n")
	
	#boundary conditions
    file.write("** BOUNDARY CONDITIONS" + "\n")
    file.write("** " + "\n")
    file.write("** Name: Disp-BC-1 Type: Symmetry/Antisymmetry/Encastre" + "\n")
    file.write("*Boundary" + "\n")
    file.write("CONSTRAINTSDRIVER1, ENCASTRE" + "\n")
    file.write("** Name: Disp-BC-2 Type: Displacement/Rotation" + "\n")
    file.write("*Boundary, amplitude= AMP-1" + "\n")
    file.write("CONSTRAINTSDRIVER0, 3, 3, 0.1" + "\n")
    file.write("** " + "\n")
	
	#interaction assignment
    file.write("** INTERACTIONS" + "\n")
    file.write("** " + "\n")
    file.write("** Interaction: general_contact" + "\n")
    file.write("*Contact, op=NEW" + "\n")
    file.write("*Contact Inclusions" + "\n")
    for i in range(2, NumYarns+2):
        file.write("SURFACE-YARN" + str(i-2) + ", SURFACE-MATRIX" + "\n")
    file.write("*Contact Property Assignment" + "\n")
    file.write(" ,  , INTPROP-2" + "\n")
    for i in range(2, NumYarns+2):
        file.write("SURFACE-YARN" + str(i-2) + " , SURFACE-MATRIX, INTPROP-1" + "\n")
    file.write("*Contact Formulation, type=PURE MASTER-SLAVE" + "\n")
    file.write(" , SURFACE-MATRIX , SLAVE" + "\n")
    file.write("**" + "\n")
	
	
	
	#file.write("*Contact Clearance Assignment" + "\n")
    #file.write("SURFACE-MATRIX, SURFACE-YARN" + str(i-2) + ", clear1" + "\n")
    #file.write("*Contact Inclusions" + "\n")
    #file.write("SURFACE-MATRIX , SURFACE-YARN" + str(i-2) + "\n")

    
    #file.write("*Contact Formulation, type=PURE MASTER-SLAVE" + "\n")
    #file.write("SURFACE-YARN" + str(i-2) +", SURFACE-MATRIX , SLAVE" + "\n")
    #file.write("** " + "\n")
	
	
	#output requests
    file.write("** OUTPUT REQUESTS" + "\n")
    file.write("** " + "\n")
    file.write("*Restart, write, number interval=1, time marks=NO" + "\n")
    file.write("** " + "\n")
    file.write("** FIELD OUTPUT: F-Output-1" + "\n")
    file.write("** " + "\n")
    file.write("*Output, field, number interval=200" + "\n")
    file.write("*Contact Output" + "\n")
    file.write("CDISP, CFORCE, CSDMG, CSMAXSCRT, CSMAXUCRT, CSQUADSCRT, CSQUADUCRT, CSTRESS, CTHICK" + "\n")
    file.write("** " + "\n")
    file.write("** FIELD OUTPUT: F-Output-2" + "\n")
    file.write("** " + "\n")
    file.write("*Node Output" + "\n")
    file.write("CF, RF, U" + "\n")
    file.write("** " + "\n")
    file.write("** FIELD OUTPUT: F-Output-4" + "\n")
    file.write("** " + "\n")
    file.write("*Element Output, directions=YES" + "\n")
    file.write("LE, PE, PEEQ, PEMAG, S" + "\n")
    file.write("** " + "\n")
    file.write("** FIELD OUTPUT: F-Output-3" + "\n")
    file.write("** " + "\n")
    file.write("*Element Output, directions=YES" + "\n")
    file.write("NFORC, " + "\n")
    file.write("** " + "\n")
    file.write("** HISTORY OUTPUT: H-Output-1" + "\n")
    file.write("** " + "\n")
    file.write("*Output, history" + "\n")
    file.write("*Node Output, nset=CONSTRAINTSDRIVER0" + "\n")
    file.write("RF1, RF2, RF3, U1, U2, U3" + "\n")
    file.write("*End Step")
    file.close()
	
	return
	



def WriteToInputCohesive(FileName):
    
    Textile=GetTextile()
    ##NumYarns=Textile.GetNumYarns()
    NumYarns=32
    
	
	#write linear constraint for constraintdriver0 node
    file=open(FileName, 'a+')
    file.write("\n")
    file.write("**Constraint: Constraint-1" + "\n")
    file.write("*Equation" + "\n")
    file.write("2" + "\n")
    file.write("BottomSurfaceNodes, 3, 1." + "\n")
    file.write("**" + "\n")
    file.write("CONSTRAINTSDRIVER1, 3, -1." + "\n")

    file.write("**Constraint: Constraint-2" + "\n")
    file.write("*Equation" + "\n")
    file.write("2" + "\n")
    file.write("TopSurfaceNodes, 3, 1." + "\n")
    file.write("**" + "\n")
    file.write("CONSTRAINTSDRIVER0, 3, -1." + "\n")
	
	#write interaction properties
    file.write("** INTERACTION PROPERTIES" + "\n")
    file.write("**" + "\n")
    file.write("*Surface Interaction, name=IntProp-1" + "\n")
    file.write("1.," + "\n")
    file.write("*Cohesive Behavior" + "\n")
    file.write(" 1e+06, 1e+06, 1e+06" + "\n")
    file.write("*Damage Initiation, criterion=QUADS" + "\n")
    file.write("60.,60.,60." + "\n")
    file.write("*Damage Evolution, type=ENERGY, mixed mode behavior=POWER LAW, power=2." + "\n")
    file.write(" 2.2, 8.4, 8.4" + "\n")
    file.write("*Distribution Table, name=PART-1_TEXGENORIENTATIONVECTORS_Table" + "\n")
    file.write("coord3d, coord3d" + "\n")
	

    
	
	#interaction behaviour
    file.write("**" + "\n")
    file.write("** INTERACTIONS" + "\n")
    file.write("**" + "\n")

	
    for i in range(NumYarns+1):
        i=i+1
        file.write("** Interaction: Int-" + str(i) + "\n")
        file.write("*Contact Pair, interaction=IntProp-1, small sliding, type=SURFACE TO SURFACE, no thickness" + "\n")
        file.write("SURFACE-YARN" + str(i-1) + ", SURFACE-MATRIX" + "\n")
        if i == NumYarns:
            break
	
	
	#Step
    file.write("** ----------------------------------------------------------------" + "\n")
    file.write("**" + "\n")
    file.write("*Step, name=Step-1, nlgeom=YES, inc=1000" + "\n")
    file.write("*Static" + "\n")
    file.write("0.01, 1., 1e-08, 1." + "\n")
	
	#loading BC
	#write BCs
    file.write("**" + "\n")
    file.write("** BOUNDARY CONDITIONS" + "\n")
    file.write("**" + "\n")
    file.write("** Name: BC-1 Type: Symmetry/Antisymmetry/Encastre" + "\n")
    file.write("*Boundary, op=NEW" + "\n")
    file.write("CONSTRAINTSDRIVER1, ENCASTRE" + "\n")
    file.write("**" + "\n")
    file.write("**" + "\n")
    file.write("** Name: Disp-BC-2 Type: Displacement/Rotation" + "\n")
    file.write("*Boundary, op=NEW" + "\n")
    file.write("CONSTRAINTSDRIVER0, 3, 3, 0.06" + "\n")
	
	#Output requests
    file.write("**" + "\n")
    file.write("** OUTPUT REQUESTS" + "\n")
    file.write("**" + "\n")
    file.write("*Restart, write, frequency=0" + "\n")
    file.write("**" + "\n")
    file.write("** FIELD OUTPUT: F-Output-1" + "\n")
    file.write("**" + "\n")
    file.write("*Output, field" + "\n")
    file.write("*Node Output" + "\n")
    file.write("CF, RF, U" + "\n")
    file.write("*Element Output, directions=YES" + "\n")
    file.write("LE, PE, PEEQ, PEMAG, S" + "\n")
    file.write("*Contact Output" + "\n")
    file.write("CDISP, CSDMG, CSMAXSCRT, CSMAXUCRT, CSQUADSCRT, CSQUADUCRT, CSTRESS" + "\n")
    file.write("**" + "\n")
    file.write("** HISTORY OUTPUT: H-Output-1" + "\n")
    file.write("**" + "\n")
    file.write("*Output, history" + "\n")
    file.write("*Node Output, nset=CONSTRAINTSDRIVER0" + "\n")
    file.write("RF3, U3" + "\n")
    file.write("*End Step")
    file.close()

    return
	
def WriteToInput(FileName):
    
    Textile=GetTextile()
    ##NumYarns=Textile.GetNumYarns()
    NumYarns=32
    
	
	#write linear constraint for constraintdriver0 node
    file=open(FileName, 'a+')
    file.write("\n")
    file.write("**Constraint: Constraint-1" + "\n")
    file.write("*Equation" + "\n")
    file.write("2" + "\n")
    file.write("BottomSurfaceNodes, 3, 1." + "\n")
    file.write("**" + "\n")
    file.write("CONSTRAINTSDRIVER1, 3, -1." + "\n")

    file.write("**Constraint: Constraint-2" + "\n")
    file.write("*Equation" + "\n")
    file.write("2" + "\n")
    file.write("TopSurfaceNodes, 3, 1." + "\n")
    file.write("**" + "\n")
    file.write("CONSTRAINTSDRIVER0, 3, -1." + "\n")
	
	
	#Step
    file.write("** ----------------------------------------------------------------" + "\n")
    file.write("**" + "\n")
    file.write("*Step, name=Step-1, nlgeom=YES, inc=1000" + "\n")
    file.write("*Static" + "\n")
    file.write("0.01, 1., 1e-08, 1." + "\n")
	
	#loading BC
	#write BCs
    file.write("**" + "\n")
    file.write("** BOUNDARY CONDITIONS" + "\n")
    file.write("**" + "\n")
    file.write("** Name: BC-1 Type: Symmetry/Antisymmetry/Encastre" + "\n")
    file.write("*Boundary, op=NEW" + "\n")
    file.write("CONSTRAINTSDRIVER1, ENCASTRE" + "\n")
    file.write("**" + "\n")
    file.write("**" + "\n")
    file.write("** Name: Disp-BC-2 Type: Displacement/Rotation" + "\n")
    file.write("*Boundary, op=NEW" + "\n")
    file.write("CONSTRAINTSDRIVER0, 3, 3, 0.06" + "\n")
	
	#Output requests
    file.write("**" + "\n")
    file.write("** OUTPUT REQUESTS" + "\n")
    file.write("**" + "\n")
    file.write("*Restart, write, frequency=0" + "\n")
    file.write("**" + "\n")
    file.write("** FIELD OUTPUT: F-Output-1" + "\n")
    file.write("**" + "\n")
    file.write("*Output, field" + "\n")
    file.write("*Node Output" + "\n")
    file.write("CF, RF, U" + "\n")
    file.write("*Element Output, directions=YES" + "\n")
    file.write("LE, PE, PEEQ, PEMAG, S" + "\n")
    file.write("*Contact Output" + "\n")
    file.write("CDISP, CSDMG, CSMAXSCRT, CSMAXUCRT, CSQUADSCRT, CSQUADUCRT, CSTRESS" + "\n")
    file.write("**" + "\n")
    file.write("** HISTORY OUTPUT: H-Output-1" + "\n")
    file.write("**" + "\n")
    file.write("*Output, history" + "\n")
    file.write("*Node Output, nset=CONSTRAINTSDRIVER0" + "\n")
    file.write("RF3, U3" + "\n")
    file.write("*End Step")
    file.close()

    return

def insert_line(FileName, line, newline):
    
    import fileinput
    for line in fileinput.FileInput(FileName,inplace=1):
        if newline in line:
            line=line.replace(line,line+newline)
        print line,

def WriteToInputExplicit(FileName):

    #file=open(FileName, 'a+')
	
    #from TexGen.Core import *
    t=GetTextile()
    NumYarns=t.GetNumYarns()
	
    file=open(FileName, 'a+')
	
	#overwrite mat props
    file.write("*Material, Name=Mat0" + "\n")
    file.write("*Elastic" + "\n")
    file.write("3.5e+003, 0.35" + "\n")
    file.write("*Expansion" + "\n")
    file.write("5.27e-005" + "\n")
    file.write("*Density" + "\n")
    file.write("1000." + "\n")
    file.write("*Material, Name=Mat1" + "\n")
    file.write("*Elastic, type=ENGINEERING CONSTANTS" + "\n")
    file.write("1.744e+005, 8.9e+003, 8.9e+003, 0.3, 0.3, 0.3, 4.2e+003, 4.2e+003" + "\n")
    file.write("3e+003" + "\n")
    file.write("*Expansion, type=ORTHO" + "\n")
    file.write("5.4, 5.4, 5.4" + "\n")
    file.write("*Density" + "\n")
    file.write("1200" + "\n")
    file.write("*Solid Section, ElSet=Matrix, Material=Mat0" + "\n")
    file.write("1.0," + "\n")
    for i in range(2, NumYarns+2):
        file.write("*Solid Section, ElSet=Yarn" + str(i-2) + ", Material=Mat1, Orientation=TexGenOrientations" + "\n")
        file.write("1.0," + "\n")
	
	#linear constraints
    file.write("** Constraint: Eqn-1" + "\n")
    file.write("*Equation" + "\n")
    file.write("2" + "\n")
    file.write("BOTTOMSURFACENODES, 3, 1." + "\n")
    file.write("CONSTRAINTSDRIVER1, 3, -1." + "\n")
    file.write("** Constraint: Eqn-2" + "\n")
    file.write("*Equation" + "\n")
    file.write("2" + "\n")
    file.write("TOPSURFACENODES, 3, 1." + "\n")
    file.write("CONSTRAINTSDRIVER0, 3, -1." + "\n")
	
    #Amplitude
    file.write("*Amplitude, name=AMP-1, time=TOTAL TIME" + "\n")
    file.write("         0.,              0.,           100.,              1." + "\n")
    file.write("*Contact Clearance, name=clear1, adjust=YES" + "\n")
	
	
	#interaction properties
    file.write("** " + "\n")
    file.write("** INTERACTION PROPERTIES" + "\n")
    file.write("** " + "\n")
    file.write("*Surface Interaction, name=INTPROP-1" + "\n")
    file.write("*Cohesive Behavior, eligibility=ORIGINAL CONTACTS" + "\n")
    file.write("1e+06.,1e+06.,1e+06." + "\n")
    file.write("*Damage Initiation, criterion=MAXS" + "\n")
    file.write("60.,60.,60." + "\n")
    file.write("*Damage Evolution, type=ENERGY, mixed mode behavior=POWER LAW, power=2." + "\n")
    file.write("2.2, 8.4, 8.4" + "\n")
    file.write("*Surface Interaction, name=INTPROP-2" + "\n")
    file.write("*Surface Behavior, pressure-overclosure=HARD" + "\n")
    file.write("*Distribution Table, name=PART-1_PART-1_TEXGENORIENTATIONVECTORS_Table" + "\n")
    file.write("coord3d, coord3d" + "\n")
	
	#step
    file.write("** ----------------------------------------------------------------" + "\n")
    file.write("** " + "\n")
    file.write("** STEP: Step-1" + "\n")
    file.write("** " + "\n")
    file.write("*Step, name=Step-1, nlgeom=YES" + "\n")
    file.write("*Dynamic, Explicit" + "\n")
    file.write(", 100." + "\n")
    file.write("*Bulk Viscosity" + "\n")
    file.write("0.06, 1.2" + "\n")
    file.write("** Mass Scaling: Semi-Automatic" + "\n")
    file.write("** Whole Model" + "\n")
    file.write("*Variable Mass Scaling, dt=1., type=below min, frequency=1" + "\n")
    file.write("** " + "\n")
	
	#boundary conditions
    file.write("** BOUNDARY CONDITIONS" + "\n")
    file.write("** " + "\n")
    file.write("** Name: Disp-BC-1 Type: Symmetry/Antisymmetry/Encastre" + "\n")
    file.write("*Boundary" + "\n")
    file.write("CONSTRAINTSDRIVER1, ENCASTRE" + "\n")
    file.write("** Name: Disp-BC-2 Type: Displacement/Rotation" + "\n")
    file.write("*Boundary, amplitude= AMP-1" + "\n")
    file.write("CONSTRAINTSDRIVER0, 3, 3, 0.1" + "\n")
    file.write("** " + "\n")
	
	#interaction assignment
    file.write("** INTERACTIONS" + "\n")
    file.write("** " + "\n")
    
    file.write("** Interaction: general_contact" + "\n")
    file.write("*Contact, op=NEW" + "\n")
    file.write("*Contact Inclusions" + "\n")
    for i in range(2, NumYarns+2):
        file.write("SURFACE-YARN" + str(i-2) + ", SURFACE-MATRIX" + "\n")
    file.write("*Contact Property Assignment" + "\n")
    file.write(" ,  , INTPROP-2" + "\n")
    for i in range(2, NumYarns+2):
        file.write("SURFACE-YARN" + str(i-2) + " , SURFACE-MATRIX, INTPROP-1" + "\n")
    file.write("*Contact Formulation, type=PURE MASTER-SLAVE" + "\n")
    file.write(" , SURFACE-MATRIX , SLAVE" + "\n")
    file.write("**" + "\n")
	
	
	
	#file.write("*Contact Clearance Assignment" + "\n")
    #file.write("SURFACE-MATRIX, SURFACE-YARN" + str(i-2) + ", clear1" + "\n")
    #file.write("*Contact Inclusions" + "\n")
    #file.write("SURFACE-MATRIX , SURFACE-YARN" + str(i-2) + "\n")

    
    #file.write("*Contact Formulation, type=PURE MASTER-SLAVE" + "\n")
    #file.write("SURFACE-YARN" + str(i-2) +", SURFACE-MATRIX , SLAVE" + "\n")
    #file.write("** " + "\n")
	
	
	#output requests
    file.write("** OUTPUT REQUESTS" + "\n")
    file.write("** " + "\n")
    file.write("*Restart, write, number interval=1, time marks=NO" + "\n")
    file.write("** " + "\n")
    file.write("** FIELD OUTPUT: F-Output-1" + "\n")
    file.write("** " + "\n")
    file.write("*Output, field, number interval=200" + "\n")
    file.write("*Contact Output" + "\n")
    file.write("CDISP, CFORCE, CSDMG, CSMAXSCRT, CSMAXUCRT, CSQUADSCRT, CSQUADUCRT, CSTRESS, CTHICK" + "\n")
    file.write("** " + "\n")
    file.write("** FIELD OUTPUT: F-Output-2" + "\n")
    file.write("** " + "\n")
    file.write("*Node Output" + "\n")
    file.write("CF, RF, U" + "\n")
    file.write("** " + "\n")
    file.write("** FIELD OUTPUT: F-Output-4" + "\n")
    file.write("** " + "\n")
    file.write("*Element Output, directions=YES" + "\n")
    file.write("LE, PE, PEEQ, PEMAG, S" + "\n")
    file.write("** " + "\n")
    file.write("** FIELD OUTPUT: F-Output-3" + "\n")
    file.write("** " + "\n")
    file.write("*Element Output, directions=YES" + "\n")
    file.write("NFORC, " + "\n")
    file.write("** " + "\n")
    file.write("** HISTORY OUTPUT: H-Output-1" + "\n")
    file.write("** " + "\n")
    file.write("*Output, history" + "\n")
    file.write("*Node Output, nset=CONSTRAINTSDRIVER0" + "\n")
    file.write("RF1, RF2, RF3, U1, U2, U3" + "\n")
    file.write("*End Step")
    file.close()
	
    return