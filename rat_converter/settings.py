import os, json

class settingsClass():
    def __init__(self, filename):
        """
        Work with settings. Settings file will be saved in home dir
        """
        home = os.path.expanduser('~')
        self.path = os.path.join(home,filename+'.json')

    def readSettings(self, name, defaultVal=False):
        """
        Read settings. Must have default value
        """
        data = self.__read()
        v = data.get(name)
        if v:
            return v
        else:
            data[name] = defaultVal
            self.__write(data)
            return defaultVal

    def writeSettings(self, data=None):
        self.__write(data)

    def writeValue(self, name, val):
        """
        write value
        """
        data = self.__read()
        data[name] = val
        self.__write(data)

    def __read(self):
        if os.path.exists(self.path):
            return json.load(open(self.path))
        else:
            return {}

    def __write(self, data):
        json.dump(data, open(self.path, 'w'), indent=2)

