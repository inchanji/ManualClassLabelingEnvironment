from __future__ import absolute_import
from PIL import Image
import ntpath
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from qobj.tabs import * 
from src.image import getPointsInside, RGBAtoInt, RGBtoInt, IntToRGBA, rgbColorSchemeLabel, BndryLabelName 

RGB_WHITE       = (255 << 16) + (255 << 8) + 255 
ALPHA_MASK 		= 0.3



class PhotoViewer(QGraphicsView):
	emitMouseOnPhoto 	= pyqtSignal(QPoint)
	emitClassLabelPos  	= pyqtSignal(list)
	emitClassLabelIdx 	= pyqtSignal(int)

	def __init__(self, parent):
		super(PhotoViewer, self).__init__(parent)
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

		self.setClassLblFont()
		self.inspectionMode = False
		self.markPtsMode 	= False
		self.fillPixMode 	= False
		self.setMouseTracking(True)

		self._pts = []
		self._lines = []
		self.ClassLabel 			= None
		self.ClassLabelLineWidth 	= 1 # [pixel]
		self.ClassLblIdx 			= None

		self._tempLine = QGraphicsLineItem()
		self._tempLine.setPen(QPen(Qt.black, 1))
		self.parent.QInputClassLabel.connect(self.selectClassLabel)
		self.parent.QLoadClassLabels.connect(self.initClassLabels)


	def setClassLblFont(self):
		self.classLblFont  = QFont()
		self.classLblFont.setFamily('Arial')
		self.classLblFont.setBold(False)
		self.classLblFont.setPointSize(10)

		self.classLblpen  = QPen() 
		self.classLblpen.setWidth(1)
		self.classLblpen.setColor(QColor('white'))

	def hasPhoto(self):
		return not self._empty

	def fitInView(self, scale=True):
		rect = QRectF(self._photo.pixmap().rect())
		if not rect.isNull():
			self.setSceneRect(rect)
			if self.hasPhoto():
				unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
				self.scale(1 / unity.width(), 1 / unity.height())
				viewrect = self.viewport().rect()
				scenerect = self.transform().mapRect(rect)
				factor = min(viewrect.width() / scenerect.width(), 
							 viewrect.height() / scenerect.height())
				self.scale(factor, factor)
			self._zoom = 0		


	def setPhoto(self, pixmap=None):
		self._zoom = 0
		if pixmap and not pixmap.isNull():
			self._empty 	= False
			self.setDragMode(QGraphicsView.ScrollHandDrag)
			self._photo.setPixmap(pixmap)
			
		else:
			self.painter 	= None
			self._empty 	= True
			self.setDragMode(QGraphicsView.NoDrag)
			self._photo.setPixmap(QPixmap())
		self.fitInView()		


	def wheelEvent(self, event):
		if self.hasPhoto() and not(self.inspectionMode):
			if event.angleDelta().y() > 0:
				factor = 1.25
				self._zoom += 1
			else:
				factor = 0.8
				self._zoom -= 1

			if self._zoom > 0:
				self.scale(factor, factor)
			elif self._zoom == 0:
				self.fitInView()
			else:
				self._zoom = 0

	def zoomIn(self):
		if self.hasPhoto():
			factor = 1.25
			self._zoom += 1	
			self.scale(factor, factor)

	def zoomOut(self):
		if self.hasPhoto():
			factor = 0.8
			self._zoom = 0
			self.scale(factor, factor)
			

	def switchInspectionMode(self):
		self.inspectionMode = not(self.inspectionMode)
		if self.hasPhoto() and not(self.inspectionMode):
			self.setDragMode(QGraphicsView.ScrollHandDrag)
			self._photo.setCursor(QCursor(Qt.OpenHandCursor))

			self.markPtsMode = False 
			self.fillPixMode = False
			
		elif self.hasPhoto() and self.inspectionMode:
			self.setDragMode(QGraphicsView.NoDrag)
			self._photo.setCursor(QCursor(Qt.ArrowCursor))
		else:
			pass

		print('Image inspection: {}'.format(self.inspectionMode))
		print('markPointMode: {}'.format(self.markPtsMode))
		print('fillPixMode: {}'.format(self.fillPixMode))
		

	def switchMarkPointMode(self):
		if not(self.inspectionMode): #and self.markPtsMode: 
			self.switchInspectionMode()

		if not self.markPtsMode:
			self._photo.setCursor(QCursor(Qt.CrossCursor))	
		else:
			if self.inspectionMode:
				self._photo.setCursor(QCursor(Qt.ArrowCursor))
			else:
				self._photo.setCursor(QCursor(Qt.OpenHandCursor))

			if len(self._pts) > 1:
				self.resetTempMarkPts()

		self.markPtsMode = not(self.markPtsMode)

		print('Image inspection: {}'.format(self.inspectionMode))
		print('markPointMode: {}'.format(self.markPtsMode))
		print('fillPixMode: {}'.format(self.fillPixMode))

	def switchFillPixelMode(self):
		if not self.inspectionMode: 
			self.switchInspectionMode()		

		if not self.fillPixMode:
			self._photo.setCursor(QCursor(Qt.CrossCursor))	
		else:
			if self.fillPixMode:
				self._photo.setCursor(QCursor(Qt.ArrowCursor))
			else:
				self._photo.setCursor(QCursor(Qt.OpenHandCursor))

		self.fillPixMode = not(self.fillPixMode)

		print('Image inspection: {}'.format(self.inspectionMode))
		print('markPointMode: {}'.format(self.markPtsMode))
		print('fillPixMode: {}'.format(self.fillPixMode))
		


	def toggleDragMode(self):
		print('toggleDragMode')
		if self.dragMode() == QGraphicsView.ScrollHandDrag:
			self.setDragMode(QGraphicsView.NoDrag)
		elif not self._photo.pixmap().isNull():
			self.setDragMode(QGraphicsView.ScrollHandDrag)


	def mouseMoveEvent(self, event):
		#print('mouseMoveEvent')
		if self._photo.isUnderMouse() and self.inspectionMode and not(self.markPtsMode):
			point = self.mapToScene(event.pos())
			self.emitMouseOnPhoto.emit(QPoint(point.x(), point.y()))
		elif self._photo.isUnderMouse() and self.inspectionMode and self.markPtsMode:
			point = self.mapToScene(event.pos())
			self.tempLine(point)
			
		super(PhotoViewer, self).mouseMoveEvent(event)


	def mousePressEvent(self, event):
		if self.hasPhoto() and self.inspectionMode and not(self.markPtsMode) and not(self.fillPixMode):
			pass
		elif self.hasPhoto() and self.inspectionMode and self.markPtsMode and not(self.fillPixMode):
			point = self.mapToScene(event.pos())
			self.addMarkPoint(point)
		elif self.hasPhoto() and self.inspectionMode and not(self.markPtsMode) and self.fillPixMode:
			point = self.mapToScene(event.pos())
			self.fillLabelOnePixel(point)
		else: 
			pass

		super(PhotoViewer, self).mousePressEvent(event)


	def update_image(self):
		print('update_image')
		pixmap 	= self._photo.pixmap()
		b 		= pixmap.toImage().bits()
		b.setsize(	self.parent.imgWidth * self.parent.imgHeight * self.parent.Nchannel)
			
		arr 	= np.frombuffer(b, np.uint8).reshape(
						(self.parent.imgHeight, 
						 self.parent.imgWidth, 
						 self.parent.Nchannel))

		qpixmap = QPixmap(QImage(arr, 
							self.parent.imgWidth, 
							self.parent.imgHeight, 
							QImage.Format_RGB32))

		self._photo.setPixmap(qpixmap)


	def tempLine(self, point):
		if len(self._pts) > 0:
			lastpos = self._pts[-1]
			curpos  = point
			self._scene.removeItem(self._tempLine)
			self._tempLine.setLine(QLineF(lastpos, curpos))
			self._scene.addItem(self._tempLine)


	def addMarkPoint(self, point):
		print('addMarkPoint')
		self._pts.append(point)

		if len(self._pts) < 2: return

		lastpos = self._pts[-2]
		curpos  = self._pts[-1]

		_line   = QGraphicsLineItem()

		if self.ClassLabel != None:
			try:
				lbl 	= self.ClassLabel[self.ClassLblIdx]
				pen 	= QPen()
				pen.setWidth(1)
				pen.setColor(QColor(lbl['r'], lbl['g'], lbl['b']))
			except:
				print('invalid class label selected')
				pen 	= QPen(Qt.red, 1)	
		else:
			pen 	= QPen(Qt.red, 1)
		
		_line.setPen(pen)
		_line.setLine(QLineF(lastpos, curpos))
		self._scene.addItem(_line)
		self._lines.append(_line)


	def delOneMarkPoint(self):
		print('delOneMarkPoint')

		if len(self._lines) > 0:
			self._scene.removeItem(self._lines[-1])
			del self._lines[-1]

		if len(self._pts) > 0: 
			del self._pts[-1]

		if len(self._lines) == 0:
			self._lines = []
			self._pts 	= []

	def resetImage(self):
		print('resetImage:')
		self.setPhoto(QPixmap(self.parent.qImage0))

		self.removeAllLines()
		self.resetTempMarkPts()


	def removeAllLines(self):
		while len(self._lines) > 0:
			self.delOneMarkPoint()

	def resetTempMarkPts(self):
		self._scene.removeItem(self._tempLine)
		self._pts 	= []


	def fillLabelOnePixel(self, point):
		pts = [[ int(point.x()), int(point.y())]]
		ClassLblIdx, Mask, lbl  = getLabelColor(self.ClassLabel, self.ClassLblIdx)
		if ClassLblIdx is not None:
			qimg 	= QImage(self._photo.pixmap())
			qimg0 	= self.parent.qImage0

			ptsInside = fillClassLabel(	qimg0, qimg, pts, Mask,
										self.ClassLabelPixPos, ClassLblIdx,
										self.parent.imgWidth, self.parent.imgHeight, 
										self.emitClassLabelPos)
			qpixmap = QPixmap(qimg)
			self._photo.setPixmap(qpixmap)
		
	def loadSegClassLabel(self, label, pos):
		if (len(label) == 0) or (len(pos) == 0): return
		qimg 	= QImage(self._photo.pixmap())
		qimg0 	= self.parent.qImage0		

		for n, (j,i) in enumerate(pos):
			lbl 	= self.ClassLabel[label[n]]
			mask 	= np.array([lbl['r'], lbl['g'], lbl['b']])
			rgba = np.array(IntToRGBA(qimg0.pixel(i,j)))
			r,g,b = (rgba[:3] * (1-ALPHA_MASK) + mask * ALPHA_MASK).astype(np.int)
			qimg.setPixel(i,j, RGBAtoInt(r,g,b))
		self._photo.setPixmap(QPixmap(qimg))

	def fillInMarkPoint(self):
		pts 	= getPoints(self._pts)
		ClassLblIdx, Mask, lbl  = getLabelColor(self.ClassLabel, self.ClassLblIdx)
		qimg 	= QImage(self._photo.pixmap())
		qimg0 	= self.parent.qImage0
	
		ptsInside = fillClassLabel(	qimg0, qimg, pts, Mask, self.ClassLabelPixPos, 
									ClassLblIdx, self.parent.imgWidth, 
									self.parent.imgHeight, self.emitClassLabelPos)

		qpixmap = QPixmap(qimg)

		if (lbl is not None) and (ptsInside is not None):
			ptsCenter = np.mean(ptsInside, axis = 0, dtype = int)
			writeClassLabel(qpixmap, self.classLblpen, self.classLblFont, ptsCenter, lbl['name'])

		self._photo.setPixmap(qpixmap)
		self.resetTempMarkPts()
		self.removeAllLines()
		self.switchInspectionMode()


	def setSegBndry(self, posBndry = None, mask = np.array([255,255,255]), alpha = ALPHA_MASK):
		if posBndry is None : return
		print('imgviewer: drawBoundary')

		qimg 	= QImage(self._photo.pixmap())
		qimg0 	= self.parent.qImage0		

		for i,j in posBndry:
			rgba = np.array(IntToRGBA(qimg0.pixel(j,i)))
			r,g,b = (rgba[:3] * (1-alpha) + mask * alpha).astype(np.int)
			qimg.setPixel(j,i, RGBAtoInt(r,g,b))

		qpixmap = QPixmap(qimg)
		self._photo.setPixmap(qpixmap)
		self.resetTempMarkPts()
		self.removeAllLines()
		self.switchInspectionMode()

	def setClassLabelLineWidth(self, val):
		self.ClassLabelLineWidth = val
		print(self.ClassLabelLineWidth)

	def drawLinebtwMarkPoint(self):
		print('drawLinebtwMarkPoint')
		
		pts 	= getPoints(self._pts)
		ClassLblIdx, Mask, lbl  = getLabelColor(self.ClassLabel, self.ClassLblIdx)
		qimg 	= QImage(self._photo.pixmap())
		qimg0 	= self.parent.qImage0

		
		Bndry, cenpos = drawLineClassLabel(	qimg0, qimg, pts, Mask, self.ClassLabelPixPos, 
							ClassLblIdx, self.parent.imgWidth, self.parent.imgHeight, 
							self.ClassLabelLineWidth, self.emitClassLabelPos)
		qpixmap = QPixmap(qimg)

		#if (lbl is not None) and (cenpos is not None):
		#	writeClassLabel(qpixmap, self.classLblpen, self.classLblFont, cenpos, lbl['name'])

		self._photo.setPixmap(qpixmap)
		self.resetTempMarkPts()
		self.removeAllLines()
		self.switchInspectionMode()		



	def selectClassLabel(self, qidx):
		try:
			self.ClassLblIdx = qidx
			self.emitClassLabelIdx.emit(self.ClassLblIdx)
		except:
			print('invalid class label')

	def initClassLabels(self, qstring):
		labels 	= qstring.split('\t')

		self.ClassLabel 		= []
		self.ClassLabelPixPos 	= [] 	# [row, col]

		for lbl in labels:
			lbls = lbl.split(',')
			self.ClassLabel += [{'name': lbls[0], 'r': int(lbls[1]), 'g': int(lbls[2]), 'b': int(lbls[3])}]
			self.ClassLabelPixPos.append([])

	def askQuestion(self, message):
		msgbox 	= QMessageBox()
		msgbox.setIcon(QMessageBox.Question)
		reply 	= msgbox.question(self, "",
									message, 
									QMessageBox.No | QMessageBox.Yes , QMessageBox.Yes)
		if reply == QMessageBox.Yes:
			return True
		else:
			return False	



