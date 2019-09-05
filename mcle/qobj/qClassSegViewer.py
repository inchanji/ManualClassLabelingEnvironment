from __future__ import absolute_import
from PIL import Image
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from src.image import rgbColorSchemeLabel, ALPHA_MASK
from qobj.qViewerUtils import * 


class ClassSegViewer(QGraphicsView):
	def __init__(self, parent):
		super(ClassSegViewer, self).__init__(parent)
		self.parent = parent
		self._zoom = 0
		self._empty = True
		self._scene = QGraphicsScene(self)
		self._photo = QGraphicsPixmapItem()
		self._scene.addItem(self._photo)
		self.setScene(self._scene)
		self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
		self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
		self.setFrameShape(QFrame.NoFrame)
		self.bndryThickness 	= 1
		self.CLASS_LABEL_BNDRY 	= 255

	def hasPhoto(self):
		return not self._empty

	def fitInView(self, scale=True):
		rect = QRectF(self._photo.pixmap().rect())
		if not rect.isNull():
			self.setSceneRect(rect)
			if self.hasPhoto():
				unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
				self.scale(1 / unity.width(), 1 / unity.height())
				viewrect 	= self.viewport().rect()
				scenerect 	= self.transform().mapRect(rect)
				factor 		= min(viewrect.width() / scenerect.width(), 
								  viewrect.height() / scenerect.height())
				self.scale(factor, factor)
			self._zoom = 0		


	def setPhoto(self, pixmap=None):
		self._zoom = 0
		if pixmap and not pixmap.isNull():
			self._empty = False
			self.setDragMode(QGraphicsView.ScrollHandDrag)
			self._photo.setPixmap(pixmap)
			self.segmap = np.zeros((pixmap.height(),pixmap.width()), dtype = np.uint8)
		else:
			self._empty = True
			self.setDragMode(QGraphicsView.NoDrag)
			self._photo.setPixmap(QPixmap())
			self.segmap = None
		self.fitInView()		


	def wheelEvent(self, event):
		if self.hasPhoto():
			if event.angleDelta().y() > 0:
				factor 		= 1.25
				self._zoom += 1
			else:
				factor 		= 0.8
				self._zoom -= 1

			if self._zoom > 0:
				self.scale(factor, factor)
			elif self._zoom == 0:
				self.fitInView()
			else:
				self._zoom = 0

	def zoomIn(self):
		if self.hasPhoto():
			factor 		= 1.25
			self._zoom += 1	
			self.scale(factor, factor)

	def zoomOut(self):
		if self.hasPhoto():
			factor 		= 0.8
			self._zoom 	= 0
			self.scale(factor, factor)

	def setNumClassLabel(self, N = None):
		if N is not None:
			self.parent.NClassLabel = N
			self.rgbaClassLabel = []
			for i in range(N):
				self.rgbaClassLabel.append(255 << 24 | rgbColorSchemeLabel(i, N))
		else:
			self.parent.NClassLabel 	= None
			self.rgbaClassLabel 		= None

	def setClassLabel(self, pos = None, idx = None):
		fn = lambda x: x if x < self.parent.NClassLabel-1 else self.CLASS_LABEL_BNDRY
		
		qimg 	= QImage(self._photo.pixmap())
		if (pos is not None) and (idx is not None):
			for i,j in pos:
				if (i >= 0) and (i < self.parent.imgWidth)  and (j >= 0) and (j < self.parent.imgHeight):
					qimg.setPixel(i,j, self.rgbaClassLabel[idx])
					self.segmap[j,i] = fn(idx)
		self._photo.setPixmap(QPixmap(qimg))

	def removeClassLabel(self, qpos):
		qimg 	= QImage(self._photo.pixmap())
		for i,j in qpos:
			qimg.setPixel(i,j, 0xff000000)
			self.segmap[j,i] = 0
		self._photo.setPixmap(QPixmap(qimg))		


	def setSegBndryThickness(self, val):
		self.bndryThickness = val

	def saveSegMap(self, path):
		print(path)
		if self.segmap is None:
			print('cannot save segmentation. it is empty :(')
		else:
			im = Image.fromarray(self.segmap)
			im.save(path)

	def setSegBndry(self, classLabelPos):
		#print('class segviewer: drawBoundary')
		qimg 		= QImage(self._photo.pixmap())
		posBndry 	= getBndryPosNew(self.segmap, self.bndryThickness, self.CLASS_LABEL_BNDRY, classLabelPos)

		for i,j in posBndry:
			if (j >= 0) and (j < self.parent.imgWidth)  and (i >= 0) and (i < self.parent.imgHeight):
				qimg.setPixel(j,i, 0xffffffff)
				self.segmap[i,j] = self.CLASS_LABEL_BNDRY

		self._photo.setPixmap(QPixmap(qimg))
		return posBndry



	def loadSegClassLabel(self, label, pos):
		if (len(label) == 0) or (len(pos) == 0): return
		qimg 	= QImage(self._photo.pixmap())

		for n, (j,i) in enumerate(pos):
			qimg.setPixel(i,j, self.rgbaClassLabel[label[n]])
			self.segmap[j,i] = label[n]

		self._photo.setPixmap(QPixmap(qimg))		
