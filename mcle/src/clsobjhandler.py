from __future__ import absolute_import
import numpy as np 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from src.image import BndryLabelValue
COLUMN_CLSOBJ = 1


class clsObjTreeHandler(QTreeView):
	emitClassObjectIdx = pyqtSignal(int)
	emitClassObjectPos = pyqtSignal(list)
	emitFillClassObject = pyqtSignal(bool)
	emitKillClassObject = pyqtSignal(list)

	def __init__(self, parent):
		super(clsObjTreeHandler, self).__init__(parent)

		self.NClassLabel 	 = None
		self.NclsObj 		 = 0
		self.listClsObj 	 = []
		self.clsObjAvailable = []
		self.deletedRowsHist = []
		self.IDcur 			 = None
		self.clsObjIdxSelected = None
		self.model 			 = QStandardItemModel()
		self.model.setHorizontalHeaderLabels(["ID","Obj No.", "Class"])
		self.rootNode 		 = self.model.invisibleRootItem()
		self.model.itemChanged.connect(self.classObjectChanged)
		self.setModel(self.model)
		self.setColumnHidden(0,True)
		#self.setColumnWidth(0, 65)
		self.setColumnWidth(1, 50)
		self.setAlternatingRowColors(True)
		self.setSortingEnabled(False)

	def reset(self):
		self.NclsObj 		 = 0
		self.clsObjAvailable = []
		self.listClsObj 	 = []
		self.deletedRowsHist = []
		self.model.removeRows(0, self.model.rowCount())


	#def mouseDoubleClickEvent(self, event):
	#	print(event)

	#def mousePressEvent(self, event):
	#	print(event)

	#def mouseReleaseEvent(self, event):
	#	print(event)

	'''
	def keyReleaseEvent(self, event):
		if event.key() == Qt.Key_Backspace:
			#print('backspace')
			pass
		elif event.key() == Qt.Key_Delete:
			#print('delete')
			pass
		elif event.key() == Qt.Key_Space:
			print('space')		
		elif event.key() == QKeySequence("k"):
			print('k')
		else:
			pass
	'''


	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Down:
			idx 	= self.getSelectedItemRow(1)
			index 	= self.model.index(idx, 0)
			self.setCurrentIndex(index)

		elif event.key() == Qt.Key_Up:
			idx 	= self.getSelectedItemRow(-1)
			index 	= self.model.index(idx, 0)
			self.setCurrentIndex(index)

		elif event.key() == QKeySequence("o"):
			idx 	= self.getSelectedItemRow(0)
			if idx == None: return
			print(self.listClsObj[idx].name)

		elif event.key() == QKeySequence("k"):
			idx 	= self.getSelectedItemRow(0)
			if idx == None: return
			if self.askQuestion('Do you want to delete item?'):
				print('kill: ', self.listClsObj[idx].name)
				self.killClsObj(idx)
		else:
			pass


	def getSelectedItemRow(self, change=None):
		rows = self.selectionModel().selectedRows()
		if len(rows) == 0:
			return None
		row = int(rows[0].data(Qt.DisplayRole))

		if change > 0:
			idx = moveIdxUp(row, self.clsObjAvailable)
		elif change == 0:
			idx = row
		else:
			idx = moveIdxDown(row, self.clsObjAvailable)
		return idx

	def askQuestion(self, message):
		msgbox 	= QMessageBox()
		msgbox.setIcon(QMessageBox.Question)
		reply 	= msgbox.question( self, "", message, 
								   QMessageBox.No | QMessageBox.Yes , QMessageBox.Yes)
		if reply == QMessageBox.Yes:
			return True
		else:
			return False

	def classObjectChanged(self, item):
		ID 		= self.getClsObjId(item, self.model)
		self.IDcur = ID

		try:
			clsobj 	= int(item.data(Qt.DisplayRole))
			print('updating {} to class object: {} -> {}'.format(
					self.listClsObj[ID].name, self.listClsObj[ID].clsobj, clsobj))	
			self.updateClassObject(ID, clsobj)
		except:
			print('invalid type of class object')
			self.setZeroClassObject(ID)

	def getClsObjId(self, item, model):
		row 		= item.index().row()
		return int(model.data(model.index(row,0), Qt.DisplayRole))

	def addClsObj(self, classLabel, labeltxt, posQimg):
		fn = lambda x: self.clsObjIdxSelected if x < self.NClassLabel-1 else BndryLabelValue

		branch 		= QStandardItem(labeltxt)
		clsobjbranch = QStandardItem(str(fn(classLabel)))
		self.rootNode.appendRow([QStandardItem(str(self.NclsObj)), clsobjbranch, branch])
		self.listClsObj.append(unitClsObjData(self.NclsObj, classLabel, labeltxt, posQimg))
		self.clsObjAvailable.append(True)
		self.NclsObj += 1


	def killClsObj(self, idx):
		self.clsObjAvailable[idx] = False
		self.emitKillClassObject.emit(self.listClsObj[idx].qpos)
		self.listClsObj[idx].kill()
		self.setRowHidden(idx, QModelIndex(), True)

	def updateClassObject(self, ID, newClsObj):
		if newClsObj < 0:
			print('newClsObj is less than zero.')
			self.setZeroClassObject(ID)
			return

		if self.listClsObj[ID].clsobj != newClsObj:
			self.listClsObj[ID].clsobj = newClsObj
			self.emitClassObjectIdx.emit(newClsObj)
			self.emitClassObjectPos.emit(self.listClsObj[ID].qpos)
			self.emitFillClassObject.emit(True)


	def setZeroClassObject(self, ID):
		self.model.setItem(ID, COLUMN_CLSOBJ, QStandardItem('0'))

	def setBndryClassObject(self):
		self.model.setItem(self.IDcur, COLUMN_CLSOBJ, QStandardItem('255'))		

	def getClassLabelPixPos(self, Nclass):
		pixPos = []
		for i in range(Nclass):
			pixPos.append([])

		for n in range(self.NclsObj):
			classLabel = self.listClsObj[n].clslbl
			if (classLabel == 0) or (classLabel == Nclass-1): continue
			for i,j in self.listClsObj[n].qpos:
				pixPos[classLabel].append([j,i])

		return pixPos


class unitClsObjData():
	def __init__(self, ID, classLabel, name, posQimg):
		self.name 	= name	
		self.ID 	= ID
		self.clslbl	= classLabel
		self.clsobj = None
		self.qpos 	= []
		self.addPos(posQimg)
		self.highlightOn = False

	def addPos(self, Qposlist):
		for p in Qposlist:
			self.qpos.append([p[0],p[1]])

	def onOffHighlight(self):
		self.highlightOn = not(self.highlightOn)

	def kill(self):
		self.name   = None
		self.clsobj = None
		self.clslbl = None
		self.qpos 	= []


def moveIdxUp(ist, arr):
	if len(arr) == ist + 1: return ist
	for i, val in enumerate(np.array(arr)[ist+1:]):
		if val: break
	if val: return ist + i + 1
	else: 	return ist

def moveIdxDown(ist, arr):
	if ist == 0: return ist
	for i, val in enumerate(np.array(arr)[:ist][::-1]):
		if val: break
	if val: return ist - i - 1
	else: return ist

