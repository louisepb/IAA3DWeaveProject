import os
import sys

#import dataHandlingBending
path = 'D:/OneDrive/OneDrive - The University of Nottingham/optimisation/binder_optim/run4/'
#sys.path.append(path) 
#sys.path.append('C:\Program Files\TexGen27\Python\libxtra')
#sys.path.append('C:\python27\Lib\site-packages\texgen')
import sys
sys.path.insert(0, 'C:\\Program Files\\TexGen311\\Python\\libxtra') 

#sys.path.remove('C:\\python27\\lib\\site-packages\\TexGen')
  
print sys.path
from TexGen.Core import *
from my_3Dweave_v2 import *
#import dataHandlingBending

def replaceFromLine(filename, cutoff_line, new_lines, tail_file):
  fro = open(filename, 'rb')

  chars = fro.readline()
  while chars: 
    chars = fro.readline()
    if cutoff_line in chars:
      fro.readline()
      break
  
  seekpoint = fro.tell()
  frw = open(filename, 'r+b')
  frw.seek(seekpoint, 0)

  fro.close()
  frw.truncate()
  for line in new_lines:
    frw.writelines(line)
  
  fri = open(tail_file, 'r')
  for line in fri:
    frw.writelines(line)
  frw.close()

############################################################

def remove_material_prop(filename, new_file, search_line, material_lines):
  fro = open(filename, 'r')
  frw = open(new_file, 'w+')
  
  chars = fro.readline()
  while chars: 
    chars = fro.readline()
    
    if '*Solid Section' in chars:
      frw.writelines(chars.rstrip() + ', controls=EC-1\n')
      continue
    
    frw.writelines(chars)
    if search_line in chars:
      chars = fro.readline() # skip one line
      frw.writelines(chars)
      for i in range(11):
        fro.readline() # skip one line
        #frw.writelines(chars)
           
      frw.writelines(material_lines)
      #break
  
    
  
  frw.close()
  fro.close()

#########################################

# Binder pattern
#P=[0,4,0,4, 4,0,4,0, 0,4,0,4, 4,0,4,0]

Pinput = sys.argv[-1]
model_name = 'my_' + Pinput
allargs = []
for a in Pinput:
  allargs.append(int(a))

# Pattern
P = allargs[0:16]   
print len(P)
binder_weight = allargs[16]
print binder_weight
warp_sp = allargs[17]
weft_sp = allargs[18]
num_layers = allargs[19]


#sx = 1.25#0.95 #x (warp) yarn spacing
#sy = 2.0 #y (weft) yarn spacing
#hx = 0.35 #x(warp) yarn heights
#hy = 0.38 #y( weft) yarn heights
#hb = 0.2 #x (binder) yarn heights
#wy=1.8 #weft yarn width
#wx=2.1 #warp (binder) yarn width
#wb=0.4#wx/2 #binder width
#g=0.0 #fixed gap between parallel x (warp and binder) yarns
#x_power=0.1 # x (warp) yarn power
#y_power=0.1 # y (weft) yarn power
#b_power=0.4 # binder yarn power 

my_geom = dict(sx=1.25, sy=2.0, hx=0.35, hy=0.38, hb=0.2, wy=1.8, wx=2.1, wb=0.4, g=0.0, x_power=0.1, y_power=0.1, b_power=0.4)

