import os
import pickle
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
import tensorflow as tf

# Load tokenizer and model
tokenizer = pickle.load(open("tokenizer.pkl", "rb"))
model = load_model("model_captioning.h5")
max_length = 10  # Make sure this matches training

# Load CNN encoder model (InceptionV3 for feature extraction)
def get_encoder():
    base_model = InceptionV3(weights='imagenet')
    model = Model(base_model.input, base_model.layers[-2].output)
    return model

encoder = get_encoder()

# Extract features from new image
def extract_features(img_path):
    img = image.load_img(img_path, target_size=(299, 299))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    feature = encoder.predict(x, verbose=0)
    return feature

# Generate caption from image feature
def generate_caption(model, tokenizer, photo, max_length=10):
    in_text = 'startseq'
    for _ in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([photo, sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = word_for_id(yhat, tokenizer)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'endseq':
            break
    final = in_text.replace('startseq', '').replace('endseq', '').strip()
    return final

# Helper to map word index to actual word
def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

# ========== MAIN ==========
if __name__ == "__main__":
    import sys
    test_img = input("📸 Enter path to test image (e.g., dataimg/images/Dog.jpg): ").strip()

    if not os.path.exists(test_img):
        print("❌ Image not found. Check path.")
        exit()

    print("🔍 Extracting features...")
    photo = extract_features(test_img)

    print("📝 Generating caption...")
    caption = generate_caption(model, tokenizer, photo, max_length)
    print(f"🖼️ Caption: {caption}")
