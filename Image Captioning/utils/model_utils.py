# utils/model_utils.py

import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# 1. Extract visual features from image using ResNet50
def extract_features(image_path):
    model = ResNet50(weights='imagenet')
    model = Model(inputs=model.inputs, outputs=model.layers[-2].output)

    img = load_img(image_path, target_size=(224, 224))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)

    feature = model.predict(img, verbose=0)
    return feature

# 2. Map word index to actual word
def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

# 3. Greedy search caption generation
def generate_caption(model, tokenizer, photo, max_length):
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
    return in_text.replace('startseq', '').replace('endseq', '').strip()

# 4. Beam search caption generation
def generate_caption_beam_search(model, tokenizer, photo, max_length, beam_index=3):
    start = [tokenizer.word_index['startseq']]
    sequences = [[start, 0.0]]  # [sequence, score]

    while len(sequences[0][0]) < max_length:
        temp = []
        for seq, score in sequences:
            padded = pad_sequences([seq], maxlen=max_length)
            preds = model.predict([photo, padded], verbose=0)[0]
            top_preds = np.argsort(preds)[-beam_index:]

            for word in top_preds:
                new_seq = seq + [word]
                new_score = score + np.log(preds[word] + 1e-10)  # prevent log(0)
                temp.append([new_seq, new_score])

        sequences = sorted(temp, reverse=True, key=lambda x: x[1])
        sequences = sequences[:beam_index]

    final_seq = sequences[0][0]
    final_words = [word_for_id(idx, tokenizer) for idx in final_seq]
    final_caption = [w for w in final_words if w not in ['startseq', 'endseq', None]]
    return ' '.join(final_caption)
