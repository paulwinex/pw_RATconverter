import os
soft = 'houdini'
path = os.path.join(os.path.expanduser('~'), 'localsettings.py')
if os.path.exists(path):
    import imp
    loc = imp.load_source('localSettings', path)
    loc.run(soft)
