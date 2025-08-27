import streamlit as st
import re
import random
import html
from collections import Counter, defaultdict

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
    return special_tokens[:1] + tokens + special_tokens[1:2]

def char_tokenizer(text):
    return special_tokens[:1] + list(text) + special_tokens[1:2]


def bpe_tokenizer(text, max_merges=50):
    """BPE (Byte Pair Encoding) tokenizer implementation."""
    words = text.lower().split()
    words_freqs = Counter(words)

    # Convert words to character sequences
    splits = {}
    for word in words_freqs:
        splits[word] = list(word) 

    def get_stats(splits):
        """Count frequency of consecutive symobol pairs."""
        pairs = defaultdict(int)
        for word, freq in splits.items():
            symbols = word
            for i in range(len(symbols) - 1):
                pairs[(symbols[i], symbols[i + 1])] += freq
        return pairs

    def merge_symbols(pair, splits):
        """Merge the most frequent pair"""
        bigram = pair
        new_splits = {}
        for word in splits:
            new_word = []
            i = 0
            while i < len(splits[word]):
                if (i < len(splits[word]) - 1 and 
                    splits[word][i] == bigram[0] and 
                    splits[word][i + 1] == bigram[1]):
                    new_word.append(bigram[0] + bigram[1])
                    i += 2
                else:
                    new_word.append(splits[word][i])
                    i += 1
            new_splits[word] = new_word
        return new_splits
    

    for _ in range(max_merges):
        pairs = get_stats(splits)
        if not pairs:
            break
        best_pais = max(pairs, key=pairs.get)
        if pairs[best_pais] < 2:
            break

        splits = merge_symbols(best_pais, splits)

    # Tokenize the input text
    tokens = []
    for word in text.lower().split():
        if word in splits:
            tokens.extend(splits[word])
        else:
            tokens.append(list(word)) 

    return special_tokens[:1] + tokens + special_tokens[1:2]

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
if tokenizer_type == "Word-based":
    tokens = bpe_tokenizer(input_text)
    st.info("📝 Word-based tokenization splits text into words and punctuation")

elif tokenizer_type == "Character-based":
    tokens = char_tokenizer(input_text)
    st.info("🔤 Character-based tokenization splits text into individual characters")

elif tokenizer_type == "Subword-based":
    tokens = bpe_tokenizer(input_text)
    st.info("🧩 Subword-based (BPE) tokenization learns common subword units from the text")

token_ids, vocab = assign_token_ids(tokens)

# Display tokens count
st.markdown(f"### Total Tokens: {len(tokens)}")

# Display tokens count
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Tokens", len(tokens))
with col2:
    st.metric("Vocabulary Size", len(vocab))
with col3:
    compression_ratio = len(input_text) / len(tokens) if tokens else 0
    st.metric("Compression Ratio", f"{compression_ratio:.2f}")


# Custom colors palette
color_palette = [
    "#8ecae6", "#f2e8cf", "#e9ff70", "#edddd4", "#ffa5ab", 
    "#e0b1cb", "#a2d6f9", "#73e2a7", "#fe6d73", "#ffff3f", "#a594f9"
]

# Display colored tokens using custom palette
st.markdown("### Tokenized Output")
colored_html = "<div style='line-height: 2.5;'>"

for i, token in enumerate(tokens):
    color = color_palette[i % len(color_palette)]
    escaped_token = html.escape(str(token))
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

colored_html += "</div>"
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
