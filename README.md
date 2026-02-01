<h1 align="center">🌾 Agri Crop Management Q&A System</h1>
<h3 align="center">RAG + Google Gemini + ChromaDB</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue"/>
  <img src="https://img.shields.io/badge/RAG-Enabled-success"/>
  <img src="https://img.shields.io/badge/LLM-Google%20Gemini-orange"/>
  <img src="https://img.shields.io/badge/VectorDB-ChromaDB-purple"/>
  <img src="https://img.shields.io/badge/LangChain-Orchestration-yellow"/>
</p>

<p align="center">
  <b>
    An intelligent, document-grounded Question Answering system for agriculture
  </b>
  <br/>
  Built using Retrieval-Augmented Generation (RAG) to answer crop-management questions from real PDFs.
</p>

<hr/>

<h2 align="center">📌 Project Overview</h2>

<p align="center">
This project is a <b>domain-specific Question Answering system</b> designed for agricultural crop management.
</p>

<p align="center">
Instead of relying on generic internet knowledge, the system retrieves information from
<b>agriculture-specific documents</b> and generates answers grounded in those documents.
</p>

<ul>
  <li>📄 Ingests agricultural PDFs</li>
  <li>✂️ Splits documents into semantic chunks</li>
  <li>🔢 Converts text into vector embeddings</li>
  <li>🔍 Retrieves only the most relevant chunks</li>
  <li>🤖 Uses Google Gemini to generate grounded answers</li>
</ul>

<hr/>

<h2 align="center">🧠 System Architecture (RAG)</h2>

<p align="center">
User Question → Embedding (Gemini) → Vector Search (ChromaDB) → Relevant Chunks → Gemini LLM → Final Answer
</p>

<pre align="center">
User Question
      ↓
Question Embedding (Gemini)
      ↓
Vector Search (ChromaDB)
      ↓
Top-K Relevant Chunks
      ↓
Gemini LLM
      ↓
Final Answer (Grounded in Documents)
</pre>

<hr/>

<h2 align="center">✨ Key Features</h2>

<ul>
  <li>✅ Document-based answers (no hallucinations)</li>
  <li>✅ Uses Google Gemini as the LLM</li>
  <li>✅ Persistent vector database (no re-embedding every run)</li>
  <li>✅ CLI-based interactive chat</li>
  <li>✅ PDF ingestion support</li>
  <li>✅ Modular and clean Python codebase</li>
  <li>✅ Easily extendable to Web UI (Streamlit / FastAPI)</li>
</ul>

<hr/>



## 📁 Project Structure

A clean and modular structure designed for clarity, scalability, and real-world RAG workflows.
```text

agri-crop-RAG/
│
├── documents/                 # Domain-specific agricultural PDFs
├── agri_db/                   # Persistent Chroma vector database
├── venv/                      # Python virtual environment (ignored by Git)
│
├── main.py                    # CLI entry point (Q&A system)
├── app.py                     # Streamlit UI (ChatGPT-like interface)
├── config.py                  # Central configuration (models, paths, params)
├── list_models.py             # Utility to list available Gemini models
│
├── requirements.txt           # Python dependencies
├── .env                       # API keys & secrets (ignored by Git)
├── .gitignore                 # Files excluded from version control
├── LICENSE                    # MIT License
└── README.md                  # Project documentation

```

<hr/>


<h2 align="center">🧪 Example Questions</h2>

<ul>
  <li>What are the soil requirements for chickpea?</li>
  <li>Which fertilizers are recommended for green gram?</li>
  <li>Why are saline soils unsuitable for pulses?</li>
  <li>How do pests affect crop yield?</li>
  <li>What is Integrated Pest Management (IPM)?</li>
</ul>

<hr/>

<h2 align="center">🖥️ Example Output</h2>


Question: What are the soil requirements for chickpea?

Answer:
Well-drained sandy loam or silt loam soils with a pH of 6–8 are ideal.
Saline soils are not suitable.

