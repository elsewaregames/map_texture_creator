import cv2
import numpy as np
import os
import time
import yaml
import sys

__app_name__ = "Map Texture Creator"
__version__ = "1.0.0"


def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()

# -------------------------------
# Load Config
# -------------------------------
CONFIG_FILE = os.path.join(BASE_PATH, "config.yaml")

with open(CONFIG_FILE, "r") as f:
    config = yaml.safe_load(f)

INPUT_DIR = os.path.join(BASE_PATH, config["paths"]["input_dir"])
OUTPUT_DIR = os.path.join(BASE_PATH, config["paths"]["output_dir"])

KMEANS_CLUSTERS = config["processing"]["kmeans_clusters"]
ALPHA_THRESHOLD = config["processing"]["alpha_threshold"]

FLATTEN_ENABLED = config["flatten_colors"]["enabled"]
TARGET_LUMINANCE = config["flatten_colors"]["target_luminance"]

VALID_EXTENSIONS = tuple(config["files"]["extensions"])

SHOW_PROGRESS = config["logging"]["show_progress"]
SHOW_STATS = config["logging"]["show_stats"]

def kmeans_numpy(pixels, k, max_iters=20):
    """
    Simple NumPy-based KMeans.
    pixels: (N, 3)
    returns: labels (N,)
    """
    # Randomly choose initial centers
    rng = np.random.default_rng(0)
    centers = pixels[rng.choice(len(pixels), k, replace=False)]

    for _ in range(max_iters):
        # Compute distances to centers
        distances = np.linalg.norm(
            pixels[:, None, :] - centers[None, :, :],
            axis=2
        )

        # Assign clusters
        labels = np.argmin(distances, axis=1)

        # Recompute centers
        new_centers = np.array([
            pixels[labels == i].mean(axis=0)
            if np.any(labels == i) else centers[i]
            for i in range(k)
        ])

        # Convergence check
        if np.allclose(centers, new_centers):
            break

        centers = new_centers

    return labels



# -------------------------------
# Core Logic
# -------------------------------
def remove_background_pixel_perfect(img):
    h, w, _ = img.shape
    pixels = img.reshape((-1, 3)).astype(np.float32)

    labels = kmeans_numpy(pixels, KMEANS_CLUSTERS)

    label_map = labels.reshape((h, w))

    border_labels = np.concatenate([
        label_map[0, :],
        label_map[-1, :],
        label_map[:, 0],
        label_map[:, -1]
    ])

    bg_clusters = np.unique(border_labels)

    mask = np.ones((h, w), dtype=np.uint8) * 255
    for bg in bg_clusters:
        mask[label_map == bg] = 0

    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    mask = np.where(mask > ALPHA_THRESHOLD, 255, 0).astype(np.uint8)
    return mask


def flatten_colors(img):
    """
    Removes lighting & gradients.
    Produces flat GTA-style minimap colors.
    """
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # FIX: split LAB image, not 'l'
    l, a, b = cv2.split(lab)

    # Replace luminance with constant value
    l_flat = np.full_like(l, TARGET_LUMINANCE)

    flat_lab = cv2.merge((l_flat, a, b))
    flat_bgr = cv2.cvtColor(flat_lab, cv2.COLOR_LAB2BGR)

    return flat_bgr



def extract_map(image_path, output_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"[ERROR] Failed to load: {image_path}")
        return False

    if FLATTEN_ENABLED:
        img = flatten_colors(img)

    mask = remove_background_pixel_perfect(img)

    coords = cv2.findNonZero(mask)
    if coords is None:
        print(f"[WARN] No map detected: {image_path}")
        return False

    x, y, w, h = cv2.boundingRect(coords)

    cropped_img = img[y:y+h, x:x+w]
    cropped_mask = mask[y:y+h, x:x+w]

    rgba = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2BGRA)
    rgba[:, :, 3] = cropped_mask

    cv2.imwrite(output_path, rgba)
    return True


# -------------------------------
# Main
# -------------------------------
def main():
    print(f"{__app_name__} v{__version__}")
    print("------------------------------------")

    start_time = time.time()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = [
        f for f in os.listdir(INPUT_DIR)
        if f.lower().endswith(VALID_EXTENSIONS)
    ]

    total_files = len(files)
    success_count = 0
    fail_count = 0

    if total_files == 0:
        print("[INFO] No valid image files found.")
        return

    for idx, file in enumerate(files, start=1):
        if SHOW_PROGRESS:
            print(f"[{idx}/{total_files}] Processing: {file}")

        input_path = os.path.join(INPUT_DIR, file)
        name, _ = os.path.splitext(file)
        output_path = os.path.join(OUTPUT_DIR, f"{name}.png")

        if extract_map(input_path, output_path):
            success_count += 1
            if SHOW_PROGRESS:
                print(f"    -> [OK] Saved: {output_path}")
        else:
            fail_count += 1
            if SHOW_PROGRESS:
                print(f"    -> [FAILED]")

    if SHOW_STATS:
        elapsed_time = time.time() - start_time
        print("\n========= MAP TEXTURE CREATOR STATS =========")
        print(f"Total files found      : {total_files}")
        print(f"Processed successfully : {success_count}")
        print(f"Failed                 : {fail_count}")
        print(f"Flatten colors enabled : {FLATTEN_ENABLED}")
        print(f"Output directory       : {OUTPUT_DIR}")
        print(f"Total time             : {elapsed_time:.2f} seconds")
        print("============================================")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("\n[ERROR] Press ENTER to exit...")

