import os
import time
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

# MODERN 2026 RETRIEVAL PATHS (Requires langchain-classic)
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from config import (
    DOCS_DIR, VECTOR_DB_DIR, CHUNK_SIZE, CHUNK_OVERLAP, 
    NUM_RETRIEVED_DOCS, TEMPERATURE, MODEL_NAME, GOOGLE_API_KEY
)

def load_documents(directory):
    """
    Load all PDF files from a dicectory. and returns a list of LngChain Document objects(one per page).

    Args:
        directory: Path to directory containing PDF files.
    
    Returns:
        List of loaded documents
    """
    if not os.path.exists(directory):
        print(f"Error: Folder {directory} does not exist.")
        return []
    
    print(f"Scanning directory: {directory}...")

    loader = DirectoryLoader(
        directory,
        glob="*.pdf",  #glob="*.pdf" or glob="**/*.pdf"
        loader_cls=PyPDFLoader,
        show_progress=True
    )

    try:
        documents = loader.load()

        if not documents:
            print(f"Warning: No PDF content found in '{directory}'.")
        else:
            print(f"Successfully loaded {len(documents)} pages from your folder.")
            
        return documents
    except Exception as e:
        print(f"Critical Error during loading: {str(e)}")
        return []
    
"""
!!!! Testing the load_documents function !!!!

if __name__ == "__main__":
    docs = load_documents(DOCS_DIR) 
    
    if docs:
        print(f"Success! Total pages loaded: {len(docs)}")
        #Print the first few words of the first page to be sure
        print(f"Sample text from first page: {docs[0].page_content[:100]}...")
    else:
        print("Failed to load any documents. Check your 'documents' folder!")

"""

def split_documents(documents):
    """
    Splits the loaded pages/document objects into smaller pieces for AI to process.

    Args: 
        documents: List of document objects
    
    Returns:
        List of document chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP,
        length_function = len,
        add_start_index = True #Remembers where in the PDF the chunk is
    )

    #Perform the splitting
    chunks = text_splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")
    print(f"Average chunk size: {CHUNK_SIZE} characters")
    
    return chunks
"""
if __name__ == "__main__":
    # 1. Load the documents first
    docs = load_documents(DOCS_DIR)
    
    # 2. Check if loading worked, then split them
    if docs:
        chunks = split_documents(docs)
        # The result 'chunks' now contains your 1,000-character slices

"""

 

def create_vector_store(chunks):
    """
    Safe-speed vector store creation for Google AI Studio Free Tier
    """
    print(f"\nBuilding knowledge base from {len(chunks)} chunks...")

    embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY
)

    batch_size = 1
    vectorstore = None

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        print(f"Processing chunks {i} → {min(i + batch_size, len(chunks))}")

        retries = 0
        while retries < 15:
            try:
                if vectorstore is None:
                    vectorstore = Chroma.from_documents(
                        documents=batch,
                        embedding=embeddings,
                        persist_directory=VECTOR_DB_DIR
                    )
                else:
                    vectorstore.add_documents(batch)

                # Sleep ONLY if there are more batches left
                if i + batch_size < len(chunks):
                    time.sleep(12)

                break  # success → exit retry loop

            except Exception as e:
                retries += 1
                print(f"Error from Google: {e}")
                print(f"Cooling down 180s (attempt {retries}/15)")
                time.sleep(180)

        else:
            raise RuntimeError("Failed to embed batch after 15 retries")

    print(f"Knowledge base built and saved in '{VECTOR_DB_DIR}'")
    return vectorstore

"""
if __name__ == "__main__":
    # Step 6.1: Load
    docs = load_documents(DOCS_DIR)
    
    if docs:
        # Step 7: Split
        chunks = split_documents(docs)
        
        # Step 8.1: Create Vector Store
        vector_db = create_vector_store(chunks)
        
        # FINAL VERIFICATION
        if vector_db:
            print(
                f"The database now contains "
                f"{vector_db._collection.count()} searchable chunks."
            )
