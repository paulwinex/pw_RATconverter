# -*- mode: python -*-
import os


name = 'RATConverter.exe'

a = Analysis(['launcher.py'],
             pathex=['.'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=name,
          debug=False,
          strip=None,
          upx=True,
          icon='icons/ratconverter.ico',
          console=False)
