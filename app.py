import streamlit as st
import re
# Ab ye library 100% chalegi (runtime.txt ki wajah se)
from st_copy_to_clipboard import st_copy_to_clipboard

st.set_page_config(page_title="Script Splitter Pro", page_icon="✂️", layout="wide")

# --- Logic ---
def split_text_strictly(text, limit, unit_type):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if unit_type == "Characters":
            len_check = len(current_chunk) + len(sentence)
        else:
            len_check = len(current_chunk.split()) + len(sentence.split())
            
        if len_check <= limit:
            current_chunk += sentence + " "
        else:
            if current_chunk: chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk: chunks.append(current_chunk.strip())
    return chunks

# --- UI ---
st.title("✂️ Script Splitter")
st.caption("Auto-split scripts into parts. Copy with one click.")

# Input
tab1, tab2 = st.tabs(["📝 Paste Text", "📂 Upload File"])
final_text = ""

with tab1:
    text_input = st.text_area("Paste text here:", height=200)
    if text_input: final_text = text_input
with tab2:
    uploaded = st.file_uploader("Upload .txt", type="txt")
    if uploaded: final_text = uploaded.read().decode("utf-8")

# Stats
if final_text:
    st.divider()
    chars = len(final_text)
    words = len(final_text.split())
    c1, c2 = st.columns(2)
    c1.metric("Total Characters", f"{chars:,}")
    c2.metric("Total Words", f"{words:,}")

# Settings
with st.sidebar:
    st.header("⚙️ Settings")
    unit = st.radio("Unit:", ["Characters", "Words"])
    mode = st.radio("Mode:", ["Fixed Limit", "Total Parts"])
    limit = 0
    if mode == "Fixed Limit":
        limit = st.number_input(f"Max {unit}:", value=2000, step=100)
    else:
        parts = st.number_input("Parts:", value=4, min_value=2)
        if final_text:
            total = len(final_text) if unit == "Characters" else len(final_text.split())
            limit = int(total / parts)

# Output
if st.button("🚀 Split Script", type="primary"):
    if not final_text:
        st.error("Text required.")
    else:
        chunks = split_text_strictly(final_text, limit, unit)
        st.subheader(f"✅ {len(chunks)} Parts Created")
        
        for i, chunk in enumerate(chunks):
            st.write(f"**Part {i+1}**")
            # --- YE RAHA VISIBLE BUTTON ---
            st_copy_to_clipboard(chunk, f"📋 Copy Part {i+1}")
            # Text Display
            st.code(chunk, language="text")
            st.divider()
