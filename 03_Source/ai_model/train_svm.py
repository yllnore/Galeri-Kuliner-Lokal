import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

# 1. Setup Path ke Folder Fisik Train dan Test yang Baru
train_path = "../../02_Data_dan_Aset/dataset_kuliner/train"
test_path = "../../02_Data_dan_Aset/dataset_kuliner/test"
output_folder = "../../05_Test_dan_Deployment"
os.makedirs(output_folder, exist_ok=True)

# 2. Fungsi untuk Ekstraksi Fitur Warna (Color Histogram)
def extract_color_histogram(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None
    # Ubah ke format RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Buat histogram 3D untuk warna RGB
    hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    return hist.flatten()

classes = ['pempek', 'rendang', 'soto']

# 3. Membaca Data Train
print(">>> Membaca data TRAINING dan mengekstrak fitur warna...")
X_train = []
y_train = []
for class_idx, class_name in enumerate(classes):
    class_dir = os.path.join(train_path, class_name)
    if not os.path.exists(class_dir):
        continue
    for img_name in os.listdir(class_dir):
        img_path = os.path.join(class_dir, img_name)
        features = extract_color_histogram(img_path)
        if features is not None:
            X_train.append(features)
            y_train.append(class_idx)

X_train = np.array(X_train)
y_train = np.array(y_train)

# 4. Membaca Data Test
print(">>> Membaca data TESTING dan mengekstrak fitur warna...")
X_test = []
y_test = []
for class_idx, class_name in enumerate(classes):
    class_dir = os.path.join(test_path, class_name)
    if not os.path.exists(class_dir):
        continue
    for img_name in os.listdir(class_dir):
        img_path = os.path.join(class_dir, img_name)
        features = extract_color_histogram(img_path)
        if features is not None:
            X_test.append(features)
            y_test.append(class_idx)

X_test = np.array(X_test)
y_test = np.array(y_test)

# 5. Latih Model SVM
print("\n>>> Melatih model Support Vector Machine (SVM)...")
svm_model = SVC(kernel='linear', random_state=42)
svm_model.fit(X_train, y_train)

# 6. Evaluasi Model SVM menggunakan Data Test Asli
print(">>> Mengevaluasi model SVM pada data test...")
y_pred = svm_model.predict(X_test)

print("\n" + "="*50)
print("             CLASSIFICATION REPORT (SVM - WARNA)")
print("="*50)
report = classification_report(y_test, y_pred, target_names=classes)
print(report)

# Simpan text report khusus SVM
with open(f"{output_folder}/svm_evaluation_metrics.txt", "w") as f:
    f.write("CLASSIFICATION REPORT (SVM)\n")
    f.write("===========================\n")
    f.write(report)

# 7. Buat dan Simpan Confusion Matrix SVM
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges', xticklabels=classes, yticklabels=classes)
plt.title('Confusion Matrix - Model SVM (Pembanding)')
plt.ylabel('Label Asli (True)')
plt.xlabel('Label Prediksi (Predicted)')

cm_path = f"{output_folder}/svm_confusion_matrix.png"
plt.savefig(cm_path)
print(f"\n>>> Sukses! Gambar Confusion Matrix SVM disimpan di: {cm_path}")
print(f">>> Kodingan AI untuk proyek ini RESMI SELESAI 100%!")