#George Spackman 19.01.2018
#functions to check constraint violation on the binder paths
# binder paths defined using z offsets between 0 and the number of layers, nly
# forms a vector
# Constraints
# 1. A binder needs to go over and another one needs to go under for every weft stack
# 2. No unbound binder yarns above or below weft stacks (applies individually for this special case).
#    implemented in linear constraints (matlab)
# 3. There has to be at least one binder yarn crossing all horizontal planes between weft layers within the unit cell
#    to interlace with wefts to prevent the textile separating between them (remove this constraint to create bifurcations).

import sys
sys.path.append("C:\SIMULIA\CAE\2018\win_b64\tools\SMApy\python2.7\Lib\site-packages")
from TexGen.Core import *

class BinderFunctions:

    """
    Binder functions class, based off TexGen code by Louise Brown
    """

    def GetXYarnIndex(self, iIndex):
        textile=GetTextile()
        weave3D=textile.Get3DWeave()
        NumXYarns=weave3D.GetNumXYarns()
        for k in range(NumXYarns):
            if k==iIndex:
                return k
        return -1

    def GetBinderOffsets(self, x, y):
        textile=GetTextile()
        weave3D=textile.Get3DWeave()
        vector1=weave3D.GetCell(x, y)
        #print('vector 1', vector1)
        TopBinder=self.FindTopBinderYarns(vector1)
        offset=((len(vector1)-1)-TopBinder)/2
        return offset

    def FindTopBinderYarns(self, vector1):
        #print('vector1 here', vector1)
        i=len(vector1)-1
        while i>0:
            if vector1[i]==1:
                return i
            i=i-1
        return i



def CheckBinderPaths3NoBifurcation(planepos, nbl):
## This function checks that binder yarns cross every internal plane between weft layers
##    
    #get the textile and relevant types with their methods
    textile=GetTextile()
    weave3D=textile.Get3DWeave()
    layertolayer=textile.GetLayerToLayerWeave()
    #to get number of x and y yarns use weave3D
    NumXYarns=weave3D.GetNumXYarns()
    NumWeftStacks=weave3D.GetNumYYarns()
    binders=[]
    IY=[]

    
    #look at XYarns only
    for i in range(NumXYarns):
        binder=weave3D.IsBinderYarn(i)
        if binder:
            binderyarn=textile.GetYarn(i)
            nodes=binderyarn.GetMasterNodes()
            for node in nodes:
                nodepos=node.GetPosition()
                nodey=nodepos.y
                print nodey
            #check this gets the correct yarn by printing out the nodes
            binders.append(binderyarn)
            #instantiate binder functions object
            BF=BinderFunctions()
            YPosition=BF.GetXYarnIndex(i)
            IY.append(YPosition)
    c=0
    #get the binder offsets
    #below would iterate through list of all the iy positions generated above
    for iy in IY:
        offsets=[]
        for ix in range(NumWeftStacks):
            offset=BF.GetBinderOffsets(ix, iy)
            offsets.append(offset)
            if nbl>=1:
                offsets.append(offset+(nbl-1)) #if 3 binders needs to be +2 etc.
        a=0
        b=0
        for value in offsets:
            #remember 0 at top of weft stack so may seem backwards
            if value > planepos:
                a=a+1
            elif value < planepos:
                b=b+1
        if a>=1 and b>=1: #one of offsets for yarn above and another below plane
            c=c+1
        else:
            c=c
    z=planepos-1
    if z>=1:
        if c>=1:
            #Recursively call the function, raising the plane position until the algorithm reaches the top of the stack
            return CheckBinderPaths3NoBifurcation(planepos-1, nbl)
        #if not satisfied for plane, exit the recursion and apply penalty
        else:
            return 1
    #check last plane
    else:
        if c>=1:
            return 0
        else:
            return 1






    
