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
from PyQt4 import QtCore, QtGui
from qgis.core import QgsDataSourceURI, QgsFeature, QgsVectorLayer
from TopoNodeDialog import Ui_TopoNodeAttrsDialog
from topoInjOutListDialog import topoInjOutListDialog
from webviewdialog import webViewDialog
from math import sqrt, acos, degrees
# create the dialog for zoom to point


class vector_toponodeDialog(QtGui.QDialog, Ui_TopoNodeAttrsDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.HOST = "localhost"
        self.DB_NAME = "postgis_21_sample"
        self.DB_NAME2 = "postgis_topo210415"
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
                self.DB_NAME2 = self.connection_value(con,u"database")
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
        self.ui = Ui_TopoNodeAttrsDialog()
        self.ui.setupUi(self)
        #self.ui.getBinaryAttr.setCheckable(True)
        self.ui.getBinaryAttr.clicked.connect(self.getAttBinary)
        self.ui.putBinaryAttr.clicked.connect(self.putAttBinary)
        self.ui.pipeInjOutListButton.clicked.connect(self.showInjOutList)
        self.ui.moveLayerButton.clicked.connect(self.moveNodeToLayer)
        self.ui.editSchema.clicked.connect(self.editNodeSchema)
        self.dlgInjList = topoInjOutListDialog()
        self.nodeSchemaDlg = webViewDialog()
        self.currFeature = None
        self.currLayer = None

    def editNodeSchema(self):
        curr_id=self.currFeature.id()
        self.nodeSchemaDlg.show()
        self.nodeSchemaDlg.fillData(curr_id, self.lname, self.lines_dict, self.currFeature)

    def setParentPlugin(self, parent_object):
        self.parent_plg=parent_object

    def showInjOutList(self):
        curr_id=self.currFeature.id()
        self.dlgInjList.show()
        self.dlgInjList.fillDictsData(curr_id, self.lname)

    def putAttBinary(self):
        fpath = QtGui.QFileDialog.getOpenFileName(self, 'Выбор файла для сохранения', '/home')
        if not fpath:
            return
        s=open(fpath).read()#"C:\\Users\\ADMIN\\Desktop\\QGIS_DEV\\anapa_qgis.qgs~","rb").read()
        head, tail = os.path.split(fpath)
        #s = "'" + s + "'"
        try:
            conn = psycopg2.connect(host=self.HOST,database=self.DB_NAME,user=self.DB_USER,password=self.DB_PASS)
        except ValueError:
            QtGui.QMessageBox.information( self, u"Запись бинарных данных в БД", u"Ошибка установления соединения с БД!" )
            return
        curs = conn.cursor()
        curs.execute("INSERT INTO \"public\".\"ATT_BIN\" ( bin_desc, bin_data, node_id, node_type, filename) "
                     "VALUES ( 'no desc', %s, %s,'TOPO_NODE_WATER',%s)",
                     (psycopg2.Binary(s), str(self.currFeature.id()), tail ))
        conn.commit()
        curs.close()
        conn.close()
        QtGui.QMessageBox.information( self, u"Запись бинарных данных в БД", u"Файл записан в БД!" )
        return

    def getAttBinary(self):
        fld_dialog=QtGui.QFileDialog(self)
        fld_dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        out_dir=fld_dialog.getExistingDirectory(self, 'Open file', '/home')
        #fld_dialog.getExistingDirectory()
        #out_dir=fld_dialog.directory()
        if not out_dir:
            return
        try:
            conn = psycopg2.connect(host=self.HOST,database=self.DB_NAME,user=self.DB_USER,password=self.DB_PASS)
        except ValueError:
            QtGui.QMessageBox.information( self, u"Получение бинарных данных из БД", u"Ошибка установления соединения с БД!" )
            return
        curs = conn.cursor()
        curs.execute("SELECT * FROM \"public\".\"ATT_BIN\" WHERE node_id=%s",
                     (str(self.currFeature.id()), ))
        rows = curs.fetchall()
        for row in rows:
            out_fname = out_dir+"\\"+row[5]
            out_file = open(out_fname,"wb")
            out_file.write(str(row[2]))
            out_file.close()
            QtGui.QMessageBox.information( self, u"Получение бинарных данных из БД", u"Данные извлечены из БД и сохранены в файле: "+
                                       out_fname)
            try:
                os.system(out_fname)
            except Exception:
                QtGui.QMessageBox.information( self, u"Открытие файла из БД",
                                               u"Ошибка открытия выгруженного файла: "+out_fname )
            #subprocess.call(out_fname)
            #print " ", str(row[3])
        #conn.commit()
        curs.close()
        conn.close()

        return

    def tofloat(self, value):
		try:
			return float(value)
		except Exception:
			return 0.0

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

    def moveNodeToLayer(self):
        items = ("TOPO_NODE_WATER", "TOPO_NODE_KANAL")
        item, ok = QtGui.QInputDialog.getItem(self, 'Input Dialog', 'Enter your name:', items, 0, False)
        if not ok:
            return
        uri = QgsDataSourceURI()
        # set host name, port, database name, username and password
        uri.setConnection(self.HOST, "5432", self.DB_NAME2, self.DB_USER, self.DB_PASS)
        uri.setDataSource("public", item, "the_geom", "")
        consolidLayer = QgsVectorLayer(uri.uri(), item, self.DB_USER)
        if not consolidLayer.isValid():
            raise IOError, u"Ошибка открытия слоя перемещения"+item
        print("Start move to layer...")
        mergeFeature = QgsFeature()
        mergeFeature.setFields(consolidLayer.dataProvider().fields())
        mergeFeature.setGeometry(self.cf.geometry())
        #mergeFeature.setAttribute("X_coord",self.cf.attribute("X_coord"))
        fields = self.cf.fields()
        for k in range(fields.count()):
            field = fields[k]
            mergeFeature.setAttribute(field.name(),self.cf.attribute(field.name()))
        consolidLayer.startEditing()
        consolidLayer.addFeature(mergeFeature, True)
        consolidLayer.commitChanges()
        self.cl.startEditing()
        self.cl.deleteFeature(self.cf.id())
        self.cl.commitChanges()
        #self.iface.setActiveLayer(consolidLayer)
        self.cl.triggerRepaint()
        consolidLayer.triggerRepaint()
        QtGui.QMessageBox.information( self, u"Перемещение", u"Вершина перемещена!" )

    def fillAttrData(self, closestFeature, cLayer, parent_object, wblayer):
        self.wb_layer = wblayer
        self.parent_plg = parent_object
        self.lname='NONE'
        self.cf = closestFeature
        self.cl = cLayer
        #table = QtGui.QTableWidget()
        #table.setColumnWidth(0,250)
        #table.item(0, 0)
        #table.rowc
        cnt=0
        prevex=0
        prevey=0
        prev2ex=0
        prev2ey=0
        prev_inarea=0
        #self.wb_dprovider = self.wb_layer.dataProvider()
        #self.wb_layer.startEditing()
        self.lines_dict = []
        qpoint = closestFeature.geometry().asPoint()
        if True:
            for elem in self.wb_layer.getFeatures():
                prev_inarea=0
                cnt=0
                prevex=0
                prevey=0
                for epoint in elem.geometry().asPolyline():

                    prev_inarea=0
                    cnt=cnt+1
                    if (epoint.x()<=qpoint.x()+50) and (epoint.x()>=qpoint.x()
                        -50) and (epoint.y()<=qpoint.y()+50) and (epoint.y()>=qpoint.y()-50):
                        if cnt>1 and prev_inarea==0:
                            self.lines_dict.append({"x1":prevex,"y1":prevey,"x2":epoint.x(),"y2":epoint.y(),"nid":elem.id(),"ord":1})
                            print "[1]x:["+str(prevex)+"],y:["+str(prevey)+"]"+"cx:["+str(epoint.x())+"],cy:["+str(epoint.y())+"]"
                        prev_inarea=1
                        if False:
                            geom = elem.geometry()
                            if not geom.insertVertex(epoint.x()+100,epoint.y()+100,0):
                                QtGui.QMessageBox.information( self, "Error", "Not success insertVertex" )
                            elem.setGeometry(geom)
                            self.wb_layer.changeGeometry(elem.id(), geom)
                            self.wb_layer.commitChanges()
                        print "x:["+str(epoint.x())+"],y:["+str(epoint.y())+"]"+"cx:["+str(qpoint.x())+"],cy:["+str(qpoint.y())+"]"
                    else:
                        if prev_inarea==1 and cnt>1:
                            self.lines_dict.append({"x1":epoint.x(),"y1":epoint.y(),"x2":prevex,"y2":prevey,"nid":elem.id(),"ord":2})
                            print "[2]x:["+str(epoint.x())+"],y:["+str(epoint.y())+"]"+"cx:["+str(prevex)+"],cy:["+str(prevey)+"]"
                        if prev_inarea==0 and cnt>1 and (((epoint.x()<=qpoint.x()) and (prevex>=qpoint.x())) or
                            ((epoint.x()>=qpoint.x()) and (prevex<=qpoint.x())) or
                            ((epoint.y()<=qpoint.y()) and (prevey>=qpoint.y())) or
                            ((epoint.y()>=qpoint.y()) and (prevey<=qpoint.y()))):
                            dst = sqrt((epoint.x()-prevex)*(epoint.x()-prevex)+(epoint.y()-prevey)*(epoint.y()-prevey))
                            qdst1 = sqrt((qpoint.x()-prevex)*(qpoint.x()-prevex)+(qpoint.y()-prevey)*(qpoint.y()-prevey))
                            qdst2 = sqrt((epoint.x()-qpoint.x())*(epoint.x()-qpoint.x())+(epoint.y()-qpoint.y())*(epoint.y()-qpoint.y()))
                            pval = (dst+qdst1+qdst2)/2
                            try:
                                if qdst1>0 and qdst2>0:
                                    dangle = degrees(acos((qdst1*qdst1+qdst2*qdst2-dst*dst)/(2*qdst1*qdst2)))
                            except Exception:
                                dangle = 0
                            hval=10000
                            if dst>0:
                                hval = 2*sqrt(pval*(pval-dst)*(pval-qdst1)*(pval-qdst2))/dst;
                            if (hval<=50) and (dst>qdst1) and (dst>qdst2):
                                print str(dst)+u"==="+str(qdst1)+u"==="+str(qdst2)
                                self.lines_dict.append({"x1":epoint.x(),"y1":epoint.y(),"x2":prevex,"y2":prevey,"nid":elem.id(),"ord":2})
                                print "[3]x:["+str(epoint.x())+"],y:["+str(epoint.y())+"]"+"cx:["+str(prevex)+"],cy:["+str(prevey)+"]"

                        prev_inarea=0
                    prevex=epoint.x()
                    prevey=epoint.y()

        #self.ui.AttrTableView.setColumnCount(2)
        self.setWindowTitle(u"Правка аттрибутов. PolFunDev.(C) 2015")
        field_titles = {'gid':u'Идентификатор','id':u'Идентификатор','topo_code':u'Топокод','Y_coord':u'Y координата','X_coord':u'X координата',
                        'H_value':u'Отметка земли, Z','NP_NAME':u'Населенный пункт','STREET_NAME':u'Улица','HS_NUM':u'№ дома','NODE_NUM':u'Номер колодца',
                        'INVERT_H':u'Отметка лотка(дна) Z','CONN_IH':u'Бок. присоед (трубы) Z','PIPE_DIAM':u'Диаметр трубы в мм','PIPE_MNAME':u'Материал трубы',
                        'WELL_MNAME':u'Материал колодца','WELL_FNAME':u'Форма колодца','WELL_DIAM':u'Размер (диам.) колода в см.','DATE_STEXP':u'Дата ввода в экспл.',
                        'EXP_PERCENT':u'Процент износа в %','STAT_DESC':u'Состояние','TOPO_GRP_CODE':u'Код прохода','FIREHYDR':u'Пож. гидрант', 'TOPOFILE':u'Топофайл',
						'y_coord':u'Y координата','x_coord':u'X координата','adr_liter':u'Литер','ADR_LITER':u'Литер','COVER_MNAME':u'Материал крышки','cover_mname':u'Материал крышки',
                        'h_value':u'Отметка земли, Z','np_name':u'Населенный пункт','street_name':u'Улица','hs_num':u'№ дома','node_num':u'Номер колодца',
                        'invert_h':u'Отметка лотка(дна) Z','conn_ih':u'Бок. присоед (трубы) Z','pipe_diam':u'Диаметр трубы в мм','pipe_mname':u'Материал трубы',
                        'well_mname':u'Материал колодца','well_fname':u'Форма колодца','well_diam':u'Размер (диам.) колода в см.','date_stexp':u'Дата ввода в экспл.',
                        'exp_percent':u'Процент износа в %','stat_desc':u'Состояние','topo_grp_code':u'Код прохода','firehydr':u'Пож. гидрант', 'topofile':u'Топофайл',
                        'COMMENTS':u'Заметки','comments':u'Заметки'}
        self.currFeature = closestFeature
        self.currLayer = cLayer
        if self.currLayer == None:
            QtGui.QMessageBox.information( self, "Closest Feature Finder", u"Не выделено векторного слоя!" )
            return
        if not (self.currLayer.name() in ["TOPO_NODE_WATER", "TOPO_NODE_KANAL"]):
            QtGui.QMessageBox.information( self, "Closest Feature Finder", u"Слой не является TOPO_NODE_WATER или TOPO_NODE_KANAL!" )
            return
        if self.currLayer.name()=='TOPO_NODE_WATER':
            self.lname='WATER'
        if self.currLayer.name()=='TOPO_NODE_KANAL':
            self.lname='KANAL'
        fields = closestFeature.fields()
        self.ui.AttrTableView.setRowCount(fields.count())
        self.ui.AttrTableView.setColumnWidth(0,235)
        self.ui.AttrTableView.setColumnWidth(1,115)
        for k in range(fields.count()):
                field = fields[k]
                auto_val = False
                twi = QtGui.QTableWidgetItem()

                tmp_str=""
                #print "["+str(type(closestFeature.attribute(field.name())))+"]"
                #<type 'float'> <class 'PyQt4.QtCore.QPyNullVariant'> <class 'PyQt4.QtCore.QDate'>
                if not (closestFeature.attribute(field.name())==None):
                    if str(type(closestFeature.attribute(field.name())))=="<type 'unicode'>":
                        tmp_str = closestFeature.attribute(field.name())
                    elif str(type(closestFeature.attribute(field.name())))=="<class 'PyQt4.QtCore.QDate'>":
                        time_fmt="dd.MM.yyyy"
                        tmp_str = closestFeature.attribute(field.name()).toString(time_fmt)
                    else:
                        tmp_str=str(closestFeature.attribute(field.name()))
                if (field.name()=="NP_NAME" or field.name()=="np_name") and ((tmp_str==None) or (tmp_str=="") and not (self.parent_plg.prev_np_name=="")):
                    tmp_str=self.parent_plg.prev_np_name
                    auto_val = True
                if (field.name()=="STREET_NAME" or field.name()=="street_name") and ((tmp_str==None) or (tmp_str=="") and not (self.parent_plg.prev_street_name=="")):
                    tmp_str=self.parent_plg.prev_street_name
                    auto_val = True
                if (field.name()=="PIPE_MNAME" or field.name()=="pipe_mname") and ((tmp_str==None) or (tmp_str=="") and not (self.parent_plg.prev_pipe_mname=="")):
                    tmp_str=self.parent_plg.prev_pipe_mname
                    auto_val = True
                if (field.name()=="WELL_MNAME" or field.name()=="well_mname") and ((tmp_str==None) or (tmp_str=="") and not (self.parent_plg.prev_well_mname=="")):
                    tmp_str=self.parent_plg.prev_well_mname
                    auto_val = True
                if (field.name()=="WELL_FNAME" or field.name()=="well_fname") and ((tmp_str==None) or (tmp_str=="") and not (self.parent_plg.prev_well_fname=="")):
                    tmp_str=self.parent_plg.prev_well_fname
                    auto_val = True
                if (field.name()=='PIPE_DIAM' or field.name()=="pipe_diam"):
                    if (closestFeature.attribute(field.name())==None or closestFeature.attribute(field.name())==0):
                        if self.parent_plg.prev_pipe_diam>0:
                            auto_val = True

                twi.setText(tmp_str)
                if (field.name()=="H_value" or field.name()=="h_value") \
                        or (field.name()=="X_coord" or field.name()=="x_coord") \
                        or (field.name()=="Y_coord" or field.name()=="y_coord") \
                        or (field.name()=="ID" or field.name()=="id") \
                        or (field.name()=="GID" or field.name()=="gid"):
                    twi.setFlags(twi.flags() ^ QtCore.Qt.ItemIsEnabled)

                twit = QtGui.QTableWidgetItem()
                if auto_val:
                    twit.setText("===>>>"+field_titles[field.name()])
                else:
                    twit.setText(field_titles[field.name()])
                if (field.name()=="H_value" or field.name()=="h_value") \
                        or (field.name()=="X_coord" or field.name()=="x_coord") \
                        or (field.name()=="Y_coord" or field.name()=="y_coord") \
                        or (field.name()=="ID" or field.name()=="id") \
                        or (field.name()=="GID" or field.name()=="gid"):
                    twit.setFlags(twit.flags() ^ QtCore.Qt.ItemIsEnabled)
                self.ui.AttrTableView.setItem(k,0,twit)

                if (field.name()=='WELL_FNAME') or field.name()=="well_fname":
                    self.combobox = QtGui.QComboBox()
                    self.combobox.setEditable(True)
                    #combobox.setCurrentText(tmp_str)
                    self.combobox.addItem(tmp_str)
                    self.combobox.addItem(u"Квадратный")
                    self.combobox.addItem(u"Круглый")
                    self.ui.AttrTableView.setCellWidget(k,1, self.combobox)
                elif (field.name()=='WELL_MNAME') or field.name()=="well_mname":
                    self.wmnCBox = QtGui.QComboBox()
                    self.wmnCBox.setEditable(True)
                    #combobox.setCurrentText(tmp_str)
                    self.wmnCBox.addItem(tmp_str)
                    self.wmnCBox.addItem(u"Кирпич")
                    self.wmnCBox.addItem(u"Железобетон")
                    self.ui.AttrTableView.setCellWidget(k,1, self.wmnCBox)
                elif (field.name()=='STAT_DESC') or field.name()=="stat_desc":
                    self.sttCBox = QtGui.QComboBox()
                    self.sttCBox.setEditable(True)
                    #combobox.setCurrentText(tmp_str)
                    self.sttCBox.addItem(tmp_str)
                    self.sttCBox.addItem(u"Хорошее")
                    self.sttCBox.addItem(u"Нужен ремонт")
                    self.ui.AttrTableView.setCellWidget(k,1, self.sttCBox)
                elif (field.name()=='FIREHYDR') or field.name()=="firehydr":
                    self.fhdrCBox = QtGui.QComboBox()
                    self.fhdrCBox.setEditable(True)
                    #combobox.setCurrentText(tmp_str)
                    self.fhdrCBox.addItem(tmp_str)
                    self.fhdrCBox.addItem(u"ДА")
                    self.fhdrCBox.addItem(u"НЕТ")
                    self.ui.AttrTableView.setCellWidget(k,1, self.fhdrCBox)
                elif (field.name()=='PIPE_MNAME') or field.name()=="pipe_mname":
                    self.pmnCBox = QtGui.QComboBox()
                    self.pmnCBox.setEditable(True)
                    #combobox.setCurrentText(tmp_str)
                    self.pmnCBox.addItem(tmp_str)
                    self.pmnCBox.addItem(u"А/ц")
                    self.pmnCBox.addItem(u"ПНД")
                    self.pmnCBox.addItem(u"Сталь")
                    self.pmnCBox.addItem(u"Чугун")
                    self.pmnCBox.addItem(u"Железобетон")
                    self.ui.AttrTableView.setCellWidget(k,1, self.pmnCBox)
                elif (field.name()=='COVER_MNAME') or field.name()=="cover_mname":
                    self.cvmNCBox = QtGui.QComboBox()
                    self.cvmNCBox.setEditable(True)
                    #combobox.setCurrentText(tmp_str)
                    self.cvmNCBox.addItem(tmp_str)
                    self.cvmNCBox.addItem(u"А/ц")
                    self.cvmNCBox.addItem(u"ПНД")
                    self.cvmNCBox.addItem(u"Сталь")
                    self.cvmNCBox.addItem(u"Чугун")
                    self.cvmNCBox.addItem(u"Железобетон")
                    self.ui.AttrTableView.setCellWidget(k,1, self.cvmNCBox)
                elif (field.name()=='X_coord') or field.name()=="x_coord":
                    self.xcQSpinBox=QtGui.QDoubleSpinBox()
                    self.xcQSpinBox.setEnabled(False)
                    self.xcQSpinBox.setMaximum(9999999999999.9999)
                    self.xcQSpinBox.setValue(self.tofloat(tmp_str))
                    self.ui.AttrTableView.setCellWidget(k,1, self.xcQSpinBox)
                elif (field.name()=='Y_coord') or field.name()=="y_coord":
                    self.ycQSpinBox=QtGui.QDoubleSpinBox()
                    self.ycQSpinBox.setEnabled(False)
                    self.ycQSpinBox.setMaximum(9999999999999.9999)
                    self.ycQSpinBox.setValue(closestFeature.attribute(field.name()) if closestFeature.attribute(field.name())!=None else 0.0)
                    self.ui.AttrTableView.setCellWidget(k,1, self.ycQSpinBox)
                elif (field.name()=='H_value') or field.name()=="h_value":
                    self.hvQSpinBox=QtGui.QDoubleSpinBox()
                    self.hvQSpinBox.setEnabled(False)
                    self.hvQSpinBox.setMaximum(9999999999999.9999)
                    self.hvQSpinBox.setValue(closestFeature.attribute(field.name()) if closestFeature.attribute(field.name())!=None else 0.0)
                    self.ui.AttrTableView.setCellWidget(k,1, self.hvQSpinBox)
                elif (field.name()=='HS_NUM') or field.name()=="hs_num":
                    self.hnQSpinBox=QtGui.QSpinBox()
                    self.hnQSpinBox.setMaximum(99999)
                    self.hnQSpinBox.setValue(closestFeature.attribute(field.name()) if closestFeature.attribute(field.name())!=None else 0)
                    self.ui.AttrTableView.setCellWidget(k,1, self.hnQSpinBox)
                elif (field.name()=='INVERT_H') or field.name()=="invert_h":
                    self.ivhQSpinBox=QtGui.QDoubleSpinBox()
                    self.ivhQSpinBox.setMaximum(9999999999999.9999)
                    self.ivhQSpinBox.setValue(closestFeature.attribute(field.name()) if closestFeature.attribute(field.name())!=None else 0.0)
                    self.ui.AttrTableView.setCellWidget(k,1, self.ivhQSpinBox)
                elif (field.name()=='CONN_IH') or field.name()=="conn_ih":
                    self.cnhQSpinBox=QtGui.QDoubleSpinBox()
                    self.cnhQSpinBox.setMaximum(9999999999999.9999)
                    self.cnhQSpinBox.setValue(closestFeature.attribute(field.name()) if closestFeature.attribute(field.name())!=None else 0.0)
                    self.ui.AttrTableView.setCellWidget(k,1, self.cnhQSpinBox)
                elif (field.name()=='PIPE_DIAM') or field.name()=="pipe_diam":
                    self.pdmQSpinBox=QtGui.QDoubleSpinBox()
                    self.pdmQSpinBox.setMaximum(9999999999999.9999)
                    self.pdmQSpinBox.setValue(closestFeature.attribute(field.name()) if (closestFeature.attribute(field.name())!=None and closestFeature.attribute(field.name())>0) else self.parent_plg.prev_pipe_diam)
                    self.ui.AttrTableView.setCellWidget(k,1, self.pdmQSpinBox)
                elif (field.name()=='WELL_DIAM') or field.name()=="well_diam":
                    self.wdmQSpinBox=QtGui.QDoubleSpinBox()
                    self.wdmQSpinBox.setMaximum(9999999999999.9999)
                    self.wdmQSpinBox.setValue(closestFeature.attribute(field.name()) if closestFeature.attribute(field.name())!=None else 0.0)
                    self.ui.AttrTableView.setCellWidget(k,1, self.wdmQSpinBox)
                elif (field.name()=='DATE_STEXP') or field.name()=="date_stexp":
                    self.stExpDT=QtGui.QDateEdit()
                    self.stExpDT.setDate(closestFeature.attribute(field.name()))
                    self.ui.AttrTableView.setCellWidget(k,1, self.stExpDT)
                elif (field.name()=='EXP_PERCENT') or field.name()=="exp_percent":
                    self.expQSpinBox=QtGui.QSpinBox()
                    self.expQSpinBox.setValue(closestFeature.attribute(field.name()) if closestFeature.attribute(field.name())!=None else 0)
                    self.ui.AttrTableView.setCellWidget(k,1, self.expQSpinBox)
                else:
                    self.ui.AttrTableView.setItem(k,1,twi)
        #text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')


    def accept(self):
        if self.currLayer == None:
            QtGui.QMessageBox.information( self, "Closest Feature Finder", "No vector layers selected" )
            return
        if not (self.currLayer.name() in ["TOPO_NODE_WATER", "TOPO_NODE_KANAL"]):
            QtGui.QMessageBox.information( self, "Closest Feature Finder", u"Слой не является  TOPO_NODE_WATER или TOPO_NODE_KANAL!" )
            return
        if self.currFeature == None:
            QtGui.QMessageBox.information( self, "Closest Feature Finder", "No feature selected" )
            return
        fields = self.currFeature.fields()
        datas = dict()
        for k in range(fields.count()):
            field = fields[k]
            if field.name()=="WELL_FNAME" or field.name()=="well_fname":
                datas[fields.indexFromName(field.name())]=self.combobox.currentText()
                self.parent_plg.prev_well_fname=self.combobox.currentText()
            elif field.name()=="WELL_MNAME" or field.name()=="well_mname":
                datas[fields.indexFromName(field.name())]=self.wmnCBox.currentText()
                self.parent_plg.prev_well_mname=self.wmnCBox.currentText()
            elif field.name()=="PIPE_MNAME" or field.name()=="pipe_mname":
                datas[fields.indexFromName(field.name())]=self.pmnCBox.currentText()
                self.parent_plg.prev_pipe_mname=self.pmnCBox.currentText()
            elif field.name()=="COVER_MNAME" or field.name()=="cover_mname":
                datas[fields.indexFromName(field.name())]=self.cvmNCBox.currentText()
                #self.parent_plg.prev_pipe_mname=self.сvmnCBox.currentText()
            elif field.name()=="STAT_DESC" or field.name()=="stat_desc":
                datas[fields.indexFromName(field.name())]=self.sttCBox.currentText()
            elif field.name()=="X_coord" or field.name()=="x_coord":
                datas[fields.indexFromName(field.name())]=self.xcQSpinBox.value()
            elif field.name()=="Y_coord" or field.name()=="y_coord":
                datas[fields.indexFromName(field.name())]=self.ycQSpinBox.value()
            elif field.name()=="H_value" or field.name()=="h_value":
                datas[fields.indexFromName(field.name())]=self.hvQSpinBox.value()
            elif field.name()=="HS_NUM" or field.name()=="hs_num":
                datas[fields.indexFromName(field.name())]=self.hnQSpinBox.value()
            elif field.name()=="INVERT_H" or field.name()=="invert_h":
                datas[fields.indexFromName(field.name())]=self.ivhQSpinBox.value()
            elif field.name()=="CONN_IH" or field.name()=="conn_ih":
                datas[fields.indexFromName(field.name())]=self.cnhQSpinBox.value()
            elif field.name()=="PIPE_DIAM" or field.name()=="pipe_diam":
                datas[fields.indexFromName(field.name())]=self.pdmQSpinBox.value()
                self.parent_plg.prev_pipe_diam=self.pdmQSpinBox.value()
            elif field.name()=="WELL_DIAM" or field.name()=="well_diam":
                datas[fields.indexFromName(field.name())]=self.wdmQSpinBox.value()
            elif field.name()=="EXP_PERCENT" or field.name()=="exp_percent":
                datas[fields.indexFromName(field.name())]=self.expQSpinBox.value()
            elif field.name()=="DATE_STEXP" or field.name()=="date_stexp":
                datas[fields.indexFromName(field.name())]=self.stExpDT.date()
            elif field.name()=="FIREHYDR" or field.name()=="firehydr":
                datas[fields.indexFromName(field.name())]=self.fhdrCBox.currentText()
            elif not (field.name() in ["id","gid"]):
                #QtGui.QMessageBox.information( self, "Closest Feature Finder", "No feature selected-"+field.name() )
                if (self.ui.AttrTableView.item(k, 1).text()!=""):
                    datas[fields.indexFromName(field.name())]=self.ui.AttrTableView.item(k, 1).text()
                    if field.name()=="NP_NAME" or field.name()=="np_name":
                        self.parent_plg.prev_np_name=self.ui.AttrTableView.item(k, 1).text()
                    if field.name()=="STREET_NAME" or field.name()=="street_name":
                        self.parent_plg.prev_street_name=self.ui.AttrTableView.item(k, 1).text()
                        #print self.parent_plg.prev_np_name
                else:
                    datas[fields.indexFromName(field.name())]=None
                #print ""
        # update feature's distance attribute
        self.currLayer.dataProvider().changeAttributeValues({self.currFeature.id(): datas } )
        #{fields.indexFromName('field_4'): 3}})
        #self.currLayer.changeAttributeValue(self.currFeature.id(),fields.indexFromName('field_4'),3,True)
        #self.currLayer.commitChanges()
        QtGui.QMessageBox.information( self, "Information", u"Изменено! id="+str(self.currFeature.id())  )
        return QtGui.QDialog.accept(self)

