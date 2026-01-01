import streamlit as st
import re

st.set_page_config(page_title="Script Splitter", page_icon="✂️")

st.title("✂️ Script Splitter (Strict Full Stop)")

# --- Logic Functions ---

def split_strictly_on_dot(text, max_limit, unit_type):
    """
    Splits text ensuring chunks represent complete sentences only.
    It will NEVER break a sentence in the middle.
    It prefers to keep the chunk size UNDER the limit if the next sentence doesn't fit.
    """
    # 1. Text ko sentences mein todein (Full stop, ?, ! ke baad space ho tou)
    # Ye regex full stop ko sentence ke sath hi rakhega.
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        # Check karein agar hum ye sentence add karein tou kya limit cross hogi?
        # Agar current_chunk khali hai, tou seedha sentence add karo (taake blank start na ho)
        potential_len = 0
        
        if unit_type == "Characters":
            potential_len = len(current_chunk) + len(sentence)
        else: # Words
            potential_len = len(current_chunk.split()) + len(sentence.split())
        
        # Logic: Agar limit ke andar hai tou add karo
        if potential_len <= max_limit:
            current_chunk += sentence + " "
        else:
            # Agar limit cross ho rahi hai, tou purana chunk save karo (Full stop wala)
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            # Aur naya chunk shuru karo is sentence se
            current_chunk = sentence + " "
            
    # Jo aakhri hissa bacha hai use add karo
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

# --- UI Layout ---

# Input
script = st.text_area("Apni Script Paste Karein:", height=200)

# Options
col1, col2 = st.columns(2)
with col1:
    unit = st.selectbox("Unit Type:", ["Characters", "Words"])
with col2:
    mode = st.selectbox("Split Method:", ["Fixed Limit (Har part ki limit)", "Total Parts (Barabar hisson mai)"])

limit = 0
if mode == "Fixed Limit (Har part ki limit)":
    limit = st.number_input(f"Max {unit} per part:", min_value=10, value=2000, step=100)
    st.caption("Script yahan tak pohanch kar peeche wale Full Stop par ruk jayegi.")
else:
    parts = st.number_input("Total Parts:", min_value=2, value=4)
    # Temporary calculation to find limit per part
    if script:
        total_len = len(script) if unit == "Characters" else len(script.split())
        limit = int(total_len / parts) + int(total_len * 0.05) # Thoda buffer

if st.button("Break Script"):
    if not script:
        st.warning("Pehle script tou likhein!")
    else:
        # Process
        parts_list = split_strictly_on_dot(script, limit, unit)
        
        st.success(f"Done! Script {len(parts_list)} hisson mai toot gayi hai.")
        st.write("---")
        
        for i, part in enumerate(parts_list):
            count = len(part) if unit == "Characters" else len(part.split())
            with st.expander(f"Part {i+1} - ({count} {unit})"):
                st.code(part, language='text')
