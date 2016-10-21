# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wateraccountdicts.ui'
#
# Created: Fri Jan 30 08:30:13 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_waterAcntDictsDialog(object):
    def setupUi(self, waterAcntDictsDialog):
        waterAcntDictsDialog.setObjectName(_fromUtf8("waterAcntDictsDialog"))
        waterAcntDictsDialog.resize(640, 512)
        self.tabWidgetDicts = QtGui.QTabWidget(waterAcntDictsDialog)
        self.tabWidgetDicts.setGeometry(QtCore.QRect(0, 0, 641, 511))
        self.tabWidgetDicts.setObjectName(_fromUtf8("tabWidgetDicts"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.StreetsTView = QtGui.QTableView(self.tab)
        self.StreetsTView.setGeometry(QtCore.QRect(0, 0, 631, 481))
        self.StreetsTView.setObjectName(_fromUtf8("StreetsTView"))
        self.tabWidgetDicts.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidgetDicts.addTab(self.tab_2, _fromUtf8(""))

        self.retranslateUi(waterAcntDictsDialog)
        self.tabWidgetDicts.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(waterAcntDictsDialog)

    def retranslateUi(self, waterAcntDictsDialog):
        waterAcntDictsDialog.setWindowTitle(_translate("waterAcntDictsDialog", "Dialog", None))
        self.tabWidgetDicts.setTabText(self.tabWidgetDicts.indexOf(self.tab), _translate("waterAcntDictsDialog", "Улицы", None))
        self.tabWidgetDicts.setTabText(self.tabWidgetDicts.indexOf(self.tab_2), _translate("waterAcntDictsDialog", "Материалы", None))

