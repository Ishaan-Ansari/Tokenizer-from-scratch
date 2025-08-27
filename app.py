import streamlit as st
import re
import random
from collections import defaultdict, Counter

st.set_page_config(page_title="Simple Tokenizer App", layout="wide")

# Title
st.title("Tokenizer Playground")

# Dropdown for tokenizer type
tokenizer_type = st.selectbox("Select Tokenizer Type", ["Word-based", "Character-based", "BPE-encoding"])

# User text input
text_input = st.text_area("Enter your text here:", height=150, value="Ishaan this side, Let's tokenize this sentence.")

# Special tokens
special_tokens = ["<start>", "<end-of-sequence>"]

if tokenizer_type == "BPE-encoding":
    num_merges = st.slider("Number of BPE Merges", min_value=1, max_value=50, value=10,
                           help="Higher values create larger vocabulary and longer tokens.")

# Tokenization logic
def word_tokenizer(text):
    tokens = re.findall(r"\b\w+(?:'\w+)?\b|[^\w\s]", text.lower())
    return special_tokens[:1] + tokens + special_tokens[1:]

def char_tokenizer(text):
    return special_tokens[:1] + list(text) + special_tokens[1:]


def bpe_tokenizer(text, num_merges=20):
    """
    Byte Pair Encoding (BPE) tokenizer
    """

    #  Pre-tokenize text into words
    words = text.split()

    # intialize the word frequencies and convert words to characters sequences
    word_freqs = Counter(words)
    
    # Conver words to sequences of characters with a special end-of-word token
    vocab = defaultdict(int)
    for word, freq in word_freqs.items():
        chars = list(word) + ["</w>"]
        for char in chars:
            vocab[char] += freq

    # initalize splits (each words as sequence of characters)
    splits = {}
    for word in word_freqs:
        splits[word] = list(word) + ["</w>"]

    # Learn BPE merges
    merges = []
    for i in range(num_merges): # Number of merges define it
        pairs = defaultdict(int)
        for word, freq in word_freqs.items():
            symbols = splits[word]
            for j in range(len(symbols)-1):
                pairs[(symbols[j], symbols[j+1])] += freq
        
        if not pairs:
            break


        # Find the most frequent pair
        best_pair = max(pairs, key=pairs.get)
        merges.append(best_pair)

        # Merge the best pair in all splits
        new_splits = {}
        for word in splits:
            new_word = []
            i = 0
            symbols = splits[word]
            while i < len(symbols):
                if (
                    i < len(symbols) - 1 and
                    symbols[i] == best_pair[0] and
                    symbols[i+1] == best_pair[1]
                ):
                    # Merge the pair
                    new_word.append(best_pair[0] + best_pair[1])
                    i += 2
                else:
                    new_word.append(symbols[i])
                    i += 1
            new_splits[word] = new_word

        splits = new_splits

        # Add merged token to vocabulary
        merged_token = best_pair[0] + best_pair[1]
        vocab[merged_token] = pairs[best_pair]


    def apply_bpe(word):
        """
        Apply learned BPE merges to a word
        """
        if not word:
            return []

        # start with characters
        symbols = list(word) + ["</w>"]

        # Apply each merge in order
        for merge in merges:
            new_symbols = []
            i = 0
            while i < len(symbols):
                if(i < len(symbols) - 1 and symbols[i] == merge[0] and symbols[i+1] == merge[1]):
                    new_symbols.append(merge[0] + merge[1])
                    i += 2
                else:
                    new_symbols.append(symbols[i])
                    i += 1
            symbols = new_symbols
        return symbols
    
    tokens = []
    for word in words:
        word_tokens = apply_bpe(word)
        tokens.extend(word_tokens)

    return special_tokens[:1] + tokens + special_tokens[1:], dict(vocab), merges

# Assign unique token IDs
def assign_token_ids(tokens):
    vocab = {}
    token_ids = []
    next_id = 100  # Start from 100 for cleaner visualization

    for token in tokens:
        if token not in vocab:
            vocab[token] = next_id
            next_id += 1
        token_ids.append(vocab[token])
    return token_ids, vocab

# Tokenize
# tokens = word_tokenizer(text_input) if tokenizer_type == "Word-based" else char_tokenizer(text_input)
if tokenizer_type == "Word-based":
    tokens = word_tokenizer(text_input)
    token_ids, vocab = assign_token_ids(tokens)

elif tokenizer_type == "Character-based":
    tokens = char_tokenizer(text_input)
    token_ids, vocab = assign_token_ids(tokens)
elif tokenizer_type == "BPE-encoding":
    tokens, bpe_vocab, merges = bpe_tokenizer(text_input, num_merges)
    # token_ids, vocab = assign_token_ids(tokens)


token_ids, vocab = assign_token_ids(tokens)

# Display token count
st.markdown(f"###  Token Count: `{len(tokens)}`")
# Custom color palette
color_palette = [
    "#8ecae6", "#f2e8cf", "#e9ff70", "#edddd4", "#ffa5ab", 
    "#e0b1cb", "#a2d6f9", "#73e2a7", "#fe6d73", "#ffff3f", "#a594f9"
]

# Display colored tokens using custom palette
st.markdown("### Tokens")
colored_html = ""
for i, token in enumerate(tokens):
    color = color_palette[i % len(color_palette)]  # Cycle through colors
    colored_html += f"""
    <span style='
        background-color:{color};
        color:black;
        padding:1px 4px;
        font-size:15px;
        margin:2px;
        display:inline-block;
    '> {token} </span>"""
st.markdown(colored_html, unsafe_allow_html=True)


# Display token IDs
st.markdown("### Token IDs")
text_color = "white"
bg_color = "#1e1e1e"

# Format the token IDs like code
token_id_html = f"""
<div style='
    background-color:{bg_color};
    color:{text_color};
    padding:10px;
    font-size:15px;
    font-family:monospace;
'>
{token_ids}
</div>
"""

st.markdown(token_id_html, unsafe_allow_html=True)

# Optional: show vocab mapping
with st.expander(" View Vocab Dictionary"):
    st.json(vocab)