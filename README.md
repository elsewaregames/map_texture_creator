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

### Windows (CMD or PowerShell)

```cmd
build.bat
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
