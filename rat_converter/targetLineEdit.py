from imports import *

class targetLineEdit(QLineEdit):
    def __init__(self,  parent = None):
        QLineEdit.__init__(self)
        self.par = parent
        self.setToolTip('Doubleclick for auto set from sources\nLeave empty for use source folder')
        self.defColor = QPalette()
        self.defColor.setColor(QPalette.Text,QColor(100,100,100))
        self.editColor = QPalette()
        self.editColor.setColor(QPalette.Text,QColor(0,0,0))
        self.errorColor = QPalette()
        self.errorColor.setColor(QPalette.Text,QColor(200,0,0))
        self.valid = True
        self.source = True


    def setDefFolder(self):
        self.setText(self.par.messages[3])
        self.setPalette(self.defColor)
        self.source = True

    def mouseDoubleClickEvent(self, event):
        self.setDefFolder()
        QLineEdit.mouseDoubleClickEvent(self, event)

    def mousePressEvent(self, event):
        self.setPalette(self.editColor)
        if str(self.text()) == self.par.messages[3]:
            self.setText('')
        QLineEdit.mousePressEvent(self, event)

    def editFinish(self):
        self.checkText()

    def checkText(self):
        text = str(self.text())
        if text and not text == self.par.messages[3]:
            if os.path.isdir(text) and os.path.exists(text):
                self.setPalette(self.editColor)
                self.valid = True
                self.source = False
            else:
                self.setPalette(self.errorColor)
                self.valid = False
        else:
            self.valid = True
            self.setDefFolder()
        self.par.checkReadyState()
        return self.valid

############ DRAGnDROP
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
            if len(event.mimeData().urls()) == 1:
                dir = event.mimeData().urls()[0].toLocalFile()
                if os.path.isdir(dir):
                    self.setText(dir)
                    self.checkText()
                    self.emit(SIGNAL("dropped"))
                else:
                    event.ignore()
            else:
                event.ignore()
        else:
            event.ignore()