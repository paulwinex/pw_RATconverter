#! /usr/bin/python
from imports import *

processes = set([])

class batchConverterClass():
    def __init__(self, fileList,targetFolder, iconvert, parent):
        self.fileList = fileList
        self.par = parent
        self.bin = iconvert
        self.targetFolder = targetFolder
        self.process = True
        self.format = self.par.outFormats[self.par.format_cb.currentIndex()]


    def run(self):
        if self.fileList:
            self.files = []
            for i, f in enumerate(self.fileList):
                if os.path.exists(f):
                    targ = None
                    if not self.targetFolder:
                        targ = os.path.splitext(f)[0] + '.' + self.format
                        if targ == f:continue
                    else:
                        if os.path.exists(self.targetFolder):
                            targ = os.path.join(self.targetFolder, os.path.splitext(os.path.basename(f))[0] + '.' + self.format)
                    self.files.append([f,targ])
            self.end = len(self.files)
            self.batch()

    def batch(self, i=None):
        self.i=i
        if self.i == None:
            self.i = 0
        if self.files and self.process:
            s = self.files[self.i][0]
            t = self.files[self.i][1]
            t = self.checktarget(t)
            if t:
                st = os.stat(s)
                size = st.st_size / 1000000.0
                self.par.message(str(self.i+1) + '/' + str(self.end) + ': ' + os.path.basename(s) + ' | ' + str(str(round(size , 2)) )+ 'Mb')
                self.convertFile(s,t)
                proc = int((float(self.i)/len(self.files))*100)
                self.par.setProcessBar(proc)

            else:
                proc = int((float(self.i)/len(self.files))*100)
                self.par.setProcessBar(proc)
                self.next()


    def next(self):

        self.i += 1
        if self.i < self.end:
            self.batch(self.i)
        else:
            self.par.setProcessBar(100)
            self.par.message('Completed!!!')
            self.par.complite()

    def checktarget(self,path):
        if os.path.exists(path):
            state = self.par.getOverWriteState()
            if state == 1:
                return path
            elif state ==  2:
                return False
            elif state == 3:
                p = QFileDialog.getSaveFileName(self.par, 'Save Rat', os.path.dirname(path),"*.rat")
                return str(p)
            elif state == 4:
                while os.path.exists(path):
                    path = self.incSave(path)
                return path

        return path


    def convertFile(self, source, target):
        cmd = ' '.join([self.bin, '"'+source+'"', '"'+target+'"'])
        self.proc = QProcess()
        processes.add(self.proc)
#        self.proc.start('notepad')
        self.proc.start(cmd)
        self.proc.finished.connect(lambda: self.next())

    def stop(self):
        self.process = False
        self.proc.kill()
        self.par.message('Stopped...')

    def incSave(self, path):
        nameExt = os.path.basename(path)
        name, ext = os.path.splitext(nameExt)
        dir = os.path.dirname(path)
        splt = name.split('_')
        nameNum = '01'
        if len(splt) > 1:
            num = splt[-1]
            if num.isdigit():
                nameNum = int(num) + 1
                nzero = len(num)
                if nzero < 2: nzero = 2
                if nzero > len(str(nameNum)):
                    nameNum = str(nameNum).zfill(nzero)
                nName = '_'.join(splt[:-1]) + '_' + nameNum
            else:
                nName = '_'.join(splt) + '_' + nameNum
        else:
            nName = name + '_' + str(nameNum)
        result = '/'.join([dir,nName+ext])
        return result

