import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# 1. Sesuaikan path folder (berdasarkan struktur komputermu sebelumnya)
model_path = "../../04_Portofolio_Al_dan_Blockchain/models/kuliner_cnn_model.h5"
dataset_path = "../../02_Data_dan_Aset/dataset_kuliner"
output_folder = "../../05_Test_dan_Deployment"

# Buat folder output jika belum ada
os.makedirs(output_folder, exist_ok=True)

# 2. Muat model yang sudah dilatih
print(">>> Memuat model CNN...")
model = tf.keras.models.load_model(model_path)

# 3. Siapkan data generator untuk validasi (shuffle=False wajib untuk evaluasi)
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
val_generator = datagen.flow_from_directory(
    dataset_path,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

# 4. Lakukan Prediksi
print("\n>>> Melakukan prediksi pada data validasi...")
predictions = model.predict(val_generator)
y_pred = np.argmax(predictions, axis=1)
y_true = val_generator.classes
class_labels = list(val_generator.class_indices.keys())

# 5. Tampilkan Classification Report (Precision, Recall, F1-Score)
print("\n" + "="*50)
print("             CLASSIFICATION REPORT")
print("="*50)
report = classification_report(y_true, y_pred, target_names=class_labels)
print(report)

# Simpan report ke file teks
with open(f"{output_folder}/evaluation_metrics.txt", "w") as f:
    f.write("CLASSIFICATION REPORT\n")
    f.write("=====================\n")
    f.write(report)

# 6. Buat dan Simpan Confusion Matrix
print("\n>>> Membuat Confusion Matrix...")
cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_labels, yticklabels=class_labels)
plt.title('Confusion Matrix - Model CNN Kuliner Lokal')
plt.ylabel('Label Asli (True)')
plt.xlabel('Label Prediksi (Predicted)')

# Simpan gambar
cm_path = f"{output_folder}/confusion_matrix.png"
plt.savefig(cm_path)
print(f">>> Sukses! Gambar Confusion Matrix disimpan di: {cm_path}")
print(f">>> Sukses! Teks metrik disimpan di: {output_folder}/evaluation_metrics.txt")