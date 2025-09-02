# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['fivem_launcher.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['win32com.client', 'winshell'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PIL', 'matplotlib', 'numpy', 'pandas', 'scipy', 'pytest', 
        'setuptools', 'distutils', 'email', 'http', 'urllib3', 'xml',
        'unittest', 'pydoc', 'doctest', 'argparse', 'multiprocessing',
        'concurrent', 'asyncio', 'sqlite3', 'ssl', 'socket', 'select',
        'mmap', 'pickle', 'zipfile', 'tarfile', 'gzip', 'bz2', 'lzma',
        'csv', 'decimal', 'fractions', 'statistics', 'wave', 'chunk',
        'sunau', 'aifc', 'sndhdr', 'colorsys', 'imghdr', 'turtle',
        'tkinter.test', 'tkinter.dnd', 'tkinter.colorchooser', 
        'tkinter.commondialog', 'tkinter.filedialog', 'tkinter.font',
        'tkinter.scrolledtext', 'tkinter.simpledialog', 'tkinter.tix',
        'tkinter.ttk'
    ],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='fivem_launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,  # UPX can cause issues with Windows Defender
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
)
