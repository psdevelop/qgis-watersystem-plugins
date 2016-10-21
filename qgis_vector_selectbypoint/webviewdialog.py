# -*- coding: utf-8 -*-
"""
developer Poltarokov SP
"""
import psycopg2
import os
import subprocess
from PyQt4 import QtCore, QtGui, QtSql, QtWebKit
from dialogWebView import Ui_nodeSchemaDialog
from customWebView import customWebView
from nodeElementsDialog import nodeElementsDialog
from math import acos, degrees, sqrt
from customWebPage import customWebPage
# create the dialog for zoom to point


class webViewDialog(QtGui.QDialog, Ui_nodeSchemaDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.HOST = "localhost"
        self.DB_NAME = "postgis_21_sample"
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
        self.ui = Ui_nodeSchemaDialog()
        self.ui.setupUi(self)
        self.nodeElmsDlg = nodeElementsDialog(self)
        self.ui.addBKlapPButton.clicked.connect(self.addBKlap)
        self.ui.addCompPButton.clicked.connect(self.addComp)
        self.ui.addDRegPButton.clicked.connect(self.addDReg)
        self.ui.addVantPButton.clicked.connect(self.addVant)
        self.ui.addWCalcPButton.clicked.connect(self.addWCalc)
        self.ui.addAbInpWCButton.clicked.connect(self.addAbInpWC)
        self.ui.addBranchButton.clicked.connect(self.addBranchElm)
        self.ui.elmTableButton.clicked.connect(self.showInjOutList)
        self.ui.showGensChBox.clicked.connect(self.clickSGenChBox)

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

    def setParentPlugin(self, parent_object):
        self.parent_plg=parent_object

    def showInjOutList(self):
        self.nodeElmsDlg.show()
        self.nodeElmsDlg.fillDictsData(self.cid, "LATCH", "WATER", 0)

    def eventChanged(self):
        self.pg = self.webNodeSchema.page().mainFrame()
        ediv = self.pg.findFirstElement("div[id=latch1]")
        #self.pg.fi
        attr = ediv.attribute("data-x")
        #print u"contents changed"
        #print attr
        #print ediv.attribute("data-x")
        #print ediv.attribute("data-y")
        if ediv.attribute("data-drag")==u'yes' or ediv.attribute("data-drag")==u'move':
            #print "data drag)))"
            ediv.setAttribute("data-drag","none")
            self.upd_latch = {"id":ediv.attribute("data-lid")}
            self.upd_latch['xc'] = self.toint(ediv.attribute("data-x"))
            self.upd_latch['yc'] = self.toint(ediv.attribute("data-y"))
            self.upd_latch['ang'] = self.tofloat(ediv.attribute("data-ang"))
            self.updateLatch(self.upd_latch)
            self.latches = []
            self.new_branches = []
            self.loadHTML()

    def contentsChanged(self):
        self.pg = self.webNodeSchema.page().mainFrame()
        ediv = self.pg.findFirstElement("div[id=latch1]")
        #self.pg.fi
        attr = ediv.attribute("data-x")
        #print u"contents changed"
        #print attr
        #if ediv.attribute("data-drag")=='yes':
        #    print "data drag)))"
        nediv = self.pg.findFirstElement("div[id=new_latch]")
        #self.pg.fi
        #print nediv.attribute("data-check")
        #print nediv.attribute("data-x")
        #print nediv.attribute("data-y")
        if nediv.attribute("data-check")==u"yes":
            nediv.setAttribute("data-check","no")
            self.new_br = {"toponode":nediv.attribute("data-toponode")}
            self.new_br['xc'] = self.toint(nediv.attribute("data-x"))
            self.new_br['yc'] = self.toint(nediv.attribute("data-y"))
            self.new_br['ang'] = self.tofloat(nediv.attribute("data-ang"))
            self.new_br['branch'] = self.toint(nediv.attribute("data-branch"))
            self.putNewNodeElm(self.new_br)
            #print u"check yes"
        else:
            self.nodeElmsDlg.show()
            self.nodeElmsDlg.fillDictsData(self.cid, "LATCH", "WATER", 0)

    def updateLatch(self, node_data):
        try:
            conn = psycopg2.connect(host=self.HOST,database=self.DB_NAME,user=self.DB_USER,password=self.DB_PASS)
        except ValueError:
            QtGui.QMessageBox.information( self, u"Запись бинарных данных в БД", u"Ошибка установления соединения с БД!" )
            return
        curs = conn.cursor()
        #query.exec_("(0 id SERIAL, 1 name varchar(255), 2 description varchar(255), 3 material INTEGER 0 NOT NULL,
            #4 toponode INTEGER,5 branch INTEGER,6 brord INTEGER NOT NULL,7 injid INTEGER,8 diametr INTEGER 0 NOT NULL,
            #9 xpos INTEGER 0 NOT NULL,10 ypos INTEGER DEFAULT 0 NOT NULL,11 inangle INTEGER 0 NOT NULL,
            #12  brtype VARCHAR(20) DEFAULT 'WATER',13 type VARCHAR(20),14 typeline VARCHAR(20),
            #15 colorline VARCHAR(20),16 widthline INTEGER
        curs.execute("UPDATE \"public\".\"latches\" SET xpos=%s, ypos=%s, inangle=%s WHERE id=%s",
                      ( str(node_data['xc']), str(node_data['yc']),
                        str(self.toint(node_data['ang'])), str(self.toint(node_data['id'])) ))
        conn.commit()
        curs.close()
        conn.close()
        #print (u"Задвижка изменена!"+("UPDATE \"public\".\"latches\" SET xpos=%s, ypos=%s, inangle=%s WHERE id=%s") %
        #              ( str(node_data['xc']), str(node_data['yc']),
        #                str(self.toint(node_data['ang'])), str(self.toint(node_data['id'])) ))
        return

    def reloadHTML(self):
        self.latches = []
        self.new_branches = []
        self.loadHTML()

    def clickSGenChBox(self):
        self.latches = []
        self.new_branches = []
        self.loadHTML()

    def addBKlap(self):
        self.addElmWType(u"REVCLAP")
        self.latches = []
        self.new_branches = []
        self.loadHTML()

    def addVant(self):
        self.addElmWType(u"VANT")
        self.latches = []
        self.new_branches = []
        self.loadHTML()

    def addComp(self):
        self.addElmWType(u"COMPENSAT")
        self.latches = []
        self.new_branches = []
        self.loadHTML()

    def addWCalc(self):
        self.addElmWType(u"WCALC")
        self.latches = []
        self.new_branches = []
        self.loadHTML()

    def addDReg(self):
        self.addElmWType(u"PRREGUL")
        self.latches = []
        self.new_branches = []
        self.loadHTML()
		
    def addBranchElm(self):
        self.addElmWType(u"BRANCHL")
        self.latches = []
        self.new_branches = []
        self.loadHTML()
		
    def addAbInpWC(self):
        self.addElmWType(u"ABINP")
        self.latches = []
        self.new_branches = []
        self.loadHTML()

    def addElmWType(self, etype):
        query = QtSql.QSqlQuery()
        query.exec_(u"insert into public.\"latches\"(name, description, material, toponode, diametr, type, brtype, brord, branch) "
                    u" values('НОВЫЙ ЭЛЕМЕНТ', 'no desc', 3, "+str(self.cid)+u", 0, '"+etype+u"','"+u"WATER"+u"',0,0)")

    def putNewNodeElm(self, node_data):
        try:
            conn = psycopg2.connect(host=self.HOST,database=self.DB_NAME,user=self.DB_USER,password=self.DB_PASS)
        except ValueError:
            QtGui.QMessageBox.information( self, u"Запись бинарных данных в БД", u"Ошибка установления соединения с БД!" )
            return
        curs = conn.cursor()
        #query.exec_("(0 id SERIAL, 1 name varchar(255), 2 description varchar(255), 3 material INTEGER 0 NOT NULL,
            #4 toponode INTEGER,5 branch INTEGER,6 brord INTEGER NOT NULL,7 injid INTEGER,8 diametr INTEGER 0 NOT NULL,
            #9 xpos INTEGER 0 NOT NULL,10 ypos INTEGER DEFAULT 0 NOT NULL,11 inangle INTEGER 0 NOT NULL,
            #12  brtype VARCHAR(20) DEFAULT 'WATER',13 type VARCHAR(20),14 typeline VARCHAR(20),
            #15 colorline VARCHAR(20),16 widthline INTEGER
        curs.execute("INSERT INTO \"public\".\"latches\" ( name, description, material, toponode, branch, brord, injid, diametr, xpos, ypos, inangle) "
                     "VALUES ( 'new latch', 'no desc', 3, %s, %s, 0, 0, 0, %s, %s, %s)",
                      ( str(self.cid), str(node_data['branch']), str(node_data['xc']), str(node_data['yc']), str(self.toint(node_data['ang'])) ))
        conn.commit()
        curs.close()
        conn.close()
        QtGui.QMessageBox.information( self, u"Запись данных в БД", u"Задвижка из предполагаемых проеобразована в реальную!" )
        return

    def getNodeDatas(self, toponode, lname):
        try:
            conn = psycopg2.connect(host=self.HOST,database=self.DB_NAME,user=self.DB_USER,password=self.DB_PASS)
        except ValueError:
            QtGui.QMessageBox.information( self, u"Получение данных колодца из БД", u"Ошибка установления соединения с БД!" )
            return
        curs = conn.cursor()
        curs.execute("SELECT lt.*, mt.name as mname FROM \"public\".\"latches\" lt LEFT OUTER JOIN \"public\".\"material\" mt ON lt.material=mt.id WHERE toponode=%s",
                     (str(toponode), ))
        self.latches = curs.fetchall()
        curs.close()
        conn.close()

        return

    def createRelationalTables(self):
        query = QtSql.QSqlQuery("", self.db)
        query.exec_("create table public.\"latches\"(id SERIAL, name varchar(255), description varchar(255), material INTEGER DEFAULT 0 NOT NULL, toponode INTEGER, branch INTEGER, brord INTEGER NOT NULL, injid INTEGER, diametr INTEGER DEFAULT 0 NOT NULL, xpos INTEGER DEFAULT 0 NOT NULL, ypos INTEGER DEFAULT 0 NOT NULL, inangle INTEGER DEFAULT 0 NOT NULL, brtype VARCHAR(20) DEFAULT 'WATER'::character varying NOT NULL, type VARCHAR(20) DEFAULT 'LATCH'::character varying NOT NULL, typeline VARCHAR(20) DEFAULT 'none'::character varying NOT NULL, colorline VARCHAR(20) DEFAULT 'fff'::character varying NOT NULL, widthline INTEGER DEFAULT -1 NOT NULL, CONSTRAINT \"latches_pkey\" PRIMARY KEY(id))")

        #query.exec_("create table public.\"material2\"(id SERIAL, name varchar(255), CONSTRAINT \"materials2_pkey\" PRIMARY KEY(id))")
        #query.exec_("insert into public.\"material\"(name) values('Асбестоцемент')")
        #query.exec_("insert into public.\"material\"(name) values('Чугун')")
        #query.exec_("insert into public.\"material\"(name) values('Бетон')")

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

    def fillData(self, closestFeatureId, lname, lines_dicts, closestFeature):
        self.db = QtSql.QSqlDatabase.addDatabase("QPSQL")
        self.db.setHostName(self.HOST)
        self.db.setDatabaseName(self.DB_NAME)
        self.db.setUserName(self.DB_USER)
        self.db.setPassword(self.DB_PASS)
        self.line_dicts = lines_dicts
        self.cid = closestFeatureId
        self.lname = lname
        self.cf = closestFeature

        if not self.db.open():
            QMessageBox.information( self.iface.mainWindow(), u"Ошибка работы с БД!", u"Неудачное соединение с БД!" )
            return

        self.createRelationalTables()

        self.setWindowTitle(u"Схема объекта (колодец). PolFunDev.(C) 2015")
        url = QtCore.QUrl("http://raphaeljs.com/animation.html")
        self.webNodeSchema = customWebView(self)
        self.webNodeSchema.setGeometry(QtCore.QRect(10, 10, 641, 441))
        self.webNodeSchema.setUrl(QtCore.QUrl(u"about:blank"))
        self.webNodeSchema.setObjectName(u"webNodeSchema")
        self.webNodeSchema.show()
        self.webNodeSchema.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)

        self.latches = []
        self.new_branches = []
        self.loadHTML()

    def loadHTML(self):
        self.getNodeDatas(self.cid, self.lname)
        self.div_html = ""
        for line_node in self.line_dicts:
            isNew = True
            for latch in self.latches:
                if latch[5]==line_node['nid'] and latch[6]==line_node['ord']:
                    isNew=False
            if isNew:
                self.new_branches.append(line_node)

        lcnt = 0;
        self.xcentr=300
        self.ycentr=210
        self.inj_len=200

        self.latches_html = ""
        #self.lcolorLineEdit.setItemText(0, _translate("nodeElementsDialog", "Белый", None))
        #self.lcolorLineEdit.setItemText(1, _translate("nodeElementsDialog", "Желтый", None))
        #self.lcolorLineEdit.setItemText(2, _translate("nodeElementsDialog", "Синий", None))
        #self.lcolorLineEdit.setItemText(3, _translate("nodeElementsDialog", "Зеленый", None))
        #self.lcolorLineEdit.setItemText(4, _translate("nodeElementsDialog", "Красный", None))
        #self.lcolorLineEdit.setItemText(5, _translate("nodeElementsDialog", "Оранжевый", None))

        #self.lstyleComboBox.setItemText(0, _translate("nodeElementsDialog", "Обычная", None))
        #self.lstyleComboBox.setItemText(1, _translate("nodeElementsDialog", "Пунктир", None))
        #self.lstyleComboBox.setItemText(2, _translate("nodeElementsDialog", "Двойной пунктир", None))
        #self.lstyleComboBox.setItemText(3, _translate("nodeElementsDialog", "Редкий пунктир", None))
        #self.lstyleComboBox.setItemText(4, _translate("nodeElementsDialog", "Точка-тире", None))
        #self.lstyleComboBox.setItemText(5, _translate("nodeElementsDialog", "Точка", None))
        #self.lstyleComboBox.setItemText(6, _translate("nodeElementsDialog", "Редкая точка", None))
        #self.lstyleComboBox.setItemText(7, _translate("nodeElementsDialog", "Две точки-тире", None))
        #self.lstyleComboBox.setItemText(8, _translate("nodeElementsDialog", "Два тире-точка", None))

        for latch in self.latches:
            lcnt = lcnt + 1
            linetype=""
            if latch[14]==u"Обычная":
                linetype=".attr(linetype1)"
            elif latch[14]==u"Пунктир":
                linetype=".attr(linetype2)"
            elif latch[14]==u"Двойной пунктир":
                linetype=".attr(linetype3)"
            elif latch[14]==u"Редкий пунктир":
                linetype=".attr(linetype4)"
            elif latch[14]==u"Точка-тире":
                linetype=".attr(linetype5)"
            elif latch[14]==u"Точка":
                linetype=".attr(linetype6)"
            elif latch[14]==u"Редкая точка":
                linetype=".attr(linetype7)"
            elif latch[14]==u"Две точки-тире":
                linetype=".attr(linetype8)"
            elif latch[14]==u"Два тире-точка":
                linetype=".attr(linetype9)"
            colortype=""
            if latch[15]==u"Белый":
                colortype=".attr(colortype1)"
            elif latch[15]==u"Желтый":
                colortype=".attr(colortype2)"
            elif latch[15]==u"Синий":
                colortype=".attr(colortype3)"
            elif latch[15]==u"Зеленый":
                colortype=".attr(colortype4)"
            elif latch[15]==u"Красный":
                colortype=".attr(colortype5)"
            elif latch[15]==u"Оранжевый":
                colortype=".attr(colortype6)"
            xcoeff=1
            ycoeff=1
            ltx=240+latch[9]
            lty=90+latch[10]
            a = ltx-self.xcentr
            b = lty-self.ycentr
            c=sqrt(a*a+b*b)
            #ang_ab = degrees( acos((c ** 2 - a ** 2 - b ** 2)/(-2 * a * b)) )
            try:
                ang_bc = degrees( acos((a ** 2 - b ** 2 - c ** 2)/(-2 * b * c)) )
            except:
                ang_bc = 0
            try:
                ang_ac = degrees( acos((b ** 2 - a ** 2 - c ** 2)/(-2 * a * c)) )
            except Exception:
                ang_ac = 0
            #if lty>0:
            #    ang_ac=ang_ac+90
            #else:
            #print "a="+str(a)+"|b="+str(b)
            #print "ang_ac="+str(ang_ac)+"|ang_bc="+str(ang_bc)
            if a<0 and b<0:
                ang_ac = ang_bc
            elif a>0 and b<0:
                ang_ac = 90 - ang_ac
            else:
                ang_ac = ang_ac + 90
            ltxt = ltx - 50
            try:
                ltl_coeff=210/sqrt((self.xcentr-ltx)*(self.xcentr-ltx)+(self.ycentr-lty)*(self.ycentr-lty))
            except Exception:
                ltl_coeff = 1
            #query.exec_("(0 id SERIAL, 1 name varchar(255), 2 description varchar(255), 3 material INTEGER 0 NOT NULL,
            #4 toponode INTEGER,5 branch INTEGER,6 brord INTEGER NOT NULL,7 injid INTEGER,8 diametr INTEGER 0 NOT NULL,
            #9 xpos INTEGER 0 NOT NULL,10 ypos INTEGER DEFAULT 0 NOT NULL,11 inangle INTEGER 0 NOT NULL,
            #12  brtype VARCHAR(20) DEFAULT 'WATER',13 type VARCHAR(20),14 typeline VARCHAR(20),
            #15 colorline VARCHAR(20),16 widthline INTEGER
            self.latches_html = self.latches_html+""" var cx"""+str(lcnt)+""" = 100,
                    cy"""+str(lcnt)+""" = 100; """
            if latch[13]==u"REVCLAP":
                self.latches_html = self.latches_html+"""var elplt"""+str(lcnt)+""" = r.set();
                var path_tangl1"""+str(lcnt)+""" = "M240,90 L270,70 270,110 Z";
                elplt"""+str(lcnt)+""".push(r.path(path_tangl1"""+str(lcnt)+""").attr(dashed));
                var path_tangl2"""+str(lcnt)+""" = "M240,90 L210,70 210,110 Z";
                elplt"""+str(lcnt)+""".push(r.path(path_tangl2"""+str(lcnt)+""").attr(filled));
                var l_coord = elplt"""+str(lcnt)+""".getBBox().x,
                    r_coord = elplt"""+str(lcnt)+""".getBBox().x2,
                    t_coord = elplt"""+str(lcnt)+""".getBBox().y,
                    b_coord = elplt"""+str(lcnt)+""".getBBox().y2;
                cx"""+str(lcnt)+""" = (l_coord + r_coord)/2;
                    cy"""+str(lcnt)+""" = (t_coord + b_coord)/2;
                """
            elif latch[13]==u"VANT":
                self.latches_html = self.latches_html+"""
                var elplt"""+str(lcnt)+""" = r.set();
                elplt"""+str(lcnt)+""".push(r.path("M200,50 l80,0").attr(dashed));
                elplt"""+str(lcnt)+""".push(r.path("M220,50 a60,60 0 0,0 50,0").attr(filled));
                elplt"""+str(lcnt)+""".push(r.path("M240,60 l0,30").attr(dashed));
                elplt"""+str(lcnt)+""".push(r.path("M230,90 l20,0").attr(dashed));
                """
            elif latch[13]==u"COMPENSAT":
                self.latches_html = self.latches_html+"""
                var elplt"""+str(lcnt)+""" = r.set();
                elplt"""+str(lcnt)+""".push(r.path("M230,50 l10,20 0,40 -10,20 -10,-20 0,-40 10,-20").attr(filled10));
                elplt"""+str(lcnt)+""".push(r.path("M250,50 l10,20 0,40 -10,20 -10,-20 0,-40 10,-20").attr(dashed));
                """
            elif latch[13]==u"WCALC":
                self.latches_html = self.latches_html+"""
                var elplt"""+str(lcnt)+""" = r.set();
                elplt"""+str(lcnt)+""".push(r.path("M200,100 L250,70 200,70 Z").attr(dashed));
                elplt"""+str(lcnt)+""".push(r.path("M200,100 L250,70 250,100 Z").attr(filled));
                """
            elif latch[13]==u"PRREGUL":
                self.latches_html = self.latches_html+"""
                var elplt"""+str(lcnt)+""" = r.set();
                elplt"""+str(lcnt)+""".push(r.path("M220,70 l40,40 -40,0 40-40 -40,0 20,0").attr(filled11)).push(r.path("M240,50 l0,80 40,0 0,-40 -40,0 Z").attr(dashed)); """
            elif latch[13]==u"BRANCHL":
                self.latches_html = self.latches_html+"""
                var pathlt"""+str(lcnt)+""" = "M220,70 l1,1 -1,0 1,-1 -1,0";
                var elplt"""+str(lcnt)+"""=r.path(pathlt"""+str(lcnt)+""");"""
            elif latch[13]==u"ABINP":
                self.latches_html = self.latches_html+"""
                var pathlt"""+str(lcnt)+""" = "M220,70 l40,40 -40,0 40-40 -40,0";
                var elplt"""+str(lcnt)+"""=r.path(pathlt"""+str(lcnt)+""").attr(dashed4);"""
            else:
                self.latches_html = self.latches_html+"""
                var pathlt"""+str(lcnt)+""" = "M220,70 l40,40 -40,0 40-40 -40,0";
                var elplt"""+str(lcnt)+"""=r.path(pathlt"""+str(lcnt)+""");"""
            #print "www===>>>"+str(ang_ac)
            if latch[13] in [u"VANT",u"PRREGUL"]:
                ang_ac=ang_ac+90
            name = latch[1] +u" ("+ latch[17]+u","+str(latch[8])+u")"
            #print name.decode('utf-8')
            #print name.encode('utf-8')
            self.latches_html = self.latches_html+"""
                r.text("""+str(ltxt)+""", """+str(lty)+""", '"""+name.encode('utf-8')+"""').attr({font: '9px Arial',fill: "none", stroke: "#fff", "stroke-dasharray": "-"});
                var pathtmpl"""+str(lcnt)+""" = "M"""+str(self.xcentr)+""","""+str(self.ycentr)+"""l"""+str((ltx-self.xcentr)*ltl_coeff)+""","""+str((lty-self.ycentr)*ltl_coeff)+""" Z";
                var elptmpl"""+str(lcnt)+"""=r.path(pathtmpl"""+str(lcnt)+""").attr(injatr);
                //r.path("M190,20 L"""+str(latch[9])+""","""+str(latch[10])+"""Z").attr(injatr);
                elplt"""+str(lcnt)+("" if (latch[13] in [u"WCALC",u"COMPENSAT",u"VANT",u"REVCLAP",u"PRREGUL",u"ABINP"]) else """.attr(dashed3)""")+colortype+linetype+""".transform("T"""+(str(latch[9]+0) if (latch[13] in [u"WCALC",u"COMPENSAT",u"VANT",u"REVCLAP"]) else str(latch[9]))+""","""+str(latch[10])+("""R"""+str(int(ang_ac+90)) if (latch[13] in [u"WCALC",u"COMPENSAT",u"VANT",u"REVCLAP",u"PRREGUL"]) else """r"""+str(int(ang_ac)))+( (""","""+str(int(ltx))+""","""+str(int(lty))) if (latch[13] in [u"WCALC",u"COMPENSAT",u"VANT",u"REVCLAP",u"PRREGUL"]) else "")+"""")."""+"""data("i", 4633).
                data("toponode", """+str(self.cid)+""").drag(omove, ostart, oup).click(function () { var output = "";
                    div = document.getElementById("latch1");
                    var attrs = div.attributes;
                    //var thisa = this.attributes;
	                div.setAttribute('data-x', this.data('data-x'));
	                div.setAttribute('data-y', this.data('data-y'));
	                div.setAttribute('data-ang', """+str(latch[11])+""");
	                div.setAttribute('data-branch', """+str(latch[5])+""");
	                div.setAttribute('data-lid', """+str(latch[0])+""");
	                div.setAttribute('data-i',this.data('i'));
	                div.setAttribute('data-toponode',this.data('toponode'));
	                for (var i = 0; i < attrs.length; i++) {
                        output = output+attrs[i].name + " = " + attrs[i].value;
                    }
                //div.innerHTML = output;
                }).data('data-x',"""+str(latch[9])+""").data('data-y',"""+str(latch[10])+""").data('data-lid',"""+str(latch[0])+""").data('data-ang',"""+str(latch[11])+""");
            """
            #self.div_html = self.div_html+"<div id=\"latch"+str(lcnt)+"\" data-lid=\""+str(latch[0])+\
            #                "\" data-name=\""+str(latch[1])+"\" data-desc=\""+str(latch[2])+"\" "+\
            #                " data-mat=\""+str(latch[3])+"\" data-tnd=\""+str(latch[4])+"\" "+\
            #                " data- />"

        self.new_br_html=""
        cnt=0;
        for branch in self.new_branches:
            cnt=cnt+1
            a= abs ( branch['x2']-branch['x1'] )
            b= abs ( branch['y2']-branch['y1'] )
            c=sqrt(a*a+b*b)
            if a>0 and b>0:
                ang_ab = degrees( acos((c ** 2 - a ** 2 - b ** 2)/(-2 * a * b)) )
            else:
                ang_ab = 0
            if c>0 and b>0:
                ang_bc = degrees( acos((a ** 2 - b ** 2 - c ** 2)/(-2 * b * c)) )
            else:
                ang_bc = 0
            if a>0 and c>0:
                ang_ac = degrees( acos((b ** 2 - a ** 2 - c ** 2)/(-2 * a * c)) )
            else:
                ang_ac = 0
            #print u"+"+str(ang_bc)
            a= branch['x2']-branch['x1']
            b= branch['y2']-branch['y1']
            tx=50
            ty=100
            xcoeff=1
            ycoeff=1
            if a>0 and b>0:
                tx=tx+50
                ty=ty+50
            if a<0 and b<0:
                tx=tx-50
                ty=ty-50
            if a>0 and b<0:
                tx=tx+50
                ty=ty-50
            if a<0 and b>0:
                tx=tx-50
                ty=ty+50
            ltx=240+tx;
            lty=90+ty;
            ptx = 220+tx;
            pty = 70+ty;
            if self.xcentr>ltx: xcoeff=-1
            if self.ycentr>lty: ycoeff=-1
            ltl_coeff=210/sqrt((self.xcentr-ltx)*(self.xcentr-ltx)+(self.ycentr-lty)*(self.ycentr-lty))
            self.new_br_html = self.new_br_html+"""
                var pathnb"""+str(cnt)+""" = "M"""+str(ptx)+""","""+str(pty)+""" l40,40 -40,0 40-40 -40,0";
                var pathtmp"""+str(cnt)+""" = "M"""+str(self.xcentr)+""","""+str(self.ycentr)+"""l"""+str((ltx-self.xcentr)*ltl_coeff)+""","""+str((lty-self.ycentr)*ltl_coeff)+""" Z";
                var elptmpb"""+str(cnt)+"""=r.path(pathtmp"""+str(cnt)+""").attr(injatr2);
                var elpnb"""+str(cnt)+"""=r.path(pathnb"""+str(cnt)+""").
                attr(dashed2).transform("r"""+str(ang_bc)+"""")."""+"""data("i", 4633).
                data("toponode", """+str(self.cid)+""").click(function () { var output = "";
                    div = document.getElementById("new_latch");
                    var attrs = div.attributes;
	                div.setAttribute('data-x', """+str(tx)+""");
	                div.setAttribute('data-y', """+str(ty)+""");
	                div.setAttribute('data-ang', """+str(ang_bc)+""");
	                div.setAttribute('data-branch', """+str(branch['nid'])+""");
	                div.setAttribute('data-check','yes');
	                div.setAttribute('data-i',this.data('i'));
	                div.setAttribute('data-toponode',this.data('toponode'));
	                for (var i = 0; i < attrs.length; i++) {
                        output = output+attrs[i].name + " = " + attrs[i].value;
                    }
                //div.innerHTML = output;
                });
            """

        #if not self.ui.showGensChBox.isChecked():
        #    self.new_br_html = ""
        self.html_code = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="utf-8">
        <title>Raphaël · Animation</title>
        <link rel="stylesheet" href=\""""+os.path.dirname(__file__)+"""/demo.css" media="screen">
        <link rel="stylesheet" href=\""""+os.path.dirname(__file__)+"""/demo-print.css" media="print">
        <style media="screen">
            #holder {
                height: 419px;
                margin: -205px 0 0 -305px;
                width: 619px;
            }
        </style>
        <script src=\""""+os.path.dirname(__file__)+"""/raphael.js"></script>

        <script>
            Raphael.fn.arrow = function (x, y) {
                return this.path(["M", x, y] + "m-10-10l20,0 0-6 10,16 -10,16 0-6 -20,0 0,6 -10-16 10-16z").attr({fill: "#fff", stroke: "none", "stroke-dasharray": "-", "fill-opacity": 0.2});
            };
            window.onload = function () {
                // var r = Raphael("holder", 619, 419),
                var r = Raphael("holder", 619, 419), //Raphael(0, 0, "100%", "100%"),
                    dashed = {fill: "none", stroke: "#fff", cursor: "move"},
                    dashed2 = {fill: "#0f0", stroke: "#fff", "stroke-dasharray": "- "},
                    dashed3 = {fill: "#00f", stroke: "#fff", cursor: "move"},
                    dashed4 = {fill: "#f00", stroke: "#fff", cursor: "move"},
                    filled = {fill: "#fff", stroke: "#fff", cursor: "move"},
                    filled10 = {fill: "#0ff", stroke: "#fff", cursor: "move"},
                    filled11 = {fill: "#f0f", stroke: "#fff", cursor: "move"},
                    colortype1 = {},
                    colortype2 = {fill: "#0ff", stroke: "#0ff"},
                    colortype3 = {fill: "#00f", stroke: "#00f"},
                    colortype4 = {fill: "#0f0", stroke: "#0f0"},
                    colortype5 = {fill: "#f00", stroke: "#f00"},
                    colortype6 = {fill: "#f00", stroke: "#f00"},
                    linetype1 = {},
                    linetype2 = {"stroke-dasharray": "-"},
                    linetype3 = {"stroke-dasharray": "-- "},
                    linetype4 = {"stroke-dasharray": " - "},
                    linetype5 = {"stroke-dasharray": ".-"},
                    linetype6 = {"stroke-dasharray": "."},
                    linetype7 = {"stroke-dasharray": ".  "},
                    linetype8 = {"stroke-dasharray": "..-"},
                    linetype9 = {"stroke-dasharray": "--."},
                    injatr = {fill: "#fff", stroke: "#fff"},
                    injatr2 = {fill: "#0f0", stroke: "#0f0", "stroke-dasharray": "--  "};
                    // start, move, and up are the drag functions

                    var ostart = function () {
                        this.odx = 0;
                        this.ody = 0;
                        this.animate({"fill-opacity": 0.2}, 500);
                    },
                    omove = function (dx, dy) {
                        this.translate(dx - this.odx, dy - this.ody);
                        this.data('data-x',this.data('data-x')+(dx - this.odx));
                        this.data('data-y',this.data('data-y')+(dy - this.ody));
                        this.odx = dx;
                        this.ody = dy;
                        var dv = document.getElementById("latch1");
                        dv.setAttribute('data-x', this.data('data-x'));
                        dv.setAttribute('data-y', this.data('data-y'));
                        dv.setAttribute('data-ang', this.data('data-ang'));
                        dv.setAttribute('data-lid', this.data('data-lid'));
                        dv.setAttribute('data-drag', 'move');
                        //var attrs = this.attributes;
                    },
                    oup = function () {
                        this.animate({"fill-opacity": 1}, 500);
                        var dv = document.getElementById("latch1");
                        dv.setAttribute('data-x', this.data('data-x'));
                        dv.setAttribute('data-y', this.data('data-y'));
                        dv.setAttribute('data-drag', 'yes');
                    };
                r.circle(300, 210, 170).attr(dashed);
                r.text(190, 190, "КОЛОДЕЦ """+self.cf.attribute(u"topo_code").encode('utf-8')+""", диам. """+str(self.cf.attribute(u"WELL_DIAM"))+""", """+self.cf.attribute(u"WELL_MNAME").encode('utf-8')+"""").attr({font: '10px Arial',
                        fill: "none", stroke: "#fff", "stroke-dasharray": "-", transform: "t100,0r360s3"});
				r.text(190, 240, " """+self.cf.attribute(u"NP_NAME").encode('utf-8')+""" """+self.cf.attribute(u"STREET_NAME").encode('utf-8')+""" ").attr({font: '10px Arial',
                        fill: "none", stroke: "#fff", "stroke-dasharray": "-", transform: "t100,0r360s3"});
                var hydr_set = r.set();
                var path_hydr = "M200,250 C170,250 170,210 200,210 L200,250";
                """+("hydr_set.push(r.path(path_hydr).attr(filled));" if self.cf.attribute("FIREHYDR")==u"ДА" else "")+"""
                var path_hydr2 = "M200,250 C230,250 230,210 200,210 L200,250";
                """+("hydr_set.push(r.path(path_hydr2).attr(dashed));" if self.cf.attribute("FIREHYDR")==u"ДА" else "")+"""
                hydr_set.transform("T100,-25,r0");
                """+self.new_br_html+"  "+self.latches_html+"""
            };
        </script>
    </head>
    <body> <div id="holder"></div>
        <p id="copy">Схема разработана<a href="http://psdevelop.ru/">==>psdevelop<==</a></p>
        <div id="latch1" data-x="100" data-y="100">СХЕМА """+self.cf.attribute(u"topo_code").encode('utf-8')+""" </div>
        <div id="new_latch" data-x="100" data-y="100" data-check="no">"""+self.cf.attribute(u"WELL_FNAME").encode('utf-8')+"""</div>
    </body>
</html>
        """

        #self.webNodeSchema.setHtml(self.html_code)
        self.webNodeSchema.setHtml(self.html_code.decode('utf-8'))
		#self.webNodeSchema.setHtml(self.html_code.encode('cp1251'))
		#self.webNodeSchema.setHtml(self.html_code)
        #self.webNodeSchema.setHtml(self.html_code.decode('cp1251').encode('cp1252'))
        #self.webNodeSchema.setHtml(self.html_code.decode('utf-8').encode('cp1252','ignore'))
		#self.webNodeSchema.setHtml(self.html_code).decode('utf-8').encode('iso-8859-1'))
        #self.webNodeSchema.setContent(self.html_code,u"text/html;charset=utf-8")
        #self.webNodeSchema.connect(self.webNodeSchema.page(),
        #                                 QtCore.SIGNAL("linkClicked (const QUrl&)"), self.linkClicked)
        #self.webNodeSchema.page().connect(self.webNodeSchema.page(),
        #                                 QtCore.SIGNAL("contentsChanged ()"), self.contentsChanged)

    def linkClicked(url):
        QtGui.QMessageBox.information( self, "Information", u"Click-click!!!))))" )
        #webbrowser.open(str(url.toString()))

    def accept(self):
        #self.page = self.ui.webViewNodeSchema.page().mainFrame()
        #doc = self.page.documentElement()
        #body = doc.firstChild().nextSibling()
        #print "["+body.firstChild().nextSibling().toPlainText()+"]"
        return QtGui.QDialog.accept(self)

    def fictive(self):
        b = """

  //r.text(460, 250, "Raphaël").attr({font: '30px "Helvetica Neue", Arial', fill: "#fff", stroke: "#fff", "stroke-width": 8, "stroke-linejoin": "round"});
  //r.text(460, 250, "Raphaël").attr({font: '30px "Helvetica Neue", Arial', fill: "#000"});
  //r.text(460, 290, "Click on arrows to see an animation").attr({font: '16px "Helvetica Neue", Arial', fill: "#fff"});
=====================================
@QWebView *ftwWebView = new QWebView();
ftwWebView->setHtml(element.toOuterXml());
QWebFrame *ftwFrame = ftwWebView->page()->mainFrame();
result = ftwFrame->evaluateJavaScript("document.getElementById('username').value = 'someusername';");
result = ftwFrame->evaluateJavaScript("document.getElementById('password').value = 'somepassword';");
result = ftwFrame->evaluateJavaScript("function include(destination) {
var e=window.document.createElement('script');
e.setAttribute('src',destination);
window.document.body.appendChild(e); }
include('http://somelink.com/somefile.js');");
result = ftwFrame->evaluateJavaScript("validate_form( document.forms[0], true );");
=====================================
var fileref = document.createElement("script");
fileref.setAttribute("type", "text/javascript");
fileref.setAttribute("src", filename);
=====================================
function include(destination)
{ var e=window.document.createElement('script');
e.setAttribute('src',destination);
window.document.body.appendChild(e); }
include('http://somelink.com/somefile.js');
=====================================
fileref.setAttribute(“type”, “text/javascript”);
ftwWebView->settings()->setAttribute(QWebSettings::LocalContentCanAccessRemoteUrls, true);
=====================================
bt.evaluateJavaScript('this.click()')
=====================================
view = new QWebView(this);
     view->load(QUrl("http://www.google.com/ncr"));
     connect(view, SIGNAL(loadFinished(bool)), SLOT(adjustLocation()));
     connect(view, SIGNAL(titleChanged(const QString&)), SLOT(adjustTitle()));
     connect(view, SIGNAL(loadProgress(int)), SLOT(setProgress(int)));
     connect(view, SIGNAL(loadFinished(bool)), SLOT(finishLoading(bool)));
     locationEdit = new QLineEdit(this);
     locationEdit->setSizePolicy(QSizePolicy::Expanding, locationEdit->sizePolicy().verticalPolicy());
     connect(locationEdit, SIGNAL(returnPressed()), SLOT(changeLocation()));
     QToolBar *toolBar = addToolBar(tr("Navigation"));
     toolBar->addAction(view->pageAction(QWebPage::Back));
     toolBar->addAction(view->pageAction(QWebPage::Forward));
     toolBar->addAction(view->pageAction(QWebPage::Reload));
     toolBar->addAction(view->pageAction(QWebPage::Stop));
     toolBar->addWidget(locationEdit);
     QMenu *effectMenu = menuBar()->addMenu(tr("&Effect"));
     effectMenu->addAction("Highlight all links", this, SLOT(highlightAllLinks()));
     QAction *rotateAction = new QAction(this);
     rotateAction->setIcon(style()->standardIcon(QStyle::SP_FileDialogDetailedView));
     rotateAction->setCheckable(true);
     rotateAction->setText(tr("Turn images upside down"));
     connect(rotateAction, SIGNAL(toggled(bool)), this, SLOT(rotateImages(bool)));
     effectMenu->addAction(rotateAction);
     setCentralWidget(view);
 }
 ================================
 void MainWindow::adjustLocation()
 {  locationEdit->setText(view->url().toString()); }
 void MainWindow::changeLocation()
 { QUrl url = QUrl(locationEdit->text());
     view->load(url);
     view->setFocus(); }
 void MainWindow::highlightAllLinks()
 { QString code = "$('a').each( function () { $(this).css('background-color', 'yellow') } )";
     view->page()->mainFrame()->evaluateJavaScript(code); }
 void MainWindow::rotateImages(bool toggle)
 { QString code = "$('img').each( function () { $(this).css('-webkit-transition', '-webkit-transform 2s') } )";
     view->page()->mainFrame()->evaluateJavaScript(code);
     if (toggle)
         code = "$('img').each( function () { $(this).css('-webkit-transform', 'rotate(180deg)') } )";
     else
         code = "$('img').each( function () { $(this).css('-webkit-transform', 'rotate(0deg)') } )";
     view->page()->mainFrame()->evaluateJavaScript(code); }
 void MainWindow::removeGifImages()
     QString code = "$('[src*=gif]').remove()";
     QString code = "$('iframe').remove()";
     QString code = "$('object').remove()";
     QString code = "$('embed').remove()";
     view->page()->mainFrame()->evaluateJavaScript(code);
        """