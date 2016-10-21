__author__ = 'ADMIN'

import psycopg2
import os
import subprocess
from PyQt4 import QtCore, QtGui, QtWebKit

class customWebPage(QtWebKit.QWebPage):
    def __init__(self, QObject_parent=None):
        super(customWebPage, self).__init__(QObject_parent)

    def contentsChanged(self, *args, **kwargs):
        print u"++--++"
        super(customWebPage, self).contentsChanged(*args, **kwargs)