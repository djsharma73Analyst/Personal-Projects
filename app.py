import streamlit as st
import pdf_conversion
import os
import multiprocessing as mp
from functools import partial

mp.freeze_support()  

st.title("PDF Conversion Tool")

input_dir = st.text_input("Input Directory") 
output_dir = st.text_input("Output Directory", "output") 
processes = int(st.text_input("Utilize cores", "4")) 


if st.button("Convert PDFs"):
    if input_dir: 
        try:
            # Gather file paths
            file_paths = []
            for root, _, files in os.walk(input_dir):
                for file in files:
                    if file.endswith(".pdf"):
                        file_paths.append(os.path.join(root, file))

            # Define the number of processes

            # Multiprocessing
            with mp.Pool(processes=processes) as pool:
                func = partial(pdf_conversion.process_pdf, output_dir=output_dir)
                pool.map(func, file_paths)

            st.success("PDF Conversion Successful!")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please provide an input directory.")

