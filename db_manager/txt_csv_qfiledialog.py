# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name                 : DB Manager
Description          : Database manager plugin for QGIS
Date                 : May 23, 2011
copyright            : (C) 2011 by Giuseppe Sucameli
email                : brush.tyler@gmail.com

The content of this file is based on
- PG_Manager by Martin Dobias (GPLv2 license)
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class TxtCsvOpenFile(QMainWindow):
	def __init__(self, iface, parent=None):
		QMainWindow.__init__(self, parent)
		self.iface = iface
		self.success = False
		self.setGeometry(300, 300, 350, 300)
		self.setWindowTitle('OpenFile')
		self.textEdit = QTextEdit()
		self.setCentralWidget(self.textEdit)
		self.statusBar()
		self.setFocus()
		exit = QAction(QIcon('open.png'), 'Open', self)
		exit.setShortcut('Ctrl+O')
		exit.setStatusTip('Open new File')
		self.connect(exit, SIGNAL('triggered()'), self.showDialog)
		
		menubar = self.menuBar()
		file = menubar.addMenu('&File')
		file.addAction(exit)
		
	def showDialog(self):
		self.filename = QFileDialog.getOpenFileName(self, 'Open file', '/home')
		try:
			if self.filename:
				file=open(self.filename)
				data = file.read()
				self.textEdit.setText(data)
				self.success = True
		except ValueError:
			infoString = "Error file test opening!"
			QMessageBox.information(self.iface.mainWindow(),"Error",infoString)
			return
