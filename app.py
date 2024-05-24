import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import google.generativeai as genai


load_dotenv()
# Load the environment variables
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)


##function to gemini pro vision

def get_gemini_response(input, image, prompt):
    ##loading the model
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image,prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
st.set_page_config(page_title="Invoice extractor")
# Title of the app
st.title('Image Upload and Display App')
st.header("Gemini Application")
# Input box for user input
user_input = st.text_input("Input prompt: ", key="input")

# File uploader for image files
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Check if a file is uploaded
if uploaded_file is not None:
    # Open and display the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

submit=st.button('Tell me about the invoice')

input_prompt="""
you are invoice extractor please read the invoice
"""

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image,user_input)

    st.subheader("this response is")
    st.write(response)



footer = """<style>.footer {position: fixed;left: 0;bottom: 0;width: 100%;background-color: #000;color: white;text-align: center;}</style><div class='footer'><p>Copyright 2024, feel free to contact leodeveloper@gmail.com</p></div>"""
st.markdown(footer, unsafe_allow_html=True)