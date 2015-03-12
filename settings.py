import os
from PyQt4.QtCore import QSettings

class settingsClass():
    def __init__(self, filename):
        """
        Work with settings. Settings file will be saved in home dir
        """
        home = os.path.expanduser('~')
        path = os.path.join(home,filename+'.ini')
        self.s = QSettings(path,QSettings.IniFormat)

    def readSettings(self, name, defaultVal=False):
        """
        Read settings. Must have default value
        """
        v = self.s.value(name)
        if v:
            return v
        else:
            self.writeValue(name, defaultVal)
            return defaultVal

    def writeSettings(self, dic = None):
        """
        Write settings from dic
        #'set1/val1':12,
         'set1/val2':34,
         'se2/x':'one',
         'set2/y':'two'}
        """
        if dic:
            for set in dic:
                self.s.setValue(set,dic[set])
            return True
        else:
            return False

    def writeValue(self, name, val):
        """
        write value
        """
        try:
            self.s.setValue(name,val)
        except:
            print 'Error write settings', name, val
            return False

