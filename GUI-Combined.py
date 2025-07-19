import numpy as np
import cv2
import matplotlib.pyplot as plt
import rasterio
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from scipy.signal import correlate2d
from scipy.ndimage import shift
from scipy.optimize import minimize
from skimage.util import crop
from sklearn.metrics import mutual_info_score

# ======= Utility Functions =======

def normalize(band):
    band = (band - np.min(band)) / (np.max(band) - np.min(band))
    return (band * 255).astype(np.uint8)

def load_rgb_bands(filepath):
    with rasterio.open(filepath) as src:
        r = src.read(1)
        g = src.read(2)
      # g = np.roll(g, 1, axis=0)
    return normalize(r), normalize(g)

def load_individual_band(filepath):
    with rasterio.open(filepath) as src:
        band = src.read(1)
    return normalize(band)


# ======= Detection Methods =======

def detect_FM(r, g, method):
    if method == "ORB":
        fm = cv2.ORB_create(500)
        norm_type = cv2.NORM_HAMMING
    elif method == "SIFT":
        fm = cv2.SIFT_create()
        norm_type = cv2.NORM_L2
    else:
        raise ValueError(f"Unsupported method: {method}")

    matcher = cv2.BFMatcher(norm_type, crossCheck=True)

    kp1, des1 = fm.detectAndCompute(r, None)
    kp2, des2 = fm.detectAndCompute(g, None)

    if des1 is None or des2 is None:
        raise ValueError("No features detected.")

    matches = matcher.match(des1, des2)

    if len(matches) == 0:
        raise ValueError("No matches found.")

    matches = sorted(matches, key=lambda x: x.distance)
    dxs, dys = [], []

    for m in matches[:10]:
        pt1 = kp1[m.queryIdx].pt
        pt2 = kp2[m.trainIdx].pt
        dxs.append(pt2[0] - pt1[0])
        dys.append(pt2[1] - pt1[1])

    dx = float(np.median(dxs))
    dy = float(np.median(dys))

    match_img = cv2.drawMatches(r, kp1, g, kp2, matches[:10], None, flags=2)
    plt.figure(figsize=(10, 5))
    plt.imshow(match_img, cmap='gray')
    plt.title(f"{method} Matching (dx = {dx:.2f}, dy = {dy:.2f})")
    plt.axis('off')
    plt.show()

    return round(dx, 3), round(dy, 3)

def detect_PC(r, g):
    # Convert to float32 for phaseCorrelate
    r = cv2.GaussianBlur(r, (5, 5), 1)
    g = cv2.GaussianBlur(g, (5, 5), 1)

    r_f = r.astype(np.float32)
    g_f = g.astype(np.float32)
    
    # Use OpenCV's phaseCorrelate which returns shift in (dx, dy) format
    shift, response = cv2.phaseCorrelate(r_f, g_f)
    dx, dy = shift  # dx: horizontal shift, dy: vertical shift

    # Plot arrow on image r showing detected shift
    plt.figure(figsize=(6,6))
    plt.title(f"Phase Correlation Shift: dx = {dx:.2f}, dy = {dy:.2f}")
    plt.imshow(r, cmap='gray')
    center_x, center_y = r.shape[1]//2, r.shape[0]//2
    plt.arrow(center_x, center_y, dx, dy, color='red', head_width=5)
    plt.axis('off')
    plt.show()

    return round(dx, 3), round(dy, 3)


# ======= Processing =======

def process_image(method, bands_tuple):
    r, g = bands_tuple

    if method == "ORB" or method == "SIFT":
        return detect_FM(r, g, method)
    elif method == "Phase-Correlation":
        return detect_PC(r, g)
    else:
        raise ValueError(f"Unknown Method {method}")

# ======= GUI Callbacks =======

band1=None
band2=None

def select_rgb_image():
    global band1, band2
    filepath = filedialog.askopenfilename(filetypes=[("TIFF files", "*.tif *.tiff"), ("All files", "*.*")])
    if not filepath:
        return
    try:
        band1, band2 = load_rgb_bands(filepath)
        dx, dy = process_image(method_var.get(), (band1, band2))
        result_label.config(text=f"Detected Shift:\ndx = {dx}, dy = {dy}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        result_label.config(text="Detection failed.")

def select_band1_image():
    global band1
    filepath = filedialog.askopenfilename(filetypes=[("TIFF files", "*.tif *.tiff"), ("All files", "*.*")])
    if not filepath:
        return
    try:
        band1 = load_individual_band(filepath)
        result_label.config(text="Band 1 loaded. Please load Band 2.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        result_label.config(text="Failed to load Band 1.")

def select_band2_image():
    global band1, band2
    filepath = filedialog.askopenfilename(filetypes=[("TIFF files", "*.tif *.tiff"), ("All files", "*.*")])
    if not filepath:
        return
    if band1 is None:
        messagebox.showwarning("Warning", "Please load Band 1 first!")
        return
    try:
        band2 = load_individual_band(filepath)
        dx, dy = process_image(method_var.get(), (band1, band2))
        result_label.config(text=f"Detected Shift:\ndx = {dx}, dy = {dy}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        result_label.config(text="Detection failed.")

def on_image_type_change(event):
    selection = image_var.get()
    # Hide all buttons first
    select_rgb_btn.pack_forget()
    select_band1_btn.pack_forget()
    select_band2_btn.pack_forget()
    # Reset result label and loaded bands
    global band1, band2
    band1, band2 = None, None
    result_label.config(text="No image selected yet.")

    if selection == "RGB Image":
        select_rgb_btn.pack(pady=20)
    elif selection == "Individual Bands":
        select_band1_btn.pack(pady=10)
        select_band2_btn.pack(pady=10)

# ======= GUI Setup =======

window = tk.Tk()
window.title("Band-to-Band Misregistration Detection")
window.geometry("480x320")

tk.Label(window, text="Select Misregistration Detection Method:", font=("Helvetica", 13)).pack(pady=10)

method_var = tk.StringVar(value="ORB")
method_menu = ttk.Combobox(window, textvariable=method_var,
                           values=["ORB", "SIFT", "Phase-Correlation"],
                           state="readonly", width=20, font=("Arial", 12))
method_menu.pack(pady=5)

tk.Label(window, text="Select Image Input Type:", font=("Helvetica", 13)).pack(pady=10)

image_var = tk.StringVar(value="RGB Image")
image_menu = ttk.Combobox(window, textvariable=image_var,
                          values=["RGB Image", "Individual Bands"],
                          state="readonly", width=20, font=("Arial", 12))
image_menu.pack(pady=5)
image_menu.bind("<<ComboboxSelected>>", on_image_type_change)

select_rgb_btn = tk.Button(window, text="Select RGB Image", command=select_rgb_image, font=("Arial", 12))
select_band1_btn = tk.Button(window, text="Select Band 1", command=select_band1_image, font=("Arial", 12))
select_band2_btn = tk.Button(window, text="Select Band 2", command=select_band2_image, font=("Arial", 12))

# Initially show RGB selection button only
select_rgb_btn.pack(pady=20)

result_label = tk.Label(window, text="No image selected yet.", font=("Arial", 12))
result_label.pack(pady=10)

window.mainloop()