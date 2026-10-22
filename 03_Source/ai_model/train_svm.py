import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# 1. Setup Path
dataset_path = "../../02_Data_dan_Aset/dataset_kuliner"
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

print(">>> Membaca dataset dan mengekstrak fitur warna...")
X = []
y = []
classes = ['pempek', 'rendang', 'soto']

# 3. Proses semua gambar
for class_idx, class_name in enumerate(classes):
    class_dir = os.path.join(dataset_path, class_name)
    for img_name in os.listdir(class_dir):
        img_path = os.path.join(class_dir, img_name)
        features = extract_color_histogram(img_path)
        if features is not None:
            X.append(features)
            y.append(class_idx)

X = np.array(X)
y = np.array(y)

# 4. Split Data (Sama seperti CNN: 80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Latih Model SVM
print("\n>>> Melatih model Support Vector Machine (SVM)...")
svm_model = SVC(kernel='linear', random_state=42)
svm_model.fit(X_train, y_train)

# 6. Evaluasi Model SVM
print(">>> Mengevaluasi model SVM...")
y_pred = svm_model.predict(X_test)

print("\n" + "="*50)
print("       CLASSIFICATION REPORT (SVM - WARNA)")
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