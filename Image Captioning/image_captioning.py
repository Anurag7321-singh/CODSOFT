# image_captioning.py

import os
import argparse
from utils.model_utils import extract_features, generate_caption_beam_search
from tensorflow.keras.models import load_model
import pickle

def main(image_path):
    # Load tokenizer and model
    with open("tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)
    model = load_model("models/encoder_decoder_model.h5")
    max_length = 34

    # Extract features and generate caption
    photo = extract_features(image_path)
    caption = generate_caption_beam_search(model, tokenizer, photo, max_length, beam_index=5)

    print("\n🖼️ Image:", image_path)
    print("📝 Caption:", caption)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="Path to the input image")
    args = parser.parse_args()
    main(args.image)
