import streamlit as st
import base64
from fpdf import FPDF
import io

st.set_page_config(page_title="CV Builder", layout="wide")

# Custom CSS for better styling with increased font sizes
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;  /* Increased from 2.5rem */
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .section-header {
        font-size: 2rem;  /* Increased from 1.5rem */
        color: #1E88E5;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .info-text {
        font-size: 1.2rem;  /* Increased from 1rem */
    }
    .download-button {
        text-align: center;
        margin-top: 2.5rem;
        font-size: 1.2rem;
    }
    .stButton>button {
        font-size: 1.1rem;  /* Larger buttons */
    }
    .stTextInput>div>div>input {
        font-size: 1.1rem;  /* Larger input text */
    }
    .stTextArea>div>div>textarea {
        font-size: 1.1rem;  /* Larger textarea text */
    }
    /* Enhanced education block styling */
    .education-block {
        background-color: #f8f9fa;
        border-left: 5px solid #1E88E5;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 5px;
    }
    .education-title {
        font-size: 1.4rem;
        font-weight: bold;
        color: #1E88E5;
    }
    .education-subtitle {
        font-size: 1.2rem;
        font-style: italic;
        color: #555;
    }
    .education-dates {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 10px;
    }
    .education-description {
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown("<h1 class='main-header'>CV Builder</h1>", unsafe_allow_html=True)
st.markdown("<p class='info-text' style='text-align: center;'>Build your professional CV and download it as a PDF</p>", unsafe_allow_html=True)

# Initialize session state for storing CV data
if 'cv_data' not in st.session_state:
    st.session_state.cv_data = {
        'personal_info': {
            'name': '',
            'email': '',
            'phone': '',
            'address': '',
            'summary': ''
        },
        'education': [],
        'experience': [],
        'skills': []
    }

# Function to create PDF with increased font sizes
def create_pdf(cv_data):
    pdf = FPDF()
    pdf.add_page()
    
    # Set font with increased sizes
    pdf.set_font("Arial", size=14)  # Increased from 12
    
    # Personal Information
    pdf.set_font("Arial", 'B', 20)  # Increased from 16
    pdf.cell(200, 12, txt=cv_data['personal_info']['name'], ln=True, align='C')
    
    pdf.set_font("Arial", size=12)  # Increased from 10
    pdf.cell(200, 6, txt=f"Email: {cv_data['personal_info']['email']}", ln=True, align='C')
    pdf.cell(200, 6, txt=f"Phone: {cv_data['personal_info']['phone']}", ln=True, align='C')
    pdf.cell(200, 6, txt=f"Address: {cv_data['personal_info']['address']}", ln=True, align='C')
    
    # Summary
    pdf.ln(12)  # Increased spacing
    pdf.set_font("Arial", 'B', 16)  # Increased from 12
    pdf.cell(200, 12, txt="PROFESSIONAL SUMMARY", ln=True)
    pdf.set_font("Arial", size=12)  # Increased from 10
    pdf.multi_cell(0, 6, txt=cv_data['personal_info']['summary'])
    
    # Education with enhanced styling
    if cv_data['education']:
        pdf.ln(12)  # Increased spacing
        pdf.set_font("Arial", 'B', 16)  # Increased from 12
        pdf.cell(200, 12, txt="EDUCATION", ln=True)
        
        for edu in cv_data['education']:
            # Add a light background for education blocks
            current_y = pdf.get_y()
            pdf.set_fill_color(240, 240, 240)  # Light gray background
            pdf.rect(10, current_y, 190, 30, style='F')  # Background rectangle
            
            # Education title with larger font
            pdf.set_xy(15, current_y + 2)
            pdf.set_font("Arial", 'B', 14)  # Increased from 10
            pdf.cell(180, 8, txt=f"{edu['degree']}", ln=True)
            
            # Institution with emphasis
            pdf.set_xy(15, pdf.get_y())
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(180, 6, txt=f"{edu['institution']}", ln=True)
            
            # Dates with styling
            pdf.set_xy(15, pdf.get_y())
            pdf.set_font("Arial", 'I', 12)
            pdf.cell(180, 6, txt=f"{edu['start_date']} - {edu['end_date']}", ln=True)
            
            # Description with proper spacing
            pdf.set_xy(15, pdf.get_y() + 2)
            pdf.set_font("Arial", '', 12)
            pdf.multi_cell(180, 6, txt=edu['description'])
            pdf.ln(10)  # Extra space between education entries
    
    # Experience
    if cv_data['experience']:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 16)  # Increased from 12
        pdf.cell(200, 12, txt="WORK EXPERIENCE", ln=True)
        
        for exp in cv_data['experience']:
            pdf.set_font("Arial", 'B', 14)  # Increased from 10
            pdf.cell(200, 8, txt=f"{exp['position']} - {exp['company']}", ln=True)
            pdf.set_font("Arial", 'I', 12)  # Increased from 10
            pdf.cell(200, 6, txt=f"{exp['start_date']} - {exp['end_date']}", ln=True)
            pdf.set_font("Arial", '', 12)  # Increased from 10
            pdf.multi_cell(0, 6, txt=exp['description'])
            pdf.ln(8)  # Increased spacing between experiences
    
    # Skills
    if cv_data['skills']:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 16)  # Increased from 12
        pdf.cell(200, 12, txt="SKILLS", ln=True)
        
        pdf.set_font("Arial", '', 12)  # Increased from 10
        skills_text = ", ".join(cv_data['skills'])
        pdf.multi_cell(0, 6, txt=skills_text)
    
    return pdf

