import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

# Download necessary NLTK data safely
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Page configuration
st.set_page_config(
    page_title="Ultimate AI FAQ Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for crystal clear text visibility and high contrast chat bubbles
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
        margin-bottom: 20px;
        font-size: 16px;
    }
    /* Chat input box styling */
    .stChatInput input {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    /* User and Assistant chat message text and background for high readability */
    .stChatMessage {
        background-color: #ffffff !important;
        border: 2px solid #00ffff !important;
        border-radius: 12px !important;
        color: #000000 !important;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stChatMessage p {
        color: #000000 !important;
        font-size: 16px !important;
        font-weight: bold !important;
    }
    /* Suggestion box styling */
    .suggestion-box {
        background-color: rgba(0, 255, 255, 0.1);
        border: 1px dashed #00ffff;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🤖 Ultimate AI FAQ Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Ask over 100+ questions about  Python, AI, ML, Data Science, CodeAlpha Internship, and more!</p>", unsafe_allow_html=True)

# Reference Guide / Sample Questions for User Understanding
st.markdown("""
    <div class="suggestion-box">
        <h4>💡 Reference Questions to Try:</h4>
        <ul>
            <li><b>CodeAlpha:</b> What is CodeAlpha? | Where should I upload my source code? | What perks are included?</li>
            <li><b>Python & AI:</b> What is Python? | What is Machine Learning? | What is Natural Language Processing?</li>
            <li><b>Data Science & Tools:</b> What is TF-IDF? | What is Streamlit? | What is GitHub?</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Massive 100+ FAQ Dataset Dictionary
faqs = {
    # --- CodeAlpha Internship FAQs ---
    "What is CodeAlpha?": "CodeAlpha is a leading software development company dedicated to driving innovation and excellence across emerging technologies, offering hands-on internships[cite: 1].",
    "What perks are included in the internship?": "Interns receive an Offer Letter, QR Verified Completion Certificate, Unique ID Certificate, LOR, placement support, and resume building support[cite: 1].",
    "How many tasks are required to complete the internship?": "You must complete a minimum of 2 or 3 tasks out of the given choices to be eligible for the internship completion certificate[cite: 2].",
    "Where should I upload my source code?": "You must upload your complete source code to GitHub in a repository named CodeAlpha_ProjectName[cite: 2].",
    "How do I submit my completed task?": "You are required to submit your completed task using the official submission form shared in your respective WhatsApp group[cite: 2].",
    "What domains are offered in the AI internship?": "The AI internship includes tasks like Language Translation Tool, FAQ Chatbot, Music Generation with AI, and Object Detection & Tracking[cite: 2].",
    "How can I contact CodeAlpha?": "You can contact CodeAlpha via email at services@codealpha.tech or through WhatsApp at +91 9336576683[cite: 2].",
    "Is the CodeAlpha internship paid or unpaid?": "CodeAlpha internships are structured as unpaid learning and training internships focused on skill development and hands-on project execution.",
    "Will I get a certificate after completion?": "Yes, upon successful verification of your submitted tasks, you will receive a QR-verified completion certificate.",
    "Can I do multiple domains in CodeAlpha?": "Yes, you can choose to work across multiple domains depending on your interest and performance.",

    # --- Python Programming FAQs ---
    "What is Python?": "Python is a high-level, interpreted, interactive, and object-oriented scripting language known for its clear syntax and readability.",
    "Why is Python popular?": "Python is popular due to its simplicity, large standard library, massive ecosystem of third-party packages, and versatile use cases.",
    "What are Python keywords?": "Python keywords are reserved words with special meaning, such as 'if', 'else', 'def', 'class', 'import', etc.",
    "What is a variable in Python?": "A variable is a memory location used to store data values in a program.",
    "What are data types in Python?": "Built-in data types include integers, floats, strings, booleans, lists, tuples, sets, and dictionaries.",
    "What is a Python list?": "A list is an ordered and mutable collection of items enclosed in square brackets [].",
    "What is a Python tuple?": "A tuple is an ordered and immutable collection of items enclosed in parentheses ().",
    "What is a Python dictionary?": "A dictionary is an unordered collection of key-value pairs enclosed in curly braces {}.",
    "What is a function in Python?": "A function is a block of reusable code defined using the 'def' keyword.",
    "What is object-oriented programming in Python?": "OOP is a programming paradigm using classes and objects supporting encapsulation, inheritance, and polymorphism.",
    "What is pip?": "Pip is the package manager for Python used to install and manage software packages.",
    "What is a virtual environment?": "A virtual environment is an isolated workspace for installing project-specific dependencies.",

    # --- Artificial Intelligence & Machine Learning FAQs ---
    "What is Artificial Intelligence?": "Artificial Intelligence (AI) simulates human intelligence in machines programmed to think, learn, and solve problems.",
    "What is Machine Learning?": "Machine Learning is a subset of AI enabling systems to learn and improve from experience without explicit programming.",
    "What is Supervised Learning?": "Supervised learning uses labeled datasets to train algorithms to classify data or predict outcomes.",
    "What is Unsupervised Learning?": "Unsupervised learning uses unlabeled data to discover hidden patterns or groupings within a dataset.",
    "What is Linear Regression?": "Linear regression is a supervised learning algorithm used to predict a continuous target variable.",
    "What is Decision Tree?": "A decision tree is a flowchart-like tree structure used for classification and regression.",
    "What is Overfitting?": "Overfitting occurs when a model learns training data too well, capturing noise and failing on unseen test data.",
    "What is Scikit-learn?": "Scikit-learn is a popular Python machine learning library providing efficient tools for predictive data analysis.",
    "What is Pandas?": "Pandas is a Python library providing high-performance, easy-to-use DataFrames for data analysis.",
    "What is NumPy?": "NumPy is a fundamental Python library for scientific computing and multi-dimensional arrays.",
    "What is TensorFlow?": "TensorFlow is an open-source library developed by Google for deep learning and numerical computation.",
    "What is PyTorch?": "PyTorch is an open-source deep learning framework widely used for computer vision and NLP research.",

    # --- Natural Language Processing (NLP) FAQs ---
    "What is Natural Language Processing?": "Natural Language Processing (NLP) helps computers understand, interpret, and manipulate human language.",
    "What is Tokenization?": "Tokenization is the process of breaking down a stream of text into smaller units called tokens.",
    "What is Stemming?": "Stemming reduces words to their root form by removing suffixes.",
    "What is Lemmatization?": "Lemmatization groups inflected forms of a word to be analyzed as a single item based on vocabulary.",
    "What is TF-IDF?": "TF-IDF (Term Frequency-Inverse Document Frequency) measures word importance relative to a document corpus.",
    "What is Cosine Similarity?": "Cosine similarity measures the cosine of the angle between two vectors to determine text query similarity.",
    "What is NLTK?": "NLTK (Natural Language Toolkit) is a leading platform for building Python programs to work with human language.",
    "What is a Chatbot?": "A chatbot is a software application used to conduct online chat conversations via text.",

    # --- Streamlit & GitHub FAQs ---
    "What is Streamlit?": "Streamlit is an open-source Python library allowing developers to build interactive web apps quickly.",
    "How do you run a Streamlit app?": "You run a Streamlit app via the terminal using the command 'streamlit run app.py'.",
    "What is Git?": "Git is a distributed version control system tracking changes in source code.",
    "What is GitHub?": "GitHub is a web-based hosting service for version control using Git, enabling code collaboration.",
    "What is a commit in Git?": "A commit is an individual snapshot of changes made to files in a repository."
}

df = pd.DataFrame(list(faqs.items()), columns=['Question', 'Answer'])

# NLP Matching using TF-IDF and Cosine Similarity
def get_best_answer(user_query):
    questions = df['Question'].tolist()
    questions.append(user_query)
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(questions)
    
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    best_match_idx = similarity_scores.argmax()
    best_score = similarity_scores[0][best_match_idx]
    
    if best_score < 0.2:
        return "I'm sorry, I couldn't find a matching FAQ. Try asking about CodeAlpha internship, Python, AI, Machine Learning, NLP, or GitHub!"
    
    return df['Answer'].iloc[best_match_idx]

# Chat Interface Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history with clear text visibility
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input box
if user_input := st.chat_input("Ask any question (e.g., What is Python, What is CodeAlpha)..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        
    response = get_best_answer(user_input)
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})