class SegViewer(QGraphicsView):
	def __init__(self, parent):
		super(SegViewer, self).__init__(parent)
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
		qimg 	= QImage(self._photo.pixmap())
		if (pos is not None) and (idx is not None):
			for i,j in pos:
				if ((i >= 0) or (i < self.parent.imgWidth))  and ((j >= 0) or (j < self.parent.imgHeight)):
					qimg.setPixel(i,j, self.rgbaClassLabel[idx])
					self.segmap[j,i] = idx

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
		print('segviewer: drawBoundary')
		qimg 		= QImage(self._photo.pixmap())
		'''
		posBndry 	= getBndryPos(self.segmap, self.bndryThickness, self.CLASS_LABEL_BNDRY)
		'''

		posBndry 	= getBndryPosNew(self.segmap, self.bndryThickness, self.CLASS_LABEL_BNDRY, classLabelPos)
		for i,j in posBndry:
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

def getPoints(qpts):
	pts = []
	for points in qpts:
		pts.append([points.x(),points.y()])
	return pts


def getLabelColor(ClassLabel, ClassLblIdx = None):
	if ClassLabel != None:
		try:
			lbl 	= ClassLabel[ClassLblIdx]
			Mask 	= [lbl['r'], lbl['g'], lbl['b']]
		except:
			print('invalid class label selected')
			Mask 	= [0, 0, 255]	
			lbl 	= None
	else:
		Mask 	 	= [255, 0, 0]	
		lbl 		= None
	return ClassLblIdx, np.array(Mask), lbl


