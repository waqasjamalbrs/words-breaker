import streamlit as st
import re
from st_copy_to_clipboard import st_copy_to_clipboard

# Page Config (Wide layout for better button positioning)
st.set_page_config(page_title="Script Splitter Pro", page_icon="✂️", layout="wide")

# --- Custom CSS for better UI (Optional but recommended) ---
st.markdown("""
<style>
    .stButton button {
        width: 100%;
    }
    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Logic Functions ---
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

# --- UI Layout ---
st.title("✂️ Script Splitter Pro")

# Input Section
tab1, tab2 = st.tabs(["📝 Paste Text", "📂 Upload File"])
final_text = ""

with tab1:
    text_input = st.text_area("Paste text here:", height=200, placeholder="Paste your script...")
    if text_input: final_text = text_input
with tab2:
    uploaded = st.file_uploader("Upload .txt file", type="txt")
    if uploaded: final_text = uploaded.read().decode("utf-8")

# Live Global Stats
if final_text:
    st.divider()
    t_chars = len(final_text)
    t_words = len(final_text.split())
    
    # Stylish Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Characters", f"{t_chars:,}")
    c2.metric("Total Words", f"{t_words:,}")
    c3.info("Ready to split!")

# Sidebar
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

# Output Section
if st.button("🚀 Split Script", type="primary", use_container_width=True):
    if not final_text:
        st.error("Please provide text first.")
    else:
        chunks = split_text_strictly(final_text, limit, unit)
        
        st.write("---")
        st.subheader(f"✅ Result: {len(chunks)} Parts Created")
        
        # --- NEW UI LOOP ---
        for i, chunk in enumerate(chunks):
            # Calculate stats for THIS part
            p_chars = len(chunk)
            p_words = len(chunk.split())
            
            # Create a nice box (Container)
            with st.container(border=True):
                
                # Create Columns: Left (Text Info) | Right (Button)
                col_info, col_btn = st.columns([0.75, 0.25])
                
                with col_info:
                    # Missing stats wapis add kar diye
                    st.markdown(f"**Part {i+1}** — <span style='color:gray'>({p_words} Words / {p_chars} Chars)</span>", unsafe_allow_html=True)
                
                with col_btn:
                    # Button Right side par aur text update kar diya
                    st_copy_to_clipboard(chunk, "📋 Copy to Clipboard")
                
                # Text Display
                st.code(chunk, language="text")
