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
from latchesSqlModel import latchesRelSqlModel
from nodeelementsdlg import Ui_nodeElementsDialog
# create the dialog for zoom to point

class nodeElementsDialog(QtGui.QDialog, Ui_nodeElementsDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
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
            if con==u"postgis_topo":
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
        self.ui = Ui_nodeElementsDialog()
        self.ui.setupUi(self)
        self.ui.addElmPButton.clicked.connect(self.addElm)
        self.ui.delElmPButton.clicked.connect(self.delElm)
        self.ui.diamLineEdit.setRange(0,999999)
        self.model = None

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

    def createRelationalTables(self):
        query = QtSql.QSqlQuery()
        #query.exec_("create table public.\"injoutpipes\"(id SERIAL, description varchar(255), material INTEGER DEFAULT 0 NOT NULL, toponode INTEGER, diametr INTEGER DEFAULT 0 NOT NULL, injcode INTEGER DEFAULT 0 NOT NULL, injorder INTEGER DEFAULT 0 NOT NULL, injdeep INTEGER DEFAULT 0 NOT NULL, type VARCHAR(20) DEFAULT 'WATER'::character varying NOT NULL, CONSTRAINT \"injoutpipes_pkey\" PRIMARY KEY(id))")

        query.exec_("create table public.\"material\"(id SERIAL, name varchar(255), CONSTRAINT \"materials_pkey\" PRIMARY KEY(id))")
        #query.exec_("insert into public.\"material\"(name) values('Асбестоцемент')")
        #query.exec_("insert into public.\"material\"(name) values('Чугун')")
        #query.exec_("insert into public.\"material\"(name) values('Бетон')")

    def initModel(self, model):
        model.setTable("")

    def fillDictsData(self, node_id, latch_type, br_type, branch_id):
        self.setWindowTitle(u"Правка элементов схемы объекта")
        self.curr_nid = node_id;
        self.branch_id = branch_id
        db = QtSql.QSqlDatabase.addDatabase("QPSQL")
        db.setHostName(self.HOST)
        db.setDatabaseName(self.DB_NAME)
        db.setUserName(self.DB_USER)
        db.setPassword(self.DB_PASS)
        self.ltype = latch_type
        self.br_type = br_type

        if not db.open():
            QMessageBox.information( self.iface.mainWindow(), u"Ошибка работы с БД!", u"Неудачное соединение с БД!" )
            return

        if self.model==None:
            self.model = latchesRelSqlModel(self.ui.tblVNodeElements)
            self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
            self.model.setTable("public.\"latches\"")
            materialIdx = self.model.fieldIndex("material")
            self.model.setRelation(materialIdx, QtSql.QSqlRelation("material", "id", "name"))
            #self.model.setRelation(2, QtSql.QSqlRelation("material", "id", "name"))
            print "new nodelms model"

            #query.exec_("(0 id SERIAL, 1 name varchar(255), 2 description varchar(255), 3 material INTEGER 0 NOT NULL,
            #4 toponode INTEGER,5 branch INTEGER,6 brord INTEGER NOT NULL,7 injid INTEGER,8 diametr INTEGER 0 NOT NULL,
            #9 xpos INTEGER 0 NOT NULL,10 ypos INTEGER DEFAULT 0 NOT NULL,11 inangle INTEGER 0 NOT NULL,
            # #12  brtype VARCHAR(20) DEFAULT 'WATER',13 type VARCHAR(20),14 typeline VARCHAR(20),
            # #15 colorline VARCHAR(20),16 widthline INTEGER
            materialIdx = self.model.fieldIndex("material")

            self.ui.tblVNodeElements.setModel(self.model)
            self.ui.tblVNodeElements.setItemDelegate(QtSql.QSqlRelationalDelegate(self.ui.tblVNodeElements))
            self.ui.tblVNodeElements.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

            self.ui.matLineEdit.setModel(self.model.relationModel(materialIdx))
            self.ui.matLineEdit.setModelColumn(self.model.relationModel(materialIdx).fieldIndex("name"))

            mapper = QtGui.QDataWidgetMapper(self)
            mapper.setModel(self.model)
            mapper.setItemDelegate(QtSql.QSqlRelationalDelegate(self.ui.tblVNodeElements))
            mapper.addMapping(self.ui.descLineEdit,self.model.fieldIndex("description"))
            mapper.addMapping(self.ui.iDLineEdit,self.model.fieldIndex("id"))
            mapper.addMapping(self.ui.naneLineEdit,self.model.fieldIndex("name"))
            mapper.addMapping(self.ui.matLineEdit,self.model.fieldIndex("material"))
            mapper.addMapping(self.ui.lcolorLineEdit,self.model.fieldIndex("colorline"))
            mapper.addMapping(self.ui.lstyleComboBox,self.model.fieldIndex("typeline"))
            mapper.addMapping(self.ui.lwidthSpinBox,self.model.fieldIndex("widthline"))
            mapper.addMapping(self.ui.diamLineEdit,self.model.fieldIndex("diametr"))

            self.connect(self.ui.tblVNodeElements.selectionModel(),
                     QtCore.SIGNAL("currentRowChanged(QModelIndex,QModelIndex)"),
                     mapper, QtCore.SLOT("setCurrentModelIndex(QModelIndex)"))

        self.model.setFilter("toponode="+str(self.curr_nid)+" AND brtype='"+self.br_type+"'")#" AND type='"+self.ltype+
        self.model.select()

        self.model.setHeaderData(6, QtCore.Qt.Horizontal, u"Порядок")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, u"Имя")
        self.model.setHeaderData(9, QtCore.Qt.Horizontal, u"X")
        self.model.setHeaderData(10, QtCore.Qt.Horizontal, u"Y")
        self.model.setHeaderData(11, QtCore.Qt.Horizontal, u"Угол")
        self.model.setHeaderData(12, QtCore.Qt.Horizontal, u"Сеть")
        self.model.setHeaderData(13, QtCore.Qt.Horizontal, u"Тип")

        self.ui.tblVNodeElements.setColumnHidden(0, True)
        self.ui.tblVNodeElements.setColumnHidden(2, True)
        self.ui.tblVNodeElements.setColumnHidden(4, True)
        self.ui.tblVNodeElements.setColumnHidden(5, True)
        self.ui.tblVNodeElements.setColumnHidden(6, True)
        self.ui.tblVNodeElements.setColumnHidden(7, True)
        self.ui.tblVNodeElements.setColumnHidden(8, True)
        self.ui.tblVNodeElements.setColumnHidden(14, True)
        self.ui.tblVNodeElements.setColumnHidden(15, True)
        self.ui.tblVNodeElements.setColumnHidden(16, True)

    def accept(self):
        #print "saving inject out pipes datas..."
        #self.model.database().transaction()
        #if self.model.submitAll():
            #self.model.database().commit()
            #print "commited"
            #QtGui.QMessageBox.information( self, "Information", u"Изменено (запись отражена в БД)! id="+str(self.curr_nid)  )
        #else:
            #QtGui.QMessageBox.information( self, "Information", u"Ошибка (запись не отражена в БД)! id="+str(self.curr_nid)  )
        self.parent.reloadHTML()
        return QtGui.QDialog.accept(self)

    def reject(self):
        self.parent.reloadHTML()
        return QtGui.QDialog.reject(self)