def writeClassLabel(qpixmap, classLblpen, classLblFont, ptsCenter, name, bndryname = BndryLabelName):
	if name == bndryname: return
	painter 	= QPainter(qpixmap)
	painter.setPen(classLblpen)
	painter.setFont(classLblFont)
	
	painter.drawText(ptsCenter[0], ptsCenter[1], name);
	painter.end()



def fillClassLabel(qimg0, qimg, pts, mask, pos, idx, w, h, emitpos):
	labelpos = []	
	if len(pts) > 2:
		ptsInside = getPointsInside(np.array(pts))
		if idx is not None:

			for i,j in ptsInside:
				if ((i >= 0) or (i < w))  and ((j >= 0) or (j < h)):
					rgba = np.array(IntToRGBA(qimg0.pixel(i,j)))
					r,g,b = (rgba[:3] * (1-ALPHA_MASK) + mask * ALPHA_MASK).astype(np.int)
					qimg.setPixel(i,j, RGBAtoInt(r,g,b))
					pos[idx].append([j,i])
					labelpos.append([i,j])
			emitpos.emit(labelpos)
		else:
			print('class label is not assigned')
			for i,j in ptsInside:
				if ((i >= 0) or (i < w))  and ((j >= 0) or (j <h)):
					rgba = np.array(IntToRGBA(qimg0.pixel(i,j)))
					r,g,b = (rgba[:3] * (1-ALPHA_MASK) + mask * ALPHA_MASK).astype(np.int)
					qimg.setPixel(i,j, RGBAtoInt(r,g,b))	
	elif len(pts) == 1:
		i, j = pts[0]
		if ((i >= 0) or (i < w))  and ((j >= 0) or (j < h)):
			rgba = np.array(IntToRGBA(qimg0.pixel(i,j)))
			r,g,b = (rgba[:3] * (1-ALPHA_MASK) + mask * ALPHA_MASK).astype(np.int)
			qimg.setPixel(i,j, RGBAtoInt(r,g,b))
			pos[idx].append([j,i])
			labelpos.append([i,j])	
		emitpos.emit(labelpos)	
		ptsInside = None
	else:
		ptsInside = None

	return ptsInside



