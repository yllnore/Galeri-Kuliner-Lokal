import os
import shutil

sumber_mentah = "../../02_Data_dan_Aset/mentahan_kotor"
target_dir = "../../02_Data_dan_Aset/dataset_kuliner"
kategori_list = ['pempek', 'rendang', 'soto']

def rapikan_dan_rename_dataset():
    if not os.path.exists(sumber_mentah):
        print(f"❌ Folder mentahan '{sumber_mentah}' tidak ditemukan.")
        return

    for kategori in kategori_list:
        folder_kategori_sumber = os.path.join(sumber_mentah, kategori)

        if not os.path.exists(folder_kategori_sumber):
            continue

        files = [f for f in os.listdir(folder_kategori_sumber) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        print(f"\n📂 Memproses kategori: {kategori} (Total ditemukan: {len(files)} file)")

        train_path = os.path.join(target_dir, 'train', kategori)
        val_path = os.path.join(target_dir, 'val', kategori)
        test_path = os.path.join(target_dir, 'test', kategori)

        os.makedirs(train_path, exist_ok=True)
        os.makedirs(val_path, exist_ok=True)
        os.makedirs(test_path, exist_ok=True)

        for i, file_lama in enumerate(files):
            file_asli_path = os.path.join(folder_kategori_sumber, file_lama)
            ekstensi = os.path.splitext(file_lama)[1].lower()

            # Pembagian: 50 Train, 10 Val, 10 Test
            if i < 50:
                nama_baru = f"{kategori}_train_{i+1:02d}{ekstensi}"
                tujuan = os.path.join(train_path, nama_baru)
            elif i < 60:
                nama_baru = f"{kategori}_val_{i-49:02d}{ekstensi}"
                tujuan = os.path.join(val_path, nama_baru)
            elif i < 70:
                nama_baru = f"{kategori}_test_{i-59:02d}{ekstensi}"
                tujuan = os.path.join(test_path, nama_baru)
            else:
                break

            shutil.copy(file_asli_path, tujuan)
            print(f" -> {file_lama} ➡️ {nama_baru}")

    print("\n✨ Selesai! File berhasil direname dan dipisah ke folder Train, Val, dan Test.")

rapikan_dan_rename_dataset()