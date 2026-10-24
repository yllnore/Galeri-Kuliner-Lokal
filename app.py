import os
import io
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf

app = Flask(__name__)
# Izinkan CORS dari frontend React (localhost:5173 / all origins)
CORS(app)

# Path model CNN yang sudah dilatih
MODEL_PATH = os.path.join("04_Portofolio_Al_dan_Blockchain", "models", "kuliner_cnn_model.h5")

# Label kelas sesuai urutan alfabet folder dataset (pempek, rendang, soto)
CLASS_LABELS = ["Pempek", "Rendang", "Soto"]

# Trait / karakteristik untuk masing-masing kuliner
TRAITS_MAP = {
    "Rendang": ["Karamelisasi Santan", "Serat Daging Sapi", "Rempah Rendang Padang"],
    "Pempek": ["Tekstur Sagu & Tenggiri", "Saus Cuko", "Warna Keemasan"],
    "Soto": ["Aroma Kunyit & Kaldu", "Potongan Daging", "Daun Bawang & Emping"]
}

print(f">>> Memuat model CNN dari {MODEL_PATH} ...")
model = tf.keras.models.load_model(MODEL_PATH)
print(">>> Model CNN berhasil dimuat!")

def preprocess_image(image_bytes):
    """
    Mengubah bytes gambar menjadi array tensor (1, 224, 224, 3) 
    dan dinormalisasi (1./255) sesuai dengan pelatihan model CNN.
    """
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))
    img_array = np.array(image, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'Tidak ada file gambar yang dikirim'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Nama file kosong'}), 400

    try:
        # Baca gambar dari request
        img_bytes = file.read()
        processed_img = preprocess_image(img_bytes)

        # Prediksi menggunakan model CNN
        predictions = model.predict(processed_img)
        predicted_idx = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][predicted_idx])
        predicted_category = CLASS_LABELS[predicted_idx]
        traits = TRAITS_MAP.get(predicted_category, ["Kuliner Lokal", "Autentik Nusantara"])

        print(f"[PREDIKSI] Kategori: {predicted_category} | Confidence: {confidence:.4f}")

        return jsonify({
            "category": predicted_category,
            "confidence": confidence,
            "traits": traits
        })
    except Exception as e:
        print(f"[ERROR] Prediksi gagal: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "Backend Galeri Kuliner Nusantara aktif"}), 200

if __name__ == '__main__':
    print(">>> Menjalankan server backend AI di http://localhost:5000 ...")
    app.run(host='0.0.0.0', port=5000, debug=False)
