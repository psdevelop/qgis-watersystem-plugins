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
from qgis.core import *
from qgis.gui import *
from reportspanel import Ui_reportGenDialog
# create the dialog for zoom to point

class reportGenerator(QtGui.QDialog, Ui_reportGenDialog):
    def __init__(self, iface):
        QtGui.QDialog.__init__(self)
        self.HOST = "localhost"
        self.DB_NAME = "postgis_topo210415"
        self.DB_USER = "postgres"
        self.DB_PASS = "29111960"
        self.HOST2 = "localhost"
        self.DB_NAME2 = "postgis_topo210415"
        self.DB_USER2 = "postgres"
        self.DB_PASS2 = "29111960"
        self.iface = iface
        conns = self.getConnections()
        self.has_s21 = False
        self.has_ptopo = False
        self.has_mtopo = False
        for con in conns:
            if con==u"postgis_21_sample":
                self.has_s21 = True
                self.HOST = self.connection_value(con,u"host")
                #print self.connection_value(con,u"port")
                self.DB_NAME = self.connection_value(con,u"database")
                self.DB_USER = self.connection_value(con,u"username")
                self.DB_PASS = self.connection_value(con,u"password")
        for con in conns:
            if con==u"postgis_topo210415":
                self.has_s21 = True
                self.has_mtopo = True
                self.HOST = self.connection_value(con,u"host")
                #print self.connection_value(con,u"port")
                self.DB_NAME = self.connection_value(con,u"database")
                self.DB_USER = self.connection_value(con,u"username")
                self.DB_PASS = self.connection_value(con,u"password")
                self.HOST2 = self.connection_value(con,u"host")
                #print self.connection_value(con,u"port")
                self.DB_NAME2 = self.connection_value(con,u"database")
                self.DB_USER2 = self.connection_value(con,u"username")
                self.DB_PASS2 = self.connection_value(con,u"password")
        if not self.has_s21:
            for con in conns:
                if con==u"postgis_topo":
                    self.has_ptopo = True
                    self.HOST = self.connection_value(con,u"host")
                    self.DB_NAME = self.connection_value(con,u"database")
                    self.DB_USER = self.connection_value(con,u"username")
                    self.DB_PASS = self.connection_value(con,u"password")
                    self.HOST2 = self.connection_value(con,u"host")
                    self.DB_NAME2 = self.connection_value(con,u"database")
                    self.DB_USER2 = self.connection_value(con,u"username")
                    self.DB_PASS2 = self.connection_value(con,u"password")

        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.ui = Ui_reportGenDialog()
        self.ui.setupUi(self)
        self.ui.generateRepPButton.clicked.connect(self.generateReport)
        self.ui.repTypeCBox.addItem(u"Отчет по протяженности сетей")
        self.ui.repTypeCBox.addItem(u"Отчет по колодцам с группировкой")
        self.repBrowse = self.ui.reportWebView

    def getConnections(self):
        s = QtCore.QSettings()
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

    def generateReport(self):
        self.getDatas(self.ui.repTypeCBox.currentIndex()+1,[])

    def getDatas(self, report_type, params):

        self.ui.outDataEdit.clear()
        try:
            conn2 = psycopg2.connect(host=self.HOST2,database=self.DB_NAME2,
                                    user=self.DB_USER2,password=self.DB_PASS2)
            conn = psycopg2.connect(host=self.HOST,database=self.DB_NAME,
                                    user=self.DB_USER,password=self.DB_PASS)
        except ValueError:
            QtGui.QMessageBox.information( self, u"Получение данных колодца из БД", u"Ошибка установления соединения с БД!" )
            return
        curs = conn.cursor()
        curs2 = conn2.cursor()
        self.rdatas = []
        if report_type==1:
            curs2.execute("SELECT COUNT(*), \"DATE_STEXP\" as edt FROM \"public\".\"TOPO_NODE_WATER\" GROUP BY \"DATE_STEXP\"")
            self.rdatas = curs2.fetchall()
            for rdata in self.rdatas:
                self.ui.outDataEdit.append(str(rdata[1])+u":"+str(rdata[0]))
        elif report_type==2:
            self.rep_area = u" по всем нас пунктам "		    
            if not self.ui.regionCBox.currentText()=='':
                self.rep_area=u" по району '"+self.ui.regionCBox.currentText()+"' "
            self.html_code = u"""
                <!DOCTYPE html>
                <html lang="en">
                    <head>
                    <meta charset="utf-8">
                    <title>Отчет по топосъемке обектов</title></head><body><h1>Отчет по топосъемке объектов""";
            self.html_code = self.html_code + self.rep_area+ u"</h1>"
            if not (self.has_ptopo or self.has_s21) and self.has_mtopo:
                layers = self.iface.legendInterface().layers()
                for layer in layers:
                    layerType = layer.type()
                    if layerType == QgsMapLayer.VectorLayer:
                        if layer.geometryType()==QGis.Line and (layer.name()==u"TOPO_WATER_BRANCH" or layer.name()==u"Участки водопровода"):
                            f = QgsFeature()
                            feat_iterator = layer.getFeatures()
                            #llen=0
                            while feat_iterator.nextFeature(f):
                                datas = dict()
                                fields = f.fields()
                                datas[fields.indexFromName("len")] = f.geometry().length()
                                #print str(f.geometry().length())
                                layer.dataProvider().changeAttributeValues({f.id(): datas } )
                curs.execute(u"SELECT coalesce(wb.\"material\",'Без материала') AS mat, coalesce((wb.\"diametr\"/100)*100,0) AS diametr,count(*) AS cnt, "
                         u"coalesce(sum(coalesce(wb.\"len\",0)),0) as lsum FROM \"TOPO_WATER_BRANCH\" wb WHERE (wb.reg='"+self.ui.regionCBox.currentText()+u"' or ''='"+self.ui.regionCBox.currentText()+u"') GROUP BY wb.\"material\", (wb.\"diametr\"/100) ORDER BY wb.\"material\", diametr ")
            else:
                curs.execute("SELECT coalesce(wb.\"MATERIAL\",'Без материала') AS mat, coalesce((wb.\"DIAMETR\"/100)*100,0) AS diametr,count(*) AS cnt, "
                         "coalesce(sum(wb.\"LEN\"),0) as lsum FROM \"WATER_BRANCH\" wb WHERE (wb.reg='"+self.ui.regionCBox.currentText().encode('utf-8')+"' or ''='"+
                         self.ui.regionCBox.currentText().encode('utf-8')+"') GROUP BY wb.\"MATERIAL\", "
                         "(wb.\"DIAMETR\"/100) ORDER BY wb.\"MATERIAL\", diametr ")
            self.rdatas = curs.fetchall()
            self.ui.outDataEdit.append(u"=============ВОДОПРОВОД МАТЕРИАЛ, ДИАМЕТР УСЛОВН % 100, УЧАСТКОВ, СУММАРН ДЛИНА")
            self.html_code = self.html_code + u"<h4>ВОДОПРОВОД МАТЕРИАЛ, ДИАМЕТР УСЛОВН % 100, УЧАСТКОВ, СУММАРН ДЛИНА</h4>"
            self.html_code = self.html_code + u"<table border=\"1\"><tr><td>Материал</td><td>Диаметр " \
                                              u"усл</td><td>Число участков</td><td>Суммарн длина</td></tr>"
            for rdata in self.rdatas:
                if not(rdata[0]==None):
                    self.html_code = self.html_code + u"<tr><td>"+rdata[0]+\
                                     u"</td><td>"+str(rdata[1])+u"-"+str(rdata[1]+99)+\
                                     u"</td><td>"+str(rdata[2])+u"</td><td>"+str("%.2f" % rdata[3])+u"</td></tr>"
                    self.ui.outDataEdit.append(u"Материал-"+rdata[0]+u":диам="+str(rdata[1])+u"-"+str(rdata[1]+99)+u",участков-"+str(rdata[2])+u",длина="+str(rdata[3]))
                else:
                    self.html_code = self.html_code + u"<tr><td>Без материала</td><td>"+str(rdata[1])+\
                                     u"-"+str(rdata[1]+99)+u"</td><td>"+str(rdata[2])+u"</td><td>"+str(rdata[3])+u"</td></tr>"
                    self.ui.outDataEdit.append(u"Без материала:"+str(rdata[1])+u","+str(rdata[2])+u","+str("%.2f" % rdata[3]))
            self.html_code = self.html_code + u"</table>";
            if not (self.has_ptopo or self.has_s21) and self.has_mtopo:
                curs.execute("SELECT coalesce(wb.\"material\",'Без материала') AS mat,coalesce(wb.\"diametr\",0) AS diametr,count(*) AS cnt, "
                         "sum(coalesce(wb.\"len\",0)) as lsum FROM \"TOPO_WATER_BRANCH\" wb WHERE (wb.reg='"+self.ui.regionCBox.currentText().encode('utf-8')+"' or ''='"+
                         self.ui.regionCBox.currentText().encode('utf-8')+"')  GROUP BY coalesce(wb.\"material\",'Без материала'), "
                         "coalesce(wb.\"diametr\",0) ORDER BY coalesce(wb.\"material\",'Без материала'), "
                         "coalesce(wb.\"diametr\",0) ")
            else:
                curs.execute("SELECT coalesce(wb.\"MATERIAL\",'Без материала') AS mat,coalesce(wb.\"DIAMETR\",0) AS diametr,count(*) AS cnt, "
                         "sum(wb.\"LEN\") as lsum FROM \"WATER_BRANCH\" wb WHERE (wb.reg='"+self.ui.regionCBox.currentText().encode('utf-8')+"' or ''='"+
                         self.ui.regionCBox.currentText().encode('utf-8')+"')  GROUP BY coalesce(wb.\"MATERIAL\",'Без материала'), "
                         "coalesce(wb.\"DIAMETR\",0) ORDER BY coalesce(wb.\"MATERIAL\",'Без материала'), "
                         "coalesce(wb.\"DIAMETR\",0) ")
            self.rdatas = curs.fetchall()
            self.ui.outDataEdit.append(u"=============ВОДОПРОВОД МАТЕРИАЛ, ДИАМЕТР ТОЧН, УЧАСТКОВ, СУММАРН ДЛИНА")
            self.html_code = self.html_code + u"<h4>ВОДОПРОВОД МАТЕРИАЛ, ДИАМЕТР ТОЧН, УЧАСТКОВ, СУММАРН ДЛИНА</h4>"
            self.html_code = self.html_code + u"<table border=\"1\"><tr><td>Материал</td><td>Диаметр " \
                                              u"точн</td><td>Число участков</td><td>Суммарн длина</td></tr>"
            for rdata in self.rdatas:
                if not(rdata[0]==None):
                    self.html_code = self.html_code + u"<tr><td>"+rdata[0]+\
                                     u"</td><td>"+str(rdata[1])+\
                                     u"</td><td>"+str(rdata[2])+u"</td><td>"+str("%.2f" % rdata[3])+u"</td></tr>"
                    self.ui.outDataEdit.append(u"Материал-"+rdata[0]+u":диам="+str(rdata[1])+u",участков-"+str(rdata[2])+u",длина="+str(rdata[3]))
                else:
                    self.html_code = self.html_code + u"<tr><td>Без материала</td><td>"+str(rdata[1])+\
                                     u"</td><td>"+str(rdata[2])+u"</td><td>"+str(rdata[3])+u"</td></tr>"
                    self.ui.outDataEdit.append(u"Без материала:"+str(rdata[1])+u","+str(rdata[2])+u","+str("%.2f" % rdata[3]))
            self.html_code = self.html_code + u"</table>";
            curs2.execute("SELECT tns.well_mname, count(*) AS cnt, round(tns.well_diam) AS rdiam "
                         "FROM topo_nodes tns  WHERE (tns.np_name='"+self.ui.regionCBox.currentText()+"' or ''='"+
                         self.ui.regionCBox.currentText()+"')  GROUP BY tns.well_mname, round(tns.well_diam) "
                         "ORDER BY tns.well_mname, round(tns.well_diam)")
            self.rdatas = curs2.fetchall()
            self.ui.outDataEdit.append(u"=============КОЛОДЦЫ")
            self.html_code = self.html_code + u"<h4>КОЛОДЦЫ</h4>"
            self.html_code = self.html_code + u"<table border=\"1\"><tr><td>Материал</td><td>Диаметр " \
                                              u"округл</td><td>Число колодцев</td></tr>"
            for rdata in self.rdatas:
                if not(rdata[0]==None):
                    self.html_code = self.html_code + u"<tr><td>"+rdata[0]+\
                                     u"</td><td>"+str(rdata[2])+u"</td><td>"+str(rdata[1])+u"</td></tr>"
                    self.ui.outDataEdit.append(rdata[0]+u":"+str(rdata[1])+u","+str(rdata[2]))
                else:
                    self.html_code = self.html_code + u"<tr><td>Без материала"+\
                                     u"</td><td>"+str(rdata[2])+u"</td><td>"+str(rdata[1])+u"</td></tr>"
                    self.ui.outDataEdit.append(u"None:"+str(rdata[1])+u","+str(rdata[2]))
            self.html_code = self.html_code + u"</table>";
            curs2.execute("SELECT COUNT(*) FROM \"public\".\"TOPO_NODE_WATER\" tns WHERE (tns.\"NP_NAME\"='"+self.ui.regionCBox.currentText()+"' or ''='"+self.ui.regionCBox.currentText()+"')" )
            self.brdatas = curs2.fetchall()
            for breg in self.brdatas:
                self.html_code = self.html_code + u"<h4>Количество колодцев водопровода: "+str(breg[0])+ u"</h4>";
                self.ui.outDataEdit.append(u"Количество колодцев водопровода: "+str(breg[0]))			
            curs2.execute("SELECT COUNT(*) FROM \"public\".\"TOPO_NODE_KANAL\" tns  WHERE (tns.\"NP_NAME\"='"+self.ui.regionCBox.currentText()+"' or ''='"+self.ui.regionCBox.currentText()+"')")
            self.brdatas = curs2.fetchall()
            for breg in self.brdatas:
                self.html_code = self.html_code + u"<h4>Количество колодцев канализации: "+str(breg[0])+ u"</h4>";
                self.ui.outDataEdit.append(u"Количество колодцев канализации: "+str(breg[0]))            
            curs2.execute("SELECT public.injoutpipes_count('"+self.ui.regionCBox.currentText().encode('utf-8')+"')")
            self.brdatas = curs2.fetchall()
            for breg in self.brdatas:
                self.html_code = self.html_code + u"<h4>Количество абонентских присоединений: "+str(breg[0])+ u"</h4>";
                self.ui.outDataEdit.append(u"Количество абонентских присоединений: "+str(breg[0]))
            curs2.execute("SELECT public.fhydr_count('"+self.ui.regionCBox.currentText().encode('utf-8')+"')")
            self.brdatas = curs2.fetchall()
            for breg in self.brdatas:
                self.html_code = self.html_code + u"<h4>Количество гидрантов: "+str(breg[0])+ u"</h4>";
                self.ui.outDataEdit.append(u"Количество гидрантов: "+str(breg[0]))
            curs2.execute("SELECT public.latchbytype_count('"+self.ui.regionCBox.currentText().encode('utf-8')+"','VANT')")
            self.brdatas = curs2.fetchall()
            for breg in self.brdatas:
                self.html_code = self.html_code + u"<h4>Количество вантузов: "+str(breg[0])+ u"</h4>";
                self.ui.outDataEdit.append(u"Количество вантузов: "+str(breg[0]))
            curs.execute("SELECT lv.\"mt_name\" AS mat, (lv.\"diametr\"/100)*100 AS diametr,count(*) AS cnt, "
                         "0 as lsum FROM \"latches_view\" lv WHERE (lv.npname='"+self.ui.regionCBox.currentText()+"' or ''='"+
                         self.ui.regionCBox.currentText()+"') GROUP BY lv.\"mt_name\", "
                         "(lv.\"diametr\"/100) ORDER BY lv.\"mt_name\", diametr ")
            self.rdatas = curs.fetchall()
            self.ui.outDataEdit.append(u"=============ЗАПОРНАЯ АРМАТУРА МАТЕРИАЛ, ДИАМЕТР УСЛОВН % 100, УЧАСТКОВ, СУММАРН ДЛИНА")
            self.html_code = self.html_code + u"<h4>ЗАПОРНАЯ АРМАТУРА МАТЕРИАЛ, ДИАМЕТР УСЛОВН % 100, КОЛИЧЕСТВО</h4>"
            self.html_code = self.html_code + u"<table border=\"1\"><tr><td>Материал</td><td>Диаметр " \
                                              u"</td><td>Количество</td></tr>"
            for rdata in self.rdatas:
                if not(rdata[0]==None):
                    self.html_code = self.html_code + u"<tr><td>"+rdata[0]+\
                                     u"</td><td>"+str(rdata[1])+u"-"+str(rdata[1]+99)+u"</td><td>"+str(rdata[2])+u"</td></tr>"
                    self.ui.outDataEdit.append(u"Материал-"+rdata[0]+u":диам="+str(rdata[1])+u"-"+str(rdata[1]+99)+u",участков-"+str(rdata[2])+u",длина="+str(rdata[3]))
                else:
                    self.html_code = self.html_code + u"<tr><td>Без материала"+\
                                     u"</td><td>"+str(rdata[1])+u"-"+str(rdata[1]+99)+u"</td><td>"+str(rdata[2])+u"</td></tr>"
                    self.ui.outDataEdit.append(u"Без материала:"+str(rdata[1])+u","+str(rdata[2])+u","+str(rdata[3]))
            self.html_code = self.html_code + u"</table>";
            ##############################################
            ##############################################
            layers = self.iface.legendInterface().layers()
            self.html_code = self.html_code + u"<h4>Протеженности линейных слоев</h4>"
            self.html_code = self.html_code + u"<table border=\"1\"><tr><td>Слой</td><td>Длина</td></tr>"
            for layer in layers:
                layerType = layer.type()
                if layerType == QgsMapLayer.VectorLayer:
                    if layer.geometryType()==QGis.Line:
                        f = QgsFeature()
                        feat_iterator = layer.getFeatures()
                        llen=0
                        ln=layer.name()
                        #self.ui.outDataEdit.append(u"СЛОЙ:"+ln)
                        while feat_iterator.nextFeature(f):
                            if ((layer.name() == u"Участки водопровода") and (self.ui.regionCBox.currentText()==u"" or f.attribute("reg")==self.ui.regionCBox.currentText())):
                                llen=llen+f.geometry().length()
                            if ((layer.name() == u"Участки канализации") and (self.ui.regionCBox.currentText()==u"" or f.attribute("reg")==self.ui.regionCBox.currentText())):
                                llen=llen+f.geometry().length()
                            if ((layer.name() == u"WATER_BRANCH") and (self.ui.regionCBox.currentText()==u"" or f.attribute("REG")==self.ui.regionCBox.currentText())):
                                llen=llen+f.geometry().length()	
                            if ((layer.name() == u"TOPO_WATER_BRANCH") and (self.ui.regionCBox.currentText()==u"" or f.attribute("REG")==self.ui.regionCBox.currentText())):
                                llen=llen+f.geometry().length()	
                            elif not (layer.name() == u"Участки водопровода"):
                                llen=llen+0
                        #self.ui.outDataEdit.append(u"ДЛИНА СЕТЕЙ В СЛОЕ:"+str(llen))
                        if llen>0:
                            self.html_code = self.html_code + u"<tr><td>"+ln+u"</td><td>"+str("%.2f" % llen)+u"</td></tr>"
            self.html_code = self.html_code + u"</table>";

            clayer = self.iface.activeLayer()
            if clayer.geometryType()==QGis.Line:
                #f = QgsFeature()
                feat_iterator = clayer.selectedFeatures()
                llen=0
                ln=clayer.name()
                #self.ui.outDataEdit.append(u"ТЕКУЩИЙ СЛОЙ:"+ln)
                #while feat_iterator.nextFeature(f):
                for ft in feat_iterator:
                    llen=llen+ft.geometry().length()
                #self.ui.outDataEdit.append(u"ДЛИНА ВЫДЕЛЕННЫХ СЕТЕЙ В ТЕКУЩЕМ СЛОЕ:"+str(llen))
                self.html_code = self.html_code + u"<h4>ДЛИНА ВЫДЕЛЕННЫХ СЕТЕЙ В ТЕКУЩЕМ СЛОЕ "+ln+u" = "+str("%.2f" % llen)+u"</h4>"

            ##############################################
            ##############################################
            self.html_code = self.html_code + u"""</body>
                </html>
                """
            self.repBrowse.setHtml(self.html_code)
            #self.webNodeSchema.setHtml(self.html_code.decode('utf-8'))
        elif report_type==3:
            layers = self.iface.legendInterface().layers()
            for layer in layers:
                layerType = layer.type()
                if layerType == QgsMapLayer.VectorLayer:
                    if layer.geometryType()==QGis.Line:
                        f = QgsFeature()
                        feat_iterator = layer.getFeatures()
                        llen=0
                        ln=layer.name()
                        self.ui.outDataEdit.append(u"СЛОЙ:"+ln)
                        while feat_iterator.nextFeature(f):
                            llen=llen+f.geometry().length()
                        self.ui.outDataEdit.append(u"ДЛИНА СЕТЕЙ В СЛОЕ:"+str(llen))

            clayer = self.iface.activeLayer()
            if clayer.geometryType()==QGis.Line:
                #f = QgsFeature()
                feat_iterator = clayer.selectedFeatures()
                llen=0
                ln=clayer.name()
                self.ui.outDataEdit.append(u"ТЕКУЩИЙ СЛОЙ:"+ln)
                #while feat_iterator.nextFeature(f):
                for ft in feat_iterator:
                    llen=llen+ft.geometry().length()
                self.ui.outDataEdit.append(u"ДЛИНА ВЫДЕЛЕННЫХ СЕТЕЙ В ТЕКУЩЕМ СЛОЕ:"+str(llen))
        elif report_type==4:
            self.html_code = u"""
                <!DOCTYPE html>
                <html lang="en">
                    <head>
                    <meta charset="utf-8">
                    <title>Отчет по топосъемке обектов</title></head><body><h1>Отчет по колодцам с группировкой 1</h1>""";
            #self.html_code = self.html_code + self.rep_area+ u""
            ##############################################
            ##############################################
            curs2.execute("SELECT coalesce(tnw.\"NP_NAME\",'Без нас пункта'), coalesce(tnw.\"STREET_NAME\",'Без назв улицы'), COUNT(*) FROM \"public\".\"TOPO_NODE_WATER\" tnw GROUP BY coalesce(tnw.\"NP_NAME\",'Без нас пункта'), coalesce(tnw.\"STREET_NAME\",'Без назв улицы') ORDER BY coalesce(tnw.\"NP_NAME\",'Без нас пункта'), coalesce(tnw.\"STREET_NAME\",'Без назв улицы') ")
            self.brdatas = curs2.fetchall()
            self.html_code = self.html_code + u"<h4>Группировочная таблица 1: </h4><table border=\"1\">";
            self.html_code = self.html_code + u"<tr><td>Нас пункт</td><td>Улица</td><td>Количество</td><tr>"	
            for breg in self.brdatas:
                self.html_code = self.html_code + u"<tr><td>"+breg[0]+u"</td><td>"+breg[1]+u"</td><td>"+str(breg[2])+u"</td><tr>"	
            self.html_code = self.html_code + u"<table>";
			
            curs2.execute("SELECT coalesce(tnw.\"NP_NAME\",'Без нас пункта'), coalesce(tnw.\"STREET_NAME\",'Без назв улицы'), coalesce(tnw.\"HS_NUM\",0) FROM \"public\".\"TOPO_NODE_WATER\" tnw ORDER BY coalesce(tnw.\"NP_NAME\",'Без нас пункта'), coalesce(tnw.\"STREET_NAME\",'Без назв улицы'), coalesce(tnw.\"HS_NUM\",0)")
            self.brdatas = curs2.fetchall()
            self.html_code = self.html_code + u"<h4>Таблица 2 с простой сортировкой: </h4><table border=\"1\">";
            self.html_code = self.html_code + u"<tr><td>Нас пункт</td><td>Улица</td><td>Номер дома</td><tr>"
            for breg in self.brdatas:
                self.html_code = self.html_code + u"<tr><td>"+breg[0]+u"</td><td>"+breg[1]+u"</td><td>"+str(breg[2])+u"</td><tr>"	
            self.html_code = self.html_code + u"<table>";				
            ##############################################
            ##############################################
            self.html_code = self.html_code + u"""</body>
                </html>
                """
            self.repBrowse.setHtml(self.html_code)
        else:
            curs.execute("SELECT * FROM public.branch_regs")
            self.brdatas = curs.fetchall()
            for breg in self.brdatas:
                self.ui.outDataEdit.append(breg[0])
                self.ui.regionCBox.addItem(breg[0])
            curs2.execute("SELECT * FROM public.tnodes_npnames")
            self.brdatas = curs2.fetchall()
            for breg in self.brdatas:
                self.ui.outDataEdit.append(breg[0])
                self.ui.regionCBox.addItem(breg[0])
        curs.close()
        conn.close()

        return

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

    def setDlg(self):
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

        self.createRelationalTables()

        self.getDatas(-1,[])

    def accept(self):
            #QtGui.QMessageBox.information( self, "Information", u"Ошибка (запись не отражена в БД)! id="+str(self.curr_nid)  )
        return QtGui.QDialog.accept(self)

    def createRelationalTables(self):
        query = QtSql.QSqlQuery()
        #query.exec_("create table public.\"injoutpipes\"(id SERIAL, description varchar(255), material INTEGER DEFAULT 0 NOT NULL, toponode INTEGER, diametr INTEGER DEFAULT 0 NOT NULL, injcode INTEGER DEFAULT 0 NOT NULL, injorder INTEGER DEFAULT 0 NOT NULL, injdeep INTEGER DEFAULT 0 NOT NULL, type VARCHAR(20) DEFAULT 'WATER'::character varying NOT NULL, CONSTRAINT \"injoutpipes_pkey\" PRIMARY KEY(id))")

        query.exec_("""CREATE OR REPLACE VIEW public.branch_regs (
    reg)
AS
SELECT DISTINCT ub."REG" AS reg
FROM (
    SELECT wb."REG"
    FROM "WATER_BRANCH" wb
    UNION
    SELECT kb."REG"
    FROM "KANAL_BRANCH" kb
    ) ub;""")
        query.exec_("""CREATE OR REPLACE VIEW public.topo_nodes (
    ttype,
    adr_liter,
    comments,
    conn_ih,
    cover_mname,
    date_stexp,
    exp_percent,
    firehydr,
    h_value,
    hs_num,
    invert_h,
    node_num,
    np_name,
    pipe_diam,
    pipe_mname,
    stat_desc,
    street_name,
    topo_code,
    topo_grp_code,
    topofile,
    well_diam,
    well_fname,
    well_mname,
    x_coord,
    y_coord)
AS
SELECT un.ttype,
    un."ADR_LITER" AS adr_liter,
    un."COMMENTS" AS comments,
    un."CONN_IH" AS conn_ih,
    un."COVER_MNAME" AS cover_mname,
    un."DATE_STEXP" AS date_stexp,
    un."EXP_PERCENT" AS exp_percent,
    un."FIREHYDR" AS firehydr,
    un."H_value" AS h_value,
    un."HS_NUM" AS hs_num,
    un."INVERT_H" AS invert_h,
    un."NODE_NUM" AS node_num,
    un."NP_NAME" AS np_name,
    un."PIPE_DIAM" AS pipe_diam,
    un."PIPE_MNAME" AS pipe_mname,
    un."STAT_DESC" AS stat_desc,
    un."STREET_NAME" AS street_name,
    un.topo_code,
    un."TOPO_GRP_CODE" AS topo_grp_code,
    un."TOPOFILE" AS topofile,
    un."WELL_DIAM" AS well_diam,
    un."WELL_FNAME" AS well_fname,
    un."WELL_MNAME" AS well_mname,
    un."X_coord" AS x_coord,
    un."Y_coord" AS y_coord
FROM (
    SELECT 'WATER'::text AS ttype,
            tnw."ADR_LITER",
            tnw."COMMENTS",
            tnw."CONN_IH",
            tnw."COVER_MNAME",
            tnw."DATE_STEXP",
            tnw."EXP_PERCENT",
            tnw."FIREHYDR",
            tnw."H_value",
            tnw."HS_NUM",
            tnw."INVERT_H",
            tnw."NODE_NUM",
            tnw."NP_NAME",
            tnw."PIPE_DIAM",
            tnw."PIPE_MNAME",
            tnw."STAT_DESC",
            tnw."STREET_NAME",
            tnw.topo_code,
            tnw."TOPO_GRP_CODE",
            tnw."TOPOFILE",
            tnw."WELL_DIAM",
            tnw."WELL_FNAME",
            tnw."WELL_MNAME",
            tnw."X_coord",
            tnw."Y_coord"
    FROM "TOPO_NODE_WATER" tnw
    UNION
    SELECT 'KANAL'::text AS ttype,
            tnw."ADR_LITER",
            tnw."COMMENTS",
            tnw."CONN_IH",
            tnw."COVER_MNAME",
            tnw."DATE_STEXP",
            tnw."EXP_PERCENT",
            tnw."FIREHYDR",
            tnw."H_value",
            tnw."HS_NUM",
            tnw."INVERT_H",
            tnw."NODE_NUM",
            tnw."NP_NAME",
            tnw."PIPE_DIAM",
            tnw."PIPE_MNAME",
            tnw."STAT_DESC",
            tnw."STREET_NAME",
            tnw.topo_code,
            tnw."TOPO_GRP_CODE",
            tnw."TOPOFILE",
            tnw."WELL_DIAM",
            tnw."WELL_FNAME",
            tnw."WELL_MNAME",
            tnw."X_coord",
            tnw."Y_coord"
    FROM "TOPO_NODE_KANAL" tnw
    ) un;""")
        query.exec_("""CREATE OR REPLACE VIEW public.tnodes_npnames (
    np_name)
AS
SELECT DISTINCT ub."NP_NAME" AS np_name
FROM (
    SELECT wb."NP_NAME"
    FROM "TOPO_NODE_KANAL" wb
    UNION
    SELECT kb."NP_NAME"
    FROM "TOPO_NODE_WATER" kb
    ) ub;""")
        query.exec_("""CREATE OR REPLACE FUNCTION public.fhydr_count (
  reg varchar = '==='::character varying
)
RETURNS integer AS
$body$
DECLARE
  ufcnt INTEGER;
BEGIN
  SELECT SUM(un.fcnt) INTO ufcnt FROM
(SELECT count(*) as fcnt
FROM "public"."TOPO_NODE_WATER" tnw
WHERE (tnw."FIREHYDR"='ДА') AND (tnw."NP_NAME"=reg or reg='')
UNION
SELECT count(*) as fcnt
FROM "public"."TOPO_NODE_KANAL" tnk
WHERE (tnk."FIREHYDR"='ДА') AND (tnk."NP_NAME"=reg or reg='')) un;
RETURN ufcnt;
EXCEPTION
WHEN others THEN
  RAISE NOTICE 'SQLSTATE: %', SQLSTATE;
  RAISE;
END;
$body$
LANGUAGE 'plpgsql'
VOLATILE
CALLED ON NULL INPUT
SECURITY INVOKER
COST 100;""")
        query.exec_("""CREATE OR REPLACE FUNCTION public.injoutpipes_count (
  reg varchar = '==='::character varying
)
RETURNS integer AS
$body$
DECLARE
  ufcnt INTEGER;
BEGIN
  SELECT SUM(un.fcnt) INTO ufcnt FROM
(SELECT count(*) as fcnt
FROM "public"."TOPO_NODE_WATER" tnw, injoutpipes iop
WHERE iop.toponode=tnw.gid and iop.type='WATER' AND (tnw."NP_NAME"=reg or reg='')
UNION
SELECT count(*) as fcnt
FROM "public"."TOPO_NODE_KANAL" tnk, injoutpipes iop
WHERE iop.toponode=tnk.gid and iop.type='KANAL' AND (tnk."NP_NAME"=reg or reg='')) un;
RETURN ufcnt;
EXCEPTION
WHEN others THEN
  RAISE NOTICE 'SQLSTATE: %', SQLSTATE;
  RAISE;
END;
$body$
LANGUAGE 'plpgsql'
VOLATILE
CALLED ON NULL INPUT
SECURITY INVOKER
COST 100;""")
        query.exec_("""CREATE OR REPLACE FUNCTION public.latchbytype_count (
  reg varchar = '==='::character varying,
  ltype varchar = '==='::character varying
)
RETURNS integer AS
$body$
DECLARE
  ufcnt INTEGER;
BEGIN
  SELECT SUM(un.fcnt) INTO ufcnt FROM
(SELECT count(*) as fcnt
FROM "public"."TOPO_NODE_WATER" tnw, latches lt
WHERE (lt.toponode=tnw.gid) AND (lt.type=ltype) AND (tnw."NP_NAME"=reg or reg='')
UNION
SELECT count(*) as fcnt
FROM "public"."TOPO_NODE_KANAL" tnk, latches lt
WHERE (lt.toponode=tnk.gid) AND (lt.type=ltype) AND (tnk."NP_NAME"=reg or reg='')) un;
RETURN ufcnt;
EXCEPTION
WHEN others THEN
  RAISE NOTICE 'SQLSTATE: %', SQLSTATE;
  RAISE;
END;
$body$
LANGUAGE 'plpgsql'
VOLATILE
CALLED ON NULL INPUT
SECURITY INVOKER
COST 100;""")
        query.exec_("""CREATE OR REPLACE VIEW public.latches_view (
    diametr,
    name,
    type,
    brtype,
    description,
    npname,
    mt_name)
AS
SELECT lt.diametr,
    lt.name,
    lt.type,
    lt.brtype,
    lt.description,
    tnw."NP_NAME" as npname,
    mt.name AS mt_name
FROM latches lt,
    material mt,
    "TOPO_NODE_WATER" tnw
WHERE lt.material = mt.id and lt.toponode=tnw.gid;""")
