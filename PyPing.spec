# -*- mode: python -*-

block_cipher = None


a = Analysis(['PyPing.py'],
             pathex=['E:\\cosas\\py\\PyPing'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas+= [('icono.ico', 'E:\\Cosas\\py\\PyPing\\icono.ico', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='PyPing',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='E:\\Cosas\\py\\PyPing\\icono.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='PyPing')
