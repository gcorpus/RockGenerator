#Tool description
"""RG: Rocks Generator
   Goal: creates 3 different types of rocks within random shape and size.
"""
#Libraries
import traceback

from PySide import QtCore
from PySide import QtGui

from shiboken import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui 

import random


def mayaMainWindow():
	"""Returns the Maya main window as a Python object"""

	mayaMainWindow = omui.MQtUtil.mainWindow()
	return wrapInstance(long(mayaMainWindow),QtGui.QWidget)

class RocksGeneratorUI(QtGui.QDialog):
	"""Builds the generator window with all its functions"""

	signals = QtCore.Signal()

	def __init__(self, parent = mayaMainWindow()):
		super(RocksGeneratorUI,self).__init__(parent)

		
	def createGUI(self):
		"""Builds the main window of the tool"""

		self.setWindowTitle("Rocks Generator")
		self.setWindowFlags(QtCore.Qt.Tool)
		self.setFixedSize(300,220)

		self.createWidgets()
		self.createLayout()

	def createWidgets(self):
		"""Builds each widget of the tool"""

		self.lRockType = QtGui.QLabel("Rock type ")
		self.lRockType.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignCenter)
		self.cbRockType = QtGui.QComboBox()
		self.cbRockType.addItems(["Boulder","Quartz","Stalagmite"])

		self.lNumberRocks = QtGui.QLabel("Number of rocks ")
		self.lNumberRocks.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignCenter)
		self.lNumberRocks.setFixedWidth(100)
		self.eNumberRocks = QtGui.QLineEdit()
		self.sNumberRocks = QtGui.QSlider(QtCore.Qt.Horizontal)
		self.sNumberRocks.setMinimum(1)
		self.sNumberRocks.setMaximum(99)
		self.sNumberRocks.setValue(10)
		self.sNumberRocks.setAccessibleName("sNumberRocks")

		self.onlyInt = QtGui.QIntValidator()
		self.eNumberRocks.setValidator(self.onlyInt)
		self.eNumberRocks.setMaxLength(2)
		self.eNumberRocks.setFixedWidth(50)
		self.eNumberRocks.setText(str(self.sNumberRocks.value()))
		self.eNumberRocks.setAccessibleName("eNumberRocks")

		self.lDistRadius = QtGui.QLabel("Distribution radius ")
		self.lDistRadius.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignCenter)
		self.lDistRadius.setFixedWidth(100)
		self.eDistRadius = QtGui.QLineEdit()
		self.sDistRadius = QtGui.QSlider(QtCore.Qt.Horizontal)
		self.sDistRadius.setMinimum(1)
		self.sDistRadius.setMaximum(99)
		self.sDistRadius.setValue(10)
		self.sDistRadius.setAccessibleName("sDistRadius")

		self.eDistRadius.setValidator(self.onlyInt)
		self.eDistRadius.setMaxLength(2)
		self.eDistRadius.setFixedWidth(50)
		self.eDistRadius.setText(str(self.sDistRadius.value()))
		self.eDistRadius.setAccessibleName("eDistRadius")

		self.lMinScale = QtGui.QLabel("Minimum scale")
		self.lMinScale.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignCenter)
		self.lMinScale.setFixedWidth(100)
		self.eMinScale = QtGui.QLineEdit()
		self.sMinScale = QtGui.QSlider(QtCore.Qt.Horizontal)
		self.sMinScale.setMinimum(1)
		self.sMinScale.setMaximum(25)
		self.sMinScale.setValue(1)
		self.sMinScale.setAccessibleName("sMinScale")

		self.eMinScale.setValidator(self.onlyInt)
		self.eMinScale.setMaxLength(2)
		self.eMinScale.setFixedWidth(50)
		self.eMinScale.setText(str(self.sMinScale.value()))
		self.eMinScale.setAccessibleName("eMinScale")

		self.lMaxScale = QtGui.QLabel("Maximum scale")
		self.lMaxScale.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignCenter)
		self.lMaxScale.setFixedWidth(100)
		self.eMaxScale = QtGui.QLineEdit()
		self.sMaxScale = QtGui.QSlider(QtCore.Qt.Horizontal)
		self.sMaxScale.setMinimum(1)
		self.sMaxScale.setMaximum(25)
		self.sMaxScale.setValue(5)
		self.sMaxScale.setAccessibleName("sMaxScale")

		self.eMaxScale.setValidator(self.onlyInt)
		self.eMaxScale.setMaxLength(2)
		self.eMaxScale.setFixedWidth(50)
		self.eMaxScale.setText(str(self.sMaxScale.value()))
		self.eMaxScale.setAccessibleName("eMaxScale")

		self.bCreateRocks = QtGui.QPushButton("Create rocks")
		self.bCreateRocks.setFixedHeight(30)
		

	def createLayout(self):
		""" Builds the needed layouts and assign the widgets to each one. 
		    The signals are created, connecting with its slots. """

		rockTypeLayout = QtGui.QHBoxLayout()
		rockTypeLayout.addWidget(self.lRockType)
		rockTypeLayout.addWidget(self.cbRockType)
	
		numberRocksLayout = QtGui.QHBoxLayout()
		numberRocksLayout.addWidget(self.lNumberRocks)
		numberRocksLayout.addWidget(self.eNumberRocks)
		numberRocksLayout.addWidget(self.sNumberRocks)

		distRadiusLayout = QtGui.QHBoxLayout()
		distRadiusLayout.addWidget(self.lDistRadius)
		distRadiusLayout.addWidget(self.eDistRadius)
		distRadiusLayout.addWidget(self.sDistRadius)

		minScaleLayout = QtGui.QHBoxLayout()
		minScaleLayout.addWidget(self.lMinScale)
		minScaleLayout.addWidget(self.eMinScale)
		minScaleLayout.addWidget(self.sMinScale)

		maxScaleLayout = QtGui.QHBoxLayout()
		maxScaleLayout.addWidget(self.lMaxScale)
		maxScaleLayout.addWidget(self.eMaxScale)
		maxScaleLayout.addWidget(self.sMaxScale)

		buttonsLayout = QtGui.QHBoxLayout()
		buttonsLayout.addWidget(self.bCreateRocks)
		
		submainLayout = QtGui.QVBoxLayout()
		submainLayout.addLayout(rockTypeLayout)
		submainLayout.addLayout(numberRocksLayout)
		submainLayout.addLayout(distRadiusLayout)
		submainLayout.addLayout(minScaleLayout)
		submainLayout.addLayout(maxScaleLayout)
		submainLayout.addLayout(buttonsLayout)

		rocksSettings = QtGui.QGroupBox("Settings")
		rocksSettings.setLayout(submainLayout)
		
		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addWidget(rocksSettings)

		#----------------------------#
		#--SIGNALS (events) ---------#
		#----------------------------#
		
		self.sNumberRocks.valueChanged.connect(self.valueChanged)
		self.eNumberRocks.textChanged.connect(self.valueChanged)
		
		self.sDistRadius.valueChanged.connect(self.valueChanged)
		self.eDistRadius.textChanged.connect(self.valueChanged)

		self.sMinScale.valueChanged.connect(self.valueChanged)
		self.eMinScale.textChanged.connect(self.valueChanged)

		self.sMaxScale.valueChanged.connect(self.valueChanged)
		self.eMaxScale.textChanged.connect(self.valueChanged)

		self.bCreateRocks.clicked.connect(self.createRocks)
		
		self.setLayout(mainLayout)

	#-------------------------------#
	#-- SLOTS (functions/methods)---#
	#-------------------------------#

	def valueChanged(self):
		""" Synchronizes the values between controls"""

		sender = self.sender()
		nameWidget = sender.accessibleName()

		if nameWidget == "sNumberRocks":
			value = str(self.sNumberRocks.value())
			self.eNumberRocks.setText(value)
			
		elif nameWidget == "eNumberRocks":
			value = int(self.eNumberRocks.text())
			self.sNumberRocks.setValue(value)

		elif nameWidget == "sDistRadius":
			value = str(self.sDistRadius.value())
			self.eDistRadius.setText(value)
			
		elif nameWidget == "eDistRadius":
			value = int(self.eDistRadius.text())
			self.sDistRadius.setValue(value)
			
		elif nameWidget == "sMinScale":
			value = str(self.sMinScale.value())
			self.eMinScale.setText(value)
			
		elif nameWidget == "eMinScale":
			value = int(self.eMinScale.text())
			self.sMinScale.setValue(value)
			
		elif nameWidget == "sMaxScale":
			value = str(self.sMaxScale.value())
			self.eMaxScale.setText(value)
			
		elif nameWidget == "eMaxScale":
			value = int(self.eMaxScale.text())
			self.sMaxScale.setValue(value)


	def boulderRock(self, nameGroup,rocks, radiusDistr, minScale, maxScale ):
		"""Creates the requested boulder style rocks """


		rocksGroup = cmds.group(empty=True , name = nameGroup)

		for r in range(rocks):

			xPos = random.uniform(-radiusDistr, radiusDistr)
			zPos = random.uniform(-radiusDistr, radiusDistr)

			xDim = random.uniform(1.0, 5.0)
			yDim = random.uniform(1.0, 5.0)
			zDim = random.uniform(1.0, 5.0)
			randomElements = ['1','2', '3']
			randomDim = random.choice(randomElements)
			xLT = random.uniform(-0.2,0.3)
			yLT = random.uniform(-0.2,0.3)
			zLT = random.uniform(-0.2,0.3)

			rock = cmds.polyCube(name= "boulder#")
			cmds.parent(rock,rocksGroup)
			cmds.move(xPos,0,zPos)

			if randomDim == '1':
				cmds.scale(xDim,yDim,zDim)
			elif randomDim == '2':
				cmds.scale(xDim,xDim,xDim)
			else: 
				cmds.scale(xDim,xDim,zDim)

			cmds.polySmooth(dv=1)
			polyVtx = cmds.polyMoveVertex(ch= True, ran=3.0,lt=(xLT,yLT,zLT))
			cmds.polySmooth(dv=1)

			rockScale = random.uniform((minScale*0.5),(maxScale*0.5))
			cmds.scale(rockScale,rockScale,rockScale)
			cmds.delete(ch=True)


	def stalagmiteRock(self, nameGroup,rocks, radiusDistr, minScale, maxScale ):
		"""Creates the requested stalagmite style rocks"""

		rocksGroup = cmds.group(empty=True , name = nameGroup)

		for r in range(rocks):

			xPos = random.uniform(-radiusDistr, radiusDistr)
			zPos = random.uniform(-radiusDistr, radiusDistr)

			list1 = (2,3,4,5,6,7,8)
			list2 = (3,4,5,6,7,8,9,10,11,12,13,14,15)
			list3 = (4,5,6,7,8)
			radius = random.choice(list1)
			height = random.choice(list2)
			sx = random.choice(list3)
			sy = random.choice(list3)
			xLT = random.uniform(-0.3,0.3)
			yLT = random.uniform(-0.3,0.3)
			zLT = random.uniform(-0.3,0.3) 

			rock = cmds.polyCone(name="stalagmite#", radius= radius, height= height, sx= sx,sy=sy)
			cmds.parent(rock,rocksGroup)
			cmds.xform(rock, piv=(0,-(height/2),0), ws=True)
			cmds.move(xPos,height/2,zPos)
			polyVtx = cmds.polyMoveVertex(ch= True, ran=3.0,lt=(xLT,yLT,zLT))
			rockScale = random.uniform((minScale*0.25),(maxScale*0.25))
			cmds.select(rock)
			cmds.scale(rockScale,rockScale,rockScale)
			cmds.polySmooth(dv=1)
			cmds.delete(ch=True)


	def quartzRock(self, nameGroup,rocks, radiusDistr, minScale, maxScale ):
		"""Creates the requested quartz style rocks """

		rocksGroup = cmds.group(empty=True , name = nameGroup)

		for r in range(rocks):

			sx = random.uniform(1, 4)
			sy = random.uniform(1, 4)
			sz = random.uniform(1, 4)
			height = random.uniform(1, 3)
			width = random.uniform(1, 3)
			xR = random.uniform(-90, 90)
			yR = random.uniform(-90, 90)
			zR = random.uniform(-90, 90)
			xLT = random.uniform(-0.1,0.1)
			yLT = random.uniform(-0.1,0.1)
			zLT = random.uniform(-0.1,0.1) 

			xPos= random.uniform(-radiusDistr, radiusDistr)
			zPos= random.uniform(-radiusDistr, radiusDistr)

			scale = random.uniform((minScale*0.35), (maxScale*0.35))

			rock = cmds.polyCube(name = "quartz#", height = height, width= width, sx=sx,sy=sy,sz=sz)
			polyVtx = cmds.polyMoveVertex(ch= True, ran=3.0,lt=(0.05,0.02,0.07))
			#polyVtx = cmds.polyMoveVertex(ch= True, ran=3.0,lt=(xLT,yLT,zLT))
			cmds.polySmooth(dv=1)
			cmds.select(rock)
			cmds.xform(r=True,ro=(xR,yR,zR))
			cmds.move(xPos,0,zPos)
			cmds.scale(scale,scale,scale)
			cmds.makeIdentity(apply=True, t=True,r=True,s=True, pn= True)
			cmds.delete(ch=True)

		
	def createRocks(self):
		"""Calls all functions needed for create the requested rocks"""

		typeRock = self.cbRockType.currentIndex()
		nameGroup = self.cbRockType.currentText() + "_group#"
		rocks = self.sNumberRocks.value()
		radiusDistr = self.sDistRadius.value()
		minScale = self.sMinScale.value()
		maxScale = self.sMaxScale.value()

		#rocksGroup = cmds.group(empty=True , name = nameGroup + "_group#")

		if typeRock == 0:
			self.boulderRock(nameGroup, rocks, radiusDistr,minScale,maxScale)
				

		elif typeRock == 1:
			self.quartzRock(nameGroup, rocks, radiusDistr, minScale, maxScale)
			

		elif typeRock == 2:
			self.stalagmiteRock(nameGroup, rocks, radiusDistr, minScale, maxScale)
				
			

if __name__=="__main__":
	"""Executes the instance of the class RocksGeneratorUI"""

	try:
		generatorUI.close()
	except:
		pass

	generatorUI = RocksGeneratorUI()
	generatorUI.createGUI()
	generatorUI.show()


