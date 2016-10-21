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
from materialsSqlModel import materialRelSqlModel
from topofeaturelinkdatas import Ui_topoFeatureLinkDatasDialog
# create the dialog for zoom to point


class topoInjOutListDialog(QtGui.QDialog, Ui_topoFeatureLinkDatasDialog):
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
        self.ui = Ui_topoFeatureLinkDatasDialog()
        self.ui.setupUi(self)
        self.ui.addInjOutPipePushButton.clicked.connect(self.addInjPipe)
        self.ui.delInjOutPipePushButton.clicked.connect(self.delInjPipe)
        self.model = None

    def getConnections(self):
        s = QtCore.QSettings()
        s.beginGroup(u"PostgreSQL/connections")
        currentConnections = s.childGroups()
        s.endGroup()
        return currentConnections

    def connection_value(self, connection, key):
        #uri = QgsDataSourceURI()
        settings = QtCore.QSettings()
        settings.beginGroup(u"/PostgreSQL/connections")
        settings.beginGroup(connection)
        value = str(settings.value(key))
        settings.endGroup()
        settings.endGroup()
        return value

    def addInjPipe(self):
        query = QtSql.QSqlQuery()
        query.exec_(u"insert into public.\"injoutpipes\"(description, material, toponode, diametr, type) values('НОВЫЙ', 3, "+str(self.curr_nid)+", 0, '"+self.ltype+"')")
        self.model.select()

    def delInjPipe(self):
        ridx=self.ui.pipeInjectOutListTableView.currentIndex().row()
        oid = self.toint(self.model.index(ridx,0).data())
        #print oid
        query = QtSql.QSqlQuery()
        reply = QtGui.QMessageBox.question(self,u"Удалить "+str(oid)+"-"+self.model.index(ridx,1).data(),
                                     u"Продолжить?", QtGui.QMessageBox.Apply, QtGui.QMessageBox.Cancel)
        if reply==QtGui.QMessageBox.Apply:
            query.exec_("DELETE FROM public.\"injoutpipes\" where id="+str(oid))
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
        query.exec_("create table public.\"injoutpipes\"(id SERIAL, description varchar(255), material INTEGER DEFAULT 0 NOT NULL, toponode INTEGER, diametr INTEGER DEFAULT 0 NOT NULL, injcode INTEGER DEFAULT 0 NOT NULL, injorder INTEGER DEFAULT 0 NOT NULL, injdeep INTEGER DEFAULT 0 NOT NULL, type VARCHAR(20) DEFAULT 'WATER'::character varying NOT NULL, CONSTRAINT \"injoutpipes_pkey\" PRIMARY KEY(id))")

        query.exec_("create table public.\"material\"(id SERIAL, name varchar(255), CONSTRAINT \"materials_pkey\" PRIMARY KEY(id))")
        #query.exec_("insert into public.\"material\"(name) values('Асбестоцемент')")
        #query.exec_("insert into public.\"material\"(name) values('Чугун')")
        #query.exec_("insert into public.\"material\"(name) values('Бетон')")

    def initModel(self, model):
        model.setTable("STREETS")
        model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        model.select()

        model.setHeaderData(0, QtCore.Qt.Horizontal, "id")
        model.setHeaderData(1, QtCore.Qt.Horizontal, "STREET_NAME")

    def fillDictsData(self, curr_id, ltype):
        self.setWindowTitle(u"Правка связанных таблиц топообъекта")
        self.curr_nid = curr_id;
        db = QtSql.QSqlDatabase.addDatabase("QPSQL")
        db.setHostName(self.HOST)
        db.setDatabaseName(self.DB_NAME)
        db.setUserName(self.DB_USER)
        db.setPassword(self.DB_PASS)
        self.ltype = ltype

        if not db.open():
            QMessageBox.information( self.iface.mainWindow(), u"Ошибка работы с БД!", u"Неудачное соединение с БД!" )
            return
        #else:
        #    for tn in db.tables():
        #        print str(tn)

        #self.createRelationalTables()

        #queryd = db.exec_("SELECT * FROM STREETS")
        #queryd = QtSql.QSqlQuery("SELECT * FROM public.\"injoutpipes\"", db)
        #queryd.exec_()
        #print queryd.lastError().text()
        #queryd.exec_("SELECT * FROM TOPO_NODE_WATER")
        #if db.isOpen():
        #    print str(queryd.size())
        #while queryd.next():
        #print "sss"
        if self.model==None:
            self.model = materialRelSqlModel()
            #print "sss1"
            self.ui.pipeInjectOutListTableView.setModel(self.model)
            #print "sss2"
            self.model.setTable("public.\"injoutpipes\"")
            #print "sss3"
            self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
            #print "sss4"
            self.model.setRelation(2, QtSql.QSqlRelation("material", "id", "name"))
            #print "sss5"
            #compositionsRelation->removeColumn(0);
            self.ui.pipeInjectOutListTableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.ui.pipeInjectOutListTableView))
            #print "sss6"

            #print dir(model)
            #print str(self.model.tableName())
            #print "columns count:"+str(self.model.columnCount())
            #print "count:"+str(self.model.rowCount())
            #print "sss8"

            self.model.setHeaderData(2, QtCore.Qt.Horizontal, u"Материал")
            self.model.setHeaderData(1, QtCore.Qt.Horizontal, u"Описание")
            self.model.setHeaderData(4, QtCore.Qt.Horizontal, u"Диаметр")
            self.model.setHeaderData(5, QtCore.Qt.Horizontal, u"Код")
            self.model.setHeaderData(6, QtCore.Qt.Horizontal, u"Порядок")
            self.model.setHeaderData(7, QtCore.Qt.Horizontal, u"Глубина")
        #except Exception:
        #    QtGui.QMessageBox.information( self, "Information", u"Error" )
        #print "sss7"

        self.ui.pipeInjectOutListTableView.setColumnHidden(0, True)
        self.ui.pipeInjectOutListTableView.setColumnHidden(3, True)
        self.ui.pipeInjectOutListTableView.setColumnHidden(5, True)
        self.ui.pipeInjectOutListTableView.setColumnHidden(6, True)
        self.ui.pipeInjectOutListTableView.setColumnHidden(8, True)
        #print "sss9"

        self.model.setFilter("toponode="+str(self.curr_nid)+" AND type='"+self.ltype+"'")
        self.model.select()

        #self.ui.StreetsTView.setItemDelegate(QtSql.QSql)
        #self.ui.StreetsTView.setEditTriggers(QAbstractItemView::NoEditTriggers);
        #edit = QtSql.QSqlTableModel.OnFieldChange
        #model.setEditStrategy(edit)
        #view.setSelectionMode(self.mode)
        #self.mode = QtGui.QAbstractItemView.SingleSelection
        #self.ui.pipeInjectOutListTableView.show()
        #self.model.s

    def accept(self):
        #print "saving inject out pipes datas..."
        #self.model.database().transaction()
        #if self.model.submitAll():
            #self.model.database().commit()
            #print "commited"
            #QtGui.QMessageBox.information( self, "Information", u"Изменено (запись отражена в БД)! id="+str(self.curr_nid)  )
        #else:
            #QtGui.QMessageBox.information( self, "Information", u"Ошибка (запись не отражена в БД)! id="+str(self.curr_nid)  )
        return QtGui.QDialog.accept(self)

