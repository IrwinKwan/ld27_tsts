# -*- mode: python -*-
a = Analysis(['tsts.py'],
             pathex=['Z:\\Development\\ld27_tsts'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
		Tree('assets', prefix='assets'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'tsts.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True )
