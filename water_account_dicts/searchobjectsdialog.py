# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'searchobjectsdialog.ui'
#
# Created: Tue May  5 00:41:09 2015
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

class Ui_searchObjectsDialog(object):
    def setupUi(self, searchObjectsDialog):
        searchObjectsDialog.setObjectName(_fromUtf8("searchObjectsDialog"))
        searchObjectsDialog.resize(443, 387)
        self.searchTypesTabWidget = QtGui.QTabWidget(searchObjectsDialog)
        self.searchTypesTabWidget.setGeometry(QtCore.QRect(0, 0, 441, 381))
        self.searchTypesTabWidget.setObjectName(_fromUtf8("searchTypesTabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.street1Edit = QtGui.QLineEdit(self.tab)
        self.street1Edit.setGeometry(QtCore.QRect(30, 50, 371, 20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.street1Edit.sizePolicy().hasHeightForWidth())
        self.street1Edit.setSizePolicy(sizePolicy)
        self.street1Edit.setObjectName(_fromUtf8("street1Edit"))
        self.street2Edit = QtGui.QLineEdit(self.tab)
        self.street2Edit.setGeometry(QtCore.QRect(30, 100, 371, 20))
        self.street2Edit.setObjectName(_fromUtf8("street2Edit"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(30, 30, 47, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(30, 80, 47, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.search2StrButton = QtGui.QPushButton(self.tab)
        self.search2StrButton.setGeometry(QtCore.QRect(170, 150, 91, 23))
        self.search2StrButton.setObjectName(_fromUtf8("search2StrButton"))
        self.searchTypesTabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.streetAdrEdit = QtGui.QLineEdit(self.tab_2)
        self.streetAdrEdit.setGeometry(QtCore.QRect(30, 50, 371, 20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.streetAdrEdit.sizePolicy().hasHeightForWidth())
        self.streetAdrEdit.setSizePolicy(sizePolicy)
        self.streetAdrEdit.setObjectName(_fromUtf8("streetAdrEdit"))
        self.label_3 = QtGui.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(30, 30, 47, 13))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.houseNumAdrSBox = QtGui.QSpinBox(self.tab_2)
        self.houseNumAdrSBox.setGeometry(QtCore.QRect(30, 100, 371, 22))
        self.houseNumAdrSBox.setObjectName(_fromUtf8("houseNumAdrSBox"))
        self.label_4 = QtGui.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(30, 80, 47, 13))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.searchAdrButton = QtGui.QPushButton(self.tab_2)
        self.searchAdrButton.setGeometry(QtCore.QRect(170, 150, 91, 23))
        self.searchAdrButton.setObjectName(_fromUtf8("searchAdrButton"))
        self.searchTypesTabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.coord1DSpBox = QtGui.QDoubleSpinBox(self.tab_3)
        self.coord1DSpBox.setGeometry(QtCore.QRect(30, 50, 371, 22))
        self.coord1DSpBox.setObjectName(_fromUtf8("coord1DSpBox"))
        self.coord2DSpBox = QtGui.QDoubleSpinBox(self.tab_3)
        self.coord2DSpBox.setGeometry(QtCore.QRect(30, 100, 371, 22))
        self.coord2DSpBox.setObjectName(_fromUtf8("coord2DSpBox"))
        self.label_6 = QtGui.QLabel(self.tab_3)
        self.label_6.setGeometry(QtCore.QRect(30, 30, 47, 13))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.tab_3)
        self.label_7.setGeometry(QtCore.QRect(30, 80, 47, 13))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.searchCoordButton = QtGui.QPushButton(self.tab_3)
        self.searchCoordButton.setGeometry(QtCore.QRect(170, 150, 91, 23))
        self.searchCoordButton.setObjectName(_fromUtf8("searchCoordButton"))
        self.searchTypesTabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.label_5 = QtGui.QLabel(self.tab_4)
        self.label_5.setGeometry(QtCore.QRect(170, 70, 91, 20))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.searchTypesTabWidget.addTab(self.tab_4, _fromUtf8(""))

        self.retranslateUi(searchObjectsDialog)
        self.searchTypesTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(searchObjectsDialog)

    def retranslateUi(self, searchObjectsDialog):
        searchObjectsDialog.setWindowTitle(_translate("searchObjectsDialog", "Найти объекты...", None))
        self.label.setText(_translate("searchObjectsDialog", "Улица 1", None))
        self.label_2.setText(_translate("searchObjectsDialog", "Улица 2", None))
        self.search2StrButton.setText(_translate("searchObjectsDialog", "ИСКАТЬ", None))
        self.searchTypesTabWidget.setTabText(self.searchTypesTabWidget.indexOf(self.tab), _translate("searchObjectsDialog", "Перекресток", None))
        self.label_3.setText(_translate("searchObjectsDialog", "<html><head/><body><p>Улица</p></body></html>", None))
        self.label_4.setText(_translate("searchObjectsDialog", "TextLabel", None))
        self.searchAdrButton.setText(_translate("searchObjectsDialog", "ИСКАТЬ", None))
        self.searchTypesTabWidget.setTabText(self.searchTypesTabWidget.indexOf(self.tab_2), _translate("searchObjectsDialog", "Адрес", None))
        self.label_6.setText(_translate("searchObjectsDialog", "Широта", None))
        self.label_7.setText(_translate("searchObjectsDialog", "Долгота ", None))
        self.searchCoordButton.setText(_translate("searchObjectsDialog", "ИСКАТЬ", None))
        self.searchTypesTabWidget.setTabText(self.searchTypesTabWidget.indexOf(self.tab_3), _translate("searchObjectsDialog", "Точка координат", None))
        self.label_5.setText(_translate("searchObjectsDialog", "В  разработке. . .", None))
        self.searchTypesTabWidget.setTabText(self.searchTypesTabWidget.indexOf(self.tab_4), _translate("searchObjectsDialog", "Объект", None))

