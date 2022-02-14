import wx
import wx.xrc
import wx.adv

import runpy
import subprocess
import sys
import os
sys.path.append("C:\\users\\emxghs\\desktop\\optimisationGUI")
from GDS.generateDesignSpace import *
from GDS.GeneticAlgorithm import *
#from GDS.GeneticAlgorithm import *


class DesignSpaceWindow ( wx.Dialog ):

	def __init__( self, parent ):
	
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Generate Design Space", pos = wx.DefaultPosition, size = wx.Size( 600, 400 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		Sizer = wx.BoxSizer( wx.VERTICAL )

		gbSizer = wx.GridBagSizer( 0, 0 )
		gbSizer.SetFlexibleDirection( wx.BOTH )
		gbSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		#Add UI Buttons
		self.GenDesignSpace = wx.Button( self, wx.ID_ANY, u"Generate Design Space", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.GenDesignSpace.SetToolTip( u"Generate design space." )

		gbSizer.Add( self.GenDesignSpace, wx.GBPosition( 7, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.CloseDialog = wx.Button( self, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.CloseDialog.SetToolTip(u"Close the dialog.")

		gbSizer.Add( self.CloseDialog, wx.GBPosition( 7, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		#Add UI Text boxes
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Composite Thickness (mm):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		gbSizer.Add( self.m_staticText1, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_textCtr1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer.Add( self.m_textCtr1, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Volume Fraction (%):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		gbSizer.Add( self.m_staticText2, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_textCtr2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer.Add( self.m_textCtr2, wx.GBPosition( 3, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		#Add UI Radio Boxes
		m_radioBoxChoices = [ u"6K", u"12K", u"24K" ]

		self.m_radioBox1 = wx.RadioBox( self, wx.ID_ANY, u"Number of Warp Filaments", wx.DefaultPosition, wx.DefaultSize, m_radioBoxChoices, 1, wx.RA_SPECIFY_COLS )
		gbSizer.Add( self.m_radioBox1, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_radioBox2 = wx.RadioBox( self, wx.ID_ANY, u"Number of Weft Filaments", wx.DefaultPosition, wx.DefaultSize, m_radioBoxChoices, 1, wx.RA_SPECIFY_COLS )
		gbSizer.Add( self.m_radioBox2, wx.GBPosition( 5, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_radioBox3 = wx.RadioBox( self, wx.ID_ANY, u"Number of Binder Filaments", wx.DefaultPosition, wx.DefaultSize, m_radioBoxChoices, 1, wx.RA_SPECIFY_COLS )
		gbSizer.Add( self.m_radioBox3, wx.GBPosition( 5, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


		Sizer.Add( gbSizer, 1, wx.EXPAND, 5 )


		self.SetSizer( Sizer )
		self.Layout()

		self.Centre( wx.BOTH )

		#close frame
		self.Bind(wx.EVT_CLOSE, self.OnClose)

		# Connect Events
		self.GenDesignSpace.Bind( wx.EVT_BUTTON, self.GenerateDesignSpace )
		self.CloseDialog.Bind(wx.EVT_BUTTON, self.OnExit)

	def __del__( self ):
		pass
		
	def OnClose( self, event ):
		self.Destroy()

	def OnExit( self, event ):
		self.Destroy()	
		
	# Event Handlers
	def GenerateDesignSpace( self, event ):
		dlg = wx.DirDialog(self, "Choose Location for Design Space File", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			os.chdir(path)
			
			tol = 0.05  #to do: add UI box for this
			thickness = float(self.m_textCtr1.GetValue())
			vf = float(self.m_textCtr2.GetValue())

			FilamentsDict = {'6K':6000, '12K':12000, '24K':240000}
			indexWarp = self.m_radioBox1.GetSelection()
			indexWeft = self.m_radioBox2.GetSelection()
			indexBinder = self.m_radioBox3.GetSelection()
			numberFilamentsWarp = self.m_radioBox1.GetString(indexWarp)
			numberFilamentsWeft = self.m_radioBox1.GetString(indexWeft)
			numberFilamentsBinder = self.m_radioBox1.GetString(indexBinder)
			SaveDesignSpace(path, vf, tol, thickness, FilamentsDict[numberFilamentsWarp], FilamentsDict[numberFilamentsWeft], FilamentsDict[numberFilamentsBinder])
			Message = 'Textile design space saved to ' + str(path)
			self.InfoBox( Message )
		dlg.Destroy()
		#event.Skip()

		frame = RunOptimisationFrame(thickness, vf, FilamentsDict, numberFilamentsWarp, numberFilamentsWeft, numberFilamentsBinder)
		frame.Show()


	# Message Boxes
	def ErrorBox( self, message ):
		dlg = wx.MessageDialog( self, message,'Error', wx.OK | wx.ICON_WARNING )
		dlg.ShowModal()
		dlg.Destroy()
		
	def InfoBox( self, message ):
		dlg = wx.MessageDialog( self, message,'Info', wx.OK | wx.ICON_INFORMATION )
		dlg.ShowModal()
		dlg.Destroy()
		
class RunOptimisationFrame(wx.Frame):


	def __init__(self, thickness, vf, FilamentsDict, numberFilamentsWarp, numberFilamentsWeft, numberFilamentsBinder):
		
		self.thickness = thickness
		self.vf = vf
		self.FilamentsDict = FilamentsDict
		self.numberFilamentsWarp = numberFilamentsWarp
		self.numberFilamentsWeft = numberFilamentsWeft
		self.numberFilamentsBinder = numberFilamentsBinder
		
		super().__init__(None, title="Run Optimisation", size=wx.Size( 600, 400 ))
		panel = wx.Panel(self)
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		Sizer = wx.BoxSizer( wx.VERTICAL )

		ThicknessString = "Composite Thickness (mm): " + str(self.thickness)
		self.m_ThicknessText = wx.StaticText( panel, label=ThicknessString )

		VolFractionString = "Composite Volume Fraction: " + str(self.vf)
		self.m_VolFractionText = wx.StaticText( panel, label = VolFractionString)

		WarpString = "Warp Filament Number : " + str(self.FilamentsDict[self.numberFilamentsWarp])
		self.m_WarpFilamentText = wx.StaticText( panel, label = WarpString)

		WeftString = "Weft Filament Number : " + str(self.FilamentsDict[self.numberFilamentsWeft])
		self.m_WeftFilamentText = wx.StaticText( panel, label = WeftString)

		BinderString = "Binder Filament Number : " + str(self.FilamentsDict[self.numberFilamentsBinder])
		self.m_BinderFilamentText = wx.StaticText( panel, label = BinderString)
		
		#Values from WeaveDesignSpace file
		with open("weavedesignspace.txt" ) as file:
			line = file.readlines()
		designSpaceList = line[0].split(", ")
		
		
		numWeftLayers = int(designSpaceList[0])
		maxnumBinderLayers = int(designSpaceList[1])
		maxSpacing = float(designSpaceList[2])
		warpHeight = float(designSpaceList[3])
		warpWidth = float(designSpaceList[4])
		weftHeight = float(designSpaceList[5])
		weftWidth = float(designSpaceList[6])
		binderHeight = float(designSpaceList[7])
		binderWidth = float(designSpaceList[8])
		
		# warpHeight, warpWidth, weftHeight, weftWidth, binderHeight, binderWidth
		NumWeftLayersString = "Number of Weft Layers : " + str(numWeftLayers)
		self.m_NumWeftLayersText = wx.StaticText( panel, label = NumWeftLayersString)
		
		NumWarpLayersString = "Number of Warp Layers : " + str(int(numWeftLayers) - 1)
		self.m_NumWarpLayersText = wx.StaticText( panel, label = NumWarpLayersString)
		
		MaxNumBinderLayersString = "Maximum Number of Binder Layers : " + str(maxnumBinderLayers)
		self.m_MaxNumBinderLayersText = wx.StaticText( panel, label = MaxNumBinderLayersString)
		
		MaxSpacingString = "Maximum Spacing Between Yarns (mm) : " + str(round(maxSpacing, 2))
		self.m_MaxSpacingText = wx.StaticText( panel, label = MaxSpacingString)

		
		msg = "Check parameters are correct and run optimisation."
		instructions = wx.StaticText(panel, label=msg)
		close_btn = wx.Button(panel, label="Optimise")
		close_btn.Bind(wx.EVT_BUTTON, self.onSendAndClose)
		
		
		gbsizer = wx.GridBagSizer( 0, 0 )
		gbsizer.SetFlexibleDirection( wx.BOTH )
		gbsizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		gbsizer.Add(self.m_ThicknessText, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		gbsizer.Add(self.m_VolFractionText,wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5)
		gbsizer.Add(self.m_WarpFilamentText, wx.GBPosition( 1, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5)
		gbsizer.Add(self.m_WeftFilamentText, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5)
		gbsizer.Add(self.m_BinderFilamentText, wx.GBPosition( 3, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5)
		
		gbsizer.Add(self.m_NumWeftLayersText, wx.GBPosition( 3, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5)
		gbsizer.Add(self.m_NumWarpLayersText, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5)
		gbsizer.Add(self.m_MaxNumBinderLayersText, wx.GBPosition( 5, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5)
		gbsizer.Add(self.m_MaxSpacingText, wx.GBPosition( 5, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5)
		
		gbsizer.Add(instructions, wx.GBPosition( 7, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5)
		gbsizer.Add(close_btn, wx.GBPosition( 7, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5)
		
		
		
		Sizer.Add( gbsizer, 1, wx.EXPAND, 5 )


		panel.SetSizer( Sizer )
		
		
	def onSendAndClose(self, event):
		
		# scriptPath = "C:\\users\\emxghs\\desktop\\optimisationGUI\\GDS"
		# os.chdir(scriptPath)
		#subprocess.call(scriptPath + " python GeneticAlgorithm.py")
		RunOptimisation(os.getcwd())
		#subprocess.call("python GeneticAlgorithm.py")
		self.Close()



# Create the weave tool app
app = wx.App(False)  
DesignSpaceFrame = DesignSpaceWindow(None) 
DesignSpaceFrame.Show(True)     # Show the frame.

app.MainLoop()


