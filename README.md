# Map Texture Creator

Map Texture Creator is a **game-oriented minimap texture generation tool**.  
It converts captured world map images into **clean, flat-colored, pixel-perfect minimap textures**, suitable for classic games and modern engines such as **Unreal Engine** and **Unity**.

The tool automatically:

- Removes background colors (any color)
- Crops maps perfectly (including non-rectangular shapes)
- Generates transparent PNGs
- Optionally flattens lighting for classic minimap aesthetics
- Supports batch processing
- Is fully configurable via YAML
- Can be distributed as a standalone executable

---

## Architecture

```
MapTextureCreator/
├── map_texture_creator.py     # Core processing logic
├── config.yaml                # Tool configuration
│
├── in/                        # Input map textures
├── out/                       # Generated minimap textures
│
├── build.sh                   # Linux / Git Bash build script
├── build.bat                  # Windows CMD build script
│
└── bin/                       # Compiled executable output
```

### Processing Pipeline

1. **Input Discovery**  
   Scans the `in/` directory for supported image formats.

2. **Optional Color Flattening**  
   Removes lighting, shadows, gradients, and gloss to produce flat, readable minimap colors.

3. **Background Removal**  
   Uses K-Means clustering to detect and remove background regions of any color.

4. **Mask Refinement**  
   Cleans edges using morphological operations to ensure pixel-perfect silhouettes.

5. **Cropping & Export**  
   Crops tightly to visible map content and exports transparent PNG textures to `out/`.

---

## Configuration

All behavior is controlled via `config.yaml`.

Example configuration:

```yaml
paths:
  input_dir: "in"
  output_dir: "out"

processing:
  kmeans_clusters: 4
  alpha_threshold: 200

flatten_colors:
  enabled: true
  target_luminance: 160

files:
  extensions:
    - ".png"
    - ".jpg"
    - ".jpeg"
    - ".tga"

logging:
  show_progress: true
  show_stats: true
```

---

## How to Run

**Using the executable (recommended):**  
Download the latest release, extract it, place your images in the `in/` folder, and run `MapTextureCreator.exe`. Generated minimap textures will appear in the `out/` folder. No Python installation is required.

**Running from source:**  
Install Python 3.9+, install dependencies using `pip install -r requirements.txt`, place images in the `in/` folder, and run `python map_texture_creator.py`.

---

## Install

### Requirements (for source usage)

- Python **3.9+**
- pip

### Install Dependencies

All required Python dependencies are listed in `requirements.txt`.

Install them using:

```bash
pip install -r requirements.txt
```

> If you use the compiled executable, **Python is not required**.

---

## Build

### Linux / Git Bash / WSL

```bash
chmod +x build.sh
./build.sh
```

### Build Output

After a successful build:

```
bin/
└── MapTextureCreator.exe
```

To run the tool:

- Place `config.yaml`, `in/`, and `out/` next to the executable
- Run `MapTextureCreator.exe`

---

## Release

Releases are used to distribute **stable, ready-to-use builds** of Map Texture Creator for end users.

Each release represents a **versioned snapshot** of the tool and includes a downloadable package containing the executable and default configuration.

---

### Release Contents

Each release package includes:

- `MapTextureCreator.exe` – Standalone Windows executable
- `config.yaml` – Default configuration file
- `in/` – Input directory for map textures
- `out/` – Output directory for generated minimaps

Release packages are distributed as a single ZIP file:

`map_texture_creator_vX-Y-Z.zip`

Example:  
`map_texture_creator_v1-0-0.zip`

---

### Versioning

Map Texture Creator follows **Semantic Versioning**:

MAJOR.MINOR.PATCH

- **MAJOR** – Breaking changes
- **MINOR** – New features (backward compatible)
- **PATCH** – Bug fixes only

The version number is:

- Defined in the source code
- Used in the release filename
- Matched with the GitHub release tag

---

### Creating a Release (Maintainers)

1. Ensure the `main` branch is stable and up to date
2. Build the executable using `build.sh`
3. Create the release package using `release.sh`
4. Upload the generated ZIP from the `releases/` directory to **GitHub Releases**
5. Create a Git tag matching the version (for example `v1.0.0`)

---

### Downloading a Release (Users)

1. Go to the **Releases** section on GitHub
2. Download the latest ZIP file
3. Extract the archive
4. Update `config.yaml` if needed
5. Place input images in the `in/` directory
6. Run `MapTextureCreator.exe`

---

### Notes

- Releases are built for **Windows**
- Python is **not required** when using release builds
- Source code remains available for advanced users and contributors

Releases are the **recommended way** to use Map Texture Creator.

## Contribution

Contributions are welcome.

### Guidelines

- Keep the processing pipeline deterministic
- Avoid engine-specific dependencies
- Maintain YAML-based configuration
- Follow existing logging and structure conventions

### Suggested Improvements

- Style presets
- Circular minimap masking
- Power-of-two resizing
- Unreal Engine import automation
- CI builds and installers

---

## License

This project is intended for **game development and tooling use**.  
Add a license file (MIT, Apache 2.0, or proprietary) as appropriate.
