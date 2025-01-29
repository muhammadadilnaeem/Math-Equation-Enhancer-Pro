import os
import re
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page and styling
st.set_page_config(
    page_title="✨ Math Equation Enhancer Pro",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/yourusername/math-equation-enhancer',
        'Report a bug': 'https://github.com/yourusername/math-equation-enhancer/issues',
        'About': '''
        ### Math Equation Enhancer Pro
        An AI-powered tool for converting LaTeX equations in Markdown.
        '''
    }
)

# Custom CSS styling
st.markdown("""
    <style>
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
    }
    
    /* App Container */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Title Styling */
    .stTitle {
        background: linear-gradient(120deg, #2c3e50, #3498db);
        padding: 1.5rem;
        border-radius: 15px;
        color: white !important;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    /* Input/Output Container Styling */
    .markdown-container {
        background: white;
        border: 3px solid #3498db;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }

    /* Button Container Styling */
    .button-container {
        padding: 1rem 0;
        margin-top: 1rem;
    }
    
    /* Unified Button Styling for both Convert and Download */
    div[data-testid="stButton"] button,
    div[data-testid="stDownloadButton"] button {
        width: 100%;
        min-height: 65px;
        background: linear-gradient(45deg, #2ecc71, #27ae60);
        color: white;
        padding: 1rem 2.5rem;
        border-radius: 12px;
        font-size: 20px;
        font-weight: bold;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        letter-spacing: 1px;
        line-height: 1.5;
        text-transform: uppercase;
    }
    
    div[data-testid="stButton"] button:hover,
    div[data-testid="stDownloadButton"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        background: linear-gradient(45deg, #27ae60, #2ecc71);
        letter-spacing: 2px;
    }

    div[data-testid="stButton"] button p,
    div[data-testid="stDownloadButton"] button p {
        font-size: 20px !important;
    }
    
    /* Footer Styling */
    .footer {
        background: linear-gradient(120deg, #2c3e50, #3498db);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Helper functions (unchanged)
def clean_equations_with_regex(text):
    return re.sub(r"\\\((.*?)\\\)", r"$\1$", text)

def get_gemini_response(text):
    prompt = (
        "You are a text processor. Your ONLY TASK is to replace ALL inline LaTeX equations formatted as \( ... \) "
        "with Markdown-style equations $ ... $. Do NOT change any other text. "
        "Return ONLY the modified text."
    )
    response = model.generate_content([prompt, text])
    processed_text = response.text.strip() if response.text else text
    return clean_equations_with_regex(processed_text)

def process_large_text(text, chunk_size=3000):
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    converted_chunks = [get_gemini_response(chunk) for chunk in chunks]
    return "".join(converted_chunks)

# Enhanced App Header
st.markdown("""
    <div class="stTitle">
        <h1>📘 Math Equation Enhancer Pro ✨</h1>
        <p style="font-size: 1.2rem; margin-top: 0.5rem;">
            Transform Your LaTeX Equations with AI Precision
        </p>
    </div>
""", unsafe_allow_html=True)

# Welcome Message
st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
        <h4>🎯 Welcome to Math Equation Enhancer Pro!</h4>
        <p>Enhance your mathematical documentation with our advanced equation converter:</p>
        <ul>
            <li>🔄 Convert LaTeX equations from \( ... \) to $ ... $ format</li>
            <li>📝 Preserve original markdown formatting</li>
            <li>⚡ Process large documents with AI precision</li>
            <li>💾 Easy export options</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if "output_text" not in st.session_state:
    st.session_state.output_text = ""

# Create two columns
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="markdown-container">', unsafe_allow_html=True)
    st.markdown("### 📝 Input Markdown")
    st.markdown("Paste your Markdown content with LaTeX equations below:")
    input_text = st.text_area("", height=400, placeholder="Enter your markdown text here...")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("🔄 Convert Equations", help="Click to process and convert equations in your markdown"):
        if input_text:
            with st.spinner("🔄 Processing equations..."):
                st.session_state.output_text = process_large_text(input_text)
            st.success("✅ Conversion completed!")
            st.balloons()
        else:
            st.warning("⚠️ Please enter some text to convert")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="markdown-container">', unsafe_allow_html=True)
    st.markdown("### ✨ Converted Output")
    st.markdown("Your processed markdown with converted equations:")
    output_text = st.text_area("", value=st.session_state.output_text, height=400, key="output_area")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.session_state.output_text:
        st.download_button(
            label="📥 Download Converted Markdown",
            data=st.session_state.output_text,
            file_name="enhanced_equations.md",
            mime="text/markdown",
            help="Download your converted markdown as a .md file"
        )
    st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Footer
st.markdown("""
    <div class="footer">
        <h4>🚀 Math Equation Enhancer Pro</h4>
        <p>Made with ❤️ using Streamlit and Google's Gemini AI</p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem;">
            💡 Pro Tip: For best results, ensure your LaTeX equations are properly formatted
        </p>
    </div>
""", unsafe_allow_html=True)


# import os
# import re
# import streamlit as st
# import google.generativeai as genai
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Configure page and styling
# st.set_page_config(
#     page_title="✨ Math Equation Enhancer Pro",
#     page_icon="📘",
#     layout="wide",
#     initial_sidebar_state="collapsed",
#     menu_items={
#         'Get Help': 'https://github.com/yourusername/math-equation-enhancer',
#         'Report a bug': 'https://github.com/yourusername/math-equation-enhancer/issues',
#         'About': '''
#         ### Math Equation Enhancer Pro
#         An AI-powered tool for converting LaTeX equations in Markdown.
#         '''
#     }
# )

# # Custom CSS styling
# st.markdown("""
#     <style>
#     /* Global Styles */
#     .main {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#         padding: 2rem;
#     }
    
#     /* App Container */
#     .stApp {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#     }
    
#     /* Title Styling */
#     .stTitle {
#         background: linear-gradient(120deg, #2c3e50, #3498db);
#         padding: 1.5rem;
#         border-radius: 15px;
#         color: white !important;
#         text-align: center;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#         margin-bottom: 2rem;
#     }
    
#     /* Input/Output Container Styling */
#     .markdown-container {
#         background: white;
#         border: 3px solid #3498db;
#         border-radius: 15px;
#         padding: 20px;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#         margin-bottom: 1rem;
#     }
    
#     /* Convert Button Styling */
#     div[data-testid="stButton"] button {
#         width: 100%;
#         background: linear-gradient(45deg, #2ecc71, #27ae60);
#         color: white;
#         padding: 0.8rem 2rem;
#         border-radius: 12px;
#         font-size: 18px;
#         font-weight: bold;
#         border: none;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#         margin: 1rem 0;
#     }
    
#     div[data-testid="stButton"] button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(0,0,0,0.15);
#     }
    
#     /* Download Button Styling */
#     div[data-testid="stDownloadButton"] button {
#         background: linear-gradient(45deg, #9b59b6, #8e44ad);
#         color: white;
#         padding: 0.8rem 2rem;
#         border-radius: 8px;
#         font-weight: bold;
#         width: 100%;
#         border: none;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
    
#     /* Footer Styling */
#     .footer {
#         background: linear-gradient(120deg, #2c3e50, #3498db);
#         padding: 1.5rem;
#         border-radius: 15px;
#         color: white;
#         text-align: center;
#         margin-top: 2rem;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Configure Google API
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash")

# # Helper functions (unchanged)
# def clean_equations_with_regex(text):
#     return re.sub(r"\\\((.*?)\\\)", r"$\1$", text)

# def get_gemini_response(text):
#     prompt = (
#         "You are a text processor. Your ONLY TASK is to replace ALL inline LaTeX equations formatted as \( ... \) "
#         "with Markdown-style equations $ ... $. Do NOT change any other text. "
#         "Return ONLY the modified text."
#     )
#     response = model.generate_content([prompt, text])
#     processed_text = response.text.strip() if response.text else text
#     return clean_equations_with_regex(processed_text)

# def process_large_text(text, chunk_size=3000):
#     chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
#     converted_chunks = [get_gemini_response(chunk) for chunk in chunks]
#     return "".join(converted_chunks)

# # Enhanced App Header
# st.markdown("""
#     <div class="stTitle">
#         <h1>📘 Math Equation Enhancer Pro ✨</h1>
#         <p style="font-size: 1.2rem; margin-top: 0.5rem;">
#             Transform Your LaTeX Equations with AI Precision
#         </p>
#     </div>
# """, unsafe_allow_html=True)

# # Welcome Message
# st.markdown("""
#     <div style='background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
#         <h4>🎯 Welcome to Math Equation Enhancer Pro!</h4>
#         <p>Enhance your mathematical documentation with our advanced equation converter:</p>
#         <ul>
#             <li>🔄 Convert LaTeX equations from \( ... \) to $ ... $ format</li>
#             <li>📝 Preserve original markdown formatting</li>
#             <li>⚡ Process large documents with AI precision</li>
#             <li>💾 Easy export options</li>
#         </ul>
#     </div>
# """, unsafe_allow_html=True)

# # Initialize session state
# if "output_text" not in st.session_state:
#     st.session_state.output_text = ""

# # Create two columns
# col1, col2 = st.columns(2)

# with col1:
#     st.markdown('<div class="markdown-container">', unsafe_allow_html=True)
#     st.markdown("### 📝 Input Markdown")
#     st.markdown("Paste your Markdown content with LaTeX equations below:")
#     input_text = st.text_area("", height=400, placeholder="Enter your markdown text here...")
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     if st.button("🔄 Convert Equations", help="Click to process and convert equations in your markdown"):
#         if input_text:
#             with st.spinner("🔄 Processing equations..."):
#                 st.session_state.output_text = process_large_text(input_text)
#             st.success("✅ Conversion completed!")
#             st.balloons()
#         else:
#             st.warning("⚠️ Please enter some text to convert")

# with col2:
#     st.markdown('<div class="markdown-container">', unsafe_allow_html=True)
#     st.markdown("### ✨ Converted Output")
#     st.markdown("Your processed markdown with converted equations:")
#     output_text = st.text_area("", value=st.session_state.output_text, height=400, key="output_area")
    
#     if st.session_state.output_text:
#         st.download_button(
#             label="📥 Download Converted Markdown",
#             data=st.session_state.output_text,
#             file_name="enhanced_equations.md",
#             mime="text/markdown",
#             help="Download your converted markdown as a .md file"
#         )
#     st.markdown('</div>', unsafe_allow_html=True)

# # Enhanced Footer
# st.markdown("""
#     <div class="footer">
#         <h4>🚀 Math Equation Enhancer Pro</h4>
#         <p>Made with ❤️ using Streamlit and Google's Gemini AI</p>
#         <p style="font-size: 0.8rem; margin-top: 0.5rem;">
#             💡 Pro Tip: For best results, ensure your LaTeX equations are properly formatted
#         </p>
#     </div>
# """, unsafe_allow_html=True)

# # Import necessary libraries

# import os
# import re
# import streamlit as st
# import google.generativeai as genai
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Configure Google API Key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash")

# # Helper function to clean equations using regex as a fallback
# def clean_equations_with_regex(text):
#     """Ensure all LaTeX equations are converted using regex as a fallback."""
#     return re.sub(r"\\\((.*?)\\\)", r"$\1$", text)  # Convert \( ... \) to $ ... $

# # Helper function to get Gemini response or fallback to regex
# def get_gemini_response(text):
#     """Convert LaTeX equations using Google Gemini API."""
#     prompt = (
#         "You are a text processor. Your ONLY TASK is to replace ALL inline LaTeX equations formatted as \( ... \) "
#         "with Markdown-style equations $ ... $. Do NOT change any other text. "
#         "Ensure every occurrence is replaced, including those inside markdown blocks. "
#         "Return ONLY the modified text."
#     )
    
#     response = model.generate_content([prompt, text])
#     processed_text = response.text.strip() if response.text else text  # Handle API failures
#     return clean_equations_with_regex(processed_text)  # Apply regex as a fallback

# # Helper function to process large text in chunks for better accuracy
# def process_large_text(text, chunk_size=3000):
#     """Chunk large text and process it in parts for better accuracy."""
#     chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
#     converted_chunks = [get_gemini_response(chunk) for chunk in chunks]
#     return "".join(converted_chunks)

# # Streamlit App UI
# st.set_page_config(page_title="Math Equation Enhancer", layout="wide")
# st.title("📘 Math Equation Enhancer")
# st.write("Convert LaTeX-style equations in Markdown from `\\( ... \\)` to `$ ... $` notation using AI.")

# # Initialize session state if not set
# if "output_text" not in st.session_state:
#     st.session_state.output_text = ""

# # Create two columns for input and output
# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("📝 Input Markdown")
#     input_text = st.text_area("Paste your Markdown with LaTeX equations:", height=400)
    
#     if st.button("🔄 Convert Markdown") and input_text:
#         st.session_state.output_text = process_large_text(input_text)

# with col2:
#     st.subheader("✅ Converted Markdown")
#     output_text = st.text_area("Converted Output:", value=st.session_state.output_text, height=400, key="output_area")
    
#     if st.session_state.output_text:
#         st.download_button(
#             label="📥 Download as .md",
#             data=st.session_state.output_text,
#             file_name="converted_markdown.md",
#             mime="text/markdown"
#         )

# st.write("Made with ❤️ using Streamlit and Google's Gemini AI")



# import os
# import streamlit as st
# import google.generativeai as genai
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Configure Google API Key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash")

# def get_gemini_response(text):
#     """Convert LaTeX equations using Google Gemini API."""
    
#     prompt = """
#     You are a text processor. Your ONLY TASK is to replace all inline LaTeX equations formatted as \( ... \) 
#     with Markdown-style equations $ ... $.  
#     Do NOT change any other text.  
#     Do NOT add any explanations.  
#     Do NOT provide any additional comments.  
#     Return ONLY the modified text.  
#     """
    
#     response = model.generate_content([prompt, text])  # Order matters: prompt first!
#     return response.text.strip()  # Remove any unexpected leading/trailing spaces

# # Streamlit App UI
# st.set_page_config(page_title="Math Equation Enhancer", layout="wide")
# st.title("📘 Math Equation Enhancer")
# st.write("Convert LaTeX-style equations in Markdown from `\\( ... \\)` to `$ ... $` notation using AI.")

# # Initialize session state if not set
# if "output_text" not in st.session_state:
#     st.session_state.output_text = ""

# # Create two columns for input and output
# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("📝 Input Markdown")
#     input_text = st.text_area("Paste your Markdown with LaTeX equations:", height=400)
    
#     if st.button("🔄 Convert Markdown") and input_text:
#         # Ensure API gets the correct input
#         st.session_state.output_text = get_gemini_response(input_text)

# with col2:
#     st.subheader("✅ Converted Markdown")
#     output_text = st.text_area("Converted Output:", value=st.session_state.output_text, height=400, key="output_area")
    
#     if st.session_state.output_text:
#         st.download_button(
#             label="📥 Download as .md",
#             data=st.session_state.output_text,
#             file_name="converted_markdown.md",
#             mime="text/markdown"
#         )

# st.write("Made with ❤️ using Streamlit and Google's Gemini AI")




# import os
# import streamlit as st
# import google.generativeai as genai
# from dotenv import load_dotenv
# import pyperclip

# # Load environment variables
# load_dotenv()

# # Configure Google API Key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash")

# def get_gemini_response(text):
#     """Convert LaTeX equations using Google Gemini API."""
#     prompt = "Convert LaTeX-style equations in Markdown from \\( ... \\) to $ ... $. Do not Provide Your Suggestions and Anything Else Except the Modified Text."
#     response = model.generate_content([text, prompt])
#     return response.text

# # Streamlit App UI
# st.set_page_config(page_title="Math Equation Enhancer", layout="wide")
# st.title("📘 Math Equation Enhancer")
# st.write("Convert LaTeX-style equations in Markdown from `\\( ... \\)` to `$ ... $` notation using AI.")

# # Initialize session state if not set
# if "output_text" not in st.session_state:
#     st.session_state.output_text = ""

# # Create two columns for input and output
# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("📝 Input Markdown")
#     input_text = st.text_area("Paste your Markdown with LaTeX equations:", height=400)
#     if st.button("🔄 Convert Markdown") and input_text:
#         st.session_state.output_text = get_gemini_response(input_text)

# with col2:
#     st.subheader("✅ Converted Markdown")
#     output_text = st.text_area("Converted Output:", value=st.session_state.output_text, height=400, key="output_area")
    
#     if st.session_state.output_text:
#         st.download_button(
#             label="📥 Download as .md",
#             data=st.session_state.output_text,
#             file_name="converted_markdown.md",
#             mime="text/markdown"
#         )

# st.write("Made with ❤️ using Streamlit and Google's Gemini AI")


# import os
# import streamlit as st
# import google.generativeai as genai
# from dotenv import load_dotenv
# import pyperclip

# # Load environment variables
# load_dotenv()

# # Configure Google API Key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash")

# def get_gemini_response(text):
#     """Convert LaTeX equations using Google Gemini API."""
#     prompt = "Convert LaTeX-style equations in Markdown from \\( ... \\) to $ ... $."
#     response = model.generate_content([text, prompt])
#     return response.text

# # Streamlit App UI
# st.set_page_config(page_title="Math Equation Enhancer", layout="wide")
# st.title("📘 Math Equation Enhancer")
# st.write("Convert LaTeX-style equations in Markdown from `\\( ... \\)` to `$ ... $` notation using AI.")

# # Create two columns for input and output
# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("📝 Input Markdown")
#     input_text = st.text_area("Paste your Markdown with LaTeX equations:", height=400)
#     convert_button = st.button("🔄 Convert Markdown")

# with col2:
#     st.subheader("✅ Converted Markdown")
#     output_text = st.text_area("Converted Output:", height=400, key="output_area")
    
#     if convert_button and input_text:
#         converted_text = get_gemini_response(input_text)
#         st.session_state.output_area = converted_text
    
#     if st.session_state.get("output_area", ""):
#         st.download_button(
#             label="📥 Download as .md",
#             data=st.session_state.output_area,
#             file_name="converted_markdown.md",
#             mime="text/markdown"
#         )

# st.write("Made with ❤️ using Streamlit and Google's Gemini AI")


# import os
# import streamlit as st
# import google.generativeai as genai
# from dotenv import load_dotenv
# import pyperclip

# # Load environment variables
# load_dotenv()

# # Configure Google API Key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash")

# def get_gemini_response(text):
#     """Convert LaTeX equations using Google Gemini API."""
#     prompt = "Convert LaTeX-style equations in Markdown from \\( ... \\) to $ ... $."
#     response = model.generate_content([text, prompt])
#     return response.text

# # Streamlit App UI
# st.set_page_config(page_title="Math Equation Enhancer", layout="wide")
# st.title("📘 Math Equation Enhancer")
# st.write("Convert LaTeX-style equations in Markdown from `\\( ... \\)` to `$ ... $` notation using AI.")

# # Create two columns for input and output
# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("📝 Input Markdown")
#     input_text = st.text_area("Paste your Markdown with LaTeX equations:", height=400)

# with col2:
#     st.subheader("✅ Converted Markdown")
#     if input_text:
#         converted_text = get_gemini_response(input_text)
#         st.code(converted_text, language='markdown')
        
#         # Copy to clipboard button
#         def copy_to_clipboard():
#             pyperclip.copy(converted_text)
#             st.success("Copied to clipboard!")
        
#         if st.button("📋 Copy to Clipboard"):
#             copy_to_clipboard()

# st.write("Made with ❤️ using Streamlit and Google's Gemini AI")
