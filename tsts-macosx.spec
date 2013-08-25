# -*- mode: python -*-
a = Analysis(['tsts.py'],
             pathex=['/Users/kwan/Development/ld27_tsts'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.darwin/tsts', 'tsts'),
          debug=False,
          strip=None,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'tsts'))
app = BUNDLE(coll,
             Tree('assets', prefix='assets'),
             name=os.path.join('dist', 'tsts.app'))
