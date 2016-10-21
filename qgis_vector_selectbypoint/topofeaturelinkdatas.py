# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'topofeaturelinkdatas.ui'
#
# Created: Sun Mar 22 03:02:55 2015
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

class Ui_topoFeatureLinkDatasDialog(object):
    def setupUi(self, topoFeatureLinkDatasDialog):
        topoFeatureLinkDatasDialog.setObjectName(_fromUtf8("topoFeatureLinkDatasDialog"))
        topoFeatureLinkDatasDialog.resize(469, 433)
        self.buttonBox = QtGui.QDialogButtonBox(topoFeatureLinkDatasDialog)
        self.buttonBox.setGeometry(QtCore.QRect(300, 400, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.tabWidget = QtGui.QTabWidget(topoFeatureLinkDatasDialog)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 471, 401))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.pipeInjectOutListTableView = QtGui.QTableView(self.tab)
        self.pipeInjectOutListTableView.setGeometry(QtCore.QRect(0, 0, 461, 341))
        self.pipeInjectOutListTableView.setObjectName(_fromUtf8("pipeInjectOutListTableView"))
        self.addInjOutPipePushButton = QtGui.QPushButton(self.tab)
        self.addInjOutPipePushButton.setGeometry(QtCore.QRect(10, 350, 131, 23))
        self.addInjOutPipePushButton.setObjectName(_fromUtf8("addInjOutPipePushButton"))
        self.delInjOutPipePushButton = QtGui.QPushButton(self.tab)
        self.delInjOutPipePushButton.setGeometry(QtCore.QRect(150, 350, 131, 23))
        self.delInjOutPipePushButton.setObjectName(_fromUtf8("delInjOutPipePushButton"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))

        self.retranslateUi(topoFeatureLinkDatasDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), topoFeatureLinkDatasDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), topoFeatureLinkDatasDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(topoFeatureLinkDatasDialog)

    def retranslateUi(self, topoFeatureLinkDatasDialog):
        topoFeatureLinkDatasDialog.setWindowTitle(_translate("topoFeatureLinkDatasDialog", "Dialog", None))
        self.addInjOutPipePushButton.setText(_translate("topoFeatureLinkDatasDialog", "Добавить врезку", None))
        self.delInjOutPipePushButton.setText(_translate("topoFeatureLinkDatasDialog", "Удалить врезку", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("topoFeatureLinkDatasDialog", "Список врезок", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("topoFeatureLinkDatasDialog", "Tab 2", None))

