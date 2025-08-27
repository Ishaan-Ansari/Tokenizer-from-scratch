# Word-Tokenizer-from-Scratch
<img width="1818" height="925" alt="Screenshot 2025-08-28 013320" src="https://github.com/user-attachments/assets/82a35e6e-9df3-40c8-a38a-76ee6307767e" />

---

An interactive Streamlit app to explore basic Tokenizers work.  
This project demonstrates word-level, character-level & Byte-Pair encoding tokenization, assigning token IDs and visualizing them with custom colors — just like how tokenization works behind the scenes in LLMs.


---

## Features

- Word-based tokenizer with special tokens like `<start>` and `<end-of-sequence>`
- Character-based tokenizer
- Token ID generation
- Token count display
---

## How It Works

1. User enters text in the Streamlit interface.
2. The text is tokenized:
   - Using a word tokenizer: splitting based on words and punctuation.
   - Or a character tokenizer: breaking down every character.
3. Tokens are displayed 
4. Each token is assigned a unique token ID.
5. Token count and optional vocab dictionary are also shown.

---

## Why This Matters

Modern Large Language Models (LLMs) like GPT or BERT don’t use word- or character-level tokenizers.  
They rely on subword tokenization methods, which break words into meaningful chunks (subwords) to handle unknown words and reduce vocabulary size.

### Common subword methods:

- Byte Pair Encoding (BPE) — used in GPT models
- SentencePiece — used in models like T5 and ALBERT

This project is a simplified educational tool to build intuition about how tokenization works before diving into real LLM tokenizers.

---

## Run the App Locally

```bash
pip install streamlit
streamlit run app.py
