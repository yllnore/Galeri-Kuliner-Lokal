import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import json
import os

# 1. Setup Path
dataset_path = "../../02_Data_dan_Aset/dataset_kuliner"
model_output_dir = "../../04_Portofolio_Al_dan_Blockchain/models"
os.makedirs(model_output_dir, exist_ok=True)

print(">>> Mempersiapkan Data Augmentation...")
# 2. Data Augmentation (Jurus rahasia untuk dataset kecil!)
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,      # Gambar diputar acak
    width_shift_range=0.2,  # Digeser kiri-kanan
    height_shift_range=0.2, # Digeser atas-bawah
    zoom_range=0.2,         # Di-zoom acak
    horizontal_flip=True,   # Dibalik seperti cermin
    fill_mode='nearest',
    validation_split=0.2
)

# Batch size dikecilkan jadi 4 karena data kita sedikit
train_generator = datagen.flow_from_directory(
    dataset_path,
    target_size=(224, 224),
    batch_size=4,
    class_mode='categorical',
    subset='training'
)

val_generator = datagen.flow_from_directory(
    dataset_path,
    target_size=(224, 224),
    batch_size=4,
    class_mode='categorical',
    subset='validation'
)

# 3. Build Model MobileNetV2
print(">>> Membangun Arsitektur Model...")
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Kunci bobot asli MobileNetV2

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.5)(x)  # Tambah dropout agar tidak overfit
predictions = Dense(3, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# Gunakan learning rate yang sedikit lebih kecil agar belajarnya teliti
model.compile(optimizer=Adam(learning_rate=0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 4. Mulai Training dengan Epoch lebih banyak (25 Epochs)
print(">>> Memulai Proses Training (25 Epochs)...")
model.fit(
    train_generator,
    epochs=25,
    validation_data=val_generator
)

# 5. Simpan Model
model_path = os.path.join(model_output_dir, "kuliner_cnn_model.h5")
model.save(model_path)
print(f"\n>>> Sukses! Model tersimpan di {model_output_dir}/")

# 6. Buat Metadata JSON untuk Tim Blockchain
metadata = {
    "name": "Kuliner Lokal AI Model",
    "version": "1.0",
    "classes": list(train_generator.class_indices.keys()),
    "base_model": "MobileNetV2"
}
with open(os.path.join(model_output_dir, "sample_metadata.json"), "w") as f:
    json.dump(metadata, f, indent=4)
print(">>> Berkas contoh metadata JSON IPFS berhasil dibuat!")