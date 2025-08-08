import os
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, Dropout, add
from tensorflow.keras.callbacks import ModelCheckpoint
import pickle

# Set path
IMAGE_DIR = 'dataimg/images'
CAPTION_FILE = 'captions.txt'

# Load and preprocess captions
def load_captions(filename):
    captions = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if '\t' in line:
                image_id, caption = line.split('\t')
                image_id = image_id.strip()
                caption = 'startseq ' + caption.strip() + ' endseq'
                if image_id not in captions:
                    captions[image_id] = []
                captions[image_id].append(caption)
    return captions

# Load images
def extract_features(directory):
    model = ResNet50(weights='imagenet')
    model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
    features = {}
    for img_name in os.listdir(directory):
        img_path = os.path.join(directory, img_name)
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        feature = model.predict(img_array, verbose=0)
        features[img_name] = feature
    return features

# Tokenizer
def create_tokenizer(captions):
    from tensorflow.keras.preprocessing.text import Tokenizer
    all_captions = []
    for cap_list in captions.values():
        all_captions.extend(cap_list)
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(all_captions)
    return tokenizer

# Max caption length
def max_length(captions):
    return max(len(caption.split()) for cap_list in captions.values() for caption in cap_list)

# Data generator
def create_sequences(tokenizer, max_len, captions, features, vocab_size):
    X1, X2, y = [], [], []
    for key, caption_list in captions.items():
        if key not in features:
            continue
        for caption in caption_list:
            seq = tokenizer.texts_to_sequences([caption])[0]
            for i in range(1, len(seq)):
                in_seq, out_seq = seq[:i], seq[i]
                in_seq = pad_sequences([in_seq], maxlen=max_len)[0]
                out_seq = to_categorical([out_seq], num_classes=vocab_size)[0]
                X1.append(features[key][0])
                X2.append(in_seq)
                y.append(out_seq)
    return np.array(X1), np.array(X2), np.array(y)

# Define model
def define_model(vocab_size, max_length):
    inputs1 = Input(shape=(2048,))
    fe1 = Dropout(0.5)(inputs1)
    fe2 = Dense(256, activation='relu')(fe1)

    inputs2 = Input(shape=(max_length,))
    se1 = Embedding(vocab_size, 256, mask_zero=True)(inputs2)
    se2 = Dropout(0.5)(se1)
    se3 = LSTM(256)(se2)

    decoder1 = add([fe2, se3])
    decoder2 = Dense(256, activation='relu')(decoder1)
    outputs = Dense(vocab_size, activation='softmax')(decoder2)

    model = Model(inputs=[inputs1, inputs2], outputs=outputs)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model

# Main training function
def main():
    print("🔹 Loading captions...")
    captions = load_captions(CAPTION_FILE)

    print("🔹 Extracting image features...")
    features = extract_features(IMAGE_DIR)

    print("🔹 Creating tokenizer...")
    tokenizer = create_tokenizer(captions)
    vocab_size = len(tokenizer.word_index) + 1
    max_len = max_length(captions)

    print(f"🔹 Vocab size: {vocab_size}, Max caption length: {max_len}")
    print("🔹 Creating training sequences...")
    X1, X2, y = create_sequences(tokenizer, max_len, captions, features, vocab_size)

    print("🔹 Defining model...")
    model = define_model(vocab_size, max_len)
    model.summary()

    print("🚀 Training...")
    model.fit([X1, X2], y, epochs=10, batch_size=32)

    print("💾 Saving model and tokenizer...")
    model.save("model_captioning.keras", save_format="keras")  # ✅ Save in .keras format
    with open("tokenizer.pkl", "wb") as f:
        pickle.dump(tokenizer, f)

    print("✅ Done!")

if __name__ == "__main__":
    main()
