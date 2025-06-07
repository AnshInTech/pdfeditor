from reportlab.pdfgen import  canvas
from reportlab.lib.pagesizes import letter, A4
from io import  BytesIO
import  PyPDF2 as pdfcreater
import streamlit as st


def angle_to_dir(angle):
    if 0<=angle<=90:
        return 90
    if 90<angle<=180:
        return 180
    if 180<angle<=270:
        return 270
    if 270<angle<=360:
        return 360
st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1508780709619-79562169bc64");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
def Create_PDF(text):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, text)
    c.save()
    buffer.seek(0)
    return buffer
def pdf_to_image_extractor(pdf_file):
    reader = pdfcreater.PdfReader(pdf_file)
    page = reader.pages[0]
    image_list=[]

    for count, image_file_object in enumerate(page.images):
        image_list.append(image_file_object.data)
    return image_list
def Extract_text(pdf_file):
    pdf=pdfcreater.PdfReader(pdf_file)
    text=""
    for page in pdf.pages:
        text_all =page.extract_text()
        text+=text_all
    return text
def Merge_pdf(pdfs):
    merged_pdf= pdfcreater.PdfWriter()
    for pdf in pdfs:
        reader=pdfcreater.PdfReader(pdf)
        for num_sum in range(len(reader.pages)):
            # page= reader.getPage(num_sum)
            # merged_pdf.addPage(page)
            merged_pdf.add_page(reader.pages[num_sum])
    buffer = BytesIO()
    merged_pdf.write(buffer)
    buffer.seek(0)
    return buffer

def Rotate_PDF(pdf,rotation):
    reader = pdfcreater.PdfReader(pdf)
    writer= pdfcreater.PdfWriter()
    for page_nim in range(len(reader.pages)):
        page = reader.pages[page_nim]
        page.rotate(rotation)
        writer.add_page(page)
    buffer = BytesIO()
    writer.write(buffer)
    buffer.seek(0)
    return buffer
def AddWatermark(pdf,text_watermark):
    output_buffer = BytesIO()

    # Create a PDF to use as watermark
    watermark_pdf = BytesIO()
    c = canvas.Canvas(watermark_pdf, pagesize=letter)
    c.setFont("Helvetica", 40)
    c.setFillGray(0.5, 0.5)
    c.drawCentredString(300, 500, text_watermark)
    c.save()
    watermark_pdf.seek(0)

    watermark_reader = pdfcreater.PdfReader(watermark_pdf)
    watermark_page = watermark_reader.pages[0]

    reader = pdfcreater.PdfReader(pdf)
    writer = pdfcreater.PdfWriter()

    for page in reader.pages:
        page.merge_page(watermark_page)
        writer.add_page(page)

    writer.write(output_buffer)
    output_buffer.seek(0)
    return output_buffer


def Encrypt_PDF(pdf,password):
    reader = pdfcreater.PdfReader(pdf)
    writer = pdfcreater.PdfWriter()

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        writer.add_page(page)

    writer.encrypt(password)
    buffer = BytesIO()
    writer.write(buffer)
    buffer.seek(0)
    return buffer
def main():
    st.title("PDF Editor Tool")

    menu = ["Create PDF", "Extract Text", "Merge PDFs",  "Rotate PDF",
            "Add Watermark", "Encrypt PDF"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice=="Create PDF":
       st.subheader("Create your PDF")
       text= st.text_input("Enter Your Text")
       if st.button("Create"):
           pdf=Create_PDF(text)
           st.download_button(
               label="Download PDF",
               data=pdf,  # <-- THIS is likely None
               file_name="report.pdf",
               mime="application/pdf"
           )
    if choice== "Merge PDFs":
        st.subheader("It can merge files")
        pdf_files = st.file_uploader("Upload your files",accept_multiple_files=True)
        if st.button("Merge PDFs"):
            merged_pdf = Merge_pdf(pdf_files)
            st.download_button(
                label="merged_pdf",
                data=merged_pdf,
                file_name="report.pdf",
                mime="application/pdf"
            )


    elif choice=="Extract Text":
        st.subheader("YOUR ALL TEXT OF PDF IS CONVERTED IN TXT FILE")
        pdf_file = st.file_uploader("Upload your PDF", type=["pdf"])
        if pdf_file is not None:
            extracted_text = Extract_text(pdf_file)
            st.text_area("Extracted Text:", extracted_text, height=300)


            if st.button("Download TXT"):
                st.download_button(
                    label="Click to Download",
                    data=extracted_text.encode("utf-8"),
                    file_name="my_file.txt",
                    mime="text/plain"
                )
    elif choice=="Rotate PDF":
        st.subheader("THIS METHOD ROTATES YOUR FILE ")

        pdf_file = st.file_uploader("Upload your PDF", type=["pdf"])

        if pdf_file :


            angle= st.number_input("JUST ENTER ANGLE")
            st.write("CONDITION:"
                     "IF YOU ENTER NUMBER BETWEEN 0 AND 90 ITS RIGHT,"
                     "IF YOU ENTER NUMBER BETWEEN 90 AND 180 ITS DOWN FLIP,"
                     "IF YOU ENTER NUMBER BETWEEN 180 AND 270 ITS LEFT,"
                     "IF YOU ENTER NUMBER BETWEEN 270 AND 360 ITS UP FLIP")
            direction=angle_to_dir(angle)
            rotated_file=Rotate_PDF(pdf_file,rotation=direction)
            if st.button("Download PDF"):
                st.download_button(
                    label="Click to Download",
                    data=rotated_file.getvalue(),  # Convert to bytes
                    file_name="rotated.pdf",
                    mime="application/pdf"
                )
    elif choice == "Add Watermark":
        st.subheader("THIS METHOD ADDS WATERMARK TO YOUR FILE ")
        pdf_file = st.file_uploader("Upload your PDF", type=["pdf"])
        if pdf_file:
            watermark =st.text_input("ENTER YOUR TEXT THAT YOU WANT TO ADD ")
            watermarkd_file=AddWatermark(pdf_file,watermark)
            if st.button("Download PDF"):
                st.download_button(
                    label="Click to Download",
                    data=watermarkd_file.getvalue(),
                    file_name="watermarked.pdf",
                    mime="application/pdf"
                )
    elif choice == "Encrypt PDF":
        st.subheader("THIS METHOD ADDS Encrypt TO YOUR FILE ")
        pdf_file = st.file_uploader("Upload your PDF", type=["pdf"])
        if pdf_file:
            user_password=st.text_input("ENTER YOUR PASSWORD")
            encrypt=Encrypt_PDF(pdf_file,user_password)
            if st.button("Download PDF"):
                st.download_button(
                    label="Click to Download",
                    data=encrypt.getvalue(),
                    file_name="watermarked.pdf",
                    mime="application/pdf"
                )

if __name__ == '__main__':
    main()