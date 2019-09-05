from __future__ import absolute_import
from PIL import ImageQt, Image
import os
import ntpath
import matplotlib.path
import matplotlib.cm
import numpy as np 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import *


RGB_WHITE = (255 << 16) + (255 << 8) + 255


BndryLabelName 	= 'BOUNDARY'
BndryLabelValue = 255
ALPHA_MASK 		= 0.3

def RGBAtoInt(R,G,B,alpha = 255):
	return alpha << 24 | B | G << 8 | R << 16

def RGBtoInt(R,G,B):
	return  B | G << 8 | R << 16

def IntToRGBA(val):
	alpha 	= val >> 24
	val 	= val - (alpha << 24)
	r 		= val >> 16
	val 	= val - (r << 16)
	g 		= val >> 8
	b 		= val - (g << 8)

	return (r,g,b,alpha)
	 
def IntToRGB(val, alpha = 255):
	r 		= val >> 16
	val 	= val - (r << 16)
	g 		= val >> 8
	b 		= val - (g << 8)
	return (r,g,b,alpha)


def rgbColorSchemeLabel(idx, Nlabel, maxval = RGB_WHITE):
	return int(maxval * idx / (Nlabel-1))



def _get_ratio_height(width, height, r_width):
	return int(r_width/width*height)

def _get_ratio_width(width, height, r_height):
	return int(r_height/height*width)


class Operations:
	def __init__(self):
		self.color_filter = None

		self.flip_left = False
		self.flip_top = False
		self.rotation_angle = 0

		self.size = None

		self.brightness = 0
		self.sharpness = 0
		self.contrast = 0

	def reset(self):
		self.color_filter = None

		self.brightness = 0
		self.sharpness = 0
		self.contrast = 0
		self.size = None

		self.flip_left = False
		self.flip_top = False
		self.rotation_angle = 0

	def has_changes(self):
		return self.color_filter or self.flip_left\
			or self.flip_top or self.rotation_angle\
			or self.contrast or self.brightness\
			or self.sharpness or self.size

	def __str__(self):
		return  f"size: {self.size}, filter: {self.color_filter}, " \
				f"b: {self.brightness} c: {self.contrast} s: {self.sharpness}, " \
				f"flip-left: {self.flip_left} flip-top: {self.flip_top} rotation: {self.rotation_angle}"


def getPointsInside(pts):
	xpos = pts[:,0]
	ypos = pts[:,1]

	xmin = int(np.min(xpos))
	xmax = int(np.max(xpos))+1
	ymin = int(np.min(ypos))
	ymax = int(np.max(ypos))+1

	x = np.arange(0, xmax - xmin + 1)
	y = np.arange(0, ymax - ymin + 1)

	xv, yv  = np.meshgrid(x, y, indexing = 'xy')
	points  = np.hstack((xv.reshape((-1,1)), yv.reshape((-1,1))))

	polygon = pts - [xmin, ymin]
	path 	= matplotlib.path.Path(polygon)
	mask 	= path.contains_points(points)

	return points[mask] + [xmin, ymin]



def loadImage(self):
	print('Open: ', self.imagePath.text())

	filename 		= ntpath.basename(self.imagePath.text())
	pathdir 		= self.imagePath.text().split(filename)[0]
	if not os.path.isdir(os.path.join(pathdir,'segmentation')):
		os.mkdir(os.path.join(pathdir,'segmentation'))

	pathClsSegsave 		= os.path.join(pathdir,'segmentation', filename.split('.')[0] + '_class_seg.bmp')
	pathObjSegsave 		= os.path.join(pathdir,'segmentation', filename.split('.')[0] + '_object_seg.bmp')

	img 	 = Image.open(self.imagePath.text())
	Nchannel = len(img.split())

	if Nchannel == 4:
		img = np.array(img)[:,:,:3].astype(np.uint8)
		height, width, channel = np.shape(img)
		bytesPerLine = 3 * width
		qimg   = QImage(img, width, height, bytesPerLine, QImage.Format_RGB888)
		pixmap = QPixmap(qimg)
	else:
		pixmap 			= QPixmap(self.imagePath.text())	

	self.qImage0 	= QImage(pixmap.copy())
	self.imgWidth 	= self.qImage0.width()
	self.imgHeight 	= self.qImage0.height()

	self.saveClsSegPath.setText(pathClsSegsave)
	self.saveObjSegPath.setText(pathObjSegsave)

	self.imgviewer.setPhoto(pixmap)

	qsegmap = QPixmap(self.imgWidth, self.imgHeight)
	qsegmap.fill(Qt.black)
	self.classSegViewer.setPhoto(qsegmap)
	self.objectSegViewer.setPhoto(qsegmap)
	self.clsObjHandler.reset()


	#if os.path.isfile(pathsave):
	#	if askQuestion(self, 'Segmentation '+ pathsave +' found. Do you want to load it?'):
	#		self.loadRetrieveClassLable(pathsave)



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





def RGBColorTable(i, cmap='prism'):
	if i == 0: return 0

	r,g,b,a = matplotlib.cm.get_cmap(cmap)(i % 255)
	R = int(r * 255)
	G = int(g * 255)
	B = int(b * 255)

	return B | G << 8 | R << 16



