import math

def hitung_jarak_penjatuhan(kecepatan_pesawat, ketinggian_pesawat, posisi_pesawat_x, posisi_target_x, g=9.8):
    """
    Menghitung jarak horizontal yang diperlukan untuk menjatuhkan paket
    agar jatuh tepat di target menggunakan prinsip gerak parabola.
    
    Parameters:
    -----------
    kecepatan_pesawat : float
        Kecepatan horizontal pesawat (m/s)
    ketinggian_pesawat : float
        Ketinggian pesawat dari tanah (m)
    posisi_pesawat_x : float
        Posisi horizontal pesawat saat ini (m)
    posisi_target_x : float
        Posisi horizontal target di tanah (m)
    g : float
        Percepatan gravitasi (m/s²), default 9.8
    
    Returns:
    --------
    tuple : (jarak_drop, waktu_jatuh, jarak_horizontal_paket, status)
        - jarak_drop: jarak horizontal dari posisi saat ini ke titik drop (m)
        - waktu_jatuh: waktu yang diperlukan paket untuk jatuh (s)
        - jarak_horizontal_paket: jarak horizontal yang ditempuh paket (m)
        - status: status apakah paket harus dijatuhkan atau tidak
    """
    
    # PERHITUNGAN FISIKA:
    # 1. Gerak Vertikal (Jatuh Bebas): h = 1/2 * g * t²
    #    Dari rumus ini: t = sqrt(2h/g)
    waktu_jatuh = math.sqrt(2 * ketinggian_pesawat / g)
    
    # 2. Gerak Horizontal (GLB - Gerak Lurus Beraturan): x = v * t
    #    Kecepatan horizontal tetap konstan (tidak ada percepatan horizontal)
    jarak_horizontal_paket = kecepatan_pesawat * waktu_jatuh
    
    # 3. Hitung jarak dari posisi pesawat saat ini ke target
    jarak_ke_target = posisi_target_x - posisi_pesawat_x
    
    # 4. Hitung jarak yang harus ditempuh pesawat sebelum menjatuhkan paket
    #    Paket harus dijatuhkan SEBELUM target sejauh jarak_horizontal_paket
    jarak_drop = jarak_ke_target - jarak_horizontal_paket
    
    # 5. Tentukan status berdasarkan jarak drop
    if jarak_drop <= 0:
        status = "TERLAMBAT! Pesawat sudah melewati titik drop"
    elif jarak_drop < kecepatan_pesawat:  # Dalam 1 detik akan sampai
        status = "JATUHKAN SEKARANG!"
    else:
        status = "Belum waktunya, terus terbang"
    
    return jarak_drop, waktu_jatuh, jarak_horizontal_paket, status


def tampilkan_visualisasi(posisi_pesawat_x, titik_drop, posisi_target_x):
    """
    Menampilkan visualisasi ASCII sederhana dari lintasan paket
    """
    print("\n" + "="*70)
    print("VISUALISASI LINTASAN PAKET")
    print("="*70)
    print()
    print("         Pesawat → → →")
    print("            |")
    print("            |    ↘")
    print("            |       ↘")
    print("            |          ↘ (Paket)")
    print("            |             ↘")
    print("            |                ↘")
    print("  __________|___________________↓_____________")
    print(" |          |                   |            |")
    print(" |      Posisi                Titik        Target")
    print(" |      Saat Ini              Drop")
    print()
    print(f"  Posisi Pesawat : {posisi_pesawat_x:.2f} m")
    print(f"  Titik Drop     : {titik_drop:.2f} m")
    print(f"  Posisi Target  : {posisi_target_x:.2f} m")
    print("="*70)


