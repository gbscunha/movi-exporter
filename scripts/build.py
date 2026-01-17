#!/usr/bin/env python
"""
Script de build para gerar o executável do Movi Exporter.

Uso:
    python scripts/build.py [--onedir]

Opções:
    --onedir: Gera uma pasta ao invés de um único executável (mais rápido para iniciar)
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Diretório raiz do projeto
ROOT_DIR = Path(__file__).parent.parent
BUILD_DIR = ROOT_DIR / "build"
DIST_DIR = ROOT_DIR / "dist"


def clean():
    """Limpa diretórios de build anteriores."""
    print("🧹 Limpando builds anteriores...")
    
    for dir_path in [BUILD_DIR, DIST_DIR]:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"   Removido: {dir_path}")


def build(onedir: bool = False):
    """Executa o PyInstaller."""
    print("🔨 Iniciando build...")
    
    spec_file = ROOT_DIR / "movi_exporter.spec"
    
    if not spec_file.exists():
        print("❌ Arquivo movi_exporter.spec não encontrado!")
        sys.exit(1)
    
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        str(spec_file),
        "--clean",
        "--noconfirm",
    ]
    
    if onedir:
        # Sobrescrever para onedir (mais rápido para debug)
        cmd = [
            sys.executable,
            "-m",
            "PyInstaller",
            "--clean",
            "--noconfirm",
            "--onedir",
            "--windowed",
            "--name", "MoviExporter",
            "--collect-data", "customtkinter",
            str(ROOT_DIR / "src" / "gui" / "main.py"),
        ]
    
    print(f"   Comando: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, cwd=ROOT_DIR)
    
    if result.returncode != 0:
        print("❌ Build falhou!")
        sys.exit(1)
    
    print("✅ Build concluído!")


def show_result():
    """Mostra o resultado do build."""
    print("\n📦 Resultado do build:")
    
    for item in DIST_DIR.iterdir():
        if item.is_file():
            size_mb = item.stat().st_size / (1024 * 1024)
            print(f"   📄 {item.name} ({size_mb:.1f} MB)")
        elif item.is_dir():
            # Calcular tamanho total da pasta
            total_size = sum(f.stat().st_size for f in item.rglob("*") if f.is_file())
            size_mb = total_size / (1024 * 1024)
            print(f"   📁 {item.name}/ ({size_mb:.1f} MB)")


def main():
    os.chdir(ROOT_DIR)
    
    onedir = "--onedir" in sys.argv
    
    print("=" * 50)
    print("🚀 Movi Exporter - Build Script")
    print("=" * 50)
    print()
    
    clean()
    build(onedir=onedir)
    show_result()
    
    print()
    print("=" * 50)
    print("✅ Build finalizado com sucesso!")
    print("=" * 50)


if __name__ == "__main__":
    main()
