
import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Load the API key
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the website
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🎓",
    layout="centered"
)

# Website heading
st.title("🎓 AI Research Assistant")
st.write("Generate research titles, abstracts, keywords and objectives using AI.")

st.divider()

# User input
st.subheader("Enter Your Project Details")

project_idea = st.text_area(
    "Describe your project idea:",
    placeholder="Example: Detect fake news using machine learning",
    height=120
)

domain = st.selectbox(
    "Select your project domain:",
    [
        "Artificial Intelligence (AI)",
        "Machine Learning",
        "Internet of Things (IoT)",
        "Web Development",
        "Cybersecurity",
        "Other"
    ]
)

# Generate button
if st.button("✨ Generate Research Content", use_container_width=True):

    if not project_idea.strip():
        st.warning("Please enter your project idea.")

    elif not API_KEY:
        st.error("API key not found. Please check your .env file.")

    else:
        with st.spinner("Gemini AI is generating your research content..."):

            try:
                client = genai.Client(api_key=API_KEY)

                prompt = f"""
                You are an expert research assistant.

                Project idea: {project_idea}
                Domain: {domain}

                Generate the following:

                1. THREE RESEARCH TITLE OPTIONS
                Make them professional and meaningful.

                2. RESEARCH ABSTRACT
                Write an abstract between 150 and 200 words.

                3. FIVE KEYWORDS
                List five important keywords.

                4. THREE RESEARCH OBJECTIVES
                Write three clear objectives.

                5. THREE FUTURE ENHANCEMENTS
                Suggest three possible improvements.

                Use simple, clear and professional English.
                Use headings for each section.
                """

                response = client.interactions.create(
                    model="gemini-3.8-flash",
                    input=prompt
                )

                result = response.output_text

                st.success("Research content generated successfully!")

                st.divider()
                st.subheader("📚 Generated Research Content")

                st.markdown(result)

                st.download_button(
                    label="📥 Download Research Content",
                    data=result,
                    file_name="research_content.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error("Something went wrong. Please try again.")
                st.caption(str(e))

st.divider()
st.caption("AI Research Assistant | Powered by Google Gemini")