"""

def load_vector_store():
    """
    Load existing Chroma vector database from disk if it exists.

    Returns:
        Chroma object or None
    """
    # Check if folder exists and is not empty
    if os.path.exists(VECTOR_DB_DIR) and os.listdir(VECTOR_DB_DIR):
        print(f"Loading existing vector database from '{VECTOR_DB_DIR}'...")

        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=GOOGLE_API_KEY
        )

        vectorstore = Chroma(
            persist_directory=VECTOR_DB_DIR,
            embedding_function=embeddings
        )

        print("Vector database loaded successfully.")
        return vectorstore

    print("No existing vector database found.")
    return None

"""
if __name__ == "__main__":
    vector_db = load_vector_store()

    if vector_db is None:
        docs = load_documents(DOCS_DIR)

        if docs:
            chunks = split_documents(docs)
            vector_db = create_vector_store(chunks)

    if vector_db:
        print(f" The database now contains {vector_db._collection.count()} searchable chunks.")
"""
def create_qa_chain(vectorstore):
    """
    Create a retrieval + Gemini answering chain.
    """
    print("\n Setting up Q&A chain (Gemini)...")

    # Create the Gemini chat model (this generates the final answer)
    llm = ChatGoogleGenerativeAI(
        model=MODEL_NAME,              # e.g. "gemini-1.5-flash" or your chosen model
        temperature=TEMPERATURE,
        google_api_key=GOOGLE_API_KEY
    )

    # Create a prompt template (instructions to Gemini)
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are an agricultural assistant. Answer ONLY using the context.\n"
         "If the answer is not in the context, say: 'I don't know based on the documents.'\n"
         "Keep the answer concise and practical."),
        ("human",
         "Question: {input}\n\n"
         "Context:\n{context}")
    ])

    # This chain tells Gemini how to combine retrieved docs into the prompt
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)

    # 4) Retriever: this searches your Chroma vector DB for top-k chunks
    retriever = vectorstore.as_retriever(search_kwargs={"k": NUM_RETRIEVED_DOCS})

    # Final chain = retrieval + generation
    qa_chain = create_retrieval_chain(retriever, combine_docs_chain)

    print("✅ Q&A chain ready")
    return qa_chain

def ask_question(qa_chain, question):
    """
    Ask a question using the Gemini Q&A chain.

    Returns:
        {
            "answer": str,
            "sources": list[Document]
        }
    """
    print(f"\n❓ Question: {question}")
    print("🔍 Searching documents...")

    try:
        # Run RAG pipeline
        result = qa_chain.invoke({"input": question})

        # 1️⃣ Get answer text (chain-dependent)
        answer = result.get("answer") or result.get("output_text")

        # 2️⃣ Get retrieved documents (VERY IMPORTANT)
        sources = result.get("context", [])

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        return {
            "answer": f"❌ Error: {str(e)}",
            "sources": []
        }

def main():
    print("=" * 60)
    print("🌾 Agri Crop Management Q&A (Gemini + RAG)")
    print("=" * 60)

    # 1) Load existing vector DB (FAST)
    vectorstore = load_vector_store()

    # 2) If not found, build it once (SLOW)
    if vectorstore is None:
        print(" No existing DB found. Building a new one...")

        docs = load_documents(DOCS_DIR)
        if not docs:
            print(" No PDFs found. Put PDF files inside the 'documents' folder.")
            return

        chunks = split_documents(docs)
        vectorstore = create_vector_store(chunks)

    print(f"DB Ready. Stored chunks: {vectorstore._collection.count()}")

    # 3) Create QA chain (Retriever + Gemini)
    qa_chain = create_qa_chain(vectorstore)

    print("\n" + "=" * 60)
    print("System ready! Type your question (type 'quit' to exit)")
    print("=" * 60)

    # 4) Question loop
    while True:
        question = input("\n👤 Your question: ").strip()

        if question.lower() in ["quit", "exit", "q"]:
            print("👋 Goodbye!")
            break

        if not question:
            print("⚠️ Please type a question.")
            continue

        # Ask (we'll use your ask_question function)
        result = ask_question(qa_chain, question)

        print("\n" + "-" * 60)
        print("🤖 Answer:")
        print("-" * 60)
        print(result["answer"])

if __name__ == "__main__":
    main()
