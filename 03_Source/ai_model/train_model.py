import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ==========================================
# 1. KONFIGURASI DIREKTORI & PARAMETER
# ==========================================
DATA_DIR = "../../02_Data_dan_Aset/dataset_kuliner"
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 10
CLASSES = ["soto", "rendang", "pempek"]

print(">>> Memulai proses penyiapan data...")

# ==========================================
# 2. DATA PREPARATION & SPLITTING (Bebas Bocor)
# ==========================================
train_datagen = ImageDataGenerator(
    rescale=1.0/255.0,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    validation_split=0.2  # 80% train, 20% validation
)

train_generator = train_datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    classes=CLASSES
)

validation_generator = train_datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    classes=CLASSES
)

# ==========================================
# 3. PEMBANGUNAN MODEL UTAMA (Transfer Learning CNN)
# ==========================================
print(">>> Membangun arsitektur model CNN (MobileNetV2)...")
base_model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
base_model.trainable = False  # Freeze base model

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(len(CLASSES), activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# ==========================================
# 4. PELATIHAN MODEL (Training)
# ==========================================
print(">>> Melatih model...")
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator
)

# Simpan model ke folder portofolio
os.makedirs("../../04_Portofolio_Al_dan_Blockchain/models", exist_ok=True)
model.save("../../04_Portofolio_Al_dan_Blockchain/models/kuliner_cnn_model.h5")
print(">>> Sukses! Model tersimpan di folder 04_Portofolio_Al_dan_Blockchain/models/")

# ==========================================
# 5. GENERATOR METADATA IPFS (Interface Agreement)
# ==========================================
def generate_ipfs_metadata(item_name, category, description, creator_address, image_cid):
    """
    Menghasilkan format JSON metadata standar IPFS yang nanti dipanggil
    oleh Smart Contract ERC-721 (tokenURI) dan Frontend kelompok.
    """
    metadata = {
        "name": f"Galeri Kuliner Lokal: {item_name}",
        "description": description,
        "image": f"ipfs://{image_cid}",
        "attributes": [
            {"trait_type": "Kategori Kuliner", "value": category},
            {"trait_type": "Pembuat (Creator)", "value": creator_address},
            {"trait_type": "Status Bantuan AI", "value": "Verified by CNN Model MobileNetV2"},
            {"trait_type": "Versi Metadata", "value": "v1.0"}
        ]
    }
    return metadata

# Contoh Eksekusi Pembuatan Metadata JSON
sample_meta = generate_ipfs_metadata(
    item_name="Soto Banjar Asli",
    category="Soto",
    description="Kuliner khas Kalimantan Selatan dengan kuah rempah pilihan.",
    creator_address="0x1234567890abcdef1234567890abcdef12345678",
    image_cid="bafybeic77g...exampleCID"
)

with open("../../04_Portofolio_Al_dan_Blockchain/models/sample_metadata.json", "w") as f:
    json.dump(sample_meta, f, indent=4)
print(">>> Berkas contoh metadata JSON IPFS berhasil dibuat!")