# Function to download PDF
def get_pdf_download_link(cv_data, filename="cv.pdf"):
    pdf = create_pdf(cv_data)
    pdf_bytes = pdf.output(dest="S").encode("latin1")
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}" style="font-size: 1.2rem; padding: 10px 15px; background-color: #1E88E5; color: white; text-decoration: none; border-radius: 5px;">Download CV as PDF</a>'
    return href

# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Personal Info", "Education", "Experience", "Skills", "Preview & Download"])

# Tab 1: Personal Information
with tab1:
    st.markdown("<h2 class='section-header'>Personal Information</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", st.session_state.cv_data['personal_info']['name'], key="name_input")
        email = st.text_input("Email", st.session_state.cv_data['personal_info']['email'], key="email_input")
        phone = st.text_input("Phone", st.session_state.cv_data['personal_info']['phone'], key="phone_input")
    
    with col2:
        address = st.text_area("Address", st.session_state.cv_data['personal_info']['address'], height=120, key="address_input")
    
    summary = st.text_area("Professional Summary", st.session_state.cv_data['personal_info']['summary'], height=180, key="summary_input")
    
    if st.button("Save Personal Information", key="save_personal_info"):
        st.session_state.cv_data['personal_info'] = {
            'name': name,
            'email': email,
            'phone': phone,
            'address': address,
            'summary': summary
        }
        st.success("Personal information saved!")

