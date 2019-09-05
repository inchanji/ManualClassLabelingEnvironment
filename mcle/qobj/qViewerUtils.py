import ntpath
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from src.image import *


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
		ptsInside = labelpos
	else:
		ptsInside = None

	return ptsInside



def drawLineClassLabel(qimg0, qimg, pts, mask, pos, idx, w, h, linewidth, emitpos):
	ptsInside 	= None
	cenpos 		= None

	if len(pts) > 1:
		pos0 	 = pts[0]
		labelpos = []
		for p in pts[1:]:
			pos1  	= p
			bndry 		= getPosLineEdge(pos0, pos1, linewidth * 0.5)
			ptsInside 	= getPointsInside(np.array(bndry))

			if idx is not None:
						
				for i,j in ptsInside:
					if ((i >= 0) or (i < w))  and ((j >= 0) or (j < h)):
						rgba = np.array(IntToRGBA(qimg0.pixel(i,j)))
						r,g,b = (rgba[:3] * (1-ALPHA_MASK) + mask * ALPHA_MASK).astype(np.int)
						qimg.setPixel(i,j, RGBAtoInt(r,g,b))
						pos[idx].append([j,i])
						labelpos.append([i,j])			
				#emitpos.emit(labelpos)
			else:
				for i,j in ptsInside:
					if ((i >= 0) or (i < w))  and ((j >= 0) or (j <h)):
						rgba = np.array(IntToRGBA(qimg0.pixel(i,j)))
						r,g,b = (rgba[:3] * (1-ALPHA_MASK) + mask * ALPHA_MASK).astype(np.int)
						qimg.setPixel(i,j, RGBAtoInt(r,g,b))							
			pos0 = pos1
		emitpos.emit(labelpos)
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
		if n == nclasslabel-1: 
			continue # skip Bndry class label

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
