import os
import hashlib

def cari_gambar_duplikat(folder_target):
    file_hashes = {}
    jumlah_duplikat = 0

    print(f"🔍 Sedang memindai folder: {folder_target}...\n")

    for root, dirs, files in os.walk(folder_target):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()

                    if file_hash in file_hashes:
                        jumlah_duplikat += 1
                        print(f"[DUPLIKAT KETEMU!] ke-{jumlah_duplikat}")
                        print(f" -> Asli : {file_hashes[file_hash]}")
                        print(f" -> Kembar: {file_path}\n")
                    else:
                        file_hashes[file_hash] = file_path
                except Exception as e:
                    print(f"Gagal membaca {file_path}: {e}")

    if jumlah_duplikat == 0:
        print("✅ Aman! Tidak ada gambar yang duplikat di dalam folder ini.")
    else:
        print(f"⚠️ Selesai! Ditemukan total {jumlah_duplikat} file gambar yang kembar.")

target_folder = "../../02_Data_dan_Aset/dataset_kuliner"
cari_gambar_duplikat(target_folder)