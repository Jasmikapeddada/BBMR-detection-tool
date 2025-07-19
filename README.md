# 🌍 Satellite Misregistration Detector

**Python-Based Computer Vision Tool | Developed during ISRO–NRSC Research Internship**

A GUI-based application to detect **band-to-band misregistration** in multi-spectral satellite images using advanced computer vision techniques. Built using Python and designed to support ISRO researchers in improving remote sensing data accuracy from ResourceSat-2 and 2A satellites.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [Screenshots](#-screenshots)
- [How It Works](#-how-it-works)
- [Challenges Faced](#-challenges-faced)
- [Key Achievements](#-key-achievements)
- [Learnings](#-learnings)

---

## 🔍 Overview

This project was developed during a 6-week research internship at **NRSC–ISRO, Hyderabad**. It addresses the issue of **band-to-band misregistration**—a common spatial misalignment between spectral bands in satellite imagery that affects analysis accuracy.

The tool allows users to:
- Upload satellite band pairs
- Choose a detection algorithm (ORB, SIFT, Phase Correlation)
- Visualize misregistration results
- Compare algorithm performance

---

## 🧪 Features

- ✅ Detects spatial misalignment between bands
- 🧠 Uses three algorithms: **SIFT**, **ORB**, **Phase Correlation**
- 🖥️ GUI built with **Tkinter** for easy interaction
- 📊 Visualizes output with overlays and accuracy metrics
- 📁 Works with large satellite datasets (e.g., ResourceSat-2, 2A)

---

## 🛠️ Technologies Used

- **Python**
- **OpenCV** – Image processing & feature detection
- **NumPy** – Numerical computations
- **Matplotlib** – Visualization
- **Tkinter** – GUI framework
- **SIFT**, **ORB**, **Phase Correlation** – Misregistration detection methods

---

## 🖼 Screenshots

> **Main GUI Interface**  
> _User-friendly interface to select bands and visualize results_

> **Detection Results**  
> _Shows spatial shifts between bands using each algorithm_

> **Performance Comparison**  
> _Compare methods based on result accuracy and timing_

(Add image links or files here using markdown `![Alt Text](image-url)`)

---

## ⚙️ How It Works

1. User selects two bands from a satellite image.
2. Chooses an algorithm to run.
3. The tool:
   - Processes images using selected method
   - Calculates offset/misalignment
   - Displays result with matching visuals
4. Output includes:
   - Visual overlays
   - Offset values
   - Statistical comparison

---

## ❗ Challenges Faced

- Parsing and handling multi-spectral satellite imagery
- Balancing algorithm speed vs accuracy
- GUI design for non-technical users
- Validating results against misregistered datasets

---

## 🏆 Key Achievements

- Built a production-ready desktop tool for BBMR detection
- Implemented 3 algorithms and evaluated on 50+ band pairs
- Used in NRSC operational workflows
- Delivered validated results with statistical confidence

---

## 📚 Learnings

- Image registration using SIFT, ORB, and Phase Correlation
- GUI development with Python’s Tkinter
- Real-world satellite image processing
- Applying statistical analysis for validation
- Collaborative research & reporting in a space organization
