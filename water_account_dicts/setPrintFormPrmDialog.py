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
import math
from PyQt4 import QtCore, QtGui
from setPrintFormParams import Ui_setPrintFormPrmDialog
# create the dialog for zoom to point

class setPrintFormParamsDialog(QtGui.QDialog, Ui_setPrintFormPrmDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_setPrintFormPrmDialog()
        self.ui.setupUi(self)
        self.rwd = -1
        self.rht = -1
        self.rx = 0
        self.ry = 0
        self.sc = 0
        self.ui.canvasTypeCBox.addItem(u"Горизонтально 1 - A4")
        self.ui.canvasTypeCBox.addItem(u"Вертикально 1 - A4")
        self.ui.canvasTypeCBox.addItem(u"Горизонтально 2(2*1) - A3")
        self.ui.canvasTypeCBox.addItem(u"Вертикально 2(2*1) - A3")
        self.ui.canvasTypeCBox.addItem(u"Горизонтально 4(2*2) - A2")
        self.ui.canvasTypeCBox.addItem(u"Вертикально 4(2*2) - A2")
        self.ui.canvasTypeCBox.addItem(u"Горизонтально 8 - A1")
        self.ui.canvasTypeCBox.addItem(u"Вертикально 8 - A1")
        self.ui.canvasTypeCBox.addItem(u"Горизонтально 16 - A0")
        self.ui.canvasTypeCBox.addItem(u"Вертикально 16 - A0")		
        self.ui.canvasTypeCBox.currentIndexChanged.connect(self.changeCSize)
        self.ui.atlasOrientTypeCBox.currentIndexChanged.connect(self.changeAtlasOrientation)
        self.ui.scaleSBox.valueChanged.connect(self.scaleValueChanged)
        self.ui.scaleSBox.setMinimum(300)
        self.ui.wElmCountSBox.valueChanged.connect(self.wElmValueChanged)
        self.ui.hElmCountSBox.valueChanged.connect(self.hElmValueChanged)
        self.ui.recalcWHModeChkBox.stateChanged.connect(self.recalcModeChanged)
        self.ui.wElmCountSBox.setDisabled(True)
        self.ui.hElmCountSBox.setDisabled(True)
        self.parent = parent
        self.width = 297
        self.height = 210
        self.zoom_level = 0.5
        self.ui.scaleSBox.setProperty("value", 30472)
        self.setWindowTitle(u"Установка параметров Атласа")
        self.ui.label_3.setText(u"Ориентация фрагмента Атласа")
        self.ui.label.setText(u"Размер Атласа (один А4 - по умолч.)")
		
    def showDlg(self, rwd, rht, rx, ry, sc):
        self.rwd = rwd
        self.rht = rht
        self.rx = rx
        self.ry = ry
        self.sc = sc
        self.ssc = sc
        self.ui.scaleSBox.setProperty("value", self.sc)
        self.show()
        self.psizesPrChange = False
		
    def recalcModeChanged(self):
        if self.ui.recalcWHModeChkBox.isChecked():
            self.ui.wElmCountSBox.setDisabled(False)
            self.ui.hElmCountSBox.setDisabled(False)
            self.ui.scaleSBox.setDisabled(True)
        else:
            self.ui.wElmCountSBox.setDisabled(True)
            self.ui.hElmCountSBox.setDisabled(True)
            self.ui.scaleSBox.setDisabled(False)

    def recalcXYCnts(self):
        if self.rwd>0 and self.rht>0 and not self.ui.recalcWHModeChkBox.isChecked():
            self.sc = self.ui.scaleSBox.value()
            self.dist_unit=self.sc/1000; #21.555555/self.correct_coeff #коэффициент единицы карты мкс 23 для см листа
            if self.ui.atlasOrientTypeCBox.currentIndex()==0:
                self.hor_width_cnt=math.ceil(self.rwd/self.dist_unit/297);
                self.ver_width_cnt=math.ceil(self.rht/self.dist_unit/210);
            else:
                self.hor_width_cnt=math.ceil(self.rwd/self.dist_unit/210);
                self.ver_width_cnt=math.ceil(self.rht/self.dist_unit/297);
            self.ui.wElmCountSBox.setProperty("value", self.hor_width_cnt)
            self.ui.hElmCountSBox.setProperty("value", self.ver_width_cnt)
			
    def recalcScaleOnXY(self):
        if self.rwd>0 and self.rht>0 and self.ui.recalcWHModeChkBox.isChecked(): #and not self.psizesPrChange:
			#self.rwd = self.ui.wElmCountSBox.value*(calc_sc/1000)*297
			#self.rht = self.ui.hElmCountSBox.value*(calc_sc/1000)*210
            #self.sc = self.ui.scaleSBox.value()
            #self.dist_unit=self.sc/1000; #21.555555/self.correct_coeff #коэффициент единицы карты мкс 23 для см листа
            print str(self.rwd)+'==='+str(self.rht)
            if self.ui.atlasOrientTypeCBox.currentIndex()==0:
                calc_sc1 = 1000.0*((self.rwd+0.0)/((self.ui.wElmCountSBox.value()+0.0)*(297+0.0)))	
                calc_sc2 = 1000.0*((self.rht+0.0)/((self.ui.hElmCountSBox.value()+0.0)*(210+0.0)))				
                #self.hor_width_cnt=math.ceil(self.rwd/self.dist_unit/297);
                #self.ver_width_cnt=math.ceil(self.rht/self.dist_unit/210);
            else:
                calc_sc1 = 1000.0*((self.rwd+0.0)/((self.ui.wElmCountSBox.value()+0.0)*(210+0.0)))
                calc_sc2 = 1000.0*((self.rht+0.0)/((self.ui.hElmCountSBox.value()+0.0)*(297+0.0)))
                #self.hor_width_cnt=math.ceil(self.rwd/self.dist_unit/210);
                #self.ver_width_cnt=math.ceil(self.rht/self.dist_unit/297);
            #self.ui.wElmCountSBox.setProperty("value", self.hor_width_cnt)
            #self.ui.hElmCountSBox.setProperty("value", self.ver_width_cnt)
            calc_sc=calc_sc1
            if calc_sc1<calc_sc2:
                calc_sc=calc_sc2
            self.ui.scaleSBox.setValue(calc_sc)
            #self.psizesPrChange = True
            #self.sc = self.ui.scaleSBox.value()
            #self.dist_unit=self.sc/1000; #21.555555/self.correct_coeff #коэффициент единицы карты мкс 23 для см листа
            #if self.ui.atlasOrientTypeCBox.currentIndex()==0:
            #    self.hor_width_cnt=math.ceil(self.rwd/self.dist_unit/297);
            #    self.ver_width_cnt=math.ceil(self.rht/self.dist_unit/210);
            #else:
            #    self.hor_width_cnt=math.ceil(self.rwd/self.dist_unit/210);
            #    self.ver_width_cnt=math.ceil(self.rht/self.dist_unit/297);
            #self.ui.wElmCountSBox.setProperty("value", self.hor_width_cnt)
            #self.ui.hElmCountSBox.setProperty("value", self.ver_width_cnt)
            #self.psizesPrChange = False


    def changeAtlasOrientation(self):
        self.recalcXYCnts()
		
    def scaleValueChanged(self):
        self.recalcXYCnts()
		
    def wElmValueChanged(self):
        print "wElmValueChanged"
        self.recalcScaleOnXY()
		
    def hElmValueChanged(self):
        print "hElmValueChanged"
        self.recalcScaleOnXY()
		
    def changeCSize(self):
        self.ui.scaleSBox.setProperty("value", 30472)
        if self.ui.canvasTypeCBox.currentIndex()==0 or self.ui.canvasTypeCBox.currentIndex()==1:
            self.ui.scaleSBox.setProperty("value", 30472)
            if self.ui.canvasTypeCBox.currentIndex()==0:
                self.width = 297
                self.height = 210
                self.zoom_level = 0.5                
            else:
                self.width = 210
                self.height = 297
                self.zoom_level = 0.5
        elif self.ui.canvasTypeCBox.currentIndex()==2 or self.ui.canvasTypeCBox.currentIndex()==3:
            self.ui.scaleSBox.setProperty("value", 25500)
            if self.ui.canvasTypeCBox.currentIndex()==2:
                self.width = 420
                self.height = 297
                self.zoom_level = 0.35                
            else:
                self.width = 297
                self.height = 420
                self.zoom_level = 0.35
        elif self.ui.canvasTypeCBox.currentIndex()==4 or self.ui.canvasTypeCBox.currentIndex()==5:
            self.ui.scaleSBox.setProperty("value", 18508)
            if self.ui.canvasTypeCBox.currentIndex()==4:
                self.width = 594
                self.height = 420
                self.zoom_level = 0.25                
            else:
                self.width = 420
                self.height = 594
                self.zoom_level = 0.25
        elif self.ui.canvasTypeCBox.currentIndex()==6 or self.ui.canvasTypeCBox.currentIndex()==7:
            self.ui.scaleSBox.setProperty("value", 11000)
            if self.ui.canvasTypeCBox.currentIndex()==6:
                self.width = 841
                self.height = 594
                self.zoom_level = 0.125                
            else:
                self.width = 594
                self.height = 841
                self.zoom_level = 0.125
        elif self.ui.canvasTypeCBox.currentIndex()==8 or self.ui.canvasTypeCBox.currentIndex()==9:
            self.ui.scaleSBox.setProperty("value", 7000)
            if self.ui.canvasTypeCBox.currentIndex()==8:
                self.width = 1189
                self.height = 841
                self.zoom_level = 0.063                
            else:
                self.width = 841
                self.height = 1189
                self.zoom_level = 0.063
				
    def accept(self):
        self.parent.runAtlasReport( self.ui.canvasTypeCBox.currentText(), self.ui.scaleSBox.value(), self.ui.canvasTypeCBox.currentIndex(), self.width, self.height, self.zoom_level, self.ui.atlasOrientTypeCBox.currentIndex())
        return QtGui.QDialog.accept(self)

    def reject(self):
        #self.parent.runAutoReport( self.ui.canvasTypeCBox.currentText(), self.ui.scaleSBox.value(), self.ui.canvasTypeCBox.currentIndex(), self.width, self.height, self.zoom_level)
        return QtGui.QDialog.reject(self)
