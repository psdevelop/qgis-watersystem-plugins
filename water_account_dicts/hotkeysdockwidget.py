# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hotkeysdockwidget.ui'
#
# Created: Wed Mar 18 01:22:58 2015
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

class Ui_hotKeysDockWidget(object):
    def setupUi(self, hotKeysDockWidget):
        hotKeysDockWidget.setObjectName(_fromUtf8("hotKeysDockWidget"))
        hotKeysDockWidget.resize(199, 231)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.pushButton = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton.setGeometry(QtCore.QRect(10, 0, 61, 31))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_2.setGeometry(QtCore.QRect(70, 0, 61, 31))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setGeometry(QtCore.QRect(130, 0, 61, 31))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_4.setEnabled(False)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 30, 61, 31))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_5 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_5.setEnabled(False)
        self.pushButton_5.setGeometry(QtCore.QRect(70, 30, 61, 31))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_6 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_6.setEnabled(False)
        self.pushButton_6.setGeometry(QtCore.QRect(130, 30, 61, 31))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_7 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_7.setGeometry(QtCore.QRect(10, 60, 61, 31))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.pushButton_8 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_8.setGeometry(QtCore.QRect(70, 60, 61, 31))
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.pushButton_9 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_9.setGeometry(QtCore.QRect(130, 60, 61, 31))
        self.pushButton_9.setObjectName(_fromUtf8("pushButton_9"))
        self.pushButton_10 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_10.setGeometry(QtCore.QRect(10, 90, 61, 31))
        self.pushButton_10.setObjectName(_fromUtf8("pushButton_10"))
        self.pushButton_11 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_11.setGeometry(QtCore.QRect(70, 90, 61, 31))
        self.pushButton_11.setObjectName(_fromUtf8("pushButton_11"))
        self.pushButton_12 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_12.setGeometry(QtCore.QRect(130, 90, 61, 31))
        self.pushButton_12.setObjectName(_fromUtf8("pushButton_12"))
        self.pushButton_13 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_13.setGeometry(QtCore.QRect(10, 120, 61, 31))
        self.pushButton_13.setObjectName(_fromUtf8("pushButton_13"))
        self.pushButton_14 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_14.setGeometry(QtCore.QRect(70, 120, 61, 31))
        self.pushButton_14.setObjectName(_fromUtf8("pushButton_14"))
        self.pushButton_15 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_15.setGeometry(QtCore.QRect(130, 120, 61, 31))
        self.pushButton_15.setObjectName(_fromUtf8("pushButton_15"))
        self.pushButton_16 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_16.setGeometry(QtCore.QRect(10, 150, 61, 31))
        self.pushButton_16.setObjectName(_fromUtf8("pushButton_16"))
        self.pushButton_17 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_17.setGeometry(QtCore.QRect(70, 150, 61, 31))
        self.pushButton_17.setObjectName(_fromUtf8("pushButton_17"))
        self.pushButton_18 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_18.setGeometry(QtCore.QRect(130, 150, 61, 31))
        self.pushButton_18.setObjectName(_fromUtf8("pushButton_18"))
        self.pushButton_19 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_19.setGeometry(QtCore.QRect(10, 180, 181, 23))
        self.pushButton_19.setObjectName(_fromUtf8("pushButton_19"))
        hotKeysDockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(hotKeysDockWidget)
        QtCore.QMetaObject.connectSlotsByName(hotKeysDockWidget)

    def retranslateUi(self, hotKeysDockWidget):
        hotKeysDockWidget.setWindowTitle(_translate("hotKeysDockWidget", "Перечень клавиш", None))
        self.pushButton.setText(_translate("hotKeysDockWidget", "PgUp", None))
        self.pushButton_2.setText(_translate("hotKeysDockWidget", "PgDn", None))
        self.pushButton_3.setText(_translate("hotKeysDockWidget", "Лупа", None))
        self.pushButton_4.setText(_translate("hotKeysDockWidget", "Объект", None))
        self.pushButton_5.setText(_translate("hotKeysDockWidget", "Планш.", None))
        self.pushButton_6.setText(_translate("hotKeysDockWidget", "Дигит.", None))
        self.pushButton_7.setText(_translate("hotKeysDockWidget", "Alt-F1", None))
        self.pushButton_8.setText(_translate("hotKeysDockWidget", "Alt-F2", None))
        self.pushButton_9.setText(_translate("hotKeysDockWidget", "Sh-F1", None))
        self.pushButton_10.setText(_translate("hotKeysDockWidget", "Ct-F1", None))
        self.pushButton_11.setText(_translate("hotKeysDockWidget", "Alt-A", None))
        self.pushButton_12.setText(_translate("hotKeysDockWidget", "Alt-L", None))
        self.pushButton_13.setText(_translate("hotKeysDockWidget", "Alt-N", None))
        self.pushButton_14.setText(_translate("hotKeysDockWidget", "Alt-S", None))
        self.pushButton_15.setText(_translate("hotKeysDockWidget", "Alt-V", None))
        self.pushButton_16.setText(_translate("hotKeysDockWidget", "Alt-W", None))
        self.pushButton_17.setText(_translate("hotKeysDockWidget", "Alt-Y", None))
        self.pushButton_18.setText(_translate("hotKeysDockWidget", "Alt-Z", None))
        self.pushButton_19.setText(_translate("hotKeysDockWidget", "Цвет", None))

