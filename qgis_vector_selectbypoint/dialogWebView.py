# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogWebView.ui'
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

class Ui_nodeSchemaDialog(object):
    def setupUi(self, nodeSchemaDialog):
        nodeSchemaDialog.setObjectName(_fromUtf8("nodeSchemaDialog"))
        nodeSchemaDialog.resize(666, 522)
        self.buttonBox = QtGui.QDialogButtonBox(nodeSchemaDialog)
        self.buttonBox.setGeometry(QtCore.QRect(480, 490, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.webViewNodeSchema = QtWebKit.QWebView(nodeSchemaDialog)
        self.webViewNodeSchema.setGeometry(QtCore.QRect(10, 10, 651, 441))
        self.webViewNodeSchema.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webViewNodeSchema.setObjectName(_fromUtf8("webViewNodeSchema"))
        self.showGensChBox = QtGui.QCheckBox(nodeSchemaDialog)
        self.showGensChBox.setGeometry(QtCore.QRect(10, 490, 181, 17))
        self.showGensChBox.setChecked(True)
        self.showGensChBox.setObjectName(_fromUtf8("showGensChBox"))
        self.addDRegPButton = QtGui.QPushButton(nodeSchemaDialog)
        self.addDRegPButton.setGeometry(QtCore.QRect(10, 460, 101, 23))
        self.addDRegPButton.setObjectName(_fromUtf8("addDRegPButton"))
        self.addWCalcPButton = QtGui.QPushButton(nodeSchemaDialog)
        self.addWCalcPButton.setGeometry(QtCore.QRect(120, 460, 101, 23))
        self.addWCalcPButton.setObjectName(_fromUtf8("addWCalcPButton"))
        self.addCompPButton = QtGui.QPushButton(nodeSchemaDialog)
        self.addCompPButton.setGeometry(QtCore.QRect(230, 460, 101, 23))
        self.addCompPButton.setObjectName(_fromUtf8("addCompPButton"))
        self.addBKlapPButton = QtGui.QPushButton(nodeSchemaDialog)
        self.addBKlapPButton.setGeometry(QtCore.QRect(340, 460, 101, 23))
        self.addBKlapPButton.setObjectName(_fromUtf8("addBKlapPButton"))
        self.addVantPButton = QtGui.QPushButton(nodeSchemaDialog)
        self.addVantPButton.setGeometry(QtCore.QRect(450, 460, 101, 23))
        self.addVantPButton.setObjectName(_fromUtf8("addVantPButton"))
        self.elmTableButton = QtGui.QPushButton(nodeSchemaDialog)
        self.elmTableButton.setGeometry(QtCore.QRect(200, 490, 161, 23))
        self.elmTableButton.setObjectName(_fromUtf8("elmTableButton"))
        self.addAbInpWCButton = QtGui.QPushButton(nodeSchemaDialog)
        self.addAbInpWCButton.setGeometry(QtCore.QRect(560, 460, 101, 23))
        self.addAbInpWCButton.setObjectName(_fromUtf8("addAbInpWCButton"))
        self.addBranchButton = QtGui.QPushButton(nodeSchemaDialog)
        self.addBranchButton.setGeometry(QtCore.QRect(380, 490, 101, 23))
        self.addBranchButton.setObjectName(_fromUtf8("addBranchButton"))

        self.retranslateUi(nodeSchemaDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), nodeSchemaDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), nodeSchemaDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(nodeSchemaDialog)

    def retranslateUi(self, nodeSchemaDialog):
        nodeSchemaDialog.setWindowTitle(_translate("nodeSchemaDialog", "Dialog", None))
        self.showGensChBox.setText(_translate("nodeSchemaDialog", "Показывать сгенерированные", None))
        self.addDRegPButton.setText(_translate("nodeSchemaDialog", "+ Рег. давления", None))
        self.addWCalcPButton.setText(_translate("nodeSchemaDialog", "+ Водомер", None))
        self.addCompPButton.setText(_translate("nodeSchemaDialog", "+ Компенсатор", None))
        self.addBKlapPButton.setText(_translate("nodeSchemaDialog", "+ Обр. клапан", None))
        self.addVantPButton.setText(_translate("nodeSchemaDialog", "+ Вантуз", None))
        self.elmTableButton.setText(_translate("nodeSchemaDialog", "Таблица всех элементов", None))
        self.addAbInpWCButton.setText(_translate("nodeSchemaDialog", "+ Аб.врезку+зд.", None))
        self.addBranchButton.setText(_translate("nodeSchemaDialog", "+ Труба", None))

from PyQt4 import QtWebKit
