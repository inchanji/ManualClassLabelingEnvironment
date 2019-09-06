from __future__ import absolute_import
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from src.image import RGBAtoInt, IntToRGBA, ALPHA_MASK
from qobj.qViewerUtils import *

MIN_DIST2_OVERLAP = 3**2

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
		self.classLblFont.setPointSize(8)

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
			self.parent.BtnInspect.setChecked(False)
			self.setDragMode(QGraphicsView.ScrollHandDrag)
			self._photo.setCursor(QCursor(Qt.OpenHandCursor))

			self.markPtsMode = False 
			self.fillPixMode = False
			self.parent.BtnMarkPoint.setChecked(False)
			self.parent.BtnFillLabelOnePixel.setChecked(False)
			
		elif self.hasPhoto() and self.inspectionMode:
			self.parent.BtnInspect.setChecked(True)
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
			self.parent.BtnMarkPoint.setChecked(True)
			self._photo.setCursor(QCursor(Qt.CrossCursor))	
		else:
			self.parent.BtnMarkPoint.setChecked(False)
			if self.inspectionMode:
				self._photo.setCursor(QCursor(Qt.ArrowCursor))
			else:
				self._photo.setCursor(QCursor(Qt.OpenHandCursor))
			self._scene.removeItem(self._tempLine)

			#if len(self._pts) > 1:
			#	self.resetTempMarkPts()

		self.markPtsMode = not(self.markPtsMode)

		print('Image inspection: {}'.format(self.inspectionMode))
		print('markPointMode: {}'.format(self.markPtsMode))
		print('fillPixMode: {}'.format(self.fillPixMode))

	def switchFillPixelMode(self):
		if not self.inspectionMode: 
			self.switchInspectionMode()		

		if not self.fillPixMode:
			self.parent.BtnFillLabelOnePixel.setChecked(True)
			self._photo.setCursor(QCursor(Qt.CrossCursor))	
		else:
			self.parent.BtnFillLabelOnePixel.setChecked(False)
			if self.inspectionMode:
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
			self.emitMouseOnPhoto.emit(QPoint(point.x(), point.y()))
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
		oripos  = self._pts[0]

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

		if (point.x() - oripos.x()) **2 + (point.y() - oripos.y()) ** 2 < MIN_DIST2_OVERLAP:
			print('distance to starting point < {} pix. Overlapping the starting point. '.format(MIN_DIST2_OVERLAP))
			self._pts[-1] = oripos
			curpos 		  = oripos
			self.switchMarkPointMode()			
		
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

		if (lbl is not None) and (ptsInside is not None):
			name = 'Pt. [{:d},{:d}]'.format(pts[0][0],pts[0][1])
			self.parent.addObjClass(name)
		
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
		if len(pts) == 1:
			return	
		elif len(pts) == 2:
			self.drawLinebtwMarkPoint()
			return
		else:
			pass	

		ClassLblIdx, Mask, lbl  = getLabelColor(self.ClassLabel, self.ClassLblIdx)
		qimg 	= QImage(self._photo.pixmap())
		qimg0 	= self.parent.qImage0
	
		ptsInside = fillClassLabel(	qimg0, qimg, pts, Mask, self.ClassLabelPixPos, 
									ClassLblIdx, self.parent.imgWidth, 
									self.parent.imgHeight, self.emitClassLabelPos)

		qpixmap = QPixmap(qimg)

		if (lbl is not None) and (ptsInside is not None):
			ptsCenter 	= np.mean(ptsInside, axis = 0, dtype = int)
			x0 			= np.min(np.array(ptsInside)[:,0])
			ptsCenter[0] = int(x0 + 0.5 * (ptsCenter[0]-x0))
			name 		= lbl['name'] + '_' + str(self.parent.clsObjHandler.NclsObj)
			writeClassLabel(qpixmap, self.classLblpen, self.classLblFont, ptsCenter, name)

		self.parent.addObjClass()
		self._photo.setPixmap(qpixmap)
		self.resetTempMarkPts()
		self.removeAllLines()
		self.switchInspectionMode()

	def setSegBndry(self, posBndry = None, mask = np.array([255,255,255]), alpha = ALPHA_MASK):
		if posBndry is None : return
		#print('imgviewer: drawBoundary')

		qimg 	= QImage(self._photo.pixmap())
		qimg0 	= self.parent.qImage0		

		for i,j in posBndry:
			rgba 	= np.array(IntToRGBA(qimg0.pixel(j,i)))
			r,g,b 	= (rgba[:3] * (1-alpha) + mask * alpha).astype(np.int)
			qimg.setPixel(j,i, RGBAtoInt(r,g,b))

		self.emitClassLabelPos.emit(list(np.roll(posBndry, 1, axis=1)))
		self.parent.addBndryClass('BNDRY [255]')

		qpixmap 	= QPixmap(qimg)
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

		_, cenpos 	= drawLineClassLabel(	qimg0, qimg, pts, Mask, self.ClassLabelPixPos, 
											ClassLblIdx, self.parent.imgWidth, self.parent.imgHeight, 
											self.ClassLabelLineWidth, self.emitClassLabelPos)
		qpixmap = QPixmap(qimg)
		if (lbl is not None) and (cenpos is not None):
			name 		= lbl['name'] + '_' + str(self.parent.clsObjHandler.NclsObj)
			writeClassLabel(qpixmap, self.classLblpen, self.classLblFont, cenpos, name )

		self.parent.addObjClass()
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

	def removeClassLabel(self, qpos):
		qimg0 	= self.parent.qImage0
		qimg 	= QImage(self._photo.pixmap())
		for i,j in qpos:
			qimg.setPixel(i,j, qimg0.pixel(i,j))
		self._photo.setPixmap(QPixmap(qimg))


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