<hr/> <h2 align="center">🛠️ Tech Stack</h2> <table align="center"> <tr> <th>Technology</th> <th>Purpose</th> </tr> <tr> <td>🐍 Python</td> <td>Main programming language</td> </tr> <tr> <td>🔗 LangChain</td> <td>RAG orchestration</td> </tr> <tr> <td>🤖 Google Gemini</td> <td>LLM + Embeddings</td> </tr> <tr> <td>📦 ChromaDB</td> <td>Vector database</td> </tr> <tr> <td>📄 PyPDFLoader</td> <td>PDF ingestion</td> </tr> <tr> <td>🔐 dotenv</td> <td>Environment variable management</td> </tr> <tr> <td>🗂 Git & GitHub</td> <td>Version control</td> </tr> </table> <hr/> <h2 align="center">🚀 Getting Started</h2> <h3>1️⃣ Clone the Repository</h3>
git clone https://github.com/<your-username>/agri-crop-RAG.git
cd agri-crop-RAG

<h3>2️⃣ Create Virtual Environment</h3>
python -m venv venv


<b>Activate:</b>

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

<h3>3️⃣ Install Dependencies</h3>
pip install -r requirements.txt

<hr/> <h2 align="center">🛠️ Tech Stack</h2> <table align="center"> <tr> <th>Technology</th> <th>Purpose</th> </tr> <tr> <td>🐍 Python</td> <td>Main programming language</td> </tr> <tr> <td>🔗 LangChain</td> <td>RAG orchestration</td> </tr> <tr> <td>🤖 Google Gemini</td> <td>LLM + Embeddings</td> </tr> <tr> <td>📦 ChromaDB</td> <td>Vector database</td> </tr> <tr> <td>📄 PyPDFLoader</td> <td>PDF ingestion</td> </tr> <tr> <td>🔐 dotenv</td> <td>Environment variable management</td> </tr> <tr> <td>🗂 Git & GitHub</td> <td>Version control</td> </tr> </table> <hr/> <h2 align="center">🚀 Getting Started</h2> <h3>1️⃣ Clone the Repository</h3>
git clone https://github.com/<your-username>/agri-crop-RAG.git
cd agri-crop-RAG

<h3>2️⃣ Create Virtual Environment</h3>
python -m venv venv


<b>Activate:</b>

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

<h3>3️⃣ Install Dependencies</h3>
pip install -r requirements.txt

<hr/> <h2 align="center">🧠 Why RAG Instead of Fine-Tuning?</h2> <table align="center"> <tr> <th>RAG</th> <th>Fine-Tuning</th> </tr> <tr> <td>Uses documents directly</td> <td>Learns patterns only</td> </tr> <tr> <td>Easy to update knowledge</td> <td>Expensive to retrain</td> </tr> <tr> <td>Less hallucination</td> <td>Can still hallucinate</td> </tr> <tr> <td>Best for factual QA</td> <td>Best for tone/style</td> </tr> </table> <hr/> <h2 align="center">🔮 Future Enhancements</h2> <ul> <li>🌐 Streamlit Web UI (ChatGPT-like interface)</li> <li>📚 Source citations per answer</li> <li>📄 DOCX / TXT support</li> <li>☁️ Cloud deployment</li> <li>🔐 User authentication</li> </ul> <hr/> <h2 align="center">🧑‍💼 What This Project Demonstrates</h2> <ul> <li>✔ Understanding of LLMs & RAG</li> <li>✔ Practical use of embeddings & vector search</li> <li>✔ Clean project structure</li> <li>✔ API usage & rate-limit handling</li> <li>✔ Real-world ML system design</li> </ul> <hr/> <h2 align="center">📄 License</h2> <p align="center"> This project is licensed under the <b>MIT License</b>. </p> <hr/> <h2 align="center">🙏 Acknowledgements</h2> <p align="center"> Google Gemini • LangChain • ChromaDB </p> <p align="center"> ⭐ If you like this project, consider starring the repo! </p>
