# -*- mode: python ; coding: utf-8 -*-
"""
Configuração PyInstaller para Movi Exporter App.

Para gerar o executável:
    pyinstaller movi_exporter.spec

Ou via script:
    python scripts/build.py
"""

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Caminhos
block_cipher = None
root_dir = os.path.dirname(os.path.abspath(SPEC))

# Importa __version__ do código fonte para manter spec e GUI sincronizados.
sys.path.insert(0, root_dir)
from src.gui import __version__ as APP_VERSION  # noqa: E402

# Coletar dados do CustomTkinter (necessário para temas e fontes)
customtkinter_datas = collect_data_files('customtkinter')

# Arquivos de dados adicionais
datas = [
    # CustomTkinter assets
    *customtkinter_datas,
    # Fonte FontAwesome (ícones da GUI) — deve ir junto no bundle.
    ('src/gui/assets/fontawesome-solid.ttf', 'src/gui/assets'),
    # Manual do usuário (HTML embarcado) — aberto pelo botão na sidebar.
    ('docs/manual', 'docs/manual'),
]

# Logo Movi (opcional) — incluída no bundle apenas se o arquivo existir.
if os.path.exists('src/gui/assets/movi-logo.png'):
    datas.append(('src/gui/assets/movi-logo.png', 'src/gui/assets'))

# Módulos ocultos (imports dinâmicos)
hiddenimports = [
    'customtkinter',
    'PIL._tkinter_finder',
    'packaging',
    'packaging.version',
    'packaging.specifiers',
    'packaging.requirements',
    # Google APIs
    'google.auth',
    'google.oauth2',
    'google_auth_oauthlib',
    'googleapiclient',
]

# Submodules
hiddenimports += collect_submodules('google')
hiddenimports += collect_submodules('googleapiclient')

a = Analysis(
    ['src/gui/main.py'],
    pathex=[root_dir],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy.distutils',
        'scipy',
        'pytest',
        'IPython',
        'jupyter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MoviExporter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    # UPX comprime binários, mas com PyInstaller costuma causar falsos positivos
    # de antivírus e corromper algumas DLLs no Windows — manter desligado.
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI app, sem console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Ícone (descomente e ajuste o caminho)
    # icon='assets/icon.ico',
)

# Para macOS: criar .app bundle
app = BUNDLE(
    exe,
    name='MoviExporter.app',
    icon=None,  # 'assets/icon.icns' para macOS
    bundle_identifier='com.movisolutions.exporter',
    info_plist={
        'CFBundleName': 'Movi Exporter',
        'CFBundleDisplayName': 'Movi Exporter',
        'CFBundleVersion': APP_VERSION,
        'CFBundleShortVersionString': APP_VERSION,
        'NSHighResolutionCapable': True,
    },
)
