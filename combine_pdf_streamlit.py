# app.py
import io
import pathlib

import streamlit as st
from PyPDF2 import PdfReader, PdfWriter

st.set_page_config(page_title="Interleave PDF Merger", layout="centered")

st.title("Interleave PDF Merger — Insert 1-page PDF after every page")

st.markdown(
    "Upload the **main** multi-page PDF and the **single-page** PDF. "
    "The app will insert the single page after every page of the main PDF "
    "and let you download the merged PDF directly."
)

main_file = st.file_uploader("Upload main PDF (large file)", type=["pdf"])
single_file = st.file_uploader("Upload single-page PDF", type=["pdf"])

if st.button("Merge PDFs"):
    if not main_file or not single_file:
        st.error("Please upload both files.")
    else:
        try:
            # Read uploaded files with PdfReader (accepts file-like objects)
            main_reader = PdfReader(main_file)
            single_reader = PdfReader(single_file)

            main_page_count = len(main_reader.pages)
            single_page_count = len(single_reader.pages)

            # Use the first page of the single PDF
            single_page = single_reader.pages[0]
            if single_page_count != 1:
                st.warning(
                    f"Single-page PDF has {single_page_count} pages — using only the first page."
                )

            # Build writer and interleave
            writer = PdfWriter()
            for page in main_reader.pages:
                writer.add_page(page)
                writer.add_page(single_page)

            # Write merged PDF into bytes buffer (merge happens here)
            merged_buffer = io.BytesIO()
            writer.write(merged_buffer)
            merged_buffer.seek(0)
            merged_bytes = merged_buffer.getvalue()
            merged_size_kb = len(merged_bytes) / 1024

            # Prepare friendly output filename
            main_name = pathlib.Path(main_file.name).stem
            output_pdf_name = f"{main_name}_updated.pdf"

            # Info for the user
            st.success("Merged successfully 🎉")
            st.write("Main PDF pages:", main_page_count)
            st.write("Inserted page(s): 1 (the first page of the uploaded single-page PDF)")
            st.write(f"Resulting pages: {main_page_count * 2}")
            st.write(f"Merged file size: {merged_size_kb:.1f} KB")

            # Direct PDF download (no ZIP)
            st.download_button(
                label="Download merged PDF",
                data=merged_bytes,
                file_name=output_pdf_name,
                mime="application/pdf",
            )

        except Exception as e:
            st.exception(e)
