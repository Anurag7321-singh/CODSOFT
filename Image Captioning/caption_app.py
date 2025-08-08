import streamlit as st
import numpy as np
import os
import pickle
from PIL import Image
from keras.models import load_model
from keras.applications.inception_v3 import InceptionV3, preprocess_input
from keras.preprocessing.image import load_img, img_to_array
from keras.preprocessing.sequence import pad_sequences

# Load tokenizer
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Load model
try:
    model = load_model("model_captioning.keras")
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

# Constants
MAX_LENGTH = 34  # or the max_length you used during training

# Load InceptionV3 model for feature extraction
inception_model = InceptionV3(weights="imagenet")
inception_model = Model(inception_model.input, inception_model.layers[-2].output)

# Set Streamlit page config
st.set_page_config(page_title="Image Captioning App", layout="wide")

# Background styling with faceimg.jpeg
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("faceimg.jpeg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("🖼️ Image Captioning Dashboard")

# Image feature extractor
def extract_features(image_path):
    img = load_img(image_path, target_size=(299, 299))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    features = inception_model.predict(img)
    return features

# Caption generation
def generate_caption(model, tokenizer, photo, max_length=MAX_LENGTH):
    in_text = "startseq"
    for _ in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([photo, sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = tokenizer.index_word.get(yhat)
        if word is None:
            break
        in_text += " " + word
        if word == "endseq":
            break
    return in_text.replace("startseq", "").replace("endseq", "").strip()

# Upload section
uploaded_image = st.file_uploader("Upload an image to caption", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Save temp image
    image_path = "temp_uploaded_image.jpg"
    image.save(image_path)

    # Extract features and caption
    with st.spinner("Generating caption..."):
        features = extract_features(image_path)
        caption = generate_caption(model, tokenizer, features)

    st.success("✅ Caption Generated!")
    st.markdown(f"**📝 Caption:** {caption}")

# Gallery section
st.subheader("📂 Example Images")
example_dir = "dataimg/images"
if os.path.exists(example_dir):
    cols = st.columns(3)
    image_files = [img for img in os.listdir(example_dir) if img.endswith((".jpg", ".png", ".jpeg"))]
    for i, img_file in enumerate(image_files):
        img_path = os.path.join(example_dir, img_file)
        with cols[i % 3]:
            image = Image.open(img_path)
            st.image(image, caption=img_file, use_column_width=True)
            if st.button(f"Caption {img_file}", key=img_file):
                with st.spinner("Generating caption..."):
                    features = extract_features(img_path)
                    caption = generate_caption(model, tokenizer, features)
                st.success(f"**📝 Caption:** {caption}")
else:
    st.warning("No example images found in dataimg/images.")
