#28.05.2015 Frank Gommer
#test 3d weave scripting
#one warp yarn stack + 2 binder yarn layers
#vary width of binder yarns at constant gap between all x yarns

#DeleteTextile("test3D")

#print("start \n \n \n \n \n \n \n")

# Nwarp - number of warp yarns (total i.e. warp + binder)
# Nweft - number of weft yarns
# Nbind - number of binder yarns
# Lwarp - number of weft layers
# Lbind - number of binder layers
# P - binder yarn positions

from TexGen.Core import * 
#from TexGen.Abaqus import *
import os
import sys
import imp
import math
import argparse
from numpy.linalg import inv
import numpy as np

fpath = os.getcwd()
sys.path.append(fpath)


#sys.path.append('C:\Program Files\TexGen_oct\Python\libxtra')
#sys.path.append('C:\Users\ezzmm2\Dropbox\optimization project\optimisation_code\torque_optimisation')
#from TexGen.Core import *
#from TexGen.Abaqus import *
 
def myLtoL(Nwarp, Nweft, Nbind, Lwarp, Lbind, my_geom, P):

############################################################
#textile base data
  nbl = Lbind #number of binder layers
  nx = Nwarp #number of x (warp) yarns
  ny = Nweft #number of y (weft) yarns -1
  
  sx = my_geom['sx'] # x (warp) yarn spacing
  sy = my_geom['sy'] # y (weft) yarn spacing
  sb = my_geom['sb'] # binder (warp) yarn spacing                     
  hx = my_geom['hx'] # x(warp) yarn heights
  hy = my_geom['hy'] #y( weft) yarn heights
  hb = my_geom['hb'] #x (binder) yarn heights
  wy = my_geom['wy'] #weft yarn width
  wx = my_geom['wx'] #warp (binder) yarn width
  wb = my_geom['wb'] #binder width
  g = my_geom['g']   #fixed gap between parallel x (warp and binder) yarns
  x_power = my_geom['x_power'] # x (warp) yarn power
  y_power = my_geom['y_power'] # y (weft) yarn power
  b_power = my_geom['b_power'] # binder yarn power 

  nly=Lwarp #number of weft layers
  nbind=nx-1 #nbind=1<=nbind<=nx
  nbind= nx - Nbind
  nwarp= Nbind

############################################################
  #sx=nwarp*(wx+g)+nbind*(wb+g)+0.5*wx
  #sx=wx+wb+g #nwarp*(wx+g)+nbind*(wb+g)+0.5*wx

############################################################
#create textile
  weave = CTextileLayerToLayer(nx, ny, sx, sy, hx, hy, nbl, True)

#set number of binder / warp yarns
  weave.SetWarpRatio( 1 )
  weave.SetBinderRatio( 1 )

#set the number of layers
  weave.SetupLayers( nly-1, nly, nbl)
  #weave.SetupLayers(3, 4, 1)

############################################################
#set yarn widths / heights
  weave.SetYYarnWidths( wy )
  weave.SetXYarnWidths( wx )
  weave.SetYYarnSpacings( sy )
  weave.SetBinderYarnWidths( wb)
  weave.SetBinderYarnHeights(hb)
  weave.SetBinderYarnSpacings( sb )
  weave.SetWeftYarnPower( y_power )
  weave.SetWarpYarnPower( x_power )
  weave.SetWarpYarnSpacings( sx )
  #weave.SetWeftYarnSpacing( sy )
  weave.SetBinderYarnPower( b_power )			
  
  ############################################################
  #set binder positions
  bind_numbers = [2*i + 1 for i in range(nbind)]
  c = 0
  print len(P)
  for iy in bind_numbers:
    for ix in range(ny):
      weave.SetBinderPosition(ix, iy, P[c*ny + ix])
      print ix, iy, c*ny+ix, P[c*ny + ix]
    c = c+1
      
  ############################################################
  # remove existing repeat vectors and set to new for new uc width
  #remove the repeat vectors
  #new uc dimensions
  uc_x=ny*sy 
  uc_y1=0
  uc_y2=uc_y1+nwarp*(wx+g) + nbind*(wb+g)
  
  yarns=weave.GetYarns()
  weave.RemoveDomain()
  
  ############################################################
  # add a user defined domains
  # Domain is defined in a way that (0,0,0) is its centre and the unit cell is symmetric relative to main axes/planes
  w1=0#w1=sx/2-wx/2 #domain width (y-direction)w2=
  #w2=nwarp*(wx+g) + nbind*(wb+g)#w2=w1+nwarp*(wx+g) + nbind*(wb+g)
  w2=(Nwarp - Nbind)*sx + (Nbind)*sb
  l1=0 #domain length (x-direction)
  l2=ny*sy
  h1=-hb
  h2=-hy*(nly)-hx*(nly-1)-hb
  weave.Translate(XYZ(sy/2,sb+sx/2.0,(h2-h1)/2.0))
  #weave.Translate(XYZ(0,0,(h2-h1)/2.0))
  domain = CDomainPlanes()
  domain.AddPlane(PLANE(XYZ(1, 0, 0), -l2/2))
  domain.AddPlane(PLANE(XYZ(-1, 0, 0), -l2/2))
  domain.AddPlane(PLANE(XYZ(0, 1, 0), -w2/2))
  domain.AddPlane(PLANE(XYZ(0, -1, 0), -w2/2))
  domain.AddPlane(PLANE(XYZ(0, 0, 1), (h2+h1)/2.0 ))
  domain.AddPlane(PLANE(XYZ(0, 0, -1), (h2+h1)/2.0 )) #z-height is a combination of the warp and weft yarn thicknesses

  weave.AssignDomain(domain)
  
  #weave.AssignDefaultDomain()

  return weave