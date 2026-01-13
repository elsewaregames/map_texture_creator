#!/usr/bin/env bash

set -e

APP_NAME="MapTextureCreator"
EXECUTABLE="MapTextureCreator.exe"
RELEASE_DIR="releases"
BIN_DIR="bin"

echo "=========================================="
echo " Map Texture Creator - Release Builder"
echo "=========================================="

# -------------------------------
# Ask for version
# -------------------------------
read -p "Enter release version (e.g. 1.0.0): " VERSION

if [[ -z "$VERSION" ]]; then
  echo "[ERROR] Version cannot be empty."
  exit 1
fi

VERSION_TAG="v${VERSION//./-}"
ZIP_NAME="map_texture_creator_${VERSION_TAG}.zip"
ZIP_PATH="${RELEASE_DIR}/${ZIP_NAME}"

# -------------------------------
# Validate executable
# -------------------------------
if [[ ! -f "${BIN_DIR}/${EXECUTABLE}" ]]; then
  echo "[ERROR] Executable not found: ${BIN_DIR}/${EXECUTABLE}"
  echo "Build the project first."
  exit 1
fi

# -------------------------------
# Handle existing release
# -------------------------------
if [[ -f "$ZIP_PATH" ]]; then
  echo "[WARN] Release already exists: $ZIP_NAME"
  read -p "Overwrite? (y/n): " OVERWRITE

  if [[ "$OVERWRITE" != "y" ]]; then
    read -p "Enter NEW version: " VERSION
    VERSION_TAG="v${VERSION//./-}"
    ZIP_NAME="map_texture_creator_${VERSION_TAG}.zip"
    ZIP_PATH="${RELEASE_DIR}/${ZIP_NAME}"
  fi
fi

# -------------------------------
# Prepare temp release structure
# -------------------------------
TMP_DIR="$(mktemp -d)"

echo "[INFO] Preparing release structure..."

mkdir -p "${TMP_DIR}/in"
mkdir -p "${TMP_DIR}/out"

# IMPORTANT: copy exe to ROOT (not /bin)
cp "${BIN_DIR}/${EXECUTABLE}" "${TMP_DIR}/"
cp "config.yaml" "${TMP_DIR}/"

touch "${TMP_DIR}/in/.gitkeep"
touch "${TMP_DIR}/out/.gitkeep"

# -------------------------------
# Create zip (Windows-safe)
# -------------------------------
mkdir -p "${RELEASE_DIR}"

echo "[INFO] Creating release zip..."

TMP_DIR_WIN=$(cygpath -w "${TMP_DIR}")
ZIP_PATH_WIN=$(cygpath -w "${ZIP_PATH}")

powershell.exe -NoProfile -Command "
  Compress-Archive -Path '${TMP_DIR_WIN}\*' -DestinationPath '${ZIP_PATH_WIN}' -Force
"

# -------------------------------
# Cleanup
# -------------------------------
rm -rf "${TMP_DIR}"

echo "=========================================="
echo " Release created successfully!"
echo " File: ${ZIP_PATH}"
echo "=========================================="
