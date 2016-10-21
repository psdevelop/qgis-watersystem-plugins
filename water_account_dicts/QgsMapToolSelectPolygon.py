# -*- coding: utf-8 -*-
"""

"""
from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
# create the dialog for zoom to point


class QgsMapToolSelectPolygon(QgsMapTool):
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.rubberBand = 0
        self.mCursor = QtCore.Qt.ArrowCursor;
        self.mFillColor = QtGui.QColor(254, 178, 76, 63)
        self.mBorderColor = QtGui.QColor(254, 58, 29, 100)

    def canvasPressEvent(self, event):
        #self.cursorPixmap = QPixmap('/mypixmap.png'
        #self.cursor = QCursor(self.cursorPix)
        #self.stdCursor = self.parent().cursor()
        #self.parent().setCursor(self.cursor)
        x = event.pos().x()
        y = event.pos().y()
        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)

        if not isinstance(self.rubberBand, QgsRubberBand):
            self.rubberBand = QgsRubberBand(self.canvas)
            # #QtGui.QRubberBand(QtGui.QRubberBand.Line)
            self.rubberBand.setColor(self.mFillColor)
            self.rubberBand.setLineStyle(QtCore.Qt.DotLine)
            self.rubberBand.setWidth(3)

        if event.button()==QtCore.Qt.LeftButton:
            self.rubberBand.addPoint(point)
            #.move(x,y)
            print "lb"
        else:
            if self.rubberBand.numberOfVertices()>2:
                polygonGeom = self.rubberBand.asGeometry()
                #QgsMapToolSelectUtils.setSelectFeatures(self.canvas, polygonGeom, event)
                del polygonGeom
            self.rubberBand.reset()
            #del self.rubberBand

    def canvasMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        #print "ddd"

        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        if isinstance(self.rubberBand, QgsRubberBand):
            self.rubberBand.removeLastPoint(0)
            #print "ffff"
            #points = [ QgsPoint(-1,-1), QgsPoint(0,1), QgsPoint(1,-1) ]
            #self.rubberBand.setToGeometry(QgsGeometry.fromPolyline(points), None)
            self.rubberBand.addPoint(point)

    def canvasReleaseEvent(self, event):
        #self.parent().setCursor(self.stdCursor)
        x = event.pos().x()
        y = event.pos().y()

        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)

    def activate(self):
        pass

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True