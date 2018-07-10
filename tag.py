import click
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from utils.utils import get_replacements

Qt = QtCore.Qt
COLS = ['id', 'source', 'dest', 'tag', 'diff']
NUM2COLS = {k: i for i, k in enumerate(COLS)}


class Model(QtCore.QAbstractTableModel):
    def __init__(self, tree, replacements, filename, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.replacements = replacements
        self.tree = tree
        self.filename = filename
        color = '<font color="red">'
        close = '</font>'
        self._data = [{
            'id': id,
            'source': k.source.center,
            'dest': k.dest.center,
            'tag': k.source.block.node.get('tag'),
            'diff': u'<html><body><table><tr><td>{x.left}{color}{x.center}{close}{x.right}</td><td>{y.left}{color}{y.center}{close}{y.right}</td></tr></table></body></html>'.format(x=k.dest, y=k.dest, color=color, close=close)
            } for id, k in enumerate(replacements)]

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
        return COLS[index.column()] == 'tag'

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
        if role == QtCore.Qt.EditRole:
            self._data[index.row()][COLS[index.column()]] = value
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


@click.command()
@click.argument('filename', type=click.Path(exists=True))
def run(filename):
    tree, replacements = get_replacements(xml_filename=filename, encoding='utf8', window_size=128)
    application = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QWidget()
    table_view = TableView()
    model = Model(tree, replacements, filename)
    proxyModel = QtCore.QSortFilterProxyModel()
    proxyModel.setSourceModel(model)
    proxyModel.save = model.save
    proxyModel._data = model._data
    table_view.setModel(proxyModel)
    table_view.setSortingEnabled(True)
    table_view.setAlternatingRowColors(True)
    table_view.resizeColumnsToContents()
    table_view.horizontalHeader().setStretchLastSection(True)
    table_view.setColumnHidden(NUM2COLS['id'], True)
    table_view.setColumnHidden(NUM2COLS['diff'], True)

    text_view = QWebEngineView()
    DIFF_COL = NUM2COLS['diff']

    def update_diff(item):
        text_view.setHtml(item.model().index(item.row(), DIFF_COL).data())

    table_view.doubleClicked.connect(update_diff)

    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(table_view)
    text_view.setFixedHeight(150)
    layout.addWidget(text_view)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    win.setLayout(layout)
    win.setWindowTitle('Medite Tagger')
    win.setGeometry(100,100, 1600, 800)
    win.show()

    sys.exit(application.exec_())


if __name__ == '__main__':
    run()
