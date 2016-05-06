from imports import *

class sourceListItemClass(QListWidgetItem):
    def __init__(self, text, type, parent=None):
        super(sourceListItemClass, self).__init__()
        self.par = parent
        self.text = str(text)
        #DATA
        self.type = type #set type
        #FONT
        self.font = QFont('Helvetica', 10)
        self.color = [QColor(20,20,40),QColor(70,20,40)]
        self.setFont(self.font)
        #TYPE
        if type:
            self.setForeground(QBrush(self.color[0]))
            self.setIcon(parent.icons['image'])
        else:
            self.setForeground(QBrush(self.color[1]))
            self.setIcon(parent.icons['folder'])

        self.updateText()

    def updateText(self):
        if self.par.show_btn.isChecked():
            self.setText(os.path.basename(self.text))
        else:
            self.setText(self.text)



