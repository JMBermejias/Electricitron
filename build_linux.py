#!/usr/bin/env python3
"""Script de build para Electricitron - Linux DEB."""
import subprocess
import sys
import os
import shutil


def build_linux_deb():
    version = "1.1.1"
    pkg_name = "electricitron"
    build_dir = f"deb_build/{pkg_name}_{version}_amd64"
    bin_dir = f"{build_dir}/usr/bin"
    deb_dir = f"{build_dir}/DEBIAN"
    share_dir = f"{build_dir}/usr/share/applications"
    icons_dir = f"{build_dir}/usr/share/icons/hicolor"
    pixmap_dir = f"{build_dir}/usr/share/pixmaps"

    if os.path.exists("deb_build"):
        shutil.rmtree("deb_build")

    dirs = [bin_dir, deb_dir, share_dir, pixmap_dir]
    for size in [16, 32, 48, 64, 128, 256]:
        dirs.append(f"{icons_dir}/{size}x{size}/apps")
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=electricitron",
        "--windowed",
        "--onefile",
        "--add-data=assets:assets",
        "--clean",
        "--noconfirm",
        "--distpath", f"{build_dir}/usr/bin",
        "electricitron/main.py"
    ]
    if os.path.exists("assets/icon.png"):
        cmd.insert(5, "--icon=assets/icon.png")
    print("Compilando ejecutable...")
    subprocess.run(cmd, check=True)

    bin_path = f"{build_dir}/usr/bin/electricitron"
    size_kb = int(os.path.getsize(bin_path) / 1024) if os.path.exists(bin_path) else 100000

    with open(f"{deb_dir}/control", "w") as f:
        f.write(f"Package: {pkg_name}\n")
        f.write(f"Version: {version}\n")
        f.write("Section: utils\n")
        f.write("Priority: optional\n")
        f.write("Architecture: amd64\n")
        f.write(f"Installed-Size: {size_kb}\n")
        f.write("Depends: libgl1, libglib2.0-0, libfontconfig1, libxrender1\n")
        f.write("Maintainer: jmbernabeu <jmbernabeu@users.noreply.github.com>\n")
        f.write("Homepage: https://github.com/JMBermejias/Electricitron\n")
        f.write("Description: Electricitron - Calculos Electricos y Telecomunicaciones\n")
        f.write(" Software profesional para calculos electricos, secciones de cables,\n")
        f.write(" protecciones, instalaciones, telecomunicaciones y distancias.\n")

    postinst = """#!/bin/sh
set -e
gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || true
update-desktop-database /usr/share/applications 2>/dev/null || true
cp /usr/share/icons/hicolor/256x256/apps/electricitron.png /usr/share/pixmaps/ 2>/dev/null || true
cp /usr/share/icons/hicolor/128x128/apps/electricitron.png /usr/share/pixmaps/ 2>/dev/null || true
exit 0
"""
    with open(f"{deb_dir}/postinst", "w") as f:
        f.write(postinst)
    os.chmod(f"{deb_dir}/postinst", 0o755)

    postrm = """#!/bin/sh
set -e
if [ "$1" = "remove" ] || [ "$1" = "purge" ]; then
    rm -f /usr/share/pixmaps/electricitron.png 2>/dev/null || true
    rm -rf /usr/share/icons/hicolor/*/apps/electricitron.png 2>/dev/null || true
    rm -f /usr/share/applications/electricitron.desktop 2>/dev/null || true
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || true
    update-desktop-database /usr/share/applications 2>/dev/null || true
fi
exit 0
"""
    with open(f"{deb_dir}/postrm", "w") as f:
        f.write(postrm)
    os.chmod(f"{deb_dir}/postrm", 0o755)

    desktop = "[Desktop Entry]\nName=Electricitron\nGenericName=Calculos Electricos\nComment=Software de calculos electricos y telecomunicaciones\nExec=/usr/bin/electricitron %F\nIcon=electricitron\nTerminal=false\nType=Application\nStartupNotify=true\nCategories=Utility;Engineering;Education;Science;\nKeywords=electricidad;electrical;calculation;telecom;\n"
    with open(f"{share_dir}/electricitron.desktop", "w") as f:
        f.write(desktop)
    os.chmod(f"{share_dir}/electricitron.desktop", 0o644)

    icon_files = {
        "assets/icon_256.png": f"{icons_dir}/256x256/apps/electricitron.png",
        "assets/icon_128.png": f"{icons_dir}/128x128/apps/electricitron.png",
        "assets/icon_64.png": f"{icons_dir}/64x64/apps/electricitron.png",
        "assets/icon_48.png": f"{icons_dir}/48x48/apps/electricitron.png",
        "assets/icon_32.png": f"{icons_dir}/32x32/apps/electricitron.png",
        "assets/icon_16.png": f"{icons_dir}/16x16/apps/electricitron.png",
    }
    for src, dst in icon_files.items():
        if os.path.exists(src):
            shutil.copy(src, dst)
            os.chmod(dst, 0o644)

    if os.path.exists("assets/icon.png"):
        shutil.copy("assets/icon.png", f"{pixmap_dir}/electricitron.png")
        os.chmod(f"{pixmap_dir}/electricitron.png", 0o644)

    for root, dnames, fnames in os.walk(build_dir):
        for fn in fnames:
            os.chmod(os.path.join(root, fn), 0o644)
        for dn in dnames:
            os.chmod(os.path.join(root, dn), 0o755)
    os.chmod(f"{deb_dir}/postinst", 0o755)
    os.chmod(f"{deb_dir}/postrm", 0o755)
    os.chmod(bin_path, 0o755)

    deb_file = f"{pkg_name}_{version}_amd64.deb"
    subprocess.run(["dpkg-deb", "--build", "--root-owner-group", build_dir, deb_file], check=True)

    print(f"\nBuild DEB completado: {deb_file}")
    print("\nEstructura:")
    subprocess.run(["find", build_dir, "-type", "f"], check=False)
    return deb_file


if __name__ == "__main__":
    build_linux_deb()
