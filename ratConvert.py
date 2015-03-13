#! /usr/bin/python
# -*- coding: utf-8 -*-

#default modules
from imports import *

#Package modules
import batchConverter
import sourceListWidget
import sourceListItem
import targetLineEdit
import settings
import formats

import pltfrm as pl
# Import the compiled UI module
from ratConvert_UI import Ui_ratWindow
# Create a class for our main window
class ratConvertClass(QMainWindow, Ui_ratWindow):
    def __init__(self, parent=None):
        super(ratConvertClass, self).__init__()
        self.setupUi(self)
        self.setWindowFlags( Qt.Window|Qt.WindowStaysOnTopHint )
        ############################
        #VARIBLES
        self.messages = ['Waiting for data...',
                         'Ready!!!!',
                         'Set IConvert path',
                         'same as source...',
                         'Out folder error!!!']
        iconsPath = os.path.join(os.path.dirname(__file__),'icons')
        self.icons = {'title':QIcon(os.path.join(iconsPath, 'rat_icon.png')),
                      'image':QIcon(os.path.join(iconsPath, 'image.png')),
                      'trash':QIcon(os.path.join(iconsPath, 'trash.png')),
                      'minus':QIcon(os.path.join(iconsPath, 'minus.png')),
                      'folder':QIcon(os.path.join(iconsPath, 'folder.png')),
                      }
        self.outFormats = formats.formats#['rat','exr']
        #Window
        self.setWindowTitle('RAT Converter v1.0')
        self.setWindowIcon(self.icons['title'])
        self.statusBar.showMessage(self.messages[0])
        #Buttons
        self.browseFiles_btn.setText('')
        self.browseFiles_btn.setIcon(self.icons['image'])
        self.browseFolder_btn.setText('')
        self.browseFolder_btn.setIcon(self.icons['folder'])
        self.remove_btn.setText('')
        self.remove_btn.setIcon(self.icons['trash'])
        self.show_btn.setText('')
        self.show_btn.setIcon(self.icons['minus'])

        self.multi_cb.setVisible(0)
        self.stop_btn.setEnabled(False)
        self.RAT_btn.setEnabled(False)
        #FORMATS
        for f in self.outFormats:
            self.format_cb.addItem(f.upper())


        #settings
        self.ini = 'ratConvertSettings'
        self.defaultExt = 'exr,hdr,tif,png,jpg'
        self.settings = settings.settingsClass(self.ini)

        self.fileList = []
        self.targetDir = None
        #Source line edit
        self.sourceList_lw.setParent(None)
        self.sourceList_lw = sourceListWidget.sourceListClass(self)
        self.source_ly.addWidget(self.sourceList_lw)
        #Target Line edit
        self.target_le.setParent(None)
        self.target_le = targetLineEdit.targetLineEdit(self)
        self.target_le.setDefFolder()
        self.newtarget_ly.addWidget(self.target_le)

        ##############################  CONNECT
        self.delExt_btn.clicked.connect(self.delExt)
        self.newExt_le.returnPressed.connect(self.addExt)
        self.RAT_btn.clicked.connect(self.start)
        self.browsIconvert_btn.clicked.connect(self.setIconvertPath)
        self.browseTarget_btn.clicked.connect(self.getTargetDir)
        self.remove_btn.clicked.connect(self.removeItem)
        self.show_btn.clicked.connect(self.updateList)
        self.stop_btn.clicked.connect(self.stopProcess)
        self.help_btn.clicked.connect(self.showHelp)
        self.target_le.editingFinished.connect(self.target_le.editFinish)

        @self.browseFiles_btn.clicked.connect
        def checkAllClick():
            self.getSourceFiles(True)

        @self.browseFolder_btn.clicked.connect
        def checkAllClick():
            self.getSourceFiles(False)

        @self.checkAll_btn.clicked.connect
        def checkAllClick():
            self.checkAll(True)
        @self.unckeckAll_btn.clicked.connect
        def uncheckAllClick():
            self.checkAll(False)

############################### START
        self.center()
        self.fillList()
        self.setIconvert()