def main():
    print("="*70)
    print(" SISTEM PERHITUNGAN PENJATUHAN PAKET DARI PESAWAT ".center(70))
    print("="*70)
    
    # ========== INPUT DATA ==========
    print("\nINPUT DATA PENERBANGAN")
    print("-"*70)
    
    try:
        kecepatan_pesawat = float(input("Kecepatan pesawat (m/s)         : "))
        ketinggian_pesawat = float(input("Ketinggian pesawat (m)          : "))
        posisi_pesawat_x = float(input("Posisi pesawat saat ini (m)     : "))
        posisi_target_x = float(input("Posisi target (m)               : "))
        
        # Validasi input
        if kecepatan_pesawat <= 0 or ketinggian_pesawat <= 0:
            print("\nERROR: Kecepatan dan ketinggian harus lebih dari 0!")
            return
        
        # ========== PERHITUNGAN ==========
        jarak_drop, waktu_jatuh, jarak_horizontal, status = hitung_jarak_penjatuhan(
            kecepatan_pesawat, 
            ketinggian_pesawat, 
            posisi_pesawat_x, 
            posisi_target_x
        )
        
        # ========== HASIL PERHITUNGAN ==========
        print("\n" + "="*70)
        print(" HASIL PERHITUNGAN ".center(70))
        print("="*70)
        
        print(f"\nDATA PERHITUNGAN:")
        print(f"  Waktu jatuh paket                  : {waktu_jatuh:.3f} detik")
        print(f"  Jarak horizontal paket             : {jarak_horizontal:.2f} meter")
        print(f"  Jarak ke target dari posisi awal  : {abs(posisi_target_x - posisi_pesawat_x):.2f} meter")
        
        print(f"\nINSTRUKSI PENJATUHAN:")
        if jarak_drop > 0:
            titik_drop = posisi_pesawat_x + jarak_drop
            waktu_sampai_drop = jarak_drop / kecepatan_pesawat
            
            print(f"  Jarak yang harus ditempuh         : {jarak_drop:.2f} meter")
            print(f"  Waktu hingga titik drop            : {waktu_sampai_drop:.3f} detik")
            print(f"  Paket harus dijatuhkan di posisi   : {titik_drop:.2f} meter")
        else:
            titik_drop = posisi_target_x - jarak_horizontal
            print(f"  Titik drop seharusnya di           : {titik_drop:.2f} meter")
        
        print(f"\nSTATUS: {status}")
        
        # ========== VISUALISASI ==========
        if jarak_drop > 0:
            tampilkan_visualisasi(posisi_pesawat_x, posisi_pesawat_x + jarak_drop, posisi_target_x)
        
        print("\n" + "="*70)
        
    except ValueError:
        print("\nERROR: Masukkan nilai numerik yang valid!")
    except Exception as e:
        print(f"\nERROR: {e}")


def contoh_kasus():
    """
    Menampilkan beberapa contoh kasus dengan data dummy
    """
    print("\n" + "="*70)
    print(" CONTOH KASUS DENGAN DATA DUMMY ".center(70))
    print("="*70)
    
    # Kasus 1
    print("\nKASUS 1:")
    print("-"*70)
    print("Kecepatan pesawat : 50 m/s")
    print("Ketinggian pesawat: 500 m")
    print("Posisi pesawat    : 0 m")
    print("Posisi target     : 600 m")
    print("-"*70)
    
    jarak_drop, waktu_jatuh, jarak_horizontal, status = hitung_jarak_penjatuhan(
        kecepatan_pesawat=50,
        ketinggian_pesawat=500,
        posisi_pesawat_x=0,
        posisi_target_x=600
    )
    
    print(f"Waktu jatuh                  : {waktu_jatuh:.3f} detik")
    print(f"Jarak horizontal paket       : {jarak_horizontal:.2f} meter")
    print(f"Paket harus dijatuhkan di x  : {jarak_drop:.2f} meter dari posisi awal")
    print(f"Status                       : {status}")
    
    # Kasus 2
    print("\nKASUS 2:")
    print("-"*70)
    print("Kecepatan pesawat : 100 m/s")
    print("Ketinggian pesawat: 1000 m")
    print("Posisi pesawat    : 500 m")
    print("Posisi target     : 2000 m")
    print("-"*70)
    
    jarak_drop, waktu_jatuh, jarak_horizontal, status = hitung_jarak_penjatuhan(
        kecepatan_pesawat=100,
        ketinggian_pesawat=1000,
        posisi_pesawat_x=500,
        posisi_target_x=2000
    )
    
    print(f"Waktu jatuh                  : {waktu_jatuh:.3f} detik")
    print(f"Jarak horizontal paket       : {jarak_horizontal:.2f} meter")
    print(f"Paket harus dijatuhkan di x  : {500 + jarak_drop:.2f} meter")
    print(f"Status                       : {status}")
    
    # Kasus 3
    print("\nKASUS 3:")
    print("-"*70)
    print("Kecepatan pesawat : 80 m/s")
    print("Ketinggian pesawat: 200 m")
    print("Posisi pesawat    : 1000 m")
    print("Posisi target     : 800 m (di belakang)")
    print("-"*70)
    
    jarak_drop, waktu_jatuh, jarak_horizontal, status = hitung_jarak_penjatuhan(
        kecepatan_pesawat=80,
        ketinggian_pesawat=200,
        posisi_pesawat_x=1000,
        posisi_target_x=800
    )
    
    print(f"Waktu jatuh                  : {waktu_jatuh:.3f} detik")
    print(f"Jarak horizontal paket       : {jarak_horizontal:.2f} meter")
    print(f"Status                       : {status}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
