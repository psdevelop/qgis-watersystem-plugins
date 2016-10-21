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
from wateraccountdicts import Ui_waterAcntDictsDialog
# create the dialog for zoom to point


class waterAccountDictsDialog(QtGui.QDialog, Ui_waterAcntDictsDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.ui = Ui_waterAcntDictsDialog()
        self.ui.setupUi(self)

    def initModel(self, model):
        model.setTable("STREETS")
        model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        model.select()

        model.setHeaderData(0, QtCore.Qt.Horizontal, "id")
        model.setHeaderData(1, QtCore.Qt.Horizontal, "STREET_NAME")
        
    def fillDictsData(self):
        self.setWindowTitle(u"Правка справочников учета Водоканал. PolFunDev.(C)-2015")
        db = QtSql.QSqlDatabase.addDatabase("QPSQL")
        db.setHostName("localhost")
        db.setDatabaseName("postgis_21_sample")
        db.setUserName("postgres")
        db.setPassword("29111960")

        if not db.open():
            QMessageBox.information( self.iface.mainWindow(), u"Ошибка работы с БД!", u"Неудачное соединение с БД!" )
            return
        else:
            for tn in db.tables():
                print str(tn)

        #queryd = db.exec_("SELECT * FROM STREETS")
        queryd = QtSql.QSqlQuery("SELECT * FROM public.\"STREETS\"", db)
        #queryd.exec_()
        print queryd.lastError().text()
        #queryd.exec_("SELECT * FROM TOPO_NODE_WATER")
        #if db.isOpen():
        #    print str(queryd.size())
        #while queryd.next():
        #    print queryd.value(1)

        model = QtSql.QSqlTableModel()
        #self.initModel(model)
        self.ui.StreetsTView.setModel(model)
        #model.setQuery(query)
        model.setTable("public.\"STREETS\"")
        model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        model.select()
        #print dir(model)
        print str(model.tableName())
        print "Streets columns count:"+str(model.columnCount())
        print "Streets count:"+str(model.rowCount())

        model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
        model.setHeaderData(1, QtCore.Qt.Horizontal, "Наименование улицы")

        #self.ui.StreetsTView.setItemDelegate(QtSql.QSql)
        #self.ui.StreetsTView.setEditTriggers(QAbstractItemView::NoEditTriggers);
        #edit = QtSql.QSqlTableModel.OnFieldChange
        #model.setEditStrategy(edit)
        #view.setSelectionMode(self.mode)
        #self.mode = QtGui.QAbstractItemView.SingleSelection
        self.ui.StreetsTView.show()

    #def clearTextBrowser(self):
        #self.ui.txtFeedback.clear()
