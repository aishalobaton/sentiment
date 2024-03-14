from textblob import TextBlob
import streamlit as st
from googletrans import Translator
import cv2
import numpy as np
import pytesseract
from PIL import Image

st.title('Los caracteres y las emociones')
image = Image.open('emoticones.jpg')
st.image(image)
st.subheader("Por favor toma una foto del texto que quieres analizar")

translator = Translator()

img_file_buffer = st.camera_input("Toma una Foto")
if img_file_buffer is not None:
    # To read image file buffer with OpenCV:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    with st.sidebar:
        filtro = st.radio("Aplicar Filtro", ('Con Filtro', 'Sin Filtro'))

    if filtro == 'Con Filtro':
        cv2_img = cv2.bitwise_not(cv2_img)

    # Display the image with or without filter
    st.image(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB), use_column_width=True)

    text = pytesseract.image_to_string(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))
    
    st.write(text)
    
    if text:
        try:
            translation = translator.translate(text, src="es", dest="en")
            trans_text = translation.text
            blob = TextBlob(trans_text)
            st.write('Polarity: ', round(blob.sentiment.polarity, 2))
            st.write('Subjectivity: ', round(blob.sentiment.subjectivity, 2))
            x = round(blob.sentiment.polarity, 2)
            if x >= 0.5:
                st.write('Es un sentimiento Positivo 😊')
            elif x <= -0.5:
                st.write('Es un sentimiento Negativo 😔')
            else:
                st.write('Es un sentimiento Neutral 😐')
        except Exception as e:
            st.error(f"Error en la traducción: {e}")
else:
    st.write("Toma una foto para analizar.")
