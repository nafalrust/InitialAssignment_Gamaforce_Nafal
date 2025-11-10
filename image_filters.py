import cv2
import numpy as np
import matplotlib.pyplot as plt

IMAGE_PATH = "tulip.jpg"

def load_image(path):
    print(f"Memuat gambar {path}...")
    try:
        img = cv2.imread(path)
        if img is not None:
            print("Gambar berhasil dimuat")
        else:
            print("Error: Gambar tidak ditemukan")
        return img
    except Exception as e:
        print(f"Error memuat gambar: {e}")
        return None

def apply_canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)
    edges = cv2.Canny(blurred, 100, 200)
    return edges

def apply_sobel(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = np.sqrt(sobelx**2 + sobely**2)
    magnitude = np.uint8(magnitude / magnitude.max() * 255)
    return magnitude

def apply_bilateral(image):
    bilateral = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)
    return bilateral

def main():
    print("="*70)
    print("PROGRAM IMAGE FILTERING")
    print("="*70)
    
    image = load_image(IMAGE_PATH)
    
    if image is None:
        print("Gagal memuat gambar!")
        return
    
    print(f"Ukuran gambar: {image.shape[1]}x{image.shape[0]}")
    print("Menerapkan filter...")
    
    canny_result = apply_canny(image)
    sobel_result = apply_sobel(image)
    bilateral_result = apply_bilateral(image)
    
    print("Filter berhasil diterapkan!")
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    bilateral_rgb = cv2.cvtColor(bilateral_result, cv2.COLOR_BGR2RGB)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Image Filtering Results', fontsize=16, fontweight='bold')
    
    axes[0, 0].imshow(image_rgb)
    axes[0, 0].set_title('Original Image')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(canny_result, cmap='gray')
    axes[0, 1].set_title('Canny Edge Detection')
    axes[0, 1].axis('off')
    
    axes[1, 0].imshow(sobel_result, cmap='gray')
    axes[1, 0].set_title('Sobel Gradient')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(bilateral_rgb)
    axes[1, 1].set_title('Bilateral Filter')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    print("\nProgram selesai.")

if __name__ == "__main__":
    main()