def drawLineClassLabel(qimg0, qimg, pts, mask, pos, idx, w, h, linewidth, emitpos):
	ptsInside 	= None
	cenpos 		= None

	if len(pts) > 1:
		pos0 = pts[0]

		for p in pts[1:]:
			pos1  	= p
			bndry 		= getPosLineEdge(pos0, pos1, linewidth * 0.5)
			ptsInside 	= getPointsInside(np.array(bndry))

			if idx is not None:
				labelpos = []		
				for i,j in ptsInside:
					if ((i >= 0) or (i < w))  and ((j >= 0) or (j < h)):
						rgba = np.array(IntToRGBA(qimg0.pixel(i,j)))
						r,g,b = (rgba[:3] * (1-ALPHA_MASK) + mask * ALPHA_MASK).astype(np.int)
						qimg.setPixel(i,j, RGBAtoInt(r,g,b))
						pos[idx].append([j,i])
						labelpos.append([i,j])			
				emitpos.emit(labelpos)
			else:
				for i,j in ptsInside:
					if ((i >= 0) or (i < w))  and ((j >= 0) or (j <h)):
						rgba = np.array(IntToRGBA(qimg0.pixel(i,j)))
						r,g,b = (rgba[:3] * (1-ALPHA_MASK) + mask * ALPHA_MASK).astype(np.int)
						qimg.setPixel(i,j, RGBAtoInt(r,g,b))							
			pos0 = pos1
		cenpos = [0.5 * (pts[0][0] + pts[1][0]), 0.5 * (pts[0][1] + pts[1][1])]

	return ptsInside, cenpos


