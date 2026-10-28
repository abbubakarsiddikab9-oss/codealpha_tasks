import streamlit as st
from translate import Translator

# Page configuration
st.set_page_config(
    page_title="Language Translation Tool",
    page_icon="🌐",
    layout="centered"
)

# Custom CSS for high contrast visibility
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: #ffffff;
    }
    .main-title {
        color: #00ffff;
        text-align: center;
        font-weight: 700;
        text-shadow: 0px 0px 10px rgba(0, 255, 255, 0.5);
    }
    .sub-text {
        color: #e0e0e0;
        text-align: center;
        margin-bottom: 30px;
    }
    /* Input text area styling for clear visibility */
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }
    /* Translated output box styling */
    .stInfo {
        background-color: #ffffff !important;
        color: #00ffff !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }
    label {
        color: #00ffff !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    .stButton>button {
        width: 100%;
        background-color: #00ffff;
        color: #0f2027;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        height: 48px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #00b3b3;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🌐Language Translation Tool</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Translate text between multiple languages instantly.</p>", unsafe_allow_html=True)

# Language codes mapping
languages_dict = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Arabic": "ar",
    "Urdu": "ur",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Chinese": "zh",
    "Japanese": "ja",
    "Korean": "ko",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru"
}

language_names = list(languages_dict.keys())

# UI Layout: Two columns
col1, col2 = st.columns(2)

with col1:
    source_lang_name = st.selectbox(
        "Source Language Code (From)", 
        options=["Auto Detect"] + language_names, 
        index=0
    )

with col2:
    target_lang_name = st.selectbox(
        "Target Language Code (To)", 
        options=language_names, 
        index=1 
    )

# Text input area
text_to_translate = st.text_area(
    "Enter text to translate:", 
    placeholder="Enter text here...", 
    height=150
)

# Translate button and logic
if st.button("Translate Text"):
    if not text_to_translate.strip():
        st.warning("Type something here to translate.")
    else:
        try:
            with st.spinner("Translating..."):
                target_code = languages_dict[target_lang_name]
                
                if source_lang_name == "Auto Detect":
                    translator = Translator(to_lang=target_code)
                else:
                    source_code = languages_dict[source_lang_name]
                    translator = Translator(from_lang=source_code, to_lang=target_code)
                
                translated_text = translator.translate(text_to_translate)
                
                st.success("Translation Successful!")
                st.markdown("### Translated Text:")
                st.info(translated_text)
                
        except Exception as e:
            st.error(f"There was an error in the Translation: {e}")