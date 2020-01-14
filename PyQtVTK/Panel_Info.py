from PyQt5 import QtCore, QtWidgets

class Info(object):
    def __init__(self, domain):
        super().__init__()

        self.output = QtWidgets.QTextBrowser(domain)