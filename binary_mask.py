import cv2
import numpy as np
import matplotlib.pyplot as plt

IMAGE_PATH = "bQ1E5K67D6wb.png"

def create_binary_mask(image, threshold_value=127):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)
    return binary

def main():
    image = cv2.imread(IMAGE_PATH)
    if image is None:
        print("Error: Gambar tidak ditemukan")
        return
    
    binary_mask = create_binary_mask(image, threshold_value=60)
    
    print("Binary mask berhasil dibuat!")
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle('Binary Mask Result', fontsize=16, fontweight='bold')
    
    axes[0].imshow(image_rgb)
    axes[0].set_title('Gambar Asli')
    axes[0].axis('off')
    
    axes[1].imshow(binary_mask, cmap='gray')
    axes[1].set_title('Output')
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
