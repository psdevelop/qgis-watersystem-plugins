# -*- coding: utf-8 -*-

import psycopg2
import os
import subprocess
from PyQt4 import QtCore, QtGui, QtWebKit

class customWebView(QtWebKit.QWebView):
    def __init__(self, QWidget_parent=None):
        self.parent = QWidget_parent;
        super(customWebView, self).__init__(QWidget_parent)

    def mouseDoubleClickEvent(self, QMouseEvent):
        #QtGui.QMessageBox.information( self, "Information", u"Click-click!!!))))" )
        self.parent.contentsChanged()
        super(customWebView, self).mouseDoubleClickEvent(QMouseEvent)

    def mouseReleaseEvent(self, QMouseEvent):
        self.parent.eventChanged()
        super(customWebView, self).mouseReleaseEvent(QMouseEvent)

    def changeEvent(self, QEvent):
        #self.parent.eventChanged()
        super(customWebView, self).changeEvent(QEvent)

    def dragEnterEvent(self, QDragEnterEvent):
        #self.parent.eventChanged()
        super(customWebView, self).dragEnterEvent(QDragEnterEvent)

    def dropEvent(self, QDropEvent):
        #self.parent.eventChanged()
        super(customWebView, self).dropEvent(QDropEvent)

    def mousePressEvent(self, QMouseEvent):
        #self.parent.eventChanged()
        super(customWebView, self).mousePressEvent(QMouseEvent)

    def dragLeaveEvent(self, QDragLeaveEvent):
        #self.parent.eventChanged()
        super(customWebView, self).dragLeaveEvent(QDragLeaveEvent)




