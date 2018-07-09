import sys
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from os.path import exists
from ansi import Fore, Style
from  utils.utils import get_replacements
import click

Qt = QtCore.Qt
COLS = ['source', 'dest', 'tag', 'id']
class Model(QtCore.QAbstractTableModel):
    def __init__(self, tree, replacements, filename, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.replacements = replacements
        self.tree = tree
        self.filename = filename
        self._data = [{'id': unicode(id), 'source':k.source.center, 'dest':k.dest.center, 'tag':k.source.block.node.get('tag')} for id, k in enumerate(replacements)]

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(COLS)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role in [Qt.DisplayRole, Qt.EditRole]:
                return QtCore.QVariant(self._data[index.row()][COLS[index.column()]])
        return QtCore.QVariant()

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return COLS[col]
        return None

    def is_tag(self, index):
        return COLS[index.column()]=='tag'

    def flags(self, index):
        if not index.isValid():
            return None

        if self.is_tag(index):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role ==QtCore.Qt.EditRole: 
            self._data[index.row()][COLS[index.column()]]=value
            self.dataChanged.emit(index, index)
            self.replacements[index.row()].source.block.node.set('tag', value)
            return True
        return False

    def save(self):
        self.tree.write(self.filename)


# override TableView to enable muliple cell editing
class TableView(QtWidgets.QTableView):
    def commitData(self, editor):
        super(TableView, self).commitData(editor)
        model = self.currentIndex().model()
        value = model.data(self.currentIndex(), QtCore.Qt.EditRole)
        for itemRange in self.selectionModel().selection():
            for index in itemRange.indexes():
                model.setData(index, value, QtCore.Qt.EditRole)
        model.save()

def update(item):
    pass

@click.command()
@click.argument('filename', type=click.Path(exists=True))
def run(filename):
    tree, replacements =  get_replacements(xml_filename=filename, encoding='utf8')
    application = QtWidgets.QApplication(sys.argv)
    view = TableView()
    model = Model(tree, replacements, filename)
    proxyModel = QtCore.QSortFilterProxyModel()
    proxyModel.setSourceModel(model)
    proxyModel.save = model.save
    view.setModel(proxyModel)
    view.setSortingEnabled(True)
    view.clicked.connect(update)
    view.show()
    sys.exit(application.exec_())


if __name__ == '__main__':
    run()
