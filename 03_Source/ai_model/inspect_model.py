import tensorflow as tf

# Load model yang sudah dibuat tadi
model_path = "../../04_Portofolio_Al_dan_Blockchain/models/kuliner_cnn_model.h5"
model = tf.keras.models.load_model(model_path)

print("="*50)
print("  RINGKASAN ARSITEKTUR MODEL AI (MOBILE NET V2)")
print("="*50)

# Menampilkan ringkasan layer dan parameter
model.summary()

print("\n" + "="*50)
print("  DAFTAR LAYER / LAPISAN DI DALAM MODEL:")
print("="*50)
for i, layer in enumerate(model.layers):
    print(f"Layer {i+1}: {layer.name} | Output Shape: {layer.output.shape}")