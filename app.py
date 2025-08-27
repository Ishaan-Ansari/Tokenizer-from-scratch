import streamlit as st
import re
import random
import html

st.set_page_config(page_title="Text Tokenizer", layout="wide")

# title
st.title("Tokenizer playground")

# Dropdown menu for selecting tokenizer type
tokenizer_type = st.selectbox("Select Tokenizer Type", ["Word-based", "Character-based", "Subword-based"])

# User input text area
input_text = st.text_area("Enter text to tokenize", height=150, value="Hello, world! This is a tokenizer playground.")

# special tokens
special_tokens = ["<start>", "<end-of-sequence>", "<pad>", "<unk>"]

def word_tokenizer(text):
    tokens = re.findall(r"\b\w+(?:'\w+)\b|[^\w\s]", text.lower())
    return special_tokens[:1] + tokens + special_tokens[1:]

def char_tokenizer(text):
    return special_tokens[:1] + list(text) + special_tokens[1:]


# Assign unique token IDs
def assign_token_ids(tokens):
    vocab = {}
    token_ids = []
    next_id = 100 # start from 100 for cleaner visualization

    for token in tokens:
        if token not in vocab:
            vocab[token] = next_id
            next_id += 1

        token_ids.append(vocab[token])
    return token_ids, vocab

# Tokenize
tokens = word_tokenizer(input_text) if tokenizer_type == "Word-based" else char_tokenizer(input_text)
token_ids, vocab = assign_token_ids(tokens)

# Display tokens count
st.markdown(f"### Total Tokens: {len(tokens)}")

# Custom colors palette
color_palette = [
    "#8ecae6", "#f2e8cf", "#e9ff70", "#edddd4", "#ffa5ab", 
    "#e0b1cb", "#a2d6f9", "#73e2a7", "#fe6d73", "#ffff3f", "#a594f9"
]

# Display colored tokens using custom palette
st.markdown("### Tokens")
colored_html = ""

for i, token in enumerate(tokens):
    color = color_palette[i % len(color_palette)]
    colored_html += f"""
    <span style="
        background-color: {color};
        color: black;
        padding: 1px 4px;
        font-size: 16px;
        margin: 2px;
        border-radius: 4px;
        display: inline-block;
    ">{token}</span>
    """
st.markdown(colored_html, unsafe_allow_html=True)

# Display token IDs
st.markdown("### Token IDs")
text_color = "white"
bg_color = "#1e1e1e"


# Format the token IDs like code blocks
token_id_html = f"""
<div style="
    background-color: {bg_color};
    color: {text_color};
    padding: 10px;
    border-radius: 5px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 16px;
">
    {token_ids}
</div>
"""

st.markdown(token_id_html, unsafe_allow_html=True)

# Optional: show vocab mapping 
with st.expander(" View Vocabulary Dictionary "):
    st.write(vocab)
