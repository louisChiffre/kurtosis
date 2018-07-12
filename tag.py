import click
import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTextBrowser
import utils.utils as ut


Qt = QtCore.Qt
COLS = ['id', 'type', 'source', 'dest', 'tag', 'diff']
DEFAULT_SIZE = 32
COL_SIZES = {'source': 600, 'dest': 600}

NUM2COLS = {k: i for i, k in enumerate(COLS)}


def get_tag(change):
    def get_tag_(block):
        if not block:
            return ''
        return block.node.get('tag')
    tag_source = get_tag_(change.source.block)
    tag_dest = get_tag_(change.dest.block)
    # if we have both tag_source and tag_dest, we verify they have the same value
    if tag_source and tag_dest:
        assert tag_source == tag_dest, 'Inconsistent tagging for the same replacement {tag_source} vs {tag_dest}'.format(**locals())
        return tag_source
    # otherwise we take the one that is set
    if tag_source:
        return tag_source
    if tag_dest:
        return tag_dest

diff_template = u'''
<html><body>
<table width="100%">
<thead>
    <td width="50%"><b>source</b></td><td width="50%"><b>dest</b></td>
</thead>
<tbody>
<tr>
    <td width="50%">{x.left}{color}{x.center}{close}{x.right}</td><td width="50%">{y.left}{color}{y.center}{close}{y.right}</td>
</tr>
</tbody>
</table>
</body>
</html>
'''

class Model(QtCore.QAbstractTableModel):
    def __init__(self, tree, changes, filename, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.changes = changes
        self.tree = tree
        self.filename = filename
        color = '<font color="red"><u>'
        close = '</u></font>'
        self._data = [{
            'id': id,
            'type': k.type,
            'source': k.source.center,
            'dest': k.dest.center,
            'tag': get_tag(k),
            'diff': diff_template.format(x=k.source, y=k.dest, color=color, close=close)
            } for id, k in enumerate(changes)]

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
        val = unicode(value.toString())
        change = self.changes[index.row()]

        def set_tag(block):
            if not block:
                return
            block.node.set('tag', val)

        if role == QtCore.Qt.EditRole:
            self._data[index.row()][COLS[index.column()]] = value
            self.dataChanged.emit(index, index)
            set_tag(change.source.block)
            set_tag(change.dest.block)
            return True
        return False

    def save(self):
        self.tree.write(self.filename)


# override TableView to enable muliple cell editing
class TableView(QtGui.QTableView):
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
    tree, changes = ut.get_changes(xml_filename=filename, encoding='utf8', window_size=128)
    application = QtGui.QApplication(sys.argv)
    win = QtGui.QWidget()
    table_view = TableView()
    model = Model(tree, changes, filename)
    proxyModel = QtGui.QSortFilterProxyModel()
    proxyModel.setSourceModel(model)
    proxyModel.save = model.save
    proxyModel._data = model._data
    table_view.setModel(proxyModel)
    table_view.setSortingEnabled(True)
    table_view.setAlternatingRowColors(True)
    for i, col in enumerate(COLS):
        if col in COL_SIZES:
            table_view.setColumnWidth(i, COL_SIZES[col])
    table_view.horizontalHeader().setStretchLastSection(True)
    table_view.setColumnHidden(NUM2COLS['id'], True)
    table_view.setColumnHidden(NUM2COLS['diff'], True)

    text_view = QTextBrowser()
    DIFF_COL = NUM2COLS['diff']

    def update_diff(item):
        text_view.setHtml(item.model().index(item.row(), DIFF_COL).data().toString())

    table_view.doubleClicked.connect(update_diff)

    layout = QtGui.QVBoxLayout()
    layout.addWidget(table_view)
    text_view.setFixedHeight(150)
    layout.addWidget(text_view)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    win.setLayout(layout)
    win.setWindowTitle('Medite Tagger')
    win.setGeometry(100, 100, 1600, 800)
    win.show()

    sys.exit(application.exec_())


if __name__ == '__main__':
    run()