def CheckBinderPaths3WarpBifurcation(planepos, bifstart, bifplane):
    #bifurcation along the warp direction, want to penalise weaves that don't satisfy con 3 before bifstart and those that do after for a certain plane

    textile=GetTextile()
    weave3D=textile.Get3DWeave()
    layertolayer=textile.GetLayerToLayerWeave()
    #to get number of x and y yarns use weave3D
    NumXYarns=weave3D.GetNumXYarns()
    NumWeftStacks=weave3D.GetNumYYarns()
    binders=[]
    IY=[]

    
    for i in range(NumXYarns):
        binder=weave3D.IsBinderYarn(i)
        if binder:
            binderyarn=textile.GetYarn(i)
            binders.append(binderyarn)
            BF=BinderFunctions()
            YPosition=BF.GetXYarnIndex(i)
            IY.append(YPosition)
    j=0
    k=0   #j, k after bifurcation
    c=0   #before bifurcation
    #get the binder offsets
    #below would iterate through list of all the iy positions generated above
    for iy in IY:
        offsets=[]


        
        #perform checks that all planes are crossed before bifurcation
        for ix in range(bifstart):
            offset=BF.GetBinderOffsets(ix, iy)
            offsets.append(offset)
        a=0
        b=0
        for value in offsets:
            #remember 0 at top of weft stack so may seem backwards
            if value > planepos:
                a=a+1
            elif value < planepos:
                b=b+1
        if a>=1 and b>=1: #yarn crosses plane
            c=c+1
        else: #yarn does not cross plane
            c=c

            
        #perform check that a yarn does not cross plane after bif, if planepos==bifplane
        bifoffsets=[]
        for ix in range(bifstart, NumWeftStacks, 1):
            offset=BF.GetBinderOffsets(ix, iy)
            bifoffsets.append(offset)
        g=0
        h=0
        for value in bifoffsets:
            if value > planepos:
                g=g+1
            elif value < planepos:
                h=h+1



        if planepos==bifplane:
            if g<1 and h<1: #means binder does not cross bifurcation plane - good
                j=j+1
            else:           #means binder does cross bifplane - raise penalty value
                j=j
        else:
            if g>=1 and h>=1: #binder must cross plane - raise penalty value
                k=k+1
            else:
                k=k


                
    # should have increases or decreases in c, j, k if constraint 3 violated or if yarn crosses at bifurcation
    print('The outcome of CBP3 is:')
    #check this tomorrow
    z=planepos-1
    if z>=1:
        if c>=1: #textile before bifplane is fully bound
            if 'k' in locals() and k>=1:
                #Recursively call the function, raising the plane position until the algorithm reaches the top of the stack
                return CheckBinderPaths3(planepos-1, bifstart, bifplane, bifurcation=True)
            elif 'j' in locals() and j>=1:
                return CheckBinderPaths3(planepos-1, bifstart, bifplane, bifurcation=True)
            elif 'k' in locals() and k<1:
                return 1
            elif 'j' in locals() and k<1:
                return 5
        #if not satisfied for plane, move to next plane for now
        elif c<1: #textile before plane not fully bound
            if 'k' in locals() and k>=1:
                #Recursively call the function, raising the plane position until the algorithm reaches the top of the stack
                return 1
            elif 'j' in locals() and j>=1:
                return 1
            elif 'k' in locals() and k<1:
                return 3
            elif 'j' in locals() and k<1:
                return 8
           
    #check last plane
    else:
        if c>=1:
            if 'k' in locals() and k>=1:
                #Recursively call the function, raising the plane position until the algorithm reaches the top of the stack
                return 0
            elif 'j' in locals() and j>=1:
                return 0
            elif 'k' in locals() and k<=1:
                return 1
            elif 'j' in locals() and k<1:
                return 5
            #if not satisfied for plane, move to next plane for now
        elif c<1:
            if 'k' in locals() and k>=1:
                #Recursively call the function, raising the plane position until the algorithm reaches the top of the stack
                return 1
            elif 'j' in locals() and j>=1:
                return 1
            elif 'k' in locals() and k<1:
                return 2
            elif 'j' in locals() and k<1:
                return 6



##def CheckBinderPaths3WeftBifurcation(planepos, bifstart, bifplane):
##
##    #check that binder yarns before the bifurcation pass all the way through the textile
##    #check that after bifurcation, binder yarns stay above or below the bifplane
##    #check that con 1 is still enforced after the bifurcation
##
##    textile=GetTextile()
##    weave3D=textile.Get3DWeave()
##    layertolayer=textile.GetLayerToLayerWeave()
##    #to get number of x and y yarns use weave3D
##    NumXYarns=weave3D.GetNumXYarns()
##    NumWeftStacks=weave3D.GetNumYYarns()
##    binders=[]
##    IY=[]
##
##    for i in range(NumXYarns):
##        binder=weave3D.IsBinderYarn(i)
##        if binder:
##            binderyarn=textile.GetYarn(i)
##            binders.append(binderyarn)
##            BF=BinderFunctions()
##            YPosition=BF.GetXYarnIndex(i)
##            IY.append(YPosition)
##
##    offsets=[]
##    bifoffsets=[]
##    for iy in IY:
##        #before bifurcation perform normal con 3 check
##        for ix in range(bifstart):
##            offset=BF.GetBinderOffsets(ix, iy)
##            offsets.append(offset)
##        a=0
##        b=0
##        for value in offsets:
##            #remember 0 at top of weft stack so may seem backwards
##            if value > planepos:
##                a=a+1
##            elif value < planepos:
##                b=b+1
##        if a>=1 and b>=1: #yarn crosses plane
##            c=c+1
##        else: #yarn does not cross plane
##            c=c
##
##
##
##        for ix in range(bifstart, NumWeftStacks):
##            offset=BF.GetBinderOffsets(ix, iy)
##            bifoffsets.append(offset)
##            
##            
##
##        #need each yarn to stay above or below the bifurcation plane after bifurcation
##        for offset in bifoffsets:
##            if bifoffsets[0] > bifplane:
##                while offset > bifplane:
##                    print('Yarn stays above bifurcation plane after bifurcation at this weft stack')
##                else:
##                    #penalise
##            else:
##                while offset < bifplane:
##                    print('Yarn stays below bifurcation plane after bifurcation at this weft stack')
##                else:
##                    #penalise
##        
##            #now need to implement con 3 after bifurcation - have a think!!


