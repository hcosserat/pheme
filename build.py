import PyInstaller.__main__
import os



PyInstaller.__main__.run([
    'main.py',
    '--name=Pheme',
    '--onefile',
    '--windowed',
    '--add-data=src;src',
    '--collect-all=matplotlib',
    '--hidden-import=matplotlib.backends.backend_tkagg',
    '--hidden-import=networkx',
    '--hidden-import=PIL',
    '--hidden-import=numpy',
    '--paths=src',
    '--clean',
    '--noconfirm'
])