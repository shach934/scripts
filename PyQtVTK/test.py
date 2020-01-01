import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import Qt


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.vlayout = QtWidgets.QVBoxLayout()

        # tree widget item
        tree_widget_item = QtWidgets.QTreeWidgetItem(['Item 1'])
        item1 = QtWidgets.QTreeWidgetItem(tree_widget_item, ["sub Item 1"])
        item1.setCheckState(0, Qt.Unchecked)

        item2 = QtWidgets.QTreeWidgetItem(tree_widget_item, ["sub item 2"])
        item2.setCheckState(0, Qt.Unchecked)

        # tree widget
        tree_widget = QtWidgets.QTreeWidget(self)
        tree_widget.addTopLevelItem(tree_widget_item)
        self.vlayout.addWidget(tree_widget)

        tree_widget.currentItemChanged.connect(self.propertyView)

    def propertyView(self, current, old):
        print(current.text(0))

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, QtWidgets.QTreeWidgetItem)
    def current_item_changed(self, current, previous):
        print('\ncurrent: {}, \nprevious: {}'.format(current, previous))


application = QtWidgets.QApplication(sys.argv)
window = Window()
window.setWindowTitle('Tree widget')
window.resize(250, 180)
window.show()
sys.exit(application.exec_())