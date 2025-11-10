# 📁 OprecGamaforce - Computer Vision Projects

Repository untuk tugas Open Recruitment Gamaforce - Divisi Computer Vision & Image Processing

## 📋 Daftar Program

### 1. **B1.py** - Object Detection dengan Canny & Hough Transform
Deteksi objek menggunakan:
- Per-channel edge detection (R, G, B)
- Canny edge detection dengan preprocessing
- Hough Circle Transform untuk deteksi lingkaran
- Morphological operations untuk noise reduction

**Cara menjalankan:**
```bash
python B1.py
```

---

### 2. **binary_mask.py** - Binary Mask Generator
Membuat binary mask dari gambar menggunakan thresholding.

**Cara menjalankan:**
```bash
python binary_mask.py
```

---

### 3. **Gamaforce_C5.py** - Simulasi Penjatuhan Paket Pesawat
Program perhitungan fisika gerak parabola untuk penjatuhan paket dari pesawat.

**Fitur:**
- Perhitungan jarak dan waktu drop
- Visualisasi ASCII lintasan paket
- Validasi input dan error handling

**Cara menjalankan:**
```bash
python Gamaforce_C5.py
```

---

### 4. **image_filters.py** - Image Filtering Demo
Implementasi berbagai filter OpenCV:
- Canny Edge Detection
- Sobel Gradient
- Bilateral Filter

**Cara menjalankan:**
```bash
python image_filters.py
```

---

### 5. **LELA Camera Streaming** - Real-time Camera Streaming System

#### 🎥 **LELA_camera_streaming_server.py** - Server
Server Flask untuk streaming kamera real-time dengan latensi rendah.

**Fitur:**
- Streaming MJPEG dengan kompresi
- Web interface dengan FPS & latency monitor
- Multi-device support (akses dari HP/laptop lain)
- Low latency optimization

**Cara menjalankan:**
```bash
python LELA_camera_streaming_server.py
```

Akses dari browser: `http://SERVER_IP:5000`

#### 📱 **LELA_camera_streaming_client.py** - Client (Optional)
Client desktop untuk menerima stream (alternatif dari browser).

**Cara menjalankan:**
```bash
python LELA_camera_streaming_client.py
```

---

## 🚀 Setup & Installation

### 1. Clone/Download Repository
```bash
cd d:\Project\OprecGamaforce
```

### 2. Buat Virtual Environment (Recommended)
```powershell
# PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 📦 Dependencies

- **opencv-python** - Computer vision & image processing
- **numpy** - Array processing
- **matplotlib** - Data visualization
- **flask** - Web server (LELA streaming)
- **requests** - HTTP client (LELA client)
- **pillow** - Image processing support

Lihat `requirements.txt` untuk daftar lengkap.

---

## 📸 File Gambar Input

- `sEuidy5yWe9A.png` - Input untuk B1.py
- `bQ1E5K67D6wb.png` - Input untuk binary_mask.py (jika ada)
- `tulip.jpg` - Input untuk image_filters.py (jika ada)

---

## 📊 Output Files

Program akan menghasilkan file output:
- `edges_b.png`, `edges_g.png`, `edges_r.png` - Per-channel edges
- `edges_combined.png` - Combined edge detection
- `result_with_circles.png` - Hasil deteksi shapes & circles
- `screenshot_*.jpg` - Screenshot dari LELA client

---

## 🔧 Troubleshooting

### Error: `cv2.imshow` tidak berfungsi
- Gunakan WSL atau environment dengan GUI support
- Atau comment bagian `cv2.imshow()`, hasil sudah disimpan sebagai file

### LELA Server: Port 5000 sudah digunakan
```python
# Edit di LELA_camera_streaming_server.py
app.run(host='0.0.0.0', port=5001)  # Ganti port
```

### Error: Kamera tidak terdeteksi
```python
# Edit di LELA_camera_streaming_server.py
CAMERA_INDEX = 1  # Coba index kamera lain
```

---

## 👨‍💻 Author

**Nafal** - Open Recruitment Gamaforce 2025

---

## 📝 License

Educational Purpose - Gamaforce DTETI UGM

---

## 🎯 TODO / Future Improvements

- [ ] Tambah deteksi shape lebih kompleks (polygon n-sisi)
- [ ] Implementasi deep learning untuk object detection
- [ ] Real-time object tracking di LELA streaming
- [ ] GUI menggunakan Tkinter/PyQt
- [ ] Export hasil ke video/GIF

---

**Happy Coding! 🚀**
