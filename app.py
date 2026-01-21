from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai
import  streamlit as st
from pdfextractor import text_extractor
from wordextractor import doc_text_extract
from image2text import extract_text_image

# Let's configure genai model
gemini_key=os.getenv('GOOGLE_API_KEY1')
genai.configure(api_key=gemini_key)
model=genai.GenerativeModel('gemini-2.5-flash-lite',
                            generation_config={'temperature':0.9})

# Let's create the sidebar
st.sidebar.title('UPLOAD YOUR NOTES')
st.sidebar.subheader('Only upload images,PDFs or DOCx')
user_file = st.sidebar.file_uploader('Upload Here: ',type=['pdf','docx','png','jpg','jpeg','jfif'])

if user_file:
    st.sidebar.success('File Uploaded Successfully')
    if user_file.type=='application/pdf':
        user_text=text_extractor(user_file)
    elif user_file.type in ['image/png','image/jpeg','image/jpg','image/jfif']:
                            user_text = extract_text_image(user_file)
    elif user_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        user_text = doc_text_extract(user_file)
    else:
        print('ERROR : Enter correct file type')  


# Let's create main page 
st.title(':rainbow[MoM Generator:-] :orange[AI Assisted Minutes of Meetings from ]')
st.subheader(':green[This application creates generalized minutes of meeting]')
st.write('''
         Follow the steps:
         1. Upload the notes in PDF , DOCx or Image Format in sidebar.
         2. Click "generate" to generate the MoM.''')

if st.button('Generate'):
    with st.spinner('Please wait...'):
        prompt=f'''
         <Role> You are an expert in writing and formating minutes of meetings.
         <Goal> Create minutes of meeting from the notes that user has provided.
         <Context> The user has provided some rough notes as text. Here are the notes: {user_text}.
         <Format> the output must follow the below format
        * Title: Assume title of the meeting.
        * Agenda: Assume agenda of the meeting.  
        * Attendees: Name of the attendees(If name of the attendees is not there keep 
        * Date and Place: Date and place of the meeting(If not provided keep it On 
        * Body: The body should follow the following sequence of points
                 * Mention Key points discussed.
                 * highlight and decision that has been taken.
                 * Mention Actionable Items.
                 * Mention any deadline if discussed.
                 * Add a 2-3 line of summary.
        <Instructions>
        * Use bullet points and highlight the important keywords by making them bold.
        * Generate the output in docx copy paste format. )  '''

        response =model.generate_content(prompt)
        st.write(response.text)

    if st.download_button(label='DOWNLOAD',
                           data=response.text,
                           file_name='MOM Generator.txt',
                           mime = 'text/plain'):
           st.success('File downloaded')