# Tab 2: Education with enhanced styling
with tab2:
    st.markdown("<h2 class='section-header'>Education</h2>", unsafe_allow_html=True)
    
    # Display existing education entries with enhanced styling
    for i, edu in enumerate(st.session_state.cv_data['education']):
        # Create a visually enhanced education block
        st.markdown(f"""
        <div class="education-block">
            <div class="education-title">{edu['degree']}</div>
            <div class="education-subtitle">{edu['institution']}</div>
            <div class="education-dates">{edu['start_date']} - {edu['end_date']}</div>
            <div class="education-description">{edu['description']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add remove button outside the HTML block
        if st.button(f"Remove Education #{i+1}", key=f"remove_edu_{i}"):
            st.session_state.cv_data['education'].pop(i)
            st.rerun()
    
    # Add new education entry with improved form
    with st.expander("Add New Education", expanded=True):
        with st.form("education_form"):
            st.markdown("<p class='info-text'>Enter your education details below:</p>", unsafe_allow_html=True)
            
            degree = st.text_input("Degree/Certificate", key="degree_input")
            institution = st.text_input("Institution", key="institution_input")
            
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.text_input("Start Date (e.g., Sep 2018)", key="edu_start_date")
            with col2:
                end_date = st.text_input("End Date (e.g., Jun 2022 or Present)", key="edu_end_date")
            
            description = st.text_area("Description (achievements, courses, thesis, etc.)", height=150, key="edu_description")
            
            submit_button = st.form_submit_button("Add Education")
            if submit_button:
                if degree and institution:  # Basic validation
                    st.session_state.cv_data['education'].append({
                        'degree': degree,
                        'institution': institution,
                        'start_date': start_date,
                        'end_date': end_date,
                        'description': description
                    })
                    st.success("Education added!")
                else:
                    st.error("Please enter at least the degree and institution.")

# Tab 3: Experience
with tab3:
    st.markdown("<h2 class='section-header'>Work Experience</h2>", unsafe_allow_html=True)
    
    # Display existing experience entries
    for i, exp in enumerate(st.session_state.cv_data['experience']):
        with st.expander(f"Experience #{i+1}: {exp['position']} at {exp['company']}", expanded=True):
            st.markdown(f"<p class='info-text'><strong>Position:</strong> {exp['position']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='info-text'><strong>Company:</strong> {exp['company']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='info-text'><strong>Duration:</strong> {exp['start_date']} - {exp['end_date']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='info-text'><strong>Description:</strong> {exp['description']}</p>", unsafe_allow_html=True)
            
            if st.button(f"Remove Experience #{i+1}", key=f"remove_exp_{i}"):
                st.session_state.cv_data['experience'].pop(i)
                st.rerun()
    
    # Add new experience entry
    with st.expander("Add New Experience", expanded=True):
        with st.form("experience_form"):
            st.markdown("<p class='info-text'>Enter your work experience details below:</p>", unsafe_allow_html=True)
            
            position = st.text_input("Position/Title", key="position_input")
            company = st.text_input("Company/Organization", key="company_input")
            
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.text_input("Start Date (e.g., Jan 2020)", key="exp_start_date")
            with col2:
                end_date = st.text_input("End Date (e.g., Dec 2022 or Present)", key="exp_end_date")
            
            description = st.text_area("Description (responsibilities, achievements)", height=150, key="exp_description")
            
            submit_button = st.form_submit_button("Add Experience")
            if submit_button:
                if position and company:  # Basic validation
                    st.session_state.cv_data['experience'].append({
                        'position': position,
                        'company': company,
                        'start_date': start_date,
                        'end_date': end_date,
                        'description': description
                    })
                    st.success("Experience added!")
                else:
                    st.error("Please enter at least the position and company.")

# Tab 4: Skills
with tab4:
    st.markdown("<h2 class='section-header'>Skills</h2>", unsafe_allow_html=True)
    
    # Display existing skills with larger text
    if st.session_state.cv_data['skills']:
        st.markdown("<p class='info-text'><strong>Current Skills:</strong></p>", unsafe_allow_html=True)
        skills_cols = st.columns(3)
        for i, skill in enumerate(st.session_state.cv_data['skills']):
            col_idx = i % 3
            with skills_cols[col_idx]:
                st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 10px;'>{skill} <span style='color: red;'>❌</span></div>", unsafe_allow_html=True)
                if st.button(f"Remove", key=f"remove_skill_{i}"):
                    st.session_state.cv_data['skills'].remove(skill)
                    st.rerun()
    
    # Add new skill with improved styling
    with st.form("skill_form"):
        st.markdown("<p class='info-text'>Add a new skill to your CV:</p>", unsafe_allow_html=True)
        new_skill = st.text_input("Skill", key="new_skill_input")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            submit_button = st.form_submit_button("Add Skill")
        
        if submit_button and new_skill:
            if new_skill not in st.session_state.cv_data['skills']:
                st.session_state.cv_data['skills'].append(new_skill)
                st.success(f"Skill '{new_skill}' added!")
            else:
                st.warning(f"Skill '{new_skill}' already exists!")

# Tab 5: Preview and Download with larger fonts
with tab5:
    st.markdown("<h2 class='section-header'>Preview & Download</h2>", unsafe_allow_html=True)
    
    # Preview CV with increased font sizes
    st.markdown("<h3 style='font-size: 1.8rem; color: #1E88E5;'>CV Preview</h3>", unsafe_allow_html=True)
    
    # Personal Info with larger fonts
    st.markdown(f"<h2 style='font-size: 2.2rem; text-align: center;'>{st.session_state.cv_data['personal_info']['name']}</h2>", unsafe_allow_html=True)
    
    contact_info = f"<p style='font-size: 1.2rem; text-align: center;'><strong>Email:</strong> {st.session_state.cv_data['personal_info']['email']} | <strong>Phone:</strong> {st.session_state.cv_data['personal_info']['phone']}</p>"
    st.markdown(contact_info, unsafe_allow_html=True)
    
    address_info = f"<p style='font-size: 1.2rem; text-align: center;'><strong>Address:</strong> {st.session_state.cv_data['personal_info']['address']}</p>"
    st.markdown(address_info, unsafe_allow_html=True)
    
    # Summary with larger font
    st.markdown("<h3 style='font-size: 1.6rem; margin-top: 20px;'>PROFESSIONAL SUMMARY</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 1.2rem;'>{st.session_state.cv_data['personal_info']['summary']}</p>", unsafe_allow_html=True)
    
    # Education with enhanced styling
    if st.session_state.cv_data['education']:
        st.markdown("<h3 style='font-size: 1.6rem; margin-top: 20px;'>EDUCATION</h3>", unsafe_allow_html=True)
        
        for edu in st.session_state.cv_data['education']:
            # Enhanced education block in preview
            st.markdown(f"""
            <div class="education-block">
                <div class="education-title">{edu['degree']}</div>
                <div class="education-subtitle">{edu['institution']}</div>
                <div class="education-dates">{edu['start_date']} - {edu['end_date']}</div>
                <div class="education-description">{edu['description']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Experience with larger font
    if st.session_state.cv_data['experience']:
        st.markdown("<h3 style='font-size: 1.6rem; margin-top: 20px;'>WORK EXPERIENCE</h3>", unsafe_allow_html=True)
        
        for exp in st.session_state.cv_data['experience']:
            st.markdown(f"<p style='font-size: 1.4rem; font-weight: bold;'>{exp['position']} - {exp['company']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 1.2rem; font-style: italic;'>{exp['start_date']} - {exp['end_date']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 1.2rem;'>{exp['description']}</p>", unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)
    
    # Skills with larger font
    if st.session_state.cv_data['skills']:
        st.markdown("<h3 style='font-size: 1.6rem; margin-top: 20px;'>SKILLS</h3>", unsafe_allow_html=True)
        
        skills_text = ", ".join(st.session_state.cv_data['skills'])
        st.markdown(f"<p style='font-size: 1.2rem;'>{skills_text}</p>", unsafe_allow_html=True)
    
    # Download button with enhanced styling
    st.markdown("<div class='download-button'>", unsafe_allow_html=True)
    st.markdown(get_pdf_download_link(st.session_state.cv_data), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Instructions on how to use the app with larger font
st.sidebar.title("How to Use")
st.sidebar.markdown("""
<p style='font-size: 1.1rem;'>
1. Fill in your personal information in the 'Personal Info' tab<br>
2. Add your education history in the 'Education' tab<br>
3. Add your work experience in the 'Experience' tab<br>
4. List your skills in the 'Skills' tab<br>
5. Preview your CV and download it as a PDF in the 'Preview & Download' tab
</p>
""", unsafe_allow_html=True)

# Run the app
st.sidebar.info("To run this app locally, save this code as 'cv_builder.py' and run 'streamlit run cv_builder.py' in your terminal.")