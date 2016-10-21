# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewmodesdialog.ui'
#
# Created: Wed Mar 18 01:53:11 2015
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

class Ui_viewModesDialog(object):
    def setupUi(self, viewModesDialog):
        viewModesDialog.setObjectName(_fromUtf8("viewModesDialog"))
        viewModesDialog.resize(438, 422)
        self.buttonBox = QtGui.QDialogButtonBox(viewModesDialog)
        self.buttonBox.setGeometry(QtCore.QRect(230, 380, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.treeWidget = QtGui.QTreeWidget(viewModesDialog)
        self.treeWidget.setGeometry(QtCore.QRect(10, 10, 421, 361))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.treeWidget.setFont(font)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(0, QtCore.Qt.Unchecked)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(1, QtCore.Qt.Unchecked)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(1, QtCore.Qt.Unchecked)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(1, QtCore.Qt.Unchecked)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(1, QtCore.Qt.Unchecked)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(0, QtCore.Qt.Unchecked)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(0, QtCore.Qt.Unchecked)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(1, QtCore.Qt.Unchecked)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(1, QtCore.Qt.Unchecked)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(1, QtCore.Qt.Unchecked)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(1, QtCore.Qt.Unchecked)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(1, QtCore.Qt.Unchecked)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(0, QtCore.Qt.Unchecked)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(1, QtCore.Qt.Unchecked)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(1, QtCore.Qt.Unchecked)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(1, QtCore.Qt.Unchecked)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(1, QtCore.Qt.Unchecked)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(1, QtCore.Qt.Unchecked)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(0, QtCore.Qt.Unchecked)
        self.treeWidget.header().setDefaultSectionSize(151)
        self.checkBox = QtGui.QCheckBox(viewModesDialog)
        self.checkBox.setGeometry(QtCore.QRect(10, 380, 141, 17))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))

        self.retranslateUi(viewModesDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), viewModesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), viewModesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(viewModesDialog)

    def retranslateUi(self, viewModesDialog):
        viewModesDialog.setWindowTitle(_translate("viewModesDialog", "Dialog", None))
        self.treeWidget.headerItem().setText(0, _translate("viewModesDialog", "Все режимы", None))
        self.treeWidget.headerItem().setText(1, _translate("viewModesDialog", "2УРОВЕНЬ", None))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("viewModesDialog", "Здания", None))
        self.treeWidget.topLevelItem(1).setText(1, _translate("viewModesDialog", "Номера зданий", None))
        self.treeWidget.topLevelItem(2).setText(1, _translate("viewModesDialog", "Адреса зданий", None))
        self.treeWidget.topLevelItem(3).setText(1, _translate("viewModesDialog", "Сокр. адреса с экспликацией", None))
        self.treeWidget.topLevelItem(4).setText(1, _translate("viewModesDialog", "Полные адреса с экспликацией", None))
        self.treeWidget.topLevelItem(5).setText(0, _translate("viewModesDialog", "Названия улиц", None))
        self.treeWidget.topLevelItem(6).setText(0, _translate("viewModesDialog", "Узлы", None))
        self.treeWidget.topLevelItem(7).setText(1, _translate("viewModesDialog", "Отметки узлов", None))
        self.treeWidget.topLevelItem(8).setText(1, _translate("viewModesDialog", "Номера колодцев", None))
        self.treeWidget.topLevelItem(9).setText(1, _translate("viewModesDialog", "Отметки узлов всех сетей", None))
        self.treeWidget.topLevelItem(10).setText(1, _translate("viewModesDialog", "Состояние колодцев", None))
        self.treeWidget.topLevelItem(11).setText(1, _translate("viewModesDialog", "Глубина заложения", None))
        self.treeWidget.topLevelItem(12).setText(0, _translate("viewModesDialog", "Участки", None))
        self.treeWidget.topLevelItem(13).setText(1, _translate("viewModesDialog", "Длины участков", None))
        self.treeWidget.topLevelItem(14).setText(1, _translate("viewModesDialog", "Типы участков", None))
        self.treeWidget.topLevelItem(15).setText(1, _translate("viewModesDialog", "Направление уклонов", None))
        self.treeWidget.topLevelItem(16).setText(1, _translate("viewModesDialog", "Длины участков всех сетей", None))
        self.treeWidget.topLevelItem(17).setText(1, _translate("viewModesDialog", "Задвижки", None))
        self.treeWidget.topLevelItem(18).setText(0, _translate("viewModesDialog", "Контуры", None))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.checkBox.setText(_translate("viewModesDialog", "Запоминание режима", None))

