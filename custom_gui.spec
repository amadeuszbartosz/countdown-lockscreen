# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['custom_gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Countdown Creator',  # changed exe name
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app-icons.icns'],
)
app = BUNDLE(
    exe,
    name='Countdown Creator.app',  # changed bundle name
    icon='/Users/amadeuszbartosz/Desktop/Projects/Yearly Countdown - Lockerscreen/assets/app-icon.icns',
    bundle_identifier=None,
)
