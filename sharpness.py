"""
Image Sharpness Analyzer
------------------------
Measures how sharp (in focus) an image is, using the variance of its gradient:
a sharp image has strong edges -> high gradient variance, while a blurry image
has soft edges -> low variance. This is the principle behind contrast-detection
autofocus.

Usage:
    python sharpness.py path/to/image.jpg      # score a single image
    python sharpness.py images/                # rank every image in a folder
"""

import sys
import os
import matplotlib.pyplot as plt
import numpy as np


def to_grayscale(image):
    """Convert an RGB image to grayscale using the standard luminance weights."""
    gray = []
    for row in image:
        gray_row = []
        for pixel in row:
            r, g, b = pixel[0], pixel[1], pixel[2]
            gray_row.append(0.299 * r + 0.587 * g + 0.114 * b)
        gray.append(gray_row)
    return gray


def sharpness_score(image_path):
    """Return a sharpness score for the image (higher = sharper)."""
    image = plt.imread(image_path)
    gray = to_grayscale(image)

    # Finite-difference gradients: difference between neighbouring pixels
    # dx = horizontal gradient, dy = vertical gradient
    dx = [[gray[l][c + 1] - gray[l][c] for c in range(len(gray[0]) - 1)]
          for l in range(len(gray))]
    dy = [[gray[l + 1][c] - gray[l][c] for c in range(len(gray[0]))]
          for l in range(len(gray) - 1)]

    # Gradient magnitude at each pixel: sqrt(dx^2 + dy^2)
    gradient_norm = []
    for l in range(len(dy)):
        norm_row = []
        for c in range(len(dx[0])):
            norm_row.append((dx[l][c] ** 2 + dy[l][c] ** 2) ** 0.5)
        gradient_norm.append(norm_row)

    # The variance of the gradient is our sharpness metric
    return np.var(gradient_norm)


def main():
    if len(sys.argv) < 2:
        print("Usage: python sharpness.py <image_or_folder>")
        return

    path = sys.argv[1]

    # Single image
    if os.path.isfile(path):
        print(f"{path}: {sharpness_score(path):.4f}")
        return

    # Folder: score every image and rank from sharpest to blurriest
    extensions = (".jpg", ".jpeg", ".png", ".bmp")
    scores = []
    for name in os.listdir(path):
        if name.lower().endswith(extensions):
            scores.append((name, sharpness_score(os.path.join(path, name))))

    scores.sort(key=lambda item: item[1], reverse=True)
    print("Ranked from sharpest to blurriest:")
    for name, score in scores:
        print(f"  {score:10.4f}   {name}")


if __name__ == "__main__":
    main()
