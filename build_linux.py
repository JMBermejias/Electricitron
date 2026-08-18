#!/usr/bin/env python3
"""Script de build para Electricitron - Linux DEB."""
import subprocess
import sys
import os
import shutil


def build_linux_deb():
    """Build .deb package for Debian/Ubuntu."""
    version = "1.0.0"
    pkg_name = "electricitron"
    build_dir = f"deb_build/{pkg_name}_{version}_amd64"
    bin_dir = f"{build_dir}/usr/bin"
    deb_dir = f"{build_dir}/DEBIAN"
    share_dir = f"{build_dir}/usr/share/applications"
    icon_dir_256 = f"{build_dir}/usr/share/icons/hicolor/256x256/apps"
    icon_dir_128 = f"{build_dir}/usr/share/icons/hicolor/128x128/apps"
    icon_dir_64 = f"{build_dir}/usr/share/icons/hicolor/64x64/apps"
    icon_dir_48 = f"{build_dir}/usr/share/icons/hicolor/48x48/apps"
    icon_dir_32 = f"{build_dir}/usr/share/icons/hicolor/32x32/apps"
    icon_dir_16 = f"{build_dir}/usr/share/icons/hicolor/16x16/apps"

    if os.path.exists("deb_build"):
        shutil.rmtree("deb_build")

    for d in [bin_dir, deb_dir, share_dir, icon_dir_256, icon_dir_128, icon_dir_64, icon_dir_48, icon_dir_32, icon_dir_16]:
        os.makedirs(d, exist_ok=True)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=electricitron",
        "--windowed",
        "--onefile",
        "--add-data=assets:assets",
        "--clean",
        "--noconfirm",
        "--distpath=deb_build/usr/bin",
        "electricitron/main.py"
    ]
    if os.path.exists("assets/icon.png"):
        cmd.insert(5, "--icon=assets/icon.png")
    print("Compilando ejecutable...")
    subprocess.run(cmd, check=True)

    control = f"""Package: {pkg_name}
Version: {version}
Section: utils
Priority: optional
Architecture: amd64
Depends: libgl1, libglib2.0-0, libfontconfig1, libxrender1
Maintainer: jmbernabeu <jmbernabeu@users.noreply.github.com>
Description: Electricitron - Calculos Electricos y Telecomunicaciones
 Software profesional para calculos electricos, secciones de cables,
 protecciones, instalaciones, telecomunicaciones y distancias.
 Exporta informes en PDF y Excel.
"""
    with open(f"{deb_dir}/control", "w") as f:
        f.write(control)

    desktop = f"""[Desktop Entry]
Name=Electricitron
Comment=Software de calculos electricos y telecomunicaciones
Exec=/usr/bin/electricitron
Icon=electricitron
Terminal=false
Type=Application
Categories=Utility;Engineering;Education;
Keywords=electricidad;electrical;calculation;
"""
    with open(f"{share_dir}/electricitron.desktop", "w") as f:
        f.write(desktop)

    icon_mapping = {
        "assets/icon_256.png": icon_dir_256,
        "assets/icon_128.png": icon_dir_128,
        "assets/icon_64.png": icon_dir_64,
        "assets/icon_48.png": icon_dir_48,
        "assets/icon_32.png": icon_dir_32,
        "assets/icon_16.png": icon_dir_16,
    }
    for src, dst in icon_mapping.items():
        if os.path.exists(src):
            shutil.copy(src, f"{dst}/electricitron.png")
            print(f"  Icon: {src} -> {dst}/electricitron.png")

    if os.path.exists("assets/icon.png"):
        shutil.copy("assets/icon.png", f"{icon_dir_256}/electricitron.png")

    deb_file = f"{pkg_name}_{version}_amd64.deb"
    cmd = ["dpkg-deb", "--build", build_dir, deb_file]
    subprocess.run(cmd, check=True)
    print(f"Build DEB completado: {deb_file}")
    return deb_file


if __name__ == "__main__":
    build_linux_deb()
