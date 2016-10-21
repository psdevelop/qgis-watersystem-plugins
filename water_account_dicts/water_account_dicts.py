# -*- coding: utf-8 -*-
"""
/***************************************************************************
 vector_selectbypoint
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from qgis.core import *
from qgis.gui import *
# Initialize Qt resources from file resources.py
import resources_rc
import math
import re
# Import the code for the dialog
#from lineMapTool import lineMapTool
#from lineMapPanTool import lineMapPanTool
from QgsMapToolSelectPolygon import QgsMapToolSelectPolygon;
from wataccdicts_dialog import waterAccountDictsDialog
from wataccoldstyle_dialog import waterAccOldStyleDialog
from hotkeys_dialog import hotKeysDialog
from viewmodes_dialog import viewModesDialog
from allnets_dialog import allNetsDialog
from searchObjDialog import searchObjectDialog
from reportGenerator import reportGenerator
from printRectangleSelection import PrintRectangleSelection
from setPrintFormPrmDialog import setPrintFormParamsDialog
import os.path


class water_account_dicts:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        
        # Reference map canvas
        self.canvas = self.iface.mapCanvas()
        
        # Emit QgsPoint after each click on canvas
        #self.clickTool = QgsMapToolEmitPoint(self.canvas)
        self.previousLayer = None
        self.index = None
        
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'water_account_dicts_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = waterAccountDictsDialog()
        self.viewModesDlg = viewModesDialog()
        self.allNetsDlg = allNetsDialog()
        self.oldStyleDockWidget = waterAccOldStyleDialog()
        self.searchObjDlg = searchObjectDialog()
        self.setPCanvParamsDlg = setPrintFormParamsDialog(self)
        self.oldStyleDockWidget.ui.pushButton.clicked.connect(self.zoomIn)
        self.oldStyleDockWidget.ui.pushButton_2.clicked.connect(self.zoomOut)
        self.oldStyleDockWidget.ui.pushButton_5.clicked.connect(self.zoomToSelected)
        self.oldStyleDockWidget.ui.pushButton_9.clicked.connect(self.runLineTool)
        self.oldStyleDockWidget.ui.pushButton_6.clicked.connect(self.showViewModesDlg)
        self.oldStyleDockWidget.ui.pushButton_7.clicked.connect(self.showAllNetDlg)
        self.oldStyleDockWidget.ui.pushButton_10.clicked.connect(self.showObjSearchDlg)
        self.oldStyleDockWidget.ui.pushButton_12.clicked.connect(self.showAdrSearchDlg)
        self.oldStyleDockWidget.ui.pushButton_15.clicked.connect(self.show2StrSearchDlg)
        self.oldStyleDockWidget.ui.pushButton_17.clicked.connect(self.showStreets)
        self.oldStyleDockWidget.ui.pushButton_18.clicked.connect(self.runAddrLabels)
        self.oldStyleDockWidget.ui.pushButton_19.clicked.connect(self.zoomFull)
        self.oldStyleDockWidget.ui.pushButton_20.clicked.connect(self.colorSelExp)
        self.oldStyleDockWidget.ui.pushButton_21.clicked.connect(self.showLabels)
        self.oldStyleDockWidget.ui.pushButton_22.clicked.connect(self.showLens)
        self.iface.addDockWidget( Qt.RightDockWidgetArea, self.oldStyleDockWidget )
        self.hotKeysDockWidget = hotKeysDialog()
        self.repGen = reportGenerator(self.iface)
        self.iface.addDockWidget( Qt.RightDockWidgetArea, self.hotKeysDockWidget )
        self.visStreet1 = False
        self.visStreet2 = False
        self.visLens1 = False
        self.visLens2 = False
        self.visLabels11 = False
        self.visLabels21 = False
        self.visLabels12 = False
        self.visLabels22 = False
        self.iface.projectRead.connect(self.initAliases)
        # Create the GUI
        #self.canvas.setMapTool( self.clickTool )

    def initAliases(self):
        layers = self.iface.legendInterface().layers()
        for layer in layers:
            layerType = layer.type()
            if layerType == QgsMapLayer.VectorLayer:
                if layer.name()==u'КАНАЛИЗАЦИЯ':
                    self.iface.setActiveLayer(layer)
                    fields = layer.dataProvider().fields()
                    idx=0
                    for field in fields:
                        #print "==="+field.name()
                        if field.name()==u"UCHASTOK":
                            layer.addAttributeAlias(idx,u"ыыыУЧАСТОК")
                        if field.name()==u"REG":
                            layer.addAttributeAlias(idx,u"РЕГИОН")
                        if field.name()==u"STREET":
                            layer.addAttributeAlias(idx,u"УЛИЦА")
                        if field.name()==u"VLADELEC":
                            layer.addAttributeAlias(idx,u"ВЛАДЕЛЕЦ")
                        if field.name()==u"INVN":
                            layer.addAttributeAlias(idx,u"ИНВЕНТ НОМЕР")
                        if field.name()==u"MATERIAL":
                            layer.addAttributeAlias(idx,u"МАТЕРИАЛ")
                        if field.name()==u"DIAMETR":
                            layer.addAttributeAlias(idx,u"ДИАМЕТР")
                        if field.name()==u"LEN":
                            layer.addAttributeAlias(idx,u"ДЛИНА ВВОДИМАЯ")
                        idx=idx+1
                if layer.name()==u'ВОДОПРОВОД':
                    self.iface.setActiveLayer(layer)
                    fields = layer.dataProvider().fields()
                    idx=0
                    for field in fields:
                        #print "==="+field.name()
                        if field.name()==u"UCHASTOK":
                            layer.addAttributeAlias(idx,u"УЧАСТОК")
                        if field.name()==u"REG":
                            layer.addAttributeAlias(idx,u"РЕГИОН")
                        if field.name()==u"STREET":
                            layer.addAttributeAlias(idx,u"УЛИЦА")
                        if field.name()==u"VLADELEC":
                            layer.addAttributeAlias(idx,u"ВЛАДЕЛЕЦ")
                        if field.name()==u"INVN":
                            layer.addAttributeAlias(idx,u"ИНВЕНТ НОМЕР")
                        if field.name()==u"MATERIAL":
                            layer.addAttributeAlias(idx,u"МАТЕРИАЛ")
                        if field.name()==u"DIAMETR":
                            layer.addAttributeAlias(idx,u"ДИАМЕТР")
                        if field.name()==u"LEN":
                            layer.addAttributeAlias(idx,u"ДЛИНА ВВОДИМАЯ")
                        idx=idx+1
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
                if layer.name()==u'TOPO_NODE_WATER' or layer.name()==u'TOPO_NODE_KANAL':
                    self.iface.setActiveLayer(layer)
                    fields = layer.dataProvider().fields()
                    idx=0
                    for field in fields:
                        fkeys = field_titles.keys()
                        if field.name() in fkeys:
                            layer.addAttributeAlias(idx,field_titles[field.name()])
                        idx=idx+1

    def show2StrSearchDlg(self):
        self.searchObjDlg.show()
        self.searchObjDlg.setDlg(u"2STREET")
        self.initAliases()

    def showAdrSearchDlg(self):
        self.searchObjDlg.show()
        self.searchObjDlg.setDlg(u"ADRES")

    def showObjSearchDlg(self):
        self.searchObjDlg.show()
        self.searchObjDlg.setDlg(u"OBJECT")

    def zoomFull(self):
        self.iface.actionZoomFullExtent().trigger()
        #self.iface.actionZoomActualSize().trigger()

    def zoomToSelected(self):
        self.iface.actionZoomToSelected().trigger()

    def showViewModesDlg(self):
        self.viewModesDlg.show()

    def showAllNetDlg(self):
        self.allNetsDlg.show()

    def zoomIn(self):
        #print "zoom in..."
        self.iface.actionZoomIn().trigger()
        #tmpActionList = self.iface.attributesToolBar().actions()
        #for action in tmpActionList:
        #    if isinstance(action, QWidgetAction):
        #        for action2 in action.defaultWidget().actions():
        #            if not isinstance(action2, QWidgetAction):
        #                print action2.text()
        #    else:
        #        print action.text()

    def zoomOut(self):
        self.iface.actionZoomOut().trigger()

    def initGui(self):
        # Create action that will start plugin configuration
        self.calc_line_action = None
        self.expess_select_action = None
        tmpActionList = self.iface.attributesToolBar().actions()
        for action in tmpActionList:
            if isinstance(action, QWidgetAction):
                for action2 in action.defaultWidget().actions():
                    if not isinstance(action2, QWidgetAction):
                        #print action2.text()
                        if action2.text()==u"Измерить линию":
                            self.calc_line_action = action2
                        if action2.text()==u"Выделить объекты удовлетворяющие условию":
                            self.expess_select_action = action
            else:
                #print action.text()
                if action.text()==u"Измерить линию":
                    self.calc_line_action = action
                if action.text()==u"Выделить объекты удовлетворяющие условию" or action.text()==u"Select By Expression...":
                    self.expess_select_action = action

        self.waview_menu = QMenu(u"ПРОСМОТР")
        #self.waview_menu.setHidden(True)
        #self.iface.mainWindow().menuBar().insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.waview_menu)

        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Все сети", self.iface.mainWindow())
        self.waview_menu.addAction(self.waview_action1)
        self.waview_action1.triggered.connect(self.showAllNetDlg)

        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Режимы просмотра", self.iface.mainWindow())
        self.waview_menu.addAction(self.waview_action1)
        self.waview_action1.triggered.connect(self.showViewModesDlg)

        self.waview_menu1 = QMenu(u"###???УЗЛЫ")
        self.waview_menu.addMenu(self.waview_menu1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Отметки и номера", self.iface.mainWindow())
        self.waview_menu1.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Номера", self.iface.mainWindow())
        self.waview_menu1.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Состояние", self.iface.mainWindow())
        self.waview_menu1.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Отметки", self.iface.mainWindow())
        self.waview_menu1.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Отметки всех сетей", self.iface.mainWindow())
        self.waview_menu1.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Поиск по номеру", self.iface.mainWindow())
        self.waview_menu1.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Продолжение поиска", self.iface.mainWindow())
        self.waview_menu1.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Деталировка узла...", self.iface.mainWindow())
        self.waview_menu1.addAction(self.waview_action1)

        self.waview_menu2 = QMenu(u"###???УЧАСТКИ")
        self.waview_menu.addMenu(self.waview_menu2)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Типы и длины", self.iface.mainWindow())
        self.waview_menu2.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Типы и длины всех сетей", self.iface.mainWindow())
        self.waview_menu2.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Типы", self.iface.mainWindow())
        self.waview_menu2.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Направления уклонов", self.iface.mainWindow())
        self.waview_menu2.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Задвижки", self.iface.mainWindow())
        self.waview_menu2.addAction(self.waview_action1)

        self.waview_menu3 = QMenu(u"###???ЗДАНИЯ")
        self.waview_menu.addMenu(self.waview_menu3)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Номера и состояния", self.iface.mainWindow())
        self.waview_menu3.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Полные адреса", self.iface.mainWindow())
        self.waview_menu3.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Адреса по экспликации КУ", self.iface.mainWindow())
        self.waview_menu3.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###Названия улиц", self.iface.mainWindow())
        self.waview_menu3.addAction(self.waview_action1)

        self.waview_menu4 = QMenu(u"???КОНТУРЫ")
        self.waview_menu.addMenu(self.waview_menu4)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Все контуры", self.iface.mainWindow())
        self.waview_menu4.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Контуры одного вида...", self.iface.mainWindow())
        self.waview_menu4.addAction(self.waview_action1)

        self.waview_menu5 = QMenu(u"ПОИСК")
        self.waview_menu.addMenu(self.waview_menu5)

        self.waview_menu6 = QMenu(u"???ОТКЛЮЧЕНИЯ")
        self.waview_menu.addMenu(self.waview_menu6)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Отключения", self.iface.mainWindow())
        self.waview_menu6.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Параметры отключений", self.iface.mainWindow())
        self.waview_menu6.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Протокол последнего отключения", self.iface.mainWindow())
        self.waview_menu6.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Проверка связности", self.iface.mainWindow())
        self.waview_menu6.addAction(self.waview_action1)

        self.waview_menu7 = QMenu(u"???ПРОЧЕЕ")
        self.waview_menu.addMenu(self.waview_menu7)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Информация", self.iface.mainWindow())
        self.waview_menu7.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???План-заставка", self.iface.mainWindow())
        self.waview_menu7.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Весь план", self.iface.mainWindow())
        self.waview_menu7.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Подложка", self.iface.mainWindow())
        self.waview_menu7.addAction(self.waview_action1)

        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###ПЕРЕТАЩИТЬ", self.iface.mainWindow())
        self.waview_menu.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???НАСТРОЙКИ...", self.iface.mainWindow())
        self.waview_menu.addAction(self.waview_action1)

        self.wadata_menu = QMenu(u"ДАННЫЕ")
        #self.iface.mainWindow().menuBar().insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.wadata_menu)

        self.waview_menu21 = QMenu(u"ТОПОГРАФИЯ")
        self.wadata_menu.addMenu(self.waview_menu21)
        self.waview_menu211 = QMenu(u"###???УЗЛЫ")
        self.waview_menu21.addMenu(self.waview_menu211)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###Ввод узлов", self.iface.mainWindow())
        self.waview_menu211.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###Удаление узлов", self.iface.mainWindow())
        self.waview_menu211.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###Корректировка узлов", self.iface.mainWindow())
        self.waview_menu211.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Привязка узла", self.iface.mainWindow())
        self.waview_menu211.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Адрес узла", self.iface.mainWindow())
        self.waview_menu211.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Деталировка узла", self.iface.mainWindow())
        self.waview_menu211.addAction(self.waview_action1)
        self.waview_menu212 = QMenu(u"###???УЧАСТКИ")
        self.waview_menu21.addMenu(self.waview_menu212)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###Ввод участков", self.iface.mainWindow())
        self.waview_menu212.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###Удаление участков", self.iface.mainWindow())
        self.waview_menu212.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###Корректировка участков", self.iface.mainWindow())
        self.waview_menu212.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Отметка трубы", self.iface.mainWindow())
        self.waview_menu212.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Владельцы сетей", self.iface.mainWindow())
        self.waview_menu212.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Год прокладки", self.iface.mainWindow())
        self.waview_menu212.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Задвижки", self.iface.mainWindow())
        self.waview_menu212.addAction(self.waview_action1)
        self.waview_menu213 = QMenu(u"###???КОНТУРЫ И ТЕРРИТОРИИ")
        self.waview_menu21.addMenu(self.waview_menu213)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Указание угодий", self.iface.mainWindow())
        self.waview_menu213.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Очистка контура", self.iface.mainWindow())
        self.waview_menu213.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Построение обременений", self.iface.mainWindow())
        self.waview_menu213.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Сечение контура", self.iface.mainWindow())
        self.waview_menu213.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Редактирование полигона", self.iface.mainWindow())
        self.waview_menu213.addAction(self.waview_action1)

        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Ввод трассы", self.iface.mainWindow())
        self.waview_menu21.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Посадка узла на участок", self.iface.mainWindow())
        self.waview_menu21.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Установка геодезической базы", self.iface.mainWindow())
        self.waview_menu21.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Режимы ввода данных", self.iface.mainWindow())
        self.waview_menu21.addAction(self.waview_action1)

        self.waview_menu214 = QMenu(u"###???ДОПОЛНИТЕЛЬНО...")
        self.waview_menu21.addMenu(self.waview_menu214)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Импорт данных", self.iface.mainWindow())
        self.waview_menu214.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Экспорт данных", self.iface.mainWindow())
        self.waview_menu214.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Передача в другую сеть", self.iface.mainWindow())
        self.waview_menu214.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Удаление области данных", self.iface.mainWindow())
        self.waview_menu214.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Обратная задача", self.iface.mainWindow())
        self.waview_menu214.addAction(self.waview_action1)

        self.waview_menu22 = QMenu(u"###???ЗДАНИЯ")
        self.wadata_menu.addMenu(self.waview_menu22)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###Ввод домов", self.iface.mainWindow())
        self.waview_menu22.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Ввод объектов", self.iface.mainWindow())
        self.waview_menu22.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###Удаление зданий", self.iface.mainWindow())
        self.waview_menu22.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Удаление названия объекта", self.iface.mainWindow())
        self.waview_menu22.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Второй адрес", self.iface.mainWindow())
        self.waview_menu22.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Переименование зданий", self.iface.mainWindow())
        self.waview_menu22.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Изменение информации по зданию", self.iface.mainWindow())
        self.waview_menu22.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###???Передвижение углов здания", self.iface.mainWindow())
        self.waview_menu22.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Формирование здания из контура", self.iface.mainWindow())
        self.waview_menu22.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Центральная точка здания", self.iface.mainWindow())
        self.waview_menu22.addAction(self.waview_action1)

        self.waview_menu23 = QMenu(u"???Картинки")
        self.wadata_menu.addMenu(self.waview_menu23)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Выбор режима", self.iface.mainWindow())
        self.waview_menu23.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Рисование", self.iface.mainWindow())
        self.waview_menu23.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Стирание", self.iface.mainWindow())
        self.waview_menu23.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Стирание в окне", self.iface.mainWindow())
        self.waview_menu23.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???Смена атрибутов", self.iface.mainWindow())
        self.waview_menu23.addAction(self.waview_action1)

        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###СПРАВОЧНИКИ", self.iface.mainWindow())
        self.wadata_menu.addAction(self.waview_action1)

        self.waview_menu24 = QMenu(u"###РЕДАКТОР")
        self.wadata_menu.addMenu(self.waview_menu24)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###Вырезать", self.iface.mainWindow())
        self.waview_menu24.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###Скопировать", self.iface.mainWindow())
        self.waview_menu24.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###Вставить", self.iface.mainWindow())
        self.waview_menu24.addAction(self.waview_action1)
        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"###Удалить", self.iface.mainWindow())
        self.waview_menu24.addAction(self.waview_action1)

        self.waview_action1 = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_macro-objects_4698.png"),
                                      u"???НЕТ РЕЖИМА", self.iface.mainWindow())
        self.wadata_menu.addAction(self.waview_action1)

        self.actionComposerSelect = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_select_print.png"),
            u"PolFunDev ПЕЧАТЬ НА ВЫБРАННОМ ХОЛСТЕ QGIS-plugin.", self.iface.mainWindow())
        self.actionShowStreets = QAction(QIcon(os.path.dirname(__file__) +"/icon5/bulbgrey_4053.png"),
            u"PolFunDev УЛИЦЫ/АДРЕСА QGIS-plugin.", self.iface.mainWindow())
        self.actionShowAddr = QAction(QIcon(os.path.dirname(__file__) +"/icon5/bulbgrey_4053.png"),
            u"PolFunDev УЛИЦЫ/АДРЕСА QGIS-plugin.", self.iface.mainWindow())
        self.action = QAction(QIcon(os.path.dirname(__file__) +"/icon.png"),
            u"PolFunDev СПРАВОЧНИКИ QGIS-plugin.", self.iface.mainWindow())
        self.actionRuler = QAction(QIcon(os.path.dirname(__file__) +"/ruler1_3565.png"),
            u"PolFunDev ЛИНЕЙКА QGIS-plugin.", self.iface.mainWindow())
        self.actionEarthProfile = QAction(QIcon(os.path.dirname(__file__) +"/line_chart_4360.png"),
            u"PolFunDev ПРОФИЛЬ РЕЛЬЕФА QGIS-plugin.", self.iface.mainWindow())
        #self.actionPipeProfile = QAction(
        #    QIcon("C:/Program Files/QGIS Brighton/apps/qgis/python/plugins/water_account_dicts/linechart_5388.png"),
        #    u"СТАРОМОДНЫЙ СТИЛЬ КНОПОК PolFunDev QGIS-plugin.", self.iface.mainWindow())
        self.actionColorSelect = QAction(QIcon(os.path.dirname(__file__) +"/applications-graphics_4842.png"),
            u"PolFunDev ВЫДЕЛЕНИЕ ЦВЕТОМ QGIS-plugin.", self.iface.mainWindow())
        #self.actionObjEdit = QAction(
        #    QIcon("C:/Program Files/QGIS Brighton/apps/qgis/python/plugins/water_account_dicts/icon2/stock_create-with-attributes_2083.png"),
        #    u"PolFunDev ПРАВКА ОБЪЕКТА ВОДОКАНАЛ QGIS-plugin.", self.iface.mainWindow())
        #self.actionGroupSelect = QAction(
        #3    QIcon("C:/Program Files/QGIS Brighton/apps/qgis/python/plugins/water_account_dicts/icon2/stock_macro-objects_4698.png"),
        #    u"PolFunDev ГРУППОВОЕ ВЫДЕЛЕНИЕ QGIS-plugin.", self.iface.mainWindow())
        self.actionContour = QAction(QIcon(os.path.dirname(__file__) +"/icon2/stock_format-object_7340.png"),
            u"PolFunDev КОНТУР QGIS-plugin.", self.iface.mainWindow())
        self.actionAdresSearch = QAction(QIcon(os.path.dirname(__file__) +"/icon3/x-office-address-book_2992.png"),
            u"PolFunDev ПОИСК АДРЕСА QGIS-plugin.", self.iface.mainWindow())
        self.actionStreetIntersect = QAction(QIcon(os.path.dirname(__file__) +"/icon4/stock_node-corner_4985.png"),
            u"PolFunDev ПЕРЕКРЕСТОК QGIS-plugin.", self.iface.mainWindow())
        #self.actionLocation = QAction(QIcon(os.path.dirname(__file__) +"/icon5/compass_3205.png"),
        #    u"PolFunDev КООРДИНАТЫ QGIS-plugin.", self.iface.mainWindow())
        self.actionViewDowning = QAction(QIcon(os.path.dirname(__file__) +"/icon4/arrow_1004.png"),
            u"PolFunDev УКЛОНЫ QGIS-plugin.", self.iface.mainWindow())
        self.actionViewTitles = QAction(QIcon(os.path.dirname(__file__) +"/icon4/insert-text_1542.png"),
            u"PolFunDev ОТМЕТКИ (МАТЕРИАЛ, ДИАМЕТР) QGIS-plugin.", self.iface.mainWindow())
        self.actionViewIntervals = QAction(QIcon(os.path.dirname(__file__) +"/icon4/length-measure_8551.png"),
            u"PolFunDev ДЛИНЫ QGIS-plugin.", self.iface.mainWindow())
        self.actionBigPlan = QAction(QIcon(os.path.dirname(__file__) +"/icon4/gwenview_5368.png"),
            u"PolFunDev ОБЩИЙ ПЛАН QGIS-plugin.", self.iface.mainWindow())
        self.actionRepGen = QAction(QIcon(os.path.dirname(__file__) +"/icon6/kdeprint-testprinter_5775.png"),
            u"PolFunDev ОТЧЕТЫ PSDEVELOP QGIS-plugin.", self.iface.mainWindow())
        self.analyticImport = QAction(QIcon(os.path.dirname(__file__) +"/icon2/kgpg_import_5463.png"),
            u"PolFunDev АНАЛИТИЧЕСКИЙ ИМПОРТ PSDEVELOP QGIS-plugin.", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)
        self.actionRuler.triggered.connect(self.runLineTool)
        self.actionShowAddr.triggered.connect(self.runAddrLabels)
        self.actionShowStreets.triggered.connect(self.showStreets)
        self.actionViewIntervals.triggered.connect(self.showLens)
        self.actionViewTitles.triggered.connect(self.showLabels)
        self.actionBigPlan.triggered.connect(self.fullZoom)
        self.actionColorSelect.triggered.connect(self.colorSelExp)
        self.actionStreetIntersect.triggered.connect(self.show2StrSearchDlg)
        self.actionAdresSearch.triggered.connect(self.showAdrSearchDlg)
        self.actionRepGen.triggered.connect(self.showRepGen)
        self.actionComposerSelect.triggered.connect(self.runRectangle)
        self.analyticImport.triggered.connect(self.runAnalytImport)
        #self.actionPipeProfile.triggered.connect(self.showOlsStyleDlg)
        self.toolRectangle = PrintRectangleSelection(self.iface.mapCanvas(), self.actionComposerSelect, self)
        self.actionComposerSelect.setCheckable(True)

        # Add toolbar button and menu item
        #self.iface.addToolBarIcon(self.actionBigPlan)
        #self.iface.addPluginToMenu(u"Полтароков/Фундукян Development", self.actionBigPlan)

        self.iface.addToolBarIcon(self.analyticImport)
        self.iface.addToolBarIcon(self.actionRepGen)
        self.iface.addToolBarIcon(self.actionComposerSelect)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.actionViewTitles)
        self.iface.addPluginToMenu(u"Полтароков/Фундукян Development", self.actionViewTitles)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.actionViewIntervals)
        self.iface.addPluginToMenu(u"Полтароков/Фундукян Development", self.actionViewIntervals)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.actionViewDowning)
        self.iface.addPluginToMenu(u"Полтароков/Фундукян Development", self.actionViewDowning)

        # Add toolbar button and menu item
        #self.iface.addToolBarIcon(self.actionLocation)
        #self.iface.addPluginToMenu(u"Полтароков/Фундукян Development", self.actionLocation)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.actionStreetIntersect)
        self.iface.addPluginToMenu(u"Полтароков/Фундукян Development", self.actionStreetIntersect)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"Полтароков/Фундукян Development", self.action)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.actionRuler)
        self.iface.addPluginToMenu(u"Полтароков/Фундукян Development", self.actionRuler)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.actionEarthProfile)
        self.iface.addPluginToMenu(u"Полтароков/Фундукян Development", self.actionEarthProfile)

        # Add toolbar button and menu item
        #self.iface.addToolBarIcon(self.actionPipeProfile)
        #self.iface.addPluginToMenu(u"Полтароков/Фундукян Development", self.actionPipeProfile)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.actionColorSelect)
        self.iface.addPluginToMenu(u"Полтароков/Фундукян Development", self.actionColorSelect)

        # Add toolbar button and menu item
        #self.iface.addToolBarIcon(self.actionObjEdit)
        #self.iface.addPluginToMenu(u"Полтароков/Фундукян Development", self.actionObjEdit)

        # Add toolbar button and menu item
        #self.iface.addToolBarIcon(self.actionGroupSelect)
        #self.iface.addPluginToMenu(u"Полтароков/Фундукян Development", self.actionGroupSelect)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.actionContour)
        self.iface.addPluginToMenu(u"Полтароков/Фундукян Development", self.actionContour)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.actionAdresSearch)
        self.iface.addPluginToMenu(u"Полтароков/Фундукян Development", self.actionAdresSearch)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.actionShowStreets)
        self.iface.addPluginToMenu(u"Полтароков/Фундукян Development", self.actionShowStreets)

        # Add toolbar button and menu item
        #self.iface.addToolBarIcon(self.actionShowAddr)
        #self.iface.addPluginToMenu(u"Полтароков/Фундукян Development", self.actionShowAddr)
        
        # Signal connections for mouse clicks
        #QObject.connect(self.dlg.ui.chkActivate,SIGNAL("stateChanged(int)"),self.callPlugin)
        #QMessageBox.information( self.iface.mainWindow(),  "Info",  "connect = %s" %str(result) )

    def setRectangle(self, rect=None):
        if(rect):
		    print "width="+str(rect.width())+",height="+str(rect.height())+\
              ",center_x="+str(rect.center().x())+",center_y="+str(rect.center().y())
        self.rect=rect
			  
        self.setPCanvParamsDlg.showDlg(rect.width(), rect.height(), self.rect.center().x(), self.rect.center().y(), self.iface.mapCanvas().scale())

    def runAtlasReport(self, rtype, scale, tindex, wd, ht, zl, amfmode):
        #print "atlas generating"
        x1 = self.rect.center().x() - (self.rect.width()//2);
        #x3 = self.rect.center().x() - (self.rect.width()//2);
        #x2 = self.rect.center().x() + (self.rect.width()//2);
        #x4 = self.rect.center().x() + (self.rect.width()//2);
		
        y1 = self.rect.center().y() + (self.rect.height()//2);
        #y3 = self.rect.center().y() + (self.rect.height()//2);
        #y2 = self.rect.center().y() - (self.rect.height()//2);
        #y4 = self.rect.center().y() + (self.rect.height()//2);
		
        self.print_scale = scale;

        layers = self.iface.legendInterface().layers()
        self.shp_layer = None
        for layer in layers:
            layerType = layer.type()
            if layerType == QgsMapLayer.VectorLayer or True:
                if layer.name()==u'ATLAS_COSMETIC' or layer.name()==u'косметический_полигон' or layer.name()=='ATLAS_COSMETIC':
                    self.shp_layer=layer			  
        
        self.correct_coeff=1.0 + 1/15; # поля  по 10 см можно варьировать.
        #self.x_coeff=6402/297 #21.555555 297/210=1.4142857
        #self.y_coeff=3786/210 #18.028571 4527=6402/1.4142857
        self.dist_unit=self.print_scale/1000; #21.555555/self.correct_coeff #коэффициент единицы карты мкс 23 для см листа
        if amfmode==0:
           hor_width_cnt=math.ceil(self.rect.width()/self.dist_unit/297);
           ver_width_cnt=math.ceil(self.rect.height()/self.dist_unit/210);
           a4_297=self.dist_unit*297
           a4_210=self.dist_unit*210
        else:
           hor_width_cnt=math.ceil(self.rect.width()/self.dist_unit/210);
           ver_width_cnt=math.ceil(self.rect.height()/self.dist_unit/297);
           a4_297=self.dist_unit*210
           a4_210=self.dist_unit*297		   

        self.curr_scale=self.iface.mapCanvas().scale()
        print "curr_acale="+str(self.curr_scale)+",set_scale="+str(self.print_scale)
        if self.shp_layer:
            #deleteFeature (QgsFeatureId fid)
            f = QgsFeature()
            feat_iterator = self.shp_layer.getFeatures()
            self.shp_layer.startEditing()
            while feat_iterator.nextFeature(f):
                self.shp_layer.deleteFeature(f.id())
            #self.shp_layer.updateExtents()
            self.shp_layer.commitChanges()
            self.shp_layer.triggerRepaint()
            pr = self.shp_layer.dataProvider()
            	
            #point1 = QgsPoint(50,50)
            hor_cnt=0
            ver_cnt=0
            while hor_cnt<hor_width_cnt:
                while ver_cnt<ver_width_cnt:
                    pt = QgsFeature()
                    pt.setGeometry(QgsGeometry.fromPolygon([[QgsPoint(x1+hor_cnt*a4_297,y1-ver_cnt*a4_210),QgsPoint(x1+(hor_cnt+1)*a4_297,y1-ver_cnt*a4_210), QgsPoint(x1+(hor_cnt+1)*a4_297,y1-(ver_cnt+1)*a4_210), QgsPoint(x1+hor_cnt*a4_297,y1-(ver_cnt+1)*a4_210)]]))
                    pr.addFeatures([pt])
                    #print "hcnt="+str(hor_cnt)+",vcnt="+str(ver_cnt)+",hwcnt="+str(hor_width_cnt)+",vwcnt="+str(ver_width_cnt)
                    ver_cnt=ver_cnt+1
                hor_cnt=hor_cnt+1
                ver_cnt=0
            # update extent of the layer
            self.shp_layer.updateExtents()
        if hor_cnt>0 and self.shp_layer:
            self.new_composer = self.iface.createNewComposer(u"Новый атлас-макет PolFunDev (CopyRight)")
            self.composit = self.new_composer.composition()
            self.composit.setAtlasMode(QgsComposition.PreviewAtlas)
            self.atlasComposit=self.composit.atlasComposition()
            self.atlasComposit.setCoverageLayer(self.shp_layer)
            self.atlasComposit.setHideCoverage(True)
            self.atlasComposit.setEnabled(True)
            self.atlasComposit.setHideCoverage(True)
            self.composit.setAtlasMode(QgsComposition.PreviewAtlas)
            if amfmode==0:
                width=297
                height=210
            else:
                width=210
                height=297			
            map_offs=5
            self.composit.setPaperSize(width, height)
            self.mComposerMap = QgsComposerMap(self.composit, map_offs, map_offs, width-map_offs*2, height-map_offs*2)
            #self.mComposerMap.setFrameEnabled(True)
            #self.mComposerMap.setNewScale(mscale)
            self.mComposerMap.setAtlasDriven(True)
            self.mComposerMap.setAtlasScalingMode(QgsComposerMap.Auto)
            self.mComposerMap.setAtlasMargin(0)
            self.mComposerMap.setFrameEnabled(True)
            self.mComposerMap.setFrameOutlineWidth(0.03)
            self.composit.addComposerMap(self.mComposerMap)
            self.mComposerMap.setAtlasMargin(0)
            self.mComposerMap.setFrameEnabled(True)
            self.mComposerMap.setFrameOutlineWidth(0.03)
            self.composit.setAtlasMode(QgsComposition.PreviewAtlas)
            self.atlasComposit.setHideCoverage(True)
            
    def runAutoReport(self, rtype, scale, tindex, wd, ht, zl):
        #items = (u"Горизонтально 1", u"Вертикально 1", u"Горизонтально 4(2*2)",u"Вертикально 4(2*2)")
        #item, ok = QInputDialog.getItem(self.iface.mainWindow(), u'Размер печати', u'Выберите размер полотна:', items, 0, False)
        #if not ok:
        #    return
        item = rtype
        width = wd
        height = ht
        zoom_level = zl
        mscale = scale	
        #print "======"+str(scale)+rtype		
        #if item==u"Вертикально 1":
            #width = 210
            #height = 297
        #if item==u"Горизонтально 4(2*2)":
            #width = 596
            #height = 420
            #zoom_level = 0.25
            #mscale = 11508
        #if item==u"Вертикально 4(2*2)":
            #width = 596
            #height = 420
            #zoom_level = 0.25
            #mscale = 11508

        self.new_composer = self.iface.createNewComposer(u"Новый макет PolFunDev (CopyRight)")
        self.composit = self.new_composer.composition()
        #self.composit.setGridVisible(True)
        self.composit.setSnapGridOffsetX(0.2)
        self.composit.setSnapGridOffsetY(0.1)
        self.composit.setSnapLinesVisible(True)
        self.composit.setPrintResolution(600);

        self.composit.setPaperSize(width, height)
        map_offs=10
        if tindex>1:
            map_offs=10
        if tindex>3:
            map_offs=12
        if tindex>5:
            map_offs=15	
        if tindex>7:
            map_offs=20				
        self.mComposerMap = QgsComposerMap(self.composit, map_offs, map_offs, width-map_offs*2, height-map_offs*2)
        self.mComposerMap.setFrameEnabled(True)
        self.mComposerMap.setNewScale(mscale)
        self.composit.addComposerMap(self.mComposerMap)
        if tindex==4:
            deltax=297
            deltay=210
            dxcnt=2
            dycnt=2
            xlim=0
            ylim=0
            while xlim<dxcnt or ylim<dycnt:
                shp = QgsComposerShape(xlim*2+xlim*deltax,ylim*2+ylim*deltay,deltax,deltay,self.composit)
                xlim=xlim+1
                if xlim>=dxcnt and ylim<dycnt:
                    ylim=ylim+1
                    if ylim<dycnt:
                        xlim=0					
                #print "======++++++"
                shp.setShapeType(QgsComposerShape.Rectangle)
                shp.setTransparency(73)
                shp.setExcludeFromExports(True)
                self.composit.addComposerShape(shp)
        if tindex==5:
            deltax=210
            deltay=297
            dxcnt=2
            dycnt=2
            xlim=0
            ylim=0
            while xlim<dxcnt or ylim<dycnt:
                shp = QgsComposerShape(xlim*2+xlim*deltax,ylim*2+ylim*deltay,deltax,deltay,self.composit)
                xlim=xlim+1
                if xlim>=dxcnt and ylim<dycnt:
                    ylim=ylim+1
                    if ylim<dycnt:
                        xlim=0					
                #print "======++++++"
                shp.setShapeType(QgsComposerShape.Rectangle)
                shp.setTransparency(73)
                shp.setExcludeFromExports(True)
                self.composit.addComposerShape(shp)
        if tindex==6:
            deltax=297
            deltay=210
            dxcnt=3
            dycnt=3
            xlim=0
            ylim=0
            while xlim<dxcnt or ylim<dycnt:
                shp = QgsComposerShape(xlim*2+xlim*deltax,ylim*2+ylim*deltay,deltax,deltay,self.composit)
                xlim=xlim+1
                if xlim>=dxcnt and ylim<dycnt:
                    ylim=ylim+1
                    if ylim<dycnt:
                        xlim=0					
                #print "======++++++"
                shp.setShapeType(QgsComposerShape.Rectangle)
                shp.setTransparency(73)
                shp.setExcludeFromExports(True)
                self.composit.addComposerShape(shp)
        if tindex==7:
            deltax=210
            deltay=297
            dxcnt=3
            dycnt=3
            xlim=0
            ylim=0
            while xlim<dxcnt or ylim<dycnt:
                shp = QgsComposerShape(xlim*2+xlim*deltax,ylim*2+ylim*deltay,deltax,deltay,self.composit)
                xlim=xlim+1
                if xlim>=dxcnt and ylim<dycnt:
                    ylim=ylim+1
                    if ylim<dycnt:
                        xlim=0					
                #print "======++++++"
                shp.setShapeType(QgsComposerShape.Rectangle)
                shp.setTransparency(73)
                shp.setExcludeFromExports(True)
                self.composit.addComposerShape(shp)
        if tindex==8:
            deltax=297
            deltay=210
            dxcnt=4
            dycnt=4
            xlim=0
            ylim=0
            while xlim<dxcnt or ylim<dycnt:
                shp = QgsComposerShape(xlim*2+xlim*deltax,ylim*2+ylim*deltay,deltax,deltay,self.composit)
                xlim=xlim+1
                if xlim>=dxcnt and ylim<dycnt:
                    ylim=ylim+1
                    if ylim<dycnt:
                        xlim=0					
                #print "======++++++"
                shp.setShapeType(QgsComposerShape.Rectangle)
                shp.setTransparency(73)
                shp.setExcludeFromExports(True)
                self.composit.addComposerShape(shp)
        if tindex==9:
            deltax=210
            deltay=297
            dxcnt=4
            dycnt=4
            xlim=0
            ylim=0
            while xlim<dxcnt or ylim<dycnt:
                shp = QgsComposerShape(xlim*2+xlim*deltax,ylim*2+ylim*deltay,deltax,deltay,self.composit)
                xlim=xlim+1
                if xlim>=dxcnt and ylim<dycnt:
                    ylim=ylim+1
                    if ylim<dycnt:
                        xlim=0					
                #print "======++++++"
                shp.setShapeType(QgsComposerShape.Rectangle)
                shp.setTransparency(73)
                shp.setExcludeFromExports(True)
                self.composit.addComposerShape(shp)				
			#shp = QgsComposerShape(298,0,296,210,self.composit)
            #shp.setShapeType(QgsComposerShape.Rectangle)
            #shp.setTransparency(73)
            #shp.setExcludeFromExports(True)
            #self.composit.addComposerShape(shp)
            #shp = QgsComposerShape(0,211,297,209,self.composit)
            #shp.setShapeType(QgsComposerShape.Rectangle)
            #shp.setTransparency(73)
            #shp.setExcludeFromExports(True)
            #self.composit.addComposerShape(shp)
            #shp = QgsComposerShape(298,211,296,209,self.composit)
            #shp.setShapeType(QgsComposerShape.Rectangle)
            #shp.setTransparency(73)
            #shp.setExcludeFromExports(True)
            #self.composit.addComposerShape(shp)
        self.new_composer.setZoomLevel(zoom_level)
        #self.new_composer
        fname = QFileDialog.getSaveFileName(self.iface.mainWindow(), u"Выбор pdf-файла для сохранения...", "", ".pdf")
        if(fname):
		    self.composit.exportAsPDF(fname)

    def runRectangle(self):
        #self.setRectangle()
        #self.actionComposerSelect.setChecked(False)
        #self.selectionButton.setDefaultAction(self.selectionButton.sender())
        if not self.action.isChecked():
            self.iface.mapCanvas().mapTool().deactivate()
            self.actionComposerSelect.setChecked(True)
            self.iface.mapCanvas().setMapTool(self.toolRectangle)
        else:
            self.actionComposerSelect.setChecked(False)
            self.iface.mapCanvas().unsetMapTool(self.toolRectangle)

    def fullZoom(self):
        self.iface.actionZoomIn()

    def showRepGen(self):
        self.repGen.show()
        self.repGen.setDlg()
		
    def runAnalytImport(self):
        self.aimp_fpath = ""
        self.filename = QFileDialog.getOpenFileName(self.iface.mainWindow(), 'Open file', '')
        try:
            if self.filename:
                file=open(self.filename, 'rb')
                self.re_data = file.read()
                #print self.re_data #.encode('utf-8')
                with open(self.filename, 'r') as fl:
                    # Read the file contents and generate a list with each line
                    flines = fl.readlines()
        except ValueError:
            infoString = "Error file opening!"
            QMessageBox.information(self.iface.mainWindow(),"Error",infoString)
            return
        p = re.compile(u"#\d+ #\d+") 
        reg_hset = '{\s*\d+.\d+\s+\d+.\d+\s+"[^"]*"\s+\d+\s+#\d+\s+#\d+\s*}'
        reg_shp = '({\s*\d+.\d+\s+\d+.\d+\s+\d+.\d+\s*})*'
        #print self.re_data
        m = p.match(self.re_data)
        if m:
            print m.group()
        else:
            QMessageBox.information(self.iface.mainWindow(),"Error",u"Не найдены объекты")

		# Iterate each line
        for fline in flines:
            # Regex applied to each line 
            match = re.search(reg_shp, fline)
            if match:
                # Make sure to add \n to display correctly when we write it back
                new_line = match.group() + '\n'
                print new_line

    def showLabels(self):
        layers = self.iface.legendInterface().layers()
        items = (u"КАНАЛИЗАЦИЯ", u"ВОДОПРОВОД")
        item, ok = QInputDialog.getItem(self.iface.mainWindow(), 'Input Dialog', 'Enter your name:', items, 0, False)
        if not ok:
            return
        for layer in layers:
            layerType = layer.type()
            #print "yyyyyy"
            if layerType == QgsMapLayer.VectorLayer:
                #print layer.name()
                if layer.name()==u"***КАНАЛИЗ МАТЕРИАЛ" and item==u"КАНАЛИЗАЦИЯ":
                    #print "rrrrr"
                    self.iface.setActiveLayer(layer)
                    self.visLabels11 = not self.visLabels11
                    self.iface.legendInterface().setLayerVisible(layer, self.visLabels11)
                if layer.name()==u"***КАНАЛИЗ ДИАМЕТР" and item==u"КАНАЛИЗАЦИЯ":
                    #print "rrrrr"
                    self.iface.setActiveLayer(layer)
                    self.visLabels12 = not self.visLabels12
                    self.iface.legendInterface().setLayerVisible(layer, self.visLabels12)
                if layer.name()==u"***ВОДОПРОВОД УЛИЦЫ" and item==u"ВОДОПРОВОД":
                    #print "rrrrr"
                    self.iface.setActiveLayer(layer)
                    self.visLabels21 = not self.visLabels21
                    self.iface.legendInterface().setLayerVisible(layer, self.visLabels21)
                if layer.name()==u"***ВОДОПРОВОД ДИАМЕТР" and item==u"ВОДОПРОВОД":
                    #print "rrrrr"
                    self.iface.setActiveLayer(layer)
                    self.visLabels22 = not self.visLabels22
                    self.iface.legendInterface().setLayerVisible(layer, self.visLabels22)

    def showStreets(self):
        layers = self.iface.legendInterface().layers()
        items = (u"КАНАЛИЗАЦИЯ", u"ВОДОПРОВОД")
        item, ok = QInputDialog.getItem(self.iface.mainWindow(), 'Input Dialog', 'Enter your name:', items, 0, False)
        if not ok:
            return
        for layer in layers:
            layerType = layer.type()
            #print "yyyyyy"
            if layerType == QgsMapLayer.VectorLayer:
                #print layer.name()
                if layer.name()==u"***КАНАЛИЗ УЛИЦЫ" and item==u"КАНАЛИЗАЦИЯ":
                    #print "rrrrr"
                    self.iface.setActiveLayer(layer)
                    self.visStreet1 = not self.visStreet1
                    self.iface.legendInterface().setLayerVisible(layer, self.visStreet1)
                if layer.name()==u"***ВОДОПРОВОД УЛИЦЫ" and item==u"ВОДОПРОВОД":
                    #print "rrrrr"
                    self.iface.setActiveLayer(layer)
                    self.visStreet2 = not self.visStreet2
                    self.iface.legendInterface().setLayerVisible(layer, self.visStreet2)

    def showLens(self):
        layers = self.iface.legendInterface().layers()
        items = (u"КАНАЛИЗАЦИЯ", u"ВОДОПРОВОД")
        item, ok = QInputDialog.getItem(self.iface.mainWindow(), 'Input Dialog', 'Enter your name:', items, 0, False)
        if not ok:
            return
        for layer in layers:
            layerType = layer.type()
            #print "yyyyyy"
            if layerType == QgsMapLayer.VectorLayer:
                #print layer.name()
                if layer.name()==u"***КАНАЛИЗ ДЛИНЫ" and item==u"КАНАЛИЗАЦИЯ":
                    #print "rrrrr"
                    self.iface.setActiveLayer(layer)
                    self.visLens1 = not self.visLens1
                    self.iface.legendInterface().setLayerVisible(layer, self.visLens1)
                if layer.name()==u"***ВОДОПРОВОД ДЛИНЫ" and item==u"ВОДОПРОВОД":
                    #print "rrrrr"
                    self.iface.setActiveLayer(layer)
                    self.visLens2 = not self.visLens2
                    self.iface.legendInterface().setLayerVisible(layer, self.visLens2)

    def handleMouseDown(self,  point,  button):
        #QMessageBox.information( self.iface.mainWindow(),  "Info",  "X,Y = %s, %s" % (str(point.x()), str(point.y())) )
        self.canvasClick(point, button)
        #self.dlg.clearTextBrowser()
        #self.dlg.setTextBrowser( str(point.x()) + " , " + str(point.y()) )

    def canvasClick(self,  point,  button):
        layer = self.iface.activeLayer()
        if layer == None or layer.type() != QgsMapLayer.VectorLayer:
            QMessageBox.information( self.iface.mainWindow(), "Closest Feature Finder", "No vector layers selected" )
            return

        if button != Qt.RightButton:
            return

        if not layer.hasGeometryType():
            #QMessageBox.warning( self, "Closest Feature Finder", "The selected layer has either no or unknown geometry" )
            QMessageBox.information( self.iface.mainWindow(),  "Closest Feature Finder",  "The selected layer has either no or unknown geometry" )
            return

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        # get the point coordinates in the layer's CRS
        point = self.canvas.mapRenderer().mapToLayerCoordinates(layer, point)

        # retrieve all the layer's features
        layer.select([])

        if self.index == None or layer != self.previousLayer:
            # there's no previously created index or it's not the same layer,
            # then create the index
            self.index = QgsSpatialIndex()
            f = QgsFeature()
            feat_iterator = layer.getFeatures()
            while feat_iterator.nextFeature(f):
                self.index.insertFeature(f)

        # get the feature which has the closest bounding box using the spatial index
        nearest = self.index.nearestNeighbor( point, 1 )
        featureId = nearest[0] if len(nearest) > 0 else None

        closestFeature = QgsFeature()
        if featureId == None or not (featureId in layer.allFeatureIds()):
        	#featureAtId(featureId, closestFeature, True, False) == False:
            closestFeature = None
        else:
            fid = QgsFeature()
            if layer.getFeatures(QgsFeatureRequest(featureId)).nextFeature(fid):
                closestFeature = fid
            else:
                closestFeature = None

        # if polygon, make a futher test
        if layer.geometryType() != QGis.Point and closestFeature != None:
            # find the furthest bounding box borders
            rect = closestFeature.geometry().boundingBox()

            dist_pX_rXmax = abs( point.x() - rect.xMaximum() )
            dist_pX_rXmin = abs( point.x() - rect.xMinimum() )
            if dist_pX_rXmax > dist_pX_rXmin:
                width = dist_pX_rXmax
            else:
                width = dist_pX_rXmin

            dist_pY_rYmax = abs( point.y() - rect.yMaximum() )
            dist_pY_rYmin = abs( point.y() - rect.yMinimum() )
            if dist_pY_rYmax > dist_pY_rYmin:
                height = dist_pY_rYmax
            else:
                height = dist_pY_rYmin

            # create the search rectangle
            rect = QgsRectangle()
            rect.setXMinimum( point.x() - width )
            rect.setXMaximum( point.x() + width )
            rect.setYMinimum( point.y() - height )
            rect.setYMaximum( point.y() + height )

            # retrieve all geometries into the search rectangle
            layer.select([], rect, True, True)

            # find the nearest feature
            minDist = -1
            featureId = None
            point = QgsGeometry.fromPoint(point)

            f = QgsFeature()
            while layer.nextFeature(f):
                geom = f.geometry()
                distance = geom.distance(point)
                if minDist < 0 or distance < minDist:
                    minDist = distance
                    featureId = f.id()

            # get the closest feature
            closestFeature = QgsFeature()
            if featureId == None or layer.featureAtId(featureId, closestFeature, True, False) == False:
                closestFeature = None

        self.previousLayer = layer

        if closestFeature == None:
            # no feature found
            #QMessageBox.warning(self, "Closest Feature Finder Plugin", QString.fromUtf8( "No features found." ) )
            QMessageBox.information( self.iface.mainWindow(), "Closest Feature Finder Plugin", "No features found" )
        else:
            layer.removeSelection()
            layer.select( closestFeature.id() )
            fields = closestFeature.fields()
            #for (k,field) in fields:
            self.attrDlg.show()
            self.attrDlg.fillAttrData(closestFeature, layer)
            for k in range(fields.count()):
                field = fields[k]
                #QMessageBox.information( self.iface.mainWindow(), "Attribute", "%d: %s" % ( k, str(closestFeature.attribute(field.name())) ) )

        QApplication.restoreOverrideCursor()

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Select vector features by point and click.", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        self.dlg.show()
        self.dlg.fillDictsData()

    def showOlsStyleDlg(self):
        self.oldStyleDockWidget.show()

    def runLineTool(self):
        if not self.calc_line_action==None:
            self.calc_line_action.trigger()
        #self.lineTool = QgsMapToolSelectPolygon( self.canvas)
        #self.canvas.setMapTool(self.lineTool)

    def colorSelExp(self):
        if not self.expess_select_action==None:
            self.expess_select_action.trigger()

    def runAddrLabels(self):

        layers = self.iface.legendInterface().layers()
        for layer in layers:
            layerType = layer.type()
            if layerType == QgsMapLayer.VectorLayer:
                if layer.name()==u'КАНАЛИЗАЦИЯ':
                    self.iface.setActiveLayer(layer)
                    fields = layer.dataProvider().fields()
                    for field in fields:
                        print "==="+field.name()

        layer = self.iface.activeLayer()
        if layer == None or layer.type() != QgsMapLayer.VectorLayer:
            QMessageBox.information( self.iface.mainWindow(), "Closest Feature Finder", "No vector layers selected" )
            return
        print "render labels"
        #layer.setCustomProperty("labeling", "pal")
        #layer.setCustomProperty("labeling/enabled", "true")
        #layer.setCustomProperty("labeling/fontFamily", "Arial")
        #layer.setCustomProperty("labeling/fontSize", "10")
        #layer.setCustomProperty("labeling/fieldName", "ErrorDescr")
        #layer.setCustomProperty("labeling/placement", "2")
        if layer.customProperty("labeling/enabled")=="true":
            layer.setCustomProperty("labeling/enabled", "false")
        else:
            layer.setCustomProperty("labeling/enabled", "true")
            layer.setCustomProperty("labeling/isExpression", True)
            layer.setCustomProperty("labeling/fieldName", "concat( STREET ,', ', NUM )")
        layer.triggerRepaint()
