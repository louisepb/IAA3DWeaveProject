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
        print('vector 1', vector1)
        TopBinder=self.FindTopBinderYarns(vector1)
        offset=((len(vector1)-1)-TopBinder)/2
        return offset

    def FindTopBinderYarns(self, vector1):
        print('vector1 here', vector1)
        i=len(vector1)-1
        while i>0:
            if vector1[i]==1:
                return i
            i=i-1
        return i