# Spacing
my_sx = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5]
my_sx = my_sx`

my_sy = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5]
my_sy = my_sy

# Corresponds to 1K, 3K, 6K and 12K binder yarns
my_wb = [0.34, 0.85, 1.42, 1.88]
my_hb = [0.21, 0.25, 0.30, 0.41]

print type(my_sx[warp_sp]) 

# wx, hx, wy, hy are from Xuesen's paper, power's too for VF=55%
my_geom = dict(sx=(my_sx[warp_sp]+1.88), sy=(my_sy[weft_sp]+2.09), sb=my_wb[binder_weight], hx=0.41, hy=0.35, hb=my_hb[binder_weight], wy=2.09, wx=1.88, wb=my_wb[binder_weight], g=0.0, x_power=0.1, y_power=0.1, b_power=0.4) 

# myLtoL(Nwarp, Nweft, Nbind, Lwarp, Lbind, my_geom, Pinput)
# Nwarp - number of warp yarns (total i.e. warp + binder)
# Nweft - number of weft yarns
# Nbind - number of binder yarns
# Lwarp - number of weft layers
# Lbind - number of binder layers
# P - binder yarn positions


AddTextile('test3D',myLtoL(8, 4, 4, num_layers, 1, my_geom, P), True)
t = GetTextile()
dom_vol = t.GetDomain().GetVolume()
my_VF = t.GetQuickDomainVolumeFraction()*0.54
weight = my_VF*dom_vol*1.8 + (1-my_VF)*dom_vol*1.0

vox_out=True
run_model=True
out_name=model_name + 'vox'
vx=100	
vy=100
vz=75

if vox_out:
  Vox = CRectangularVoxelMesh('CPeriodicBoundaries')
  Vox.SaveVoxelMesh(GetTextile('test3D'), (out_name +'.inp'), vx,vy,vz,True,True,0,0)

#remove_material_prop('vox_out.inp')
my_lines = '*** testline\n*********************\n'
material_lines = """ *Material, Name=Mat0
*USER MATERIAL,CONSTANTS=4, TYPE=MECHANICAL
1e+003, 0.3, 60, 100
*Depvar
8
*Material, Name=Mat1
*USER MATERIAL,CONSTANTS=13, TYPE=MECHANICAL
  45.6e3, 16.23e3, 5.5e3, 5.8e3, 0.273, 0.4, 1378, 950, 
  40, 125, 97, 0.082, 0.2
*DEPVAR
8
*Section controls, name=EC-1,hourglass=enhanced
1., 1., 1.
*PARAMETER
my_force = 0.0125\n"""
print my_lines



remove_material_prop(model_name + 'vox.inp', model_name+ '.inp', '*** MATERIALS ***', material_lines)
 
replaceFromLine(model_name + '.inp', '*** BOUNDARY CONDITIONS ***', my_lines, 'bending_UC_tail.inp')

os.system('run_fort.bat & C:\\SIMULIA\\Commands\\abaqus.bat job=' + model_name + '.inp user=optim_failure_init_v3 scratch=D:\ cpus=6 interactive ask_delete=OFF')
os.system('C:\\SIMULIA\\Commands\\abaqus.bat cae noGUI=effectiveMatPropRVE.py -- ' + model_name)

reportFilename = model_name + '_ABD_results.txt'
fOutputReport = open(reportFilename, 'a')
str1 = "Current VF\n"
str2 = "%3.3e\n" % (weight)
fOutputReport.write(str1)
fOutputReport.write(str2)
fOutputReport.close()

os.system('C:\\SIMULIA\\Commands\\abaqus.bat job=' + model_name + '_macro.inp interactive ask_delete=OFF')
os.system('C:\\SIMULIA\\Commands\\abaqus.bat cae noGUI=run_macro_model_RO.py -- ' + model_name + ' interactive -- ' + model_name)

reportFilename = model_name + '_macro_res.txt'
fOutputReport = open(reportFilename, 'a')
str1 = "Current VF\n"
str2 = "%3.3e\n" % (weight)
fOutputReport.write(str1)
fOutputReport.write(str2)
fOutputReport.close()

#files_list = os.listdir(path)
#for f in files_list:
#  if ( f.endswith(".sim") ) or (f.endswith(".prt") ) or (f.endswith(".pes")):
#    os.remove(os.path.join(path,f)

#dataHandlingBending.mainScript('my_test_new', 0)

#add_tail('vox_out.inp', 'my_tail_file.inp')  