# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nodeelementsdlg.ui'
#
# Created: Sun May  3 08:43:54 2015
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

class Ui_nodeElementsDialog(object):
    def setupUi(self, nodeElementsDialog):
        nodeElementsDialog.setObjectName(_fromUtf8("nodeElementsDialog"))
        nodeElementsDialog.resize(455, 473)
        self.buttonBox = QtGui.QDialogButtonBox(nodeElementsDialog)
        self.buttonBox.setGeometry(QtCore.QRect(290, 431, 161, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.groupBox = QtGui.QGroupBox(nodeElementsDialog)
        self.groupBox.setGeometry(QtCore.QRect(0, 190, 451, 241))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayoutWidget = QtGui.QWidget(self.groupBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 20, 431, 211))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.iDLabel = QtGui.QLabel(self.formLayoutWidget)
        self.iDLabel.setObjectName(_fromUtf8("iDLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.iDLabel)
        self.iDLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.iDLineEdit.setEnabled(False)
        self.iDLineEdit.setObjectName(_fromUtf8("iDLineEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.iDLineEdit)
        self.nameLabel = QtGui.QLabel(self.formLayoutWidget)
        self.nameLabel.setObjectName(_fromUtf8("nameLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.nameLabel)
        self.naneLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.naneLineEdit.setObjectName(_fromUtf8("naneLineEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.naneLineEdit)
        self.descLabel = QtGui.QLabel(self.formLayoutWidget)
        self.descLabel.setObjectName(_fromUtf8("descLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.descLabel)
        self.descLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.descLineEdit.setObjectName(_fromUtf8("descLineEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.descLineEdit)
        self.matLabel = QtGui.QLabel(self.formLayoutWidget)
        self.matLabel.setObjectName(_fromUtf8("matLabel"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.matLabel)
        self.matLineEdit = QtGui.QComboBox(self.formLayoutWidget)
        self.matLineEdit.setObjectName(_fromUtf8("matLineEdit"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.matLineEdit)
        self.lcolorLabel = QtGui.QLabel(self.formLayoutWidget)
        self.lcolorLabel.setObjectName(_fromUtf8("lcolorLabel"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.lcolorLabel)
        self.lcolorLineEdit = QtGui.QComboBox(self.formLayoutWidget)
        self.lcolorLineEdit.setEditable(True)
        self.lcolorLineEdit.setObjectName(_fromUtf8("lcolorLineEdit"))
        self.lcolorLineEdit.addItem(_fromUtf8(""))
        self.lcolorLineEdit.addItem(_fromUtf8(""))
        self.lcolorLineEdit.addItem(_fromUtf8(""))
        self.lcolorLineEdit.addItem(_fromUtf8(""))
        self.lcolorLineEdit.addItem(_fromUtf8(""))
        self.lcolorLineEdit.addItem(_fromUtf8(""))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.lcolorLineEdit)
        self.lstyleLabel = QtGui.QLabel(self.formLayoutWidget)
        self.lstyleLabel.setObjectName(_fromUtf8("lstyleLabel"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.lstyleLabel)
        self.lstyleComboBox = QtGui.QComboBox(self.formLayoutWidget)
        self.lstyleComboBox.setEditable(True)
        self.lstyleComboBox.setObjectName(_fromUtf8("lstyleComboBox"))
        self.lstyleComboBox.addItem(_fromUtf8(""))
        self.lstyleComboBox.addItem(_fromUtf8(""))
        self.lstyleComboBox.addItem(_fromUtf8(""))
        self.lstyleComboBox.addItem(_fromUtf8(""))
        self.lstyleComboBox.addItem(_fromUtf8(""))
        self.lstyleComboBox.addItem(_fromUtf8(""))
        self.lstyleComboBox.addItem(_fromUtf8(""))
        self.lstyleComboBox.addItem(_fromUtf8(""))
        self.lstyleComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.lstyleComboBox)
        self.lwidthLabel = QtGui.QLabel(self.formLayoutWidget)
        self.lwidthLabel.setObjectName(_fromUtf8("lwidthLabel"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.lwidthLabel)
        self.lwidthSpinBox = QtGui.QSpinBox(self.formLayoutWidget)
        self.lwidthSpinBox.setObjectName(_fromUtf8("lwidthSpinBox"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.lwidthSpinBox)
        self.diamLabel = QtGui.QLabel(self.formLayoutWidget)
        self.diamLabel.setObjectName(_fromUtf8("diamLabel"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.diamLabel)
        self.diamLineEdit = QtGui.QSpinBox(self.formLayoutWidget)
        self.diamLineEdit.setObjectName(_fromUtf8("diamLineEdit"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.diamLineEdit)
        self.groupBox_2 = QtGui.QGroupBox(nodeElementsDialog)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 0, 451, 191))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayoutWidget = QtGui.QWidget(self.groupBox_2)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 431, 161))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblVNodeElements = QtGui.QTableView(self.verticalLayoutWidget)
        self.tblVNodeElements.setObjectName(_fromUtf8("tblVNodeElements"))
        self.verticalLayout.addWidget(self.tblVNodeElements)
        self.addElmPButton = QtGui.QPushButton(nodeElementsDialog)
        self.addElmPButton.setGeometry(QtCore.QRect(10, 440, 111, 23))
        self.addElmPButton.setObjectName(_fromUtf8("addElmPButton"))
        self.delElmPButton = QtGui.QPushButton(nodeElementsDialog)
        self.delElmPButton.setGeometry(QtCore.QRect(130, 440, 111, 23))
        self.delElmPButton.setObjectName(_fromUtf8("delElmPButton"))

        self.retranslateUi(nodeElementsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), nodeElementsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), nodeElementsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(nodeElementsDialog)

    def retranslateUi(self, nodeElementsDialog):
        nodeElementsDialog.setWindowTitle(_translate("nodeElementsDialog", "Dialog", None))
        self.groupBox.setTitle(_translate("nodeElementsDialog", "Свойства элемента", None))
        self.iDLabel.setText(_translate("nodeElementsDialog", "ID", None))
        self.nameLabel.setText(_translate("nodeElementsDialog", "Наименование", None))
        self.descLabel.setText(_translate("nodeElementsDialog", "Описание", None))
        self.matLabel.setText(_translate("nodeElementsDialog", "Материал", None))
        self.lcolorLabel.setText(_translate("nodeElementsDialog", "Цвет линии", None))
        self.lcolorLineEdit.setItemText(0, _translate("nodeElementsDialog", "Белый", None))
        self.lcolorLineEdit.setItemText(1, _translate("nodeElementsDialog", "Желтый", None))
        self.lcolorLineEdit.setItemText(2, _translate("nodeElementsDialog", "Синий", None))
        self.lcolorLineEdit.setItemText(3, _translate("nodeElementsDialog", "Зеленый", None))
        self.lcolorLineEdit.setItemText(4, _translate("nodeElementsDialog", "Красный", None))
        self.lcolorLineEdit.setItemText(5, _translate("nodeElementsDialog", "Оранжевый", None))
        self.lstyleLabel.setText(_translate("nodeElementsDialog", "Тип линии", None))
        self.lstyleComboBox.setItemText(0, _translate("nodeElementsDialog", "Обычная", None))
        self.lstyleComboBox.setItemText(1, _translate("nodeElementsDialog", "Пунктир", None))
        self.lstyleComboBox.setItemText(2, _translate("nodeElementsDialog", "Двойной пунктир", None))
        self.lstyleComboBox.setItemText(3, _translate("nodeElementsDialog", "Редкий пунктир", None))
        self.lstyleComboBox.setItemText(4, _translate("nodeElementsDialog", "Точка-тире", None))
        self.lstyleComboBox.setItemText(5, _translate("nodeElementsDialog", "Точка", None))
        self.lstyleComboBox.setItemText(6, _translate("nodeElementsDialog", "Редкая точка", None))
        self.lstyleComboBox.setItemText(7, _translate("nodeElementsDialog", "Две точки-тире", None))
        self.lstyleComboBox.setItemText(8, _translate("nodeElementsDialog", "Два тире-точка", None))
        self.lwidthLabel.setText(_translate("nodeElementsDialog", "Толщина линии", None))
        self.diamLabel.setText(_translate("nodeElementsDialog", "Диаметр", None))
        self.groupBox_2.setTitle(_translate("nodeElementsDialog", "Элементы схемы", None))
        self.addElmPButton.setText(_translate("nodeElementsDialog", "Новый", None))
        self.delElmPButton.setText(_translate("nodeElementsDialog", "Удалить", None))

