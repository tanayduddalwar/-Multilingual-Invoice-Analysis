from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(input,image,prompt):
     #input-what i want the llm to behave like as pdf extractor
     #image-the uploading image
     #prompt-what message i want what is address i have written in pdf 
    response=model.generate_content([input,image[0],prompt])
    return response.text

#function to convert the image to bytes so that it can read the image properly    
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
st.set_page_config(page_title="MultiLanguage Invoice Extractor")
st.header("MultiLanguage Invoice Extractor")
input=st.text_input("Input Prompt:",key="input")
uploaded_file=st.file_uploader("Choose an image of the invoice...",type=["jpg","png","jpeg"])
image=""
if uploaded_file is not None:
       image=Image.open(uploaded_file)
       st.image(image,caption="Uploaded Image.",use_column_width=True) 
submit=st.button("Tell me about the Invoice")

input_prompt="""
You are an expert in understanding invoices we will upload a image as invoice and you will have to answer any question based on the uploaded image
"""
if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is:")
    st.write(response)