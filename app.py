import streamlit as st
import re
# Copy button library import karein
from st_copy_to_clipboard import st_copy_to_clipboard

st.set_page_config(page_title="Script Splitter Pro", page_icon="✂️", layout="wide")

# --- Helper Functions ---

def get_text_stats(text):
    """Returns character and word count."""
    chars = len(text)
    words = len(text.split())
    return chars, words

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

# --- UI Interface ---

st.title("✂️ Script Splitter (Strict Full Stop)")
st.markdown("Split long scripts & Copy with one click.")

# 1. Input Section
tab1, tab2 = st.tabs(["📝 Paste Text", "📂 Upload .txt File"])

final_text = ""

with tab1:
    text_input = st.text_area("Paste your script here:", height=250)
    if text_input:
        final_text = text_input

with tab2:
    uploaded_file = st.file_uploader("Choose a text file", type="txt")
    if uploaded_file is not None:
        string_data = uploaded_file.read().decode("utf-8")
        final_text = string_data
        st.success("File loaded successfully!")

# 2. Live Stats
if final_text:
    st.divider()
    t_chars, t_words = get_text_stats(final_text)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Characters", f"{t_chars:,}")
    col2.metric("Total Words", f"{t_words:,}")
    col3.info("Stats calculated automatically.")
    st.divider()

# 3. Settings Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    unit_option = st.radio("Count Unit:", ["Characters", "Words"])
    split_method = st.radio("Splitting Logic:", ["Fixed Limit (Max per part)", "Total Parts (Equal split)"])
    
    process_limit = 0
    if split_method == "Fixed Limit (Max per part)":
        process_limit = st.number_input(f"Max {unit_option} per part:", min_value=50, value=2000, step=100)
    else:
        num_parts = st.number_input("How many parts?", min_value=2, value=4)
        if final_text:
            total_count = len(final_text) if unit_option == "Characters" else len(final_text.split())
            process_limit = int(total_count / num_parts)

# 4. Output Generation
if st.button("🚀 Split Script", type="primary"):
    if not final_text:
        st.error("Please paste text or upload a file first.")
    else:
        result_chunks = split_text_strictly(final_text, process_limit, unit_option)
        
        st.subheader(f"✅ Result: {len(result_chunks)} Parts")
        
        for i, chunk in enumerate(result_chunks):
            c_len = len(chunk)
            w_len = len(chunk.split())
            label = f"Part {i+1} — ({w_len} Words / {c_len} Chars)"
            
            with st.expander(label, expanded=True):
                # Yahan "Copy" Button lagaya hai
                st_copy_to_clipboard(chunk, f"📋 Click to Copy Part {i+1}")
                
                # Text ko display karwaya hai (Code block mai taake clean lagay)
                st.code(chunk, language="text")
