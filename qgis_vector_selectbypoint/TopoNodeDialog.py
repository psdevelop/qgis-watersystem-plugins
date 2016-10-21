# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TopoNodeDialog.ui'
#
# Created: Fri May 29 18:33:57 2015
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

class Ui_TopoNodeAttrsDialog(object):
    def setupUi(self, TopoNodeAttrsDialog):
        TopoNodeAttrsDialog.setObjectName(_fromUtf8("TopoNodeAttrsDialog"))
        TopoNodeAttrsDialog.resize(468, 495)
        self.buttonBox = QtGui.QDialogButtonBox(TopoNodeAttrsDialog)
        self.buttonBox.setGeometry(QtCore.QRect(290, 460, 171, 21))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(TopoNodeAttrsDialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 111, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.AttrTableView = QtGui.QTableWidget(TopoNodeAttrsDialog)
        self.AttrTableView.setGeometry(QtCore.QRect(20, 30, 431, 381))
        self.AttrTableView.setObjectName(_fromUtf8("AttrTableView"))
        self.AttrTableView.setColumnCount(2)
        self.AttrTableView.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.AttrTableView.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.AttrTableView.setHorizontalHeaderItem(1, item)
        self.AttrTableView.horizontalHeader().setMinimumSectionSize(40)
        self.getBinaryAttr = QtGui.QPushButton(TopoNodeAttrsDialog)
        self.getBinaryAttr.setGeometry(QtCore.QRect(20, 420, 91, 23))
        self.getBinaryAttr.setObjectName(_fromUtf8("getBinaryAttr"))
        self.putBinaryAttr = QtGui.QPushButton(TopoNodeAttrsDialog)
        self.putBinaryAttr.setGeometry(QtCore.QRect(120, 420, 91, 23))
        self.putBinaryAttr.setObjectName(_fromUtf8("putBinaryAttr"))
        self.pipeInjOutListButton = QtGui.QPushButton(TopoNodeAttrsDialog)
        self.pipeInjOutListButton.setGeometry(QtCore.QRect(364, 420, 91, 23))
        self.pipeInjOutListButton.setObjectName(_fromUtf8("pipeInjOutListButton"))
        self.editSchema = QtGui.QPushButton(TopoNodeAttrsDialog)
        self.editSchema.setGeometry(QtCore.QRect(220, 420, 101, 23))
        self.editSchema.setObjectName(_fromUtf8("editSchema"))
        self.moveLayerButton = QtGui.QPushButton(TopoNodeAttrsDialog)
        self.moveLayerButton.setGeometry(QtCore.QRect(20, 460, 91, 23))
        self.moveLayerButton.setObjectName(_fromUtf8("moveLayerButton"))

        self.retranslateUi(TopoNodeAttrsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TopoNodeAttrsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TopoNodeAttrsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TopoNodeAttrsDialog)

    def retranslateUi(self, TopoNodeAttrsDialog):
        TopoNodeAttrsDialog.setWindowTitle(_translate("TopoNodeAttrsDialog", "Dialog", None))
        self.label.setText(_translate("TopoNodeAttrsDialog", "Таблица атрибутов", None))
        item = self.AttrTableView.horizontalHeaderItem(0)
        item.setText(_translate("TopoNodeAttrsDialog", "Наименование", None))
        item = self.AttrTableView.horizontalHeaderItem(1)
        item.setText(_translate("TopoNodeAttrsDialog", "Значение", None))
        self.getBinaryAttr.setText(_translate("TopoNodeAttrsDialog", "Извлечь", None))
        self.getBinaryAttr.setShortcut(_translate("TopoNodeAttrsDialog", "Shift+C", None))
        self.putBinaryAttr.setText(_translate("TopoNodeAttrsDialog", "Прикрепить", None))
        self.pipeInjOutListButton.setText(_translate("TopoNodeAttrsDialog", "Врезки", None))
        self.editSchema.setText(_translate("TopoNodeAttrsDialog", "Схемы...", None))
        self.moveLayerButton.setText(_translate("TopoNodeAttrsDialog", "Перенос в слой", None))

