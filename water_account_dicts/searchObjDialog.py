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
import psycopg2
import os
import subprocess
from PyQt4 import QtCore, QtGui, QtSql
from searchobjectsdialog import Ui_searchObjectsDialog
# create the dialog for zoom to point

class searchObjectDialog(QtGui.QDialog, Ui_searchObjectsDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.HOST = "localhost"
        self.DB_NAME = "postgis_topo210415"
        self.DB_USER = "postgres"
        self.DB_PASS = "29111960"
        conns = self.getConnections()
        for con in conns:
            if con==u"postgis_21_sample":
                self.HOST = self.connection_value(con,u"host")
                #print self.connection_value(con,u"port")
                self.DB_NAME = self.connection_value(con,u"database")
                self.DB_USER = self.connection_value(con,u"username")
                self.DB_PASS = self.connection_value(con,u"password")
        for con in conns:
            if con==u"postgis_topo210415":
                self.HOST = self.connection_value(con,u"host")
                #print self.connection_value(con,u"port")
                self.DB_NAME = self.connection_value(con,u"database")
                self.DB_USER = self.connection_value(con,u"username")
                self.DB_PASS = self.connection_value(con,u"password")
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.ui = Ui_searchObjectsDialog()
        self.ui.setupUi(self)
        #self.ui.addElmPButton.clicked.connect(self.addElm)

    def getConnections(self):
        s = QtCore.QSettings( )
        s.beginGroup(u"PostgreSQL/connections")
        currentConnections = s.childGroups()
        s.endGroup()
        return currentConnections

    def connection_value(self,  connection, key):
        #uri = QgsDataSourceURI ()
        settings = QtCore.QSettings()
        settings.beginGroup(u"/PostgreSQL/connections")
        settings.beginGroup(connection)
        value = str(settings.value( key))
        settings.endGroup()
        settings.endGroup()
        return value

    def addElm(self):
        query = QtSql.QSqlQuery()
        query.exec_(u"insert into public.\"latches\"(name, description, material, toponode, diametr, type, brtype, brord, branch) "
                    u" values('НОВЫЙ ЭЛЕМЕНТ', 'no desc', 3, "+str(self.curr_nid)+u", 0, '"+self.ltype+u"','"+self.br_type+u"',0,"+str(self.branch_id)+")")
        self.model.select()

    def delElm(self):
        ridx=self.ui.tblVNodeElements.currentIndex().row()
        oid = self.toint(self.model.index(ridx,0).data())
        #print oid
        query = QtSql.QSqlQuery()
        reply = QtGui.QMessageBox.question(self,u"Удалить "+str(oid)+"-"+self.model.index(ridx,1).data(),
                                      u"Продолжить?", QtGui.QMessageBox.Apply, QtGui.QMessageBox.Cancel)
        if reply==QtGui.QMessageBox.Apply:
            query.exec_("DELETE FROM public.\"latches\" where id="+str(oid))
            self.model.select()

    def tofloat(self, value):
        try:
            return float(value)
        except Exception:
            return 0.0

    def toint(self, value):
        try:
            return int(value)
        except Exception:
            return 0

    def setDlg(self, search_type):
        #self.setWindowTitle(u"Правка элементов схемы объекта")
        #self.curr_nid = node_id;
        #self.branch_id = branch_id
        db = QtSql.QSqlDatabase.addDatabase("QPSQL")
        db.setHostName(self.HOST)
        db.setDatabaseName(self.DB_NAME)
        db.setUserName(self.DB_USER)
        db.setPassword(self.DB_PASS)
        #self.ltype = latch_type
        #self.br_type = br_type

        if not db.open():
            QMessageBox.information( self.iface.mainWindow(), u"Ошибка работы с БД!", u"Неудачное соединение с БД!" )
            return

    def accept(self):
            #QtGui.QMessageBox.information( self, "Information", u"Ошибка (запись не отражена в БД)! id="+str(self.curr_nid)  )
        return QtGui.QDialog.accept(self)

