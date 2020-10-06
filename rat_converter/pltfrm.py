#! /usr/bin/python
import os
pl = None
defFolder = None
iconvert = None


if os.name == 'posix':
    pl = 'Lin'
    defFolder = '/'
    iconvert = 'iconvert'

elif os.name == 'nt':
    pl = 'Win'
    defFolder = 'C:/'
    iconvert = 'iconvert.exe'
elif os.name == 'os2':
    pl = 'Mac'
    defFolder = '/'
    iconvert = 'iconvert'