import streamlit as st
import re

st.set_page_config(page_title="Script Splitter Pro", page_icon="✂️", layout="wide")

# --- Helper Functions ---

def split_text_strictly(text, limit, unit_type):
    """
    Splits text strictly respecting full stops.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if unit_type == "Characters":
            current_size = len(current_chunk)
            sentence_size = len(sentence)
        else:
            current_size = len(current_chunk.split())
            sentence_size = len(sentence.split())
            
        if (current_size + sentence_size) <= limit:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

def get_text_stats(text):
    return len(text), len(text.split())

# --- UI Interface ---

st.title("✂️ Script Splitter")

# 1. Input Section
tab1, tab2 = st.tabs(["📝 Paste Text", "📂 Upload .txt File"])

final_text = ""

with tab1:
    text_input = st.text_area("Paste script here:", height=200)
    if text_input: final_text = text_input
with tab2:
    uploaded_file = st.file_uploader("Choose a text file", type="txt")
    if uploaded_file: final_text = uploaded_file.read().decode("utf-8")

# 2. Stats
if final_text:
    st.divider()
    chars, words = get_text_stats(final_text)
    c1, c2 = st.columns(2)
    c1.metric("Total Characters", f"{chars:,}")
    c2.metric("Total Words", f"{words:,}")

# 3. Settings Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    unit_option = st.radio("Count Unit:", ["Characters", "Words"])
    split_method = st.radio("Mode:", ["Fixed Limit", "Total Parts"])
    
    limit = 0
    if split_method == "Fixed Limit":
        limit = st.number_input(f"Max {unit_option}:", value=2000, step=100)
    else:
        parts = st.number_input("Parts:", value=4)
        if final_text:
            total = len(final_text) if unit_option == "Characters" else len(final_text.split())
            limit = int(total / parts)

# 4. Output with Copy Button
if st.button("🚀 Split Script", type="primary"):
    if not final_text:
        st.error("No text found.")
    else:
        chunks = split_text_strictly(final_text, limit, unit_option)
        
        st.subheader(f"✅ Result: {len(chunks)} Parts")
        st.info("💡 Tip: Mouse ko text box ke upar le kar jayen, Copy button Top-Right par nazar aayega.")
        
        for i, chunk in enumerate(chunks):
            # Expander khula rakha hai
            with st.expander(f"Part {i+1}", expanded=True):
                # st.code automatically Top-Right corner par Copy button deta hai
                st.code(chunk, language="text")
