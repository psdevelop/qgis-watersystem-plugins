# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setPrintFormParams.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_setPrintFormPrmDialog(object):
    def setupUi(self, setPrintFormPrmDialog):
        setPrintFormPrmDialog.setObjectName(_fromUtf8("setPrintFormPrmDialog"))
        setPrintFormPrmDialog.resize(393, 283)
        self.buttonBox = QtGui.QDialogButtonBox(setPrintFormPrmDialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.canvasTypeCBox = QtGui.QComboBox(setPrintFormPrmDialog)
        self.canvasTypeCBox.setGeometry(QtCore.QRect(30, 210, 341, 22))
        self.canvasTypeCBox.setObjectName(_fromUtf8("canvasTypeCBox"))
        self.scaleSBox = QtGui.QSpinBox(setPrintFormPrmDialog)
        self.scaleSBox.setGeometry(QtCore.QRect(30, 90, 341, 22))
        self.scaleSBox.setMinimum(1)
        self.scaleSBox.setMaximum(999999999)
        self.scaleSBox.setProperty("value", 45000)
        self.scaleSBox.setObjectName(_fromUtf8("scaleSBox"))
        self.label = QtGui.QLabel(setPrintFormPrmDialog)
        self.label.setGeometry(QtCore.QRect(30, 190, 231, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(setPrintFormPrmDialog)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 141, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.wElmCountSBox = QtGui.QSpinBox(setPrintFormPrmDialog)
        self.wElmCountSBox.setGeometry(QtCore.QRect(30, 160, 151, 22))
        self.wElmCountSBox.setMinimum(1)
        self.wElmCountSBox.setObjectName(_fromUtf8("wElmCountSBox"))
        self.atlasOrientTypeCBox = QtGui.QComboBox(setPrintFormPrmDialog)
        self.atlasOrientTypeCBox.setGeometry(QtCore.QRect(30, 40, 341, 22))
        self.atlasOrientTypeCBox.setObjectName(_fromUtf8("atlasOrientTypeCBox"))
        self.atlasOrientTypeCBox.addItem(_fromUtf8(""))
        self.atlasOrientTypeCBox.addItem(_fromUtf8(""))
        self.label_3 = QtGui.QLabel(setPrintFormPrmDialog)
        self.label_3.setGeometry(QtCore.QRect(30, 20, 111, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(setPrintFormPrmDialog)
        self.label_4.setGeometry(QtCore.QRect(30, 140, 131, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(setPrintFormPrmDialog)
        self.label_5.setGeometry(QtCore.QRect(220, 140, 131, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.hElmCountSBox = QtGui.QSpinBox(setPrintFormPrmDialog)
        self.hElmCountSBox.setGeometry(QtCore.QRect(220, 160, 151, 22))
        self.hElmCountSBox.setMinimum(1)
        self.hElmCountSBox.setObjectName(_fromUtf8("hElmCountSBox"))
        self.recalcWHModeChkBox = QtGui.QCheckBox(setPrintFormPrmDialog)
        self.recalcWHModeChkBox.setGeometry(QtCore.QRect(30, 120, 341, 17))
        self.recalcWHModeChkBox.setObjectName(_fromUtf8("recalcWHModeChkBox"))

        self.retranslateUi(setPrintFormPrmDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), setPrintFormPrmDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), setPrintFormPrmDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(setPrintFormPrmDialog)

    def retranslateUi(self, setPrintFormPrmDialog):
        setPrintFormPrmDialog.setWindowTitle(_translate("setPrintFormPrmDialog", "Dialog", None))
        self.label.setText(_translate("setPrintFormPrmDialog", "Размер фрагмента атласа (по умолчанию A4)", None))
        self.label_2.setText(_translate("setPrintFormPrmDialog", "Масштаб основной карты", None))
        self.atlasOrientTypeCBox.setItemText(0, _translate("setPrintFormPrmDialog", "Альбом", None))
        self.atlasOrientTypeCBox.setItemText(1, _translate("setPrintFormPrmDialog", "Портрет", None))
        self.label_3.setText(_translate("setPrintFormPrmDialog", "Ориентация атласа", None))
        self.label_4.setText(_translate("setPrintFormPrmDialog", "Фрагментов по ширине", None))
        self.label_5.setText(_translate("setPrintFormPrmDialog", "Фрагментов по высоте", None))
        self.recalcWHModeChkBox.setText(_translate("setPrintFormPrmDialog", "Пересчитывать исходя из ширины и высоты атласа в листах", None))

