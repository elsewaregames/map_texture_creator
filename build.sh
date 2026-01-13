#!/usr/bin/env bash

set -e

echo "=========================================="
echo " Building MapTextureCreator executable"
echo "=========================================="

# Clean previous builds
echo "[INFO] Cleaning old builds..."
rm -rf build dist bin/MapTextureCreator.exe 2>/dev/null || true

# Ensure bin directory exists
mkdir -p bin

# Run PyInstaller
echo "[INFO] Running PyInstaller..."
pyinstaller \
  --onefile \
  --clean \
  --name MapTextureCreator \
  --distpath bin \
  map_texture_creator.py

echo "=========================================="
echo " Build completed successfully!"
echo " Output: bin/MapTextureCreator.exe"
echo "=========================================="