def getPosLineEdge(p0, p1, l):
	bndry = []
	if 	p1[0] == p0[0]:
		print('vertical line')

		bndry.append([p0[0] - l, p0[1]])
		bndry.append([p0[0] + l, p0[1]])
		bndry.append([p1[0] + l, p1[1]])
		bndry.append([p1[0] - l, p1[1]])

	elif p1[1] == p0[1]:
		print('horizontal line')

		bndry.append([p0[0], p0[1] - l])
		bndry.append([p0[0], p0[1] + l])
		bndry.append([p1[0], p1[1] + l])
		bndry.append([p1[0], p1[1] - l])		

	else:
		print('diagonal line')	
		slope = (p1[1] - p0[1]) / (p1[0] - p0[0])
		slope = - 1 / slope

		dx = l / np.sqrt(1 + slope**2)
		dy = dx * slope

		bndry.append([p0[0] + dx, p0[1] + dy])
		bndry.append([p0[0] - dx, p0[1] - dy])
		bndry.append([p1[0] - dx, p1[1] - dy])
		bndry.append([p1[0] + dx, p1[1] + dy])

	return bndry



def getBndryPosNew(segmap, thickness, valbndry, classlabelpos):
	nrow, ncol 	= np.shape(segmap)
	posBndry 	= []
	nclasslabel = len(classlabelpos)
	dl 			= thickness
	dl2_half_diag = (1.5 * np.max([1, 0.5 * dl])) ** 2 

	for n in range(nclasslabel):
		if n == 0: 
			continue # skip background / NULL class label

		for i, j in classlabelpos[n]: # Qimage Coord: row & col are swapped
			val 	= segmap[i,j]
			if val == valbndry:	
				continue			
			#print('| at (x,y) = ',j,i, ', seg val:' , val)
			labelsneighbor, indneighbor = getNeighborLabelNew(segmap, dl, i, j, nrow, ncol)

			if np.all(labelsneighbor == val): 
				continue 

			if np.all(np.logical_or(labelsneighbor == val, labelsneighbor == valbndry)):
				continue
			
			for k, v in enumerate(labelsneighbor):
				ii, jj 	= indneighbor[k][0], indneighbor[k][1]

				if v == 0:
					#print('>>Marking Bndry.     seg val:' , v, ' at (x,y) =', jj,ii)
					posBndry.append([ii,jj])
				elif v == valbndry: 
					continue
				elif v == val:
					continue
				else: # v != val & v != 0 & v != bndry  <> v has diff label from v at (i,j)
					d2 		= (ii - i)**2 + (jj - j)**2
					if d2 < dl2_half_diag:
						#print('>>Marking Bndry.     seg val:' , v, ' at (x,y) =', jj,ii)
						posBndry.append([ii,jj])
	return posBndry


def getNeighborLabelNew(seg, thickness, i, j, nrow, ncol):
	i0 		= np.max([0, 	i-thickness])
	i1 		= np.min([nrow, i+thickness+1])
	j0 		= np.max([0, 	j-thickness])
	j1 		= np.min([ncol, j+thickness+1])	

	w  		= j1-j0 
	h  		= i1-i0 
	idx 	= w * (i-i0) + (j-j0) 
	row, col 	= np.indices((h, w))
	indices 	= getSteckedIndices(row.ravel(),col.ravel(), i0, j0, idx)


	labels 			= seg[i0:i1,j0:j1].ravel()
	lablesneighbor = np.delete(labels, idx)

	return lablesneighbor, indices

def getSteckedIndices(row, col, i0, j0, iskip):
	indices = []
	for n, (i,j) in enumerate(zip(row,col)):
		if n == iskip: continue
		indices.append([i+i0,j+j0])
	return np.array(indices)