################################################# UI
    def center(self):
        """
        center window on screen
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setIconvert(self):
        """
        Start conver process
        """
        path =  self.getIconvert()
        if path:
            self.iconvert_lb.setText(path)
        else:
            self.iconvert_lb.setText('iconvert bin not set')

    def getIconvert(self):
        """
        get iconvert binary file
        """
        ic = self.settings.readSettings('iconvert','').toString()
        if not ic or not os.path.exists(ic):
            box = QMessageBox(self)
            box.setWindowTitle('iConvert')
            box.setText('Please, set path to iconvert binary')
            box.exec_()
            ic = self.getIconvertDialog()
        if os.path.exists(ic):
            self.setIconvertPath(ic)
            return ic
        return False

    def setIconvertPath(self, path=None):
        """
        sep path iconvert
        """
        if not path:
            path = self.getIconvertDialog()
        if path:
            self.iconvert_lb.setText(path)
            self.settings.writeValue('iconvert',path)

    def getIconvertDialog(self):
        """
        dialog for set iconvert path
        """
        return str(QFileDialog.getOpenFileName(self,'Select iconvert binary',pl.defFolder,  pl.iconvert  ))

    def showHelp(self):
        """
        help window
        """
        text = '''1. Select iconvert binary path
2. Select files or folder
3. Select extensions
4. Push RAT!!!

See tooltips of widgets!
        '''
        box = QMessageBox(self)
        box.setWindowTitle('iConvert about')
        box.setText('RAT Converter v1.0\nPaulWinex 2012')
        box.setDetailedText(text)
        box.exec_()

    def fillList(self):
        """
        fill extension list
        """
        lst = self.getExtList()
        for e in lst.split(','):
            item = QListWidgetItem()
            item.setText('.'+ e)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            item.setCheckState(Qt.Checked)
            self.extList_lw.addItem(item)

    def getExtList(self):
        """
        get extension list
        """
        extList = str(self.settings.readSettings('ext','').toString())
        if not extList:
            self.settings.writeValue('ext',self.defaultExt)
            return self.defaultExt
        else:
            return extList

    def addExt(self):
        """
        add new extension
        """
        ext = str(self.newExt_le.text())
        if not ext[0] == '.':
            ext = '.' + ext
        if self.addExtToSettings(ext[1:]):
            item = QListWidgetItem()
            item.setText(ext)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            item.setCheckState(Qt.Checked)
            self.extList_lw.addItem(item)
        self.newExt_le.clear()

    def addExtToSettings(self,ext):
        """
        save extensions
        """
        extList = str(self.settings.readSettings('ext').toString())
        if not extList:
            extList = self.defaultExt
        if not ext.lower() in extList.split(','):# and not ext.lower() == 'rat':
            self.settings.writeValue('ext',','.join([extList,ext.lower()]))
            return True
        return False

    def delExt(self):
        """
        remove extension
        """
        item = self.extList_lw.selectedItems()
        ext = []
        if item:
            for i in item:
                ext.append(str(i.text()).replace('.',''))
                d = self.extList_lw.takeItem(self.extList_lw.row(i))
                del d
            self.delExtFromSettings(ext)

    def delExtFromSettings(self,ext):
        """
        remove ext from settings
        """
        extList = str(self.settings.readSettings('ext').toString()).split(',')
        for e in ext:
            if e in extList:
                extList.pop(extList.index(e))
        self.settings.writeValue('ext',','.join(extList))


    def checkAll(self, s):
        state = {True:Qt.Checked,False:Qt.Unchecked}
        c =self.extList_lw.count()
        for i in range(c):
            self.extList_lw.item(i).setCheckState(state[s])

    def message(self, line):
        """
        Show message in statusBar
        """
        self.statusBar.showMessage(line)

    def checkReadyState(self):
        """
        check all data before starting
        """
        if os.path.exists(self.iconvert_lb.text()):
            if self.sourceList_lw.count():
                if self.target_le.valid:
                    self.message(self.messages[1])  #READY
                    self.RAT_btn.setEnabled(1)
                    if not str(self.target_le.text()) == self.messages[3]:
                        self.settings.writeValue('defOut', str(self.target_le.text()))
                else:
                    self.message(self.messages[4])  #Waiting data
                    self.RAT_btn.setEnabled(0)
            else:
                self.message(self.messages[0])  #Waiting data
                self.RAT_btn.setEnabled(0)
        else:
            self.message(self.messages[2]) #No iConvert
            self.RAT_btn.setEnabled(0)

    def updateList(self):
        """
        Update list
        """
        for i in range(self.sourceList_lw.count()):
            self.sourceList_lw.item(i).updateText()


#########################################################  FILES
    def getSourceFiles(self, tp):
        """
        set source file button
        """
        extList = self.checkExtChecked()
        dir = str(self.settings.readSettings('defIn',QVariant(os.path.expanduser('~'))).toString())
        #ADD FILES
        if tp:
            extFilter = ''
            for e in extList:
                extFilter += ' *.'+str(e)#+' *.'+str(e.upper())
            list = QFileDialog.getOpenFileNames(self,'Select files',dir, extFilter )
            if list:
                self.addFilesToList(list)
                dir = os.path.dirname(str(list[0]))
                self.settings.writeValue('defIn', dir)
        #ADD FOLDERS
        else:
            folder = str(QFileDialog.getExistingDirectory(self,'Select Folder', dir))
            if folder:
                self.addFoldersToList([folder])
                self.settings.writeValue('defIn', folder)
        self.checkReadyState()

    def checkFolder(self, folder, extList):
        lst = os.listdir(folder)
        if lst:
            for f in lst:
                fl = os.path.join(folder,f)
                if not os.path.isdir(fl):
                    if os.path.splitext(fl)[1].replace('.','') in extList:
                        return True
        return False

    def addFilesToList(self, files):
        for l in files:
            if self.checkExistPath(l):
                self.sourceList_lw.addItem(sourceListItem.sourceListItemClass(l, 1, self ))

    def addFoldersToList(self, folders):
        for f in folders:
            if self.checkExistPath(f):
                self.sourceList_lw.addItem(sourceListItem.sourceListItemClass(f, 0, self ))


    def getTargetDir(self):
        dir = str(self.settings.readSettings('defOut',QVariant('')).toString()).replace('/','\\')
        if not dir: dir = self.getFolderFromFiles()
        folder = str(QFileDialog.getExistingDirectory(self,'Select Folder', dir))
        if folder:
            self.targetDir = folder
            self.target_le.setText(folder.replace('\\','/'))
            if self.target_le.checkText():
                self.settings.writeValue('defOut', folder)
        self.checkReadyState()

    def getFolderFromFiles(self):
        c = self.sourceList_lw.count()
        if c:
            path = self.sourceList_lw.item(c-1).text
            if path:
                path = str(path)
                if not os.path.isdir(path): path = os.path.dirname(path)
                return path
        else:
            return os.path.expanduser('~')

    def checkExtChecked(self):
        allExt = []
        for index in xrange(self.extList_lw.count()):
            if self.extList_lw.item(index).checkState():
                allExt.append(str(self.extList_lw.item(index).text().replace('.','')))
        return allExt

    def removeItem(self):
        sel = self.sourceList_lw.selectedItems()
        if sel:
            for s in sel:
                self.sourceList_lw.takeItem(self.sourceList_lw.row(s))
            self.checkReadyState()

    def dropFiles(self, array):
        if array:
            files = []
            dirs = []
            extList = self.checkExtChecked()
            for a in array:
                if os.path.isdir(a):
                    dirs.append(a)
                elif os.path.isfile(a):
                    if os.path.splitext(a)[1][1:] in extList:
                        files.append(a)
            if files: self.addFilesToList(files)
            if dirs: self.addFoldersToList(dirs)
            self.checkReadyState()

    def checkExistPath(self, path):
        for i in range(self.sourceList_lw.count()):
            if path == self.sourceList_lw.item(i).text:
                return False
        return True

######################################################### PROCESS

    def start(self):
        files = self.getFileListFromSource()
        if files:
            if self.target_le.source:
                out = False
            else:
                out = str(self.target_le.text())
                if not os.path.exists(out):
                    try:
                        pass
#                        os.makedirs(out, 0777)
                    except:
                        self.parent.message('Error out Folder!!!')
                        return
        self.batch = batchConverter.batchConverterClass(files, out, str(self.iconvert_lb.text()),self)
        self.startEndProcess(True)
        self.RAT_btn.setEnabled(False)
        self.batch.run()

    def getFileListFromSource(self):
        files = []
        folders = []
        extList = self.checkExtChecked()
        for i in range(self.sourceList_lw.count()):
            text = self.sourceList_lw.item(i).text
            if not os.path.isdir(text) and os.path.splitext(text)[1][1:].lower() in extList:
                if os.path.exists(text):
                    files.append(text)
            else:
                if os.path.exists(text):
                    folders.append(text)
        for f in folders:
            files += self.readFolder(f, extList, self.sub_cb.isChecked())

        return list(set(files))


    def readFolder(self, folder, ext, sub = 0,):
        files = []
        if os.path.exists(folder):
            list = os.listdir(folder)
            for l in list:
                if not os.path.isdir(os.path.join(folder,l)):
                    if os.path.splitext(l)[1][1:] in ext:
                        files.append(os.path.join(folder,l))
                else:
                    if sub:
                        files += self.readFolder(os.path.join(folder,l), ext, sub)
        return files

    def startEndProcess(self, p):
        self.stop_btn.setEnabled(p)
        self.RAT_btn.setEnabled(not p)
        self.sourceList_lw.setEnabled(not p)
        self.remove_btn.setEnabled(not p)
        self.browseFolder_btn.setEnabled(not p)
        self.browseFiles_btn.setEnabled(not p)
        self.show_btn.setEnabled(not p)
        self.extList_lw.setEnabled(not p)
        self.checkAll_btn.setEnabled(not p)
        self.unckeckAll_btn.setEnabled(not p)
        self.delExt_btn.setEnabled(not p)
        self.format_cb.setEnabled(not p)
        self.browseTarget_btn.setEnabled(not p)
        self.target_le.setEnabled(not p)
        self.sub_cb.setEnabled(not p)
        self.browsIconvert_btn.setEnabled(not p)
        self.newExt_le.setEnabled(not p)



    def stopProcess(self):
        self.batch.stop()
        self.setProcessBar(0)
        self.startEndProcess(False)

    def setProcessBar(self, val):
        self.progress_bar.setValue(val)

    def getOverWriteState(self):
        if self.over_rb.isChecked():
            return 1
        elif self.skip_rb.isChecked():
            return 2
        elif self.ask_rb.isChecked():
            return 3
        elif self.autoRename_rb.isChecked():
            return 4

    def complite(self):
        self.startEndProcess(False)
        
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('mycompany.myproduct.subproduct.version')

def main():
    app = QApplication(sys.argv)
    window=ratConvertClass()
    window.show()
    print window.windowTitle()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
