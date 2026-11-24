
import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🎓",
    layout="centered"
)

# Get Groq API key
api_key = os.getenv("GROQ_API_KEY")

try:
    if not api_key:
        api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

# Website heading
st.title("🎓 AI Research Assistant")

st.write(
    "Generate research titles, abstracts, "
    "keywords and objectives using AI."
)

st.divider()

# Main input section
st.header("Enter Your Project Details")

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
        "Deep Learning",
        "Data Science",
        "Computer Science",
        "Internet of Things (IoT)",
        "Cyber Security",
        "Other"
    ]
)

# Generate button
if st.button("✨ Generate Research Content", use_container_width=True):

    if not project_idea.strip():
        st.warning("Please enter your project idea.")

    elif not api_key:
        st.error(
            "Groq API key not found. "
            "Please add GROQ_API_KEY in Streamlit Secrets."
        )

    else:
        try:
            with st.spinner("AI is generating your research content..."):

                client = Groq(api_key=api_key)

                prompt = f"""
                You are an academic research assistant.

                Project Idea: {project_idea}
                Project Domain: {domain}

                Generate the following academic research content:

                1. Research Title:
                Suggest three suitable research titles.

                2. Abstract:
                Write a clear academic abstract of approximately
                150-200 words.

                3. Keywords:
                Provide 5-8 relevant research keywords.

                4. Research Objectives:
                Provide 4-5 clear and achievable objectives.

                Use simple academic English.
                Organize the answer with clear headings.
                Make the content relevant to the project idea.
                """

                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a helpful academic "
                                "research assistant."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.5,
                    max_completion_tokens=2500
                )

                result = response.choices[0].message.content

            st.success("Research content generated successfully!")

            st.divider()

            st.header("📚 Generated Research Content")

            st.markdown(result)

            st.download_button(
                label="📥 Download Research Content",
                data=result,
                file_name="AI_Research_Content.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error("Something went wrong while generating content.")
            st.exception(e)

# Footer
st.divider()

st.caption(
    "AI Research Assistant | Powered by Groq"
)
