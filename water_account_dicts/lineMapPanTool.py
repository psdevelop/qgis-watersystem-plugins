# -*- coding: utf-8 -*-
"""

"""
from PyQt4 import QtCore, QtGui
from qgis.gui import *
# create the dialog for zoom to point


class lineMapPanTool(QgsMapToolPan):
    def __init__(self, canvas):
        QgsMapToolPan.__init__(self, canvas)
        self.canvas = canvas

    def canvasPressEvent(self, event):
        pass

    def canvasMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        #print "ddd"

        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)

    def canvasReleaseEvent(self, event):
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