def CheckBinderPaths1NoBifurcation(nly, nbl):
    #making a list of a list of all the zpos offsets ie. the yarns, make a list of
    #offsets in a weft stack in Matrix and a list of all the z offsets in a yarn in znode


    #check CBP3 works first before imposing bifurcation in here
    maxOffset = nly - (nbl-1)
    textile=GetTextile()
    weave3D=textile.Get3DWeave()
    layertolayer=textile.GetLayerToLayerWeave()
    #to get number of x and y yarns use weave3D
    NumXYarns=weave3D.GetNumXYarns()
    NumWeftStacks=weave3D.GetNumYYarns()
    binders=[]
    IY=[]

    for i in range(NumXYarns):
        binder=weave3D.IsBinderYarn(i)
        if binder:
            binderyarn=textile.GetYarn(i)
            binders.append(binderyarn)
            BF=BinderFunctions()
            YPosition=BF.GetXYarnIndex(i)
            IY.append(YPosition)

    offsets=[]       
    for iy in IY:
        for ix in range(NumWeftStacks):
            offset=BF.GetBinderOffsets(ix, iy)
            offsets.append(offset)

    WeftStacks=[]
    for i in range(NumWeftStacks):
        WeftStacks.append(offsets[i::NumWeftStacks])

    b=0
    for Stack in WeftStacks:
        stack=Stack
        #print stack
        if all(x in stack for x in [0, maxOffset]):
            b=b+0
            print 'first constraint not violated, all yarns bound in stack'      
        else:
            b=b+1
            print 'first constraint violated, not all yarns are bound'

    print 'the value of b is', b

    return b

def CheckBinderPaths1WarpBifurcation(nly, bifstart, bifplane):
#Check the 1st constraint before and after the bifurcation in the warp direction



    textile=GetTextile()
    weave3D=textile.Get3DWeave()
    layertolayer=textile.GetLayerToLayerWeave()
    NumYarns=textile.GetNumYarns()
    NumXYarns=weave3D.GetNumXYarns()
    NumWeftStacks=weave3D.GetNumYYarns()
    binders=[]
    IY=[]

    for i in range(NumXYarns):
        binder=weave3D.IsBinderYarn(i)
        if binder:
            binderyarn=textile.GetYarn(i)
            binders.append(binderyarn)
            BF=BinderFunctions()
            YPosition=BF.GetXYarnIndex(i)
            IY.append(YPosition)

    offsets=[]       
    for iy in IY:
        for ix in range(NumWeftStacks):
            offset=BF.GetBinderOffsets(ix, iy)
            offsets.append(offset)

    
    StacksBefore=[]
    StacksAfter=[]
    #this is where to modify the code
    for i in range(bifstart):
        StacksBefore.append(offsets[i::bifstart])
        
    for i in range(bifstart, NumWeftStacks):
        StacksAfter.append(offsets[i::NumWeftStacks])
    a=0
    b=0
    c=0
    
    for Stack in StacksBefore:
        stack=Stack
        #print stack
        if all(x in stack for x in [0, nly]):
            a=a+0
            print 'first constraint not violated, all yarns bound in stack'      
        else:
            a=a+1
            print 'first constraint violated, not all yarns are bound'

    

    for Stack in StacksAfter:
        stack=Stack
        seen=[]
        #need 2 in list at bifplane so that both strands after bifurcation are fully bound
        for x in stack:
            if x==bifplane:
                seen.append(x)
        if len(seen)>1:
            c=c
        else:
            c=c+1
        #print stack
        if all(x in stack for x in [0, nly, bifplane]):
            b=b+0
            print 'first constraint not violated, all yarns bound in stack'      
        else:
            b=b+1
            print 'first constraint violated, not all yarns are bound'

       
    violation = a + b + c
    print 'the value of constraint violation is', violation

    return violation

##
##
###to get the bifurcations along the warp stacks (in the weft direction) use the NumWarpStacks=NumXYarns??
