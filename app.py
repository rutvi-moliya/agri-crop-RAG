import os
import streamlit as st

from main import load_vector_store, create_qa_chain, ask_question

st.set_page_config(
    page_title="Agri Crop Q&A",
    page_icon="🌾",
    layout="wide"
)

# ----------------------------
# Sidebar (controls)
# ----------------------------
st.sidebar.title("Agri Crop Q&A")
st.sidebar.caption("Gemini + RAG (Chroma)")

if st.sidebar.button("🧹 Clear chat"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! Ask me anything from your agricultural PDFs"}
    ]

st.sidebar.divider()
st.sidebar.subheader("Settings")

# These are UI settings. (If your create_qa_chain uses MODEL_NAME/TEMPERATURE from config,
# you can either keep those OR update your create_qa_chain to accept these.)
top_k = st.sidebar.slider("Top-K chunks to retrieve", 1, 8, 3)
temperature = st.sidebar.slider("Temperature (creativity)", 0.0, 1.0, 0.2, 0.1)

show_sources = st.sidebar.checkbox("Show sources", value=True)

st.sidebar.divider()
st.sidebar.caption("Tip: For a demo, enable sources ")

# ----------------------------
# Load chain once (cached)
# ----------------------------
@st.cache_resource
def get_chain():
    vectorstore = load_vector_store()
    if vectorstore is None:
        return None, "Vector DB not found. Build it first (run your DB creation once)."
    qa_chain = create_qa_chain(vectorstore)
    return qa_chain, None

qa_chain, err = get_chain()

# ----------------------------
# Main header
# ----------------------------
st.title("🌾 Agri Crop Management Q&A")
st.caption("Ask natural language questions. Answers are grounded in your uploaded PDFs.")

if err:
    st.error(err)
    st.stop()

# ----------------------------
# Session state for messages
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! Ask me anything from your agricultural PDFs 🌿"}
    ]

# ----------------------------
# Render chat history
# ----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------
# Chat input
# ----------------------------
user_question = st.chat_input("Type your question…")

if user_question:
    #show user message
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    # answer
    with st.chat_message("assistant"):
        with st.spinner("Searching your documents…"):
            # You can pass top_k/temperature if your functions support it.
            # For now, we just call your ask_question.
            result = ask_question(qa_chain, user_question)

        answer = result.get("answer", "No answer returned.")
        st.markdown(answer)

        # 3) show sources (optional)
        sources = result.get("sources", [])
        if show_sources and sources:
            with st.expander("📚 Sources used"):
                for i, doc in enumerate(sources[:top_k], 1):
                    page = doc.metadata.get("page", "N/A")
                    src = doc.metadata.get("source", "Unknown")
                    st.write(f"{i}. **{os.path.basename(src)}** — page **{page}**")
                    st.caption(doc.page_content[:300] + "…")

    # store assistant message (so it stays in history)
    st.session_state.messages.append({"role": "assistant", "content": answer})
