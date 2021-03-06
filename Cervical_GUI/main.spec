# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=[
                          'C:\\Users\\Guillaume\\Documents\\GitHub\\projetlong\\Cervical_GUI',
                          'C:\\Users\\Guillaume\\AppData\\Local\\Programs\\Python\\Python36-32\\Lib\\site-packages\\scipy\\extra-dll',
             ],
             binaries=[],
             datas=[],
             hiddenimports=[
                          'scipy.special._ufuncs_cxx',
                          'scipy.linalg.cython_blas',
                          'scipy.linalg.cython_lapack',
                          'scipy.integrate',
                          'scipy.integrate.quadrature',
                          'scipy.integrate.odepack',
                          'scipy.integrate._odepack',
                          'scipy.integrate.quadpack',
                          'scipy.integrate._quadpack',
                          'scipy.integrate._ode',
                          'scipy.integrate.vode',
                          'scipy.integrate._dop',
                          'scipy.integrate.lsoda',
                          'scipy.interpolate',
                          'scipy.linalg',
                          'scipy.linalg.misc',
                          'scipy.linalg.blas',
                          'scipy._lib.messagestream',
                          'sklearn.neighbors.typedefs',
                          'pywt._extensions._cwt',
             ],
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
          name='main',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='icone.ico')
