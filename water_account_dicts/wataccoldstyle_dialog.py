# -*- coding: utf-8 -*-
"""
/***************************************************************************
 vector_selectbypointDialog
                                 A QGIS plugin
 Select vector features, point and click.
                             -------------------
        begin                : 2014-04-07
        copyright            : (C) 2014 by Brylie Oxley
        email                : brylie@geolibre.org
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

from PyQt4 import QtCore, QtGui, QtSql, Qt
from wataccolstyledockwidget import Ui_waOldStyleDockWidget
# create the dialog for zoom to point


class waterAccOldStyleDialog(QtGui.QDockWidget, Ui_waOldStyleDockWidget):
    def __init__(self):
        QtGui.QDockWidget.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        #self.parent = parent
        self.ui = Ui_waOldStyleDockWidget()
        self.ui.setupUi(self)
        #self.ui.pushButton.clicked.connect(self.pushOneBtn)

    def pushOneBtn(self):
        print u"dddddddffffggggg"

