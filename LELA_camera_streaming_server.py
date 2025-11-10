"""
PROGRAM STREAMING KAMERA - SERVER
Menggunakan Flask dan OpenCV untuk streaming video kamera laptop

Dibuat untuk: LELA (Low Latency Efficient Local Area streaming)
Tanggal: 8 November 2025

FITUR:
- Streaming video real-time dengan latensi rendah
- Kompresi JPEG untuk efisiensi bandwidth
- Resolusi dapat disesuaikan (default 640x480 untuk performa optimal)
- Dapat diakses dari perangkat lain di jaringan yang sama
- Web interface sederhana untuk viewing
"""

from flask import Flask, render_template_string, Response
import cv2
import threading
import socket

app = Flask(__name__)

# Konfigurasi
CAMERA_INDEX = 0  # 0 untuk kamera default, 1 untuk kamera eksternal
FRAME_WIDTH = 640  # Resolusi lebih rendah = lebih efisien
FRAME_HEIGHT = 480
JPEG_QUALITY = 70  # 0-100, lebih rendah = file lebih kecil, kualitas lebih rendah
FPS = 30  # Frame per second

# Global variable untuk kamera
camera = None
camera_lock = threading.Lock()


def get_camera():
    """Inisialisasi dan mengembalikan objek kamera"""
    global camera
    if camera is None:
        with camera_lock:
            if camera is None:
                camera = cv2.VideoCapture(CAMERA_INDEX)
                camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
                camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
                camera.set(cv2.CAP_PROP_FPS, FPS)
                # Buffer kecil untuk mengurangi latensi
                camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return camera


def generate_frames():
    """
    Generator function untuk menghasilkan frame video
    Menggunakan motion JPEG untuk streaming
    """
    cam = get_camera()
    
    while True:
        success, frame = cam.read()
        if not success:
            break
        
        # Encode frame ke JPEG untuk kompresi
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY]
        ret, buffer = cv2.imencode('.jpg', frame, encode_param)
        
        if not ret:
            continue
        
        frame_bytes = buffer.tobytes()
        
        # Yield frame dalam format multipart
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Route untuk streaming video"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Halaman utama dengan player video"""
    
    # Dapatkan IP address lokal
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    # HTML template sederhana
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LELA Camera</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                background: #000;
                overflow: hidden;
            }
            #video {
                width: 100%;
                height: 100vh;
                object-fit: contain;
            }
            #info {
                position: fixed;
                top: 10px;
                right: 10px;
                background: rgba(0,0,0,0.7);
                color: #fff;
                padding: 10px;
                font-family: monospace;
                font-size: 14px;
                border-radius: 5px;
            }
            #info div {
                margin: 3px 0;
            }
        </style>
    </head>
    <body>
        <img id="video" src="{{ url_for('video_feed') }}" alt="Stream">
        <div id="info">
            <div>FPS: <span id="fps">--</span></div>
            <div>Latency: <span id="latency">--</span> ms</div>
            <div>{{ width }}x{{ height }}</div>
        </div>
        
        <script>
            let lastUpdate = Date.now();
            let frameCount = 0;
            
            const video = document.getElementById('video');
            const fpsDisplay = document.getElementById('fps');
            const latencyDisplay = document.getElementById('latency');
            
            // Hitung FPS
            setInterval(() => {
                const now = Date.now();
                const elapsed = (now - lastUpdate) / 1000;
                const fps = Math.round(frameCount / elapsed);
                fpsDisplay.textContent = fps;
                frameCount = 0;
                lastUpdate = now;
            }, 1000);
            
            // Hitung latency (ping ke server)
            setInterval(() => {
                const start = Date.now();
                fetch('/status')
                    .then(() => {
                        const latency = Date.now() - start;
                        latencyDisplay.textContent = latency;
                    })
                    .catch(() => {
                        latencyDisplay.textContent = 'Error';
                    });
            }, 2000);
            
            // Count frames
            video.onload = () => frameCount++;
        </script>
    </body>
    </html>
    """
    
    return render_template_string(
        html_template,
        local_ip=local_ip,
        width=FRAME_WIDTH,
        height=FRAME_HEIGHT,
        quality=JPEG_QUALITY,
        fps=FPS
    )


@app.route('/status')
def status():
    """Route untuk mengecek status server"""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    return {
        'status': 'online',
        'server_ip': local_ip,
        'port': 5000,
        'resolution': f'{FRAME_WIDTH}x{FRAME_HEIGHT}',
        'jpeg_quality': JPEG_QUALITY,
        'fps': FPS
    }


def get_local_ip():
    """Mendapatkan IP address lokal"""
    try:
        # Membuat socket dummy untuk mendapatkan IP lokal
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return socket.gethostbyname(socket.gethostname())


if __name__ == '__main__':
    print("="*70)
    print("LELA CAMERA STREAMING SERVER")
    print("="*70)
    
    # Test kamera
    test_cam = get_camera()
    if not test_cam.isOpened():
        print("\nERROR: Tidak dapat mengakses kamera!")
        print("Pastikan kamera terhubung dan tidak digunakan aplikasi lain.")
        exit(1)
    
    print("Kamera berhasil diinisialisasi")
    print(f"Resolusi: {FRAME_WIDTH}x{FRAME_HEIGHT}, Kualitas: {JPEG_QUALITY}%, FPS: {FPS}")
    
    local_ip = get_local_ip()
    
    print("\n" + "-"*70)
    print("AKSES DARI PERANGKAT LAIN:")
    print(f"  http://{local_ip}:5000")
    print("\nTIPS:")
    print("  - Pastikan firewall mengizinkan port 5000")
    print("  - Gunakan jaringan WiFi yang sama")
    print("  - Tekan Ctrl+C untuk menghentikan server")
    print("-"*70)
    print("\nServer starting...\n")
    
    # Jalankan server Flask
    try:
        from waitress import serve
        print("Menggunakan Waitress WSGI server\n")
        serve(app, host='0.0.0.0', port=5000, threads=4)
    except ImportError:
        print("Menggunakan Flask development server\n")
        import os
        hostname_backup = socket.gethostname()
        try:
            socket.gethostname = lambda: 'localhost'
            app.run(host='0.0.0.0', port=5000, debug=False, threaded=True, use_reloader=False)
        finally:
            socket.gethostname = lambda: hostname_backup
