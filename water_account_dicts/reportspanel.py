# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reportspanel.ui'
#
# Created: Fri May 29 01:18:26 2015
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

class Ui_reportGenDialog(object):
    def setupUi(self, reportGenDialog):
        reportGenDialog.setObjectName(_fromUtf8("reportGenDialog"))
        reportGenDialog.resize(733, 387)
        self.groupBox = QtGui.QGroupBox(reportGenDialog)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 731, 101))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.repTypeCBox = QtGui.QComboBox(self.groupBox)
        self.repTypeCBox.setGeometry(QtCore.QRect(8, 20, 321, 22))
        self.repTypeCBox.setObjectName(_fromUtf8("repTypeCBox"))
        self.repTypeCBox.addItem(_fromUtf8(""))
        self.repTypeCBox.addItem(_fromUtf8(""))
        self.generateRepPButton = QtGui.QPushButton(self.groupBox)
        self.generateRepPButton.setGeometry(QtCore.QRect(370, 20, 131, 23))
        self.generateRepPButton.setObjectName(_fromUtf8("generateRepPButton"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 50, 141, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.startDTEdit = QtGui.QDateEdit(self.groupBox)
        self.startDTEdit.setGeometry(QtCore.QRect(200, 70, 81, 22))
        self.startDTEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2015, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startDTEdit.setObjectName(_fromUtf8("startDTEdit"))
        self.endDTEdit = QtGui.QDateEdit(self.groupBox)
        self.endDTEdit.setGeometry(QtCore.QRect(290, 70, 81, 22))
        self.endDTEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2016, 1, 1), QtCore.QTime(0, 0, 0)))
        self.endDTEdit.setObjectName(_fromUtf8("endDTEdit"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(200, 50, 81, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(290, 50, 81, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.regionCBox = QtGui.QComboBox(self.groupBox)
        self.regionCBox.setGeometry(QtCore.QRect(10, 70, 181, 22))
        self.regionCBox.setEditable(True)
        self.regionCBox.setObjectName(_fromUtf8("regionCBox"))
        self.groupBox_2 = QtGui.QGroupBox(reportGenDialog)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 100, 731, 281))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.outGenTWidget = QtGui.QTabWidget(self.groupBox_2)
        self.outGenTWidget.setGeometry(QtCore.QRect(10, 20, 711, 261))
        self.outGenTWidget.setObjectName(_fromUtf8("outGenTWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.reportWebView = QtWebKit.QWebView(self.tab)
        self.reportWebView.setGeometry(QtCore.QRect(0, 0, 711, 241))
        self.reportWebView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.reportWebView.setObjectName(_fromUtf8("reportWebView"))
        self.outGenTWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.outDataEdit = QtGui.QTextEdit(self.tab_2)
        self.outDataEdit.setGeometry(QtCore.QRect(0, 0, 711, 241))
        self.outDataEdit.setObjectName(_fromUtf8("outDataEdit"))
        self.outGenTWidget.addTab(self.tab_2, _fromUtf8(""))

        self.retranslateUi(reportGenDialog)
        self.outGenTWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(reportGenDialog)

    def retranslateUi(self, reportGenDialog):
        reportGenDialog.setWindowTitle(_translate("reportGenDialog", "Генератор отчетов", None))
        self.groupBox.setTitle(_translate("reportGenDialog", "Настройки", None))
        self.repTypeCBox.setItemText(0, _translate("reportGenDialog", "Сводный отчет по загрузке данных", None))
        self.repTypeCBox.setItemText(1, _translate("reportGenDialog", "Отчет по топосъемке объектов", None))
        self.generateRepPButton.setText(_translate("reportGenDialog", "Сформировать", None))
        self.label.setText(_translate("reportGenDialog", "Регион выборки отчета", None))
        self.label_2.setText(_translate("reportGenDialog", "Начало (дата1)", None))
        self.label_3.setText(_translate("reportGenDialog", "Оконч. (дата2)", None))
        self.groupBox_2.setTitle(_translate("reportGenDialog", "Вывод", None))
        self.outGenTWidget.setTabText(self.outGenTWidget.indexOf(self.tab), _translate("reportGenDialog", "Верстка", None))
        self.outGenTWidget.setTabText(self.outGenTWidget.indexOf(self.tab_2), _translate("reportGenDialog", "Вывод данных", None))

from PyQt4 import QtWebKit
