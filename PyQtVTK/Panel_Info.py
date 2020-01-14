from PyQt5 import QtCore, QtWidgets

class Info(object):
    def __init__(self, domain):
        super().__init__()
        self.log = ""
        self.output = QtWidgets.QTextBrowser(domain)

    def write(self, path):
        try:
            fid = open(path + "/log.log", "wr")
            fid.write(self.log)
        except IOError as e:
            self.__message__("cannot open the log file")