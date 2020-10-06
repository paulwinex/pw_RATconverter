from imports import *

class sourceListClass(QListWidget):
    def __init__(self, parent=None):
        super(sourceListClass, self).__init__()
        self.par = parent
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropOverwriteMode(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            ulrs = []
            for url in event.mimeData().urls():
                ulrs.append(str(url.toLocalFile()))
            self.emit(SIGNAL("dropped"))
            self.par.dropFiles(ulrs)

        else:
            event.ignore()