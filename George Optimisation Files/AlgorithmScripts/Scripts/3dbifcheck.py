import os
cwd=os.getcwd()

Vox = CBifurcationVoxelMesh('CPeriodicBoundaries')

Vox.InitialiseBifurcationVoxelMesh(16, 10, 2, -3, 7, 16)
weave=GetTextile()
ModelName='Tpiece'
Vox.SaveVoxelMesh(weave, cwd+ '\\' + ModelName + '.inp', 100,100,100,1,1,0,0)
