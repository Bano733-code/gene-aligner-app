import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

st.set_page_config(page_title="Gene Aligner + Chatbot", layout="wide")

# Caching model + tokenizer
@st.cache_resource(show_spinner="Loading BioBot...")
def load_chatbot():
    try:
        tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
        return tokenizer, model
    except Exception as e:
        st.error(f"⚠️ Could not load chatbot model: {e}")
        return None, None

tokenizer, model = load_chatbot()

st.title("🧬 Gene Aligner + 🤖 Chatbot")

with st.expander("💬 Chat with BioBot"):
    if tokenizer is None or model is None:
        st.warning("Model not available. Please try again later or check logs.")
        st.stop()

    user_input = st.text_input("Ask me anything about gene alignment, sequences, or bioinformatics")

    if user_input:
        try:
            input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")

            # Move model to CPU (Streamlit Cloud doesn't support GPU)
            device = torch.device("cpu")
            model.to(device)
            input_ids = input_ids.to(device)

            chat_history_ids = model.generate(
                input_ids,
                max_length=1000,
                pad_token_id=tokenizer.eos_token_id,
                no_repeat_ngram_size=3,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.75,
            )

            response = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
            st.markdown(f"**BioBot:** {response}")
        except Exception as e:
            st.error(f"❌ Error while generating response: {e}")
