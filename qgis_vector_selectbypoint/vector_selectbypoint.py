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
# Import the PyQt and QGIS libraries fr
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from vector_selectbypointdialog import vector_selectbypointDialog
from vector_toponodedialog import vector_toponodeDialog
#from lineMapTool import lineMapTool
#from lineMapPanTool import lineMapPanTool
import os.path


class vector_selectbypoint:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        
        # Reference map canvas
        self.canvas = self.iface.mapCanvas()
        
        # Emit QgsPoint after each click on canvas
        self.clickTool = QgsMapToolEmitPoint(self.canvas)
        self.previousLayer = None
        self.index = None
        
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'vector_selectbypoint_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = vector_selectbypointDialog()
        self.attrDlg = vector_toponodeDialog()
        
        # Create the GUI
        self.canvas.setMapTool( self.clickTool )
        self.prev_np_name="";
        self.prev_street_name="";
        self.prev_pipe_mname="";
        self.prev_pipe_diam=0;
        self.prev_well_mname="";
        self.prev_well_fname="";
        #self.lineTool = lineMapPanTool( self.canvas)
        #self.canvas.setMapTool(self.lineTool)
        #print "set map tool"

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(os.path.dirname(__file__) +"/icon.png"),
                              u"ПРАВКА ТОПОГРАФИЧЕСКИХ ОБЪЕКТОВ PolFunDev QGIS-plugin", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)
        self.action.setCheckable(True)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"ПРАВКА ТОПОГРАФИЧЕСКИХ ОБЪЕКТОВ PolFunDev QGIS-plugin", self.action)
        
        # Signal connections for mouse clicks
        QObject.connect(self.dlg.ui.chkActivate,SIGNAL("stateChanged(int)"),self.changeActive)
        #QMessageBox.information( self.iface.mainWindow(),  "Info",  "connect = %s" %str(result) )

    def changeActive(self,state):
        #print "ssssssfffff"
        if (state==Qt.Checked):
            self.canvas.mapTool().deactivate()
            #print "rrrrr"
            self.canvas.setMapTool( self.clickTool )
            QObject.connect(self.clickTool,  SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"),  self.handleMouseDown)
        else:
            QObject.disconnect(self.clickTool,  SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"),  self.handleMouseDown)

    def changeOnChecked(self,checked):
        #print "rrrrrttttt"
        if (checked):
            self.canvas.mapTool().deactivate()
            #print "sssssss"
            self.canvas.setMapTool( self.clickTool )
            QObject.connect(self.clickTool,  SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"),  self.handleMouseDown)
            #self.canvas.setMapTool(self.lineTool)
            #print "set map tool"
        else:
            QObject.disconnect(self.clickTool,  SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"),  self.handleMouseDown)

    def handleMouseDown(self,  point,  button):
        #QMessageBox.information( self.iface.mainWindow(),  "Info",  "X,Y = %s, %s" % (str(point.x()), str(point.y())) )
        self.canvasClick(point, button)
        #self.dlg.clearTextBrowser()
        #self.dlg.setTextBrowser( str(point.x()) + " , " + str(point.y()) )

    def canvasClick(self,  point,  button):
        layers = self.iface.legendInterface().layers()
        items = (u"TOPO_NODE_WATER", u"TOPO_NODE_KANAL")
        item, ok = QInputDialog.getItem(self.iface.mainWindow(), u'Слой для правки', u'Выберите слой:', items, 0, False)
        if not ok:
            return
        for layer in layers:
            layerType = layer.type()
            if layerType == QgsMapLayer.VectorLayer:
                if layer.name()==item:
                    self.iface.setActiveLayer(layer)
                if layer.name()==u'WATER_BRANCH' or layer.name()==u'ВОДОПРОВОД':
                    self.wb_layer=layer
                    #QMessageBox.information( self.iface.mainWindow(),  "layer.name()",  "layer="+layer.name() )

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
            self.attrDlg.fillAttrData(closestFeature, layer, self, self.wb_layer)
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
        # Activate click tool
        # show the dialog
        if self.action.isChecked():
            self.changeOnChecked(True)
            #self.dlg.show()
            # Run the dialog event loop
            #result = self.dlg.exec_()
            # See if OK was pressed
            #if result == 1:
                # do something useful (delete the line containing pass and
                # substitute with your code)
                #pass
        else:
            self.changeOnChecked(False)
