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
import time
import csv
import ntpath
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import QgsFeature, QgsVectorLayer, QgsVectorLayerImport, QgsMapLayerRegistry, \
	QgsDataSourceURI, QgsGraduatedSymbolRendererV2, QgsSymbolV2, QgsRendererRangeV2, QgsSymbolLayerV2Registry, \
	QgsMarkerSymbolV2, QgsSingleSymbolRendererV2, QgsGeometry, QgsPoint, QgsField, QgsFeatureRequest, QgsFeatureIterator
from qgis.gui import QgsMessageBar, QgsMessageViewer
from .info_viewer import InfoViewer
from .table_viewer import TableViewer
from .layer_preview import LayerPreview
from .txt_csv_qfiledialog import TxtCsvOpenFile

from .db_tree import DBTree

from .db_plugins.plugin import BaseError
from .dlg_db_error import DlgDbError


class DBManager(QMainWindow):

	def __init__(self, iface, parent=None):
		QMainWindow.__init__(self, parent)
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.setupUi()
		self.iface = iface

		# restore the window state
		settings = QSettings()
		self.restoreGeometry( settings.value("/DB_Manager/mainWindow/geometry", QByteArray(), type=QByteArray ) )
		self.restoreState( settings.value("/DB_Manager/mainWindow/windowState", QByteArray(), type=QByteArray ) )

		self.connect(self.tabs, SIGNAL("currentChanged(int)"), self.tabChanged)
		self.connect(self.tree, SIGNAL("selectedItemChanged"), self.itemChanged)
		self.itemChanged(None)


	def closeEvent(self, e):
		self.unregisterAllActions()

		# save the window state
		settings = QSettings()
		settings.setValue( "/DB_Manager/mainWindow/windowState", self.saveState() )
		settings.setValue( "/DB_Manager/mainWindow/geometry", self.saveGeometry() )

		QMainWindow.closeEvent(self, e)


	def refreshItem(self, item=None):
		QApplication.setOverrideCursor(Qt.WaitCursor)
		try:
			if item == None:
				item = self.tree.currentItem()
			self.tree.refreshItem(item)	# refresh item children in the db tree
		except BaseError, e:
			DlgDbError.showError(e, self)
			return
		finally:
			QApplication.restoreOverrideCursor()

	def itemChanged(self, item):
		QApplication.setOverrideCursor(Qt.WaitCursor)
		try:
			self.reloadButtons()
			self.refreshTabs()
		except BaseError, e:
			DlgDbError.showError(e, self)
			return
		finally:
			QApplication.restoreOverrideCursor()


	def reloadButtons(self):
		db = self.tree.currentDatabase()
		if not hasattr(self, '_lastDb'):
			self._lastDb = db

		elif db == self._lastDb:
			return

		# remove old actions
		if self._lastDb != None:
			self.unregisterAllActions()

		# add actions of the selected database
		self._lastDb = db
		if self._lastDb != None:
			self._lastDb.registerAllActions(self)


	def tabChanged(self, index):
		QApplication.setOverrideCursor(Qt.WaitCursor)
		try:
			self.refreshTabs()
		except BaseError, e:
			DlgDbError.showError(e, self)
			return
		finally:
			QApplication.restoreOverrideCursor()


	def refreshTabs(self):
		index = self.tabs.currentIndex()
		item  = self.tree.currentItem()
		table  = self.tree.currentTable()

		# enable/disable tabs
		self.tabs.setTabEnabled( self.tabs.indexOf(self.table), table != None )
		self.tabs.setTabEnabled( self.tabs.indexOf(self.preview), table != None and table.type in [table.VectorType, table.RasterType] and table.geomColumn != None )
		# show the info tab if the current tab is disabled
		if not self.tabs.isTabEnabled( index ):
			self.tabs.setCurrentWidget( self.info )

		current_tab = self.tabs.currentWidget()
		if current_tab == self.info:
			self.info.showInfo( item )
		elif current_tab == self.table:
			self.table.loadData( item )
		elif current_tab == self.preview:
			self.preview.loadPreview( item )


	def refreshActionSlot(self):
		self.info.setDirty()
		self.table.setDirty()
		self.preview.setDirty()
		self.refreshItem()

	def importActionSlot(self):
		db = self.tree.currentDatabase()
		if db is None:
			self.infoBar.pushMessage(self.tr("No database selected or you are not connected to it."), QgsMessageBar.INFO, self.iface.messageTimeout())
			return

		outUri = db.uri()
		schema = self.tree.currentSchema()
		if schema:
			outUri.setDataSource( schema.name, "", "", "" )

		from .dlg_import_vector import DlgImportVector
		dlg = DlgImportVector(None, db, outUri, self)
		dlg.exec_()

	def tofloat(self, value):
		try:
			return float(value)
		except Exception:
			return 0.0

	def getConnections(self):
		s = QSettings()
		s.beginGroup(u"PostgreSQL/connections")
		currentConnections = s.childGroups()
		s.endGroup()
		return currentConnections

	def connection_value(self, connection, key):
		#uri = QgsDataSourceURI()
		settings = QSettings()
		settings.beginGroup(u"/PostgreSQL/connections")
		settings.beginGroup(connection)
		value = str(settings.value(key))
		settings.endGroup()
		settings.endGroup()
		return value

	def importCSVSlot(self):
		default_pk = "id"
		default_geom = "geom"
		self.db_host="localhost"
		self.db_pwd="29111960"
		self.db_port="5432"
		self.db_name="postgis_21_sample"
		self.db_user="postgres"
		self.db_shema="public"
		conns = self.getConnections()
		for con in conns:
			if con==u"postgis_21_sample":
				self.db_host = self.connection_value(con,u"host")
				#print self.connection_value(con,u"port")
				self.db_name = self.connection_value(con,u"database")
				self.db_user = self.connection_value(con,u"username")
				self.db_pwd = self.connection_value(con,u"password")
		cd = TxtCsvOpenFile(self.iface)
		cd.showDialog()
		time_fmt="_%d%m%Y_%H%M%S"
		layer_name=time.strftime(time_fmt)
		if cd.success:
			from .dlg_import_vector import DlgImportVector
			
			self.vLayer = None
			
			try:
				#uri = "file:///"+cd.filename+("?srsname=EPSG:20023&delimiter=%s&xField=%s&yField=%s" % (",", "3", "2"))
				#self.vLayer = QgsVectorLayer(uri, "layer_name_you_like", "delimitedtext")
				self.vLayer = QgsVectorLayer("Point", "temp_layer"+layer_name, "memory")
				#caps = self.vLayer.dataProvider().capabilities()
				self.vLayer.dataProvider().addAttributes([QgsField("topo_code", QVariant.String), QgsField("Y_coord", QVariant.String),
													QgsField("X_coord", QVariant.String), QgsField("H_value", QVariant.String), QgsField("TOPOFILE", QVariant.String)])
				self.vLayer.updateFields()
				f_obj=open(cd.filename, "rb")
				head, tail = ntpath.split(cd.filename)
				print head
				print tail
				basefn = ntpath.basename(head)
				print basefn
				reader = csv.reader(f_obj, delimiter=',')
				for line in reader:
					mergeFeature = QgsFeature()
					mergeFeature.setFields(self.vLayer.dataProvider().fields())
					mergeFeature.setAttribute("TOPOFILE",tail)
					fcounter=0
					xc=0
					yc=0
					for field in line:
						fcounter=fcounter+1
						if fcounter==1:
							mergeFeature.setAttribute("topo_code",field)
						elif fcounter==2:
							yc=self.tofloat(field)
							mergeFeature.setAttribute("Y_coord",field)
						elif fcounter==3:
							xc=self.tofloat(field)
							mergeFeature.setAttribute("X_coord",field)
						elif fcounter==4:
							mergeFeature.setAttribute("H_value",field)
					#print(str(xc)+":"+str(yc))
					if (xc>0) and (yc>0):
						mergeFeature.setGeometry(QgsGeometry.fromPoint(QgsPoint(float(xc),float(yc))))
						self.vLayer.startEditing()
						self.vLayer.addFeature(mergeFeature, True)
						self.vLayer.commitChanges()
					#print(field)
					#print(line[1])
				merge_reader = csv.reader(open(cd.filename, "rb"), delimiter=',')
				if merge_reader:
					self.mergeCSVWithTopoNodeLayer(merge_reader, tail)
					#return
			except ValueError:
				infoString = "Error loading vector layer from CSV topology file "+uri
				QMessageBox.information(self.iface.mainWindow(),"Error",infoString)
				QMessageBox.information(self, self.tr("Import topology CSV to database"), self.tr(infoString))
				return
			
			schema = self.db_shema
			table = "TOPO_NODES_IMP"+layer_name
			
			# sanity checks
			if self.vLayer is None:
				infoString = "Input layer missing or not valid"
				QMessageBox.information(self.iface.mainWindow(),"Error",infoString)
				QMessageBox.information(self, self.tr("Import topology CSV to database"), self.tr(infoString))
				return
				
			# override cursor
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			# store current input layer crs and encoding, so I can restore it
			#prevInCrs = self.vLayer.crs()
			#prevInEncoding = self.vLayer.dataProvider().encoding()
			
			try:
				# get pk and geom field names from the source layer or use the
				# ones defined by the user
				pk = default_pk #outUri.keyColumn()
				
				#if self.vLayer.hasGeometryType():
				#	geom = outUri.geometryColumn()
				#	geom = geom if geom != "" else default_geom
				#else:
				#	geom = None
				geom = default_geom
				
				# get output params, update output URI
				#outUri.setDataSource( schema, table, geom, "", pk )
				#uri = outUri.uri()
				uri = "dbname='"+self.db_name+"' host="+self.db_host+" port="+self.db_port+" user='"+self.db_user+"'"+\
					  " password='"+self.db_pwd+"' sslmode='allow' table='"+self.db_shema+"'.'TOPO_NODES_IMP"+\
					  layer_name+"' (the_geom) sql="
				
				providerName = 'postgres' #db.dbplugin().providerName()
				
				#infoString = "Trying load vector layer from CSV topology file "+providerName
				#QMessageBox.information(self.iface.mainWindow(),"Trying load topo file",infoString)

				options = {}
				
				options['append'] = True
				
				outCrs = None
				
				# do the import!
				ret, errMsg = QgsVectorLayerImport.importLayer( self.vLayer, uri, providerName, outCrs, False, False, options )
			except Exception as e:
				ret = -1
				errMsg = unicode( e )

			finally:
				# restore input layer crs and encoding
				#self.vLayer.setCrs( prevInCrs )
				#self.vLayer.setProviderEncoding( prevInEncoding )
				# restore cursor
				
				#self.addPostGISLayer('localhost', '5432', 'postgis_21_sample', 'postgres', '29111960',
                #             'public', 'UROVKA_KOLODCI2', None)
				myRangeList = []
				myTargetField = 'field_2'
				# Make our first symbol and range...
				myMin = 0.0
				myMax = 5000000.0
				myLabel = 'Group 1'
				myColour = QColor('#ffee00')

				uri = QgsDataSourceURI()
				# set host name, port, database name, username and password
				uri.setConnection(self.db_host, self.db_port, self.db_name, self.db_user, self.db_pwd)
				# set database schema, table name, geometry column and optionaly
				# subset (WHERE clause)

				uri.setDataSource(self.db_shema, "TOPO_NODES_IMP"+layer_name, "the_geom", "")
				pgLayer = QgsVectorLayer(uri.uri(), "TOPO_NODES_IMP"+layer_name, self.db_user)
				if not pgLayer.isValid():
					raise IOError, "Failed to open the layer"
				mySymbol1 = QgsSymbolV2.defaultSymbol( pgLayer.geometryType())
				#mySymbol1.setColor(myColour)
				#mySymbol1.setAlpha(0)
				myRange1 = QgsRendererRangeV2(
					myMin,
					myMax,
					mySymbol1,
					myLabel)
				#myRangeList.append(myRange1)
				
				myRenderer = QgsGraduatedSymbolRendererV2( '', myRangeList)
				myRenderer.setMode( QgsGraduatedSymbolRendererV2.EqualInterval)
				myRenderer.setClassAttribute(myTargetField)
				props = { 'color' : '255,0,0' }
				sl = QgsSymbolLayerV2Registry.instance().symbolLayerMetadata("SimpleMarker").createSymbolLayer(props)
				s = QgsMarkerSymbolV2([])
				pgLayer.setRendererV2(QgsSingleSymbolRendererV2(s))

				#pgLayer.setRendererV2(myRenderer)
				QgsMapLayerRegistry.instance().addMapLayer(pgLayer)
				QApplication.restoreOverrideCursor()

			if ret != 0:
				#infoString = "Error %d\n%s" % (ret, errMsg)
				#QMessageBox.information(self.iface.mainWindow(),"Failed import",infoString)
				output = QgsMessageViewer()
				output.setTitle( self.tr("Import topology CSV to database") )
				output.setMessageAsPlainText( self.tr("Error %d\n%s") % (ret, errMsg) )
				output.showMessage()
				return
			
			infoString = u"Импорт топоданных из CSV файла"
			QMessageBox.information(self.iface.mainWindow(),u"Импорт выполнен без ошибок",infoString)
		else:
			infoString = u"Топофайл CSV-данных не найден."
			QMessageBox.information(self.iface.mainWindow(),u"Неудачный импорт",infoString)
		#QMessageBox.information(self, self.tr("Import topology CSV to database"), self.tr(infoString))
		#self.mergeWithTopoNodeLayer(pgLayer)
		#infoString = "Merge imported layer was successful."
		#QMessageBox.information(self.iface.mainWindow(),"Success merged imported layer with TOPO_NODES_WATER!",infoString)
		return

	def mergeWithTopoNodeLayer(self, incLayer):
		if not incLayer.isValid():
			raise IOError, "Failed to open the included layer"
		uri = QgsDataSourceURI()
		# set host name, port, database name, username and password
		uri.setConnection(self.db_host, self.db_port, self.db_name, self.db_user, self.db_pwd)
		uri.setDataSource(self.db_shema, "TOPO_NODE_WATER", "the_geom", "")
		consolidLayer = QgsVectorLayer(uri.uri(), "TOPO_NODE_WATER", self.db_user)
		if not consolidLayer.isValid():
			raise IOError, "Failed to open the consolidated layer"
		currIncFeature = QgsFeature()
		inc_feat_iterator = incLayer.getFeatures()
		while inc_feat_iterator.nextFeature(currIncFeature):
			fields = currIncFeature.fields()
			mergeFeature = QgsFeature()
			mergeFeature.setGeometry(currIncFeature.geometry())
			mergeFeature.setFields(consolidLayer.dataProvider().fields())
			mergeFeature.setAttribute("topo_code",currIncFeature.attribute("field_1"))
			mergeFeature.setAttribute("Y_coord",currIncFeature.attribute("field_2"))
			mergeFeature.setAttribute("X_coord",currIncFeature.attribute("field_3"))
			mergeFeature.setAttribute("H_value",currIncFeature.attribute("field_4"))
			consolidLayer.startEditing()
			consolidLayer.addFeature(mergeFeature, True)
			consolidLayer.commitChanges()

	def mergeCSVWithTopoNodeLayer(self, reader, fntile):
		items = ("TOPO_NODE_WATER", "TOPO_NODE_KANAL")
		item, ok = QInputDialog.getItem(self, 'Input Dialog', 'Enter your name:', items, 0, False)
		if not ok:
			return
		uri = QgsDataSourceURI()
		# set host name, port, database name, username and password
		uri.setConnection(self.db_host, self.db_port, self.db_name, self.db_user, self.db_pwd)
		uri.setDataSource(self.db_shema, item, "the_geom", "")
		consolidLayer = QgsVectorLayer(uri.uri(), item, self.db_user)
		if not consolidLayer.isValid():
			raise IOError, u"Ошибка открытия консолидирующего слоя "+item
		print("Start merging CSV...")

		request = QgsFeatureRequest().setFilterExpression( '"TOPOFILE" = \''+fntile+'\'' )
		itFeature = QgsFeature()
		hasPrevTopo = False
		it = consolidLayer.getFeatures( request )
		if it.nextFeature(itFeature):
			hasPrevTopo = True

		duplicate_cnt=0
		go_cnt=0
		if hasPrevTopo:
			reply = QMessageBox.question(self.iface.mainWindow(),u"В базу данных загружались данные из файла с таким же именем",
										 u"Продолжить?", QMessageBox.Apply, QMessageBox.Cancel)
			if reply==QMessageBox.Cancel:
				return
		for line in reader:
			mergeFeature = QgsFeature()
			mergeFeature.setFields(consolidLayer.dataProvider().fields())
			mergeFeature.setAttribute("TOPOFILE",fntile)
			fcounter=0
			xc=0
			yc=0
			for field in line:
				fcounter=fcounter+1
				if fcounter==1:
					mergeFeature.setAttribute("topo_code",field)
				elif fcounter==2:
					yc=self.tofloat(field)
					mergeFeature.setAttribute("Y_coord",yc)
				elif fcounter==3:
					xc=self.tofloat(field)
					mergeFeature.setAttribute("X_coord",xc)
				elif fcounter==4:
					mergeFeature.setAttribute("H_value",field)
			if (xc>0) and (yc>0):
				mergeFeature.setGeometry(QgsGeometry.fromPoint(QgsPoint(float(xc),float(yc))))
				request = QgsFeatureRequest().setFilterExpression( '"X_coord" = \''+str(xc)+'\' AND "Y_coord" = \''+str(yc)+'\'' )
				itFeature = QgsFeature()
				it = consolidLayer.getFeatures( request )
				if it.nextFeature(itFeature):
					#print "yyyyyyyyyyyyeeeeeeesssssssss===>>>"+str(xc)+":"+str(yc)
					duplicate_cnt = duplicate_cnt+1
				else:
					#print "no"+' "X_coord" = '+str(xc)+' AND "Y_coord" = '+str(yc)
					consolidLayer.startEditing()
					consolidLayer.addFeature(mergeFeature, True)
					consolidLayer.commitChanges()
					go_cnt = go_cnt+1
				#print(str(xc)+"-:-"+str(yc))
		self.iface.setActiveLayer(consolidLayer)
		consolidLayer.triggerRepaint()
		infoString = u"Объединение импортированного слоя со слоем в БД, повторяющихся и неперенесенных - "+str(duplicate_cnt)+u", перенесенных - "+str(go_cnt)
		QMessageBox.information(self.iface.mainWindow(),u"Завершен процесс объединения импортированного слоя с "+item,infoString)
		
	def addPostGISLayer(self, host, port, dbname, username, password, schema, table, geom_col):
		uri = QgsDataSourceURI()
		uri.setConnection(str(host), str(port), str(dbname), str(username), str(password))
		uri.setDataSource(str(schema), str(table), str(geom_col)) #, '', str(key_col))
		vlayer = QgsVectorLayer(uri.uri(), str('test'), self.db_user)
		# QgsMapLayerRegistry.instance().addMapLayer(vlayer)
		if not vlayer.isValid():
			msgbox('Layer not loaded', uri.host(), uri.database(), uri.port(), uri.username(), 
				uri.password(), uri.schema(), uri.table(), uri.geometryColumn())

	def exportActionSlot(self):
		table = self.tree.currentTable()
		if table is None:
			self.infoBar.pushMessage(self.tr("Select the table you want export to file."), QgsMessageBar.INFO, self.iface.messageTimeout())
			return

		inLayer = table.toMapLayer()

		from .dlg_export_vector import DlgExportVector
		dlg = DlgExportVector(inLayer, table.database(), self)
		dlg.exec_()

		inLayer.deleteLater()

	def runSqlWindow(self):
		db = self.tree.currentDatabase()
		if db == None:
			self.infoBar.pushMessage(self.tr("No database selected or you are not connected to it."), QgsMessageBar.INFO, self.iface.messageTimeout())
			return

		from dlg_sql_window import DlgSqlWindow
		dlg = DlgSqlWindow(self.iface, db, self)
		#refreshDb = lambda x: self.refreshItem( db.connection() ) # refresh the database tree
		#self.connect( dlg, SIGNAL( "queryExecuted(const QString &)" ), refreshDb )
		dlg.show()
		dlg.exec_()


	def showSystemTables(self):
		self.tree.showSystemTables( self.actionShowSystemTables.isChecked() )


	def registerAction(self, action, menuName, callback=None):
		""" register an action to the manager's main menu """
		if not hasattr(self, '_registeredDbActions'):
			self._registeredDbActions = {}

		if callback != None:
			invoke_callback = lambda x: self.invokeCallback( callback )

		if menuName == None or menuName == "":
			self.addAction( action )

			if not self._registeredDbActions.has_key(menuName):
				self._registeredDbActions[menuName] = list()
			self._registeredDbActions[menuName].append(action)

			if callback != None:
				QObject.connect( action, SIGNAL("triggered(bool)"), invoke_callback )
			return True

		# search for the menu
		actionMenu = None
		helpMenuAction = None
		for a in self.menuBar.actions():
			if not a.menu() or a.menu().title() != menuName:
				continue
			if a.menu() != self.menuHelp:
				helpMenuAction = a

			actionMenu = a
			break

		# not found, add a new menu before the help menu
		if actionMenu == None:
			menu = QMenu(menuName, self)
			if helpMenuAction != None:
				actionMenu = self.menuBar.insertMenu(helpMenuAction, menu)
			else:
				actionMenu = self.menuBar.addMenu(menu)

		menu = actionMenu.menu()
		menuActions = menu.actions()

		# get the placeholder's position to insert before it
		pos = 0
		for pos in range(len(menuActions)):
			if menuActions[pos].isSeparator() and menuActions[pos].objectName().endswith("_placeholder"):
				menuActions[pos].setVisible(True)
				break

		if pos < len(menuActions):
			before = menuActions[pos]
			menu.insertAction( before, action )
		else:
			menu.addAction( action )

		actionMenu.setVisible(True)	# show the menu

		if not self._registeredDbActions.has_key(menuName):
			self._registeredDbActions[menuName] = list()
		self._registeredDbActions[menuName].append(action)

		if callback != None:
			QObject.connect( action, SIGNAL("triggered(bool)"), invoke_callback )

		return True


	def invokeCallback(self, callback, params=None):
		""" Call a method passing the selected item in the database tree,
			the sender (usually a QAction), the plugin mainWindow and
			optionally additional parameters.

			This method takes care to override and restore the cursor,
			but also catches exceptions and displays the error dialog.
		"""
		QApplication.setOverrideCursor(Qt.WaitCursor)
		try:
			if params is None:
				callback( self.tree.currentItem(), self.sender(), self )
			else:
				callback( self.tree.currentItem(), self.sender(), self, *params )

		except BaseError, e:
			# catch database errors and display the error dialog
			DlgDbError.showError(e, self)
			return

		finally:
			QApplication.restoreOverrideCursor()


	def unregisterAction(self, action, menuName):
		if not hasattr(self, '_registeredDbActions'):
			return

		if menuName == None or menuName == "":
			self.removeAction( action )

			if self._registeredDbActions.has_key(menuName):
				if self._registeredDbActions[menuName].count( action ) > 0:
					self._registeredDbActions[menuName].remove( action )

			action.deleteLater()
			return True

		for a in self.menuBar.actions():
			if not a.menu() or a.menu().title() != menuName:
				continue

			menu = a.menu()
			menuActions = menu.actions()

			menu.removeAction( action )
			if menu.isEmpty():	# hide the menu
				a.setVisible(False)

			if self._registeredDbActions.has_key(menuName):
				if self._registeredDbActions[menuName].count( action ) > 0:
					self._registeredDbActions[menuName].remove( action )

				# hide the placeholder if there're no other registered actions
				if len(self._registeredDbActions[menuName]) <= 0:
					for i in range(len(menuActions)):
						if menuActions[i].isSeparator() and menuActions[i].objectName().endswith("_placeholder"):
							menuActions[i].setVisible(False)
							break

			action.deleteLater()
			return True

		return False

	def unregisterAllActions(self):
		if not hasattr(self, '_registeredDbActions'):
			return

		for menuName in self._registeredDbActions:
			for action in list(self._registeredDbActions[menuName]):
				self.unregisterAction( action, menuName )
		del self._registeredDbActions

	def setupUi(self):
		self.setWindowTitle(self.tr("DB Manager"))
		self.setWindowIcon(QIcon(":/db_manager/icon"))
		self.resize(QSize(700,500).expandedTo(self.minimumSizeHint()))

		# create central tab widget
		self.tabs = QTabWidget()
		self.info = InfoViewer(self)
		self.tabs.addTab(self.info, self.tr("Info"))
		self.table = TableViewer(self)
		self.tabs.addTab(self.table, self.tr("Table"))
		self.preview = LayerPreview(self)
		self.tabs.addTab(self.preview, self.tr("Preview"))
		self.setCentralWidget(self.tabs)

		# Creates layout for message bar
		self.layout = QGridLayout(self.info)
		self.layout.setContentsMargins(0, 0, 0, 0)
		spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.layout.addItem(spacerItem, 1, 0, 1, 1)
		# init messageBar instance
		self.infoBar = QgsMessageBar(self.info)
		sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
		self.infoBar.setSizePolicy(sizePolicy)
		self.layout.addWidget(self.infoBar, 0, 0, 1, 1)

		# create database tree
		self.dock = QDockWidget("Tree", self)
		self.dock.setObjectName("DB_Manager_DBView")
		self.dock.setFeatures(QDockWidget.DockWidgetMovable)
		self.tree = DBTree(self)
		self.dock.setWidget(self.tree)
		self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

		# create status bar
		self.statusBar = QStatusBar(self)
		self.setStatusBar(self.statusBar)

		# create menus
		self.menuBar = QMenuBar(self)
		self.menuDb = QMenu(self.tr("&Database"), self)
		actionMenuDb = self.menuBar.addMenu(self.menuDb)
		self.menuSchema = QMenu(self.tr("&Schema"), self)
		actionMenuSchema = self.menuBar.addMenu(self.menuSchema)
		self.menuTable = QMenu(self.tr("&Table"), self)
		actionMenuTable = self.menuBar.addMenu(self.menuTable)
		
		self.menuHelp = None # QMenu(self.tr("&Help"), self)
		#actionMenuHelp = self.menuBar.addMenu(self.menuHelp)

		self.setMenuBar(self.menuBar)

		# create toolbar
		self.toolBar = QToolBar("Default", self)
		self.toolBar.setObjectName("DB_Manager_ToolBar")
		self.addToolBar(self.toolBar)

		# create menus' actions

		# menu DATABASE
		sep = self.menuDb.addSeparator(); sep.setObjectName("DB_Manager_DbMenu_placeholder"); sep.setVisible(False)
		self.actionRefresh = self.menuDb.addAction( QIcon(":/db_manager/actions/refresh"), self.tr("&Refresh"), self.refreshActionSlot, QKeySequence("F5") )
		self.actionSqlWindow = self.menuDb.addAction( QIcon(":/db_manager/actions/sql_window"), self.tr("&SQL window"), self.runSqlWindow, QKeySequence("F2") )
		self.menuDb.addSeparator()
		self.actionClose = self.menuDb.addAction( QIcon(), self.tr("&Exit"), self.close, QKeySequence("CTRL+Q") )

		# menu SCHEMA
		sep = self.menuSchema.addSeparator(); sep.setObjectName("DB_Manager_SchemaMenu_placeholder"); sep.setVisible(False)
		actionMenuSchema.setVisible(False)

		# menu TABLE
		sep = self.menuTable.addSeparator(); sep.setObjectName("DB_Manager_TableMenu_placeholder"); sep.setVisible(False)
		self.actionImport = self.menuTable.addAction( QIcon(":/db_manager/actions/import"), self.tr("&Import layer/file"), self.importActionSlot )
		self.actionExport = self.menuTable.addAction( QIcon(":/db_manager/actions/export"), self.tr("&Export to file"), self.exportActionSlot )
		self.menuTable.addSeparator()
		#self.menuImportCSV = QMenu(self.tr("&Import CSV (Poltarokov&Fundukyan Development)"), self)
		#actionImportCSV = self.menuBar.addMenu(self.menuTable)
		self.actionImportCSV = self.menuTable.addAction( QIcon(":/db_manager/actions/import"), self.tr("&Import CSV Topology file (Poltarokov/Fundukyan Development)"), self.importCSVSlot )
		#self.actionShowSystemTables = self.menuTable.addAction(self.tr("Show system tables/views"), self.showSystemTables)
		#self.actionShowSystemTables.setCheckable(True)
		#self.actionShowSystemTables.setChecked(True)
		self.menuTable.addSeparator()
		actionMenuTable.setVisible(False)

		# add actions to the toolbar
		self.toolBar.addAction( self.actionRefresh )
		self.toolBar.addAction( self.actionSqlWindow )
		self.toolBar.addAction( self.actionImport )
		self.toolBar.addAction( self.actionExport )
