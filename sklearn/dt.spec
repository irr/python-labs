# -*- mode: python -*-

block_cipher = None

from PyInstaller.utils.hooks import collect_submodules

a = Analysis(['dt.py'],
             hiddenimports = collect_submodules('sklearn'),
             pathex=['/home/irocha/git/python-labs/sklearn'],
             binaries=None,
             datas=None,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='dt',
          debug=False,
          strip=False,
          upx=True,
          console=True )
