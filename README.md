
---

# 🚀 Multi-Agent IT Ticket Resolver with RAG & Escalation

An intelligent IT support system that combines **AutoGen multi-agent orchestration**, **FAISS-based semantic retrieval**, and **automated ticket escalation**.
The system resolves user issues instantly and escalates unresolved cases with **generated ticket IDs via email**.

---

## ⚠️ Acknowledgements

This project is based on and inspired by:

* [Intelligent-It-Ticket-Resolver-Multiagent-Project](https://github.com/Sandesh-hase/Intelligent-It-Ticket-Resolver-Multiagent-Project) by Sandesh Hase

Licensed under the MIT License.

---

## 🔧 Key Enhancements & Modifications

* 🔄 Replaced **Azure AI Search → FAISS (local vector DB)**
* 🤖 Replaced **Azure OpenAI → Ollama (local LLM)**
* 🎨 Migrated UI from **Streamlit → Gradio**
* ⚡ Switched dependency management from **pip → uv**
* 🧠 Implemented **Hybrid AutoGen + Deterministic RAG architecture**
* 📴 Enabled **fully local AI pipeline (except SMTP email)**

---

## ⚡ Key Highlights

* 🧠 Local LLM inference (Ollama — no cloud dependency)
* 🔍 Semantic search using FAISS + embeddings
* 🤖 Multi-agent system (AutoGen)
* 🎯 Deterministic RAG (guaranteed retrieval)
* 📧 Ticket-based escalation workflow
* 🌐 Interactive Gradio UI

---

## ✨ Features

* Natural language IT issue resolution
* Automatic ticket classification
* Semantic retrieval from knowledge base
* Top-1 solution extraction (clean output)
* Ticket ID generation for unresolved issues
* Email escalation to IT support
* User feedback loop (Resolved / Not Resolved)

---

## 🏗️ Project Structure

```bash
.
├── app.py                       # Gradio UI + pipeline controller
├── group_chat.py               # AutoGen multi-agent orchestration
├── agents/
│   ├── classifier_agent.py
│   ├── knowledge_base_agent.py
│   └── notification_agent.py
├── tools/
│   ├── knowledge_base_tool.py  # FAISS semantic retrieval
│   └── send_email.py           # Ticket + email escalation
├── utility/
│   ├── llm_config.py           # Ollama configuration
│   └── prompt.py
├── data/
│   └── knowledge_base.json     # IT knowledge base
├── .env
└── README.md
```

---

## ⚙️ Tech Stack

* **LLM:** Ollama (`llama3.2`)
* **Framework:** AutoGen
* **Vector Search:** FAISS
* **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)
* **UI:** Gradio
* **Email:** SMTP (Gmail App Password)

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

---

### 2️⃣ Install dependencies

```bash
uv sync
```

---

### 3️⃣ Configure `.env`

```env
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3.2

EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

ESCALATION_EMAIL=it_support@company.com
```

---

### 4️⃣ Start Ollama

```bash
ollama run llama3.2
```

---

### 5️⃣ Run the app

```bash
uv run app.py
```

---

### 6️⃣ Open in browser

```
http://127.0.0.1:7860
```

---

## 🔄 How It Works (Updated Logic)

1. User submits IT issue

2. **Classifier Agent (AutoGen)** categorizes the issue

3. **Knowledge Base Agent triggers FAISS retrieval**

4. System extracts the **best matching solution (top-1)**

5. User provides feedback:

   * ✅ Resolved → Process ends
   * ❌ Not resolved → Escalation triggered

6. **Ticket ID is generated**

7. **Email sent to IT support (ESCALATION_EMAIL)**

---

## 🧠 Architecture Flow (Actual Implementation)

```text
User Input
   ↓
Classifier Agent (AutoGen)
   ↓
Knowledge Base Agent (Tool Call)
   ↓
FAISS Semantic Search
   ↓
Tool Response (Solution)
   ↓
App Layer (Extract + Display)
   ↓
User Feedback
   ↓
Escalation (Ticket + Email)
```

---

## ⚠️ Important Design Note

This project uses a **Hybrid Architecture**:

* AutoGen → agent reasoning & tool invocation
* Code layer → deterministic output handling

👉 This ensures:

* ✅ No hallucination in RAG
* ✅ Guaranteed retrieval
* ✅ Stable UI behavior

---

## 📧 Email & Ticket System

* Emails are sent to **ESCALATION_EMAIL (IT support)**
* Each escalation generates a unique ticket:

```text
TKT-YYYYMMDD-XXXXXX
```

Example:

```text
TKT-20260329-A1B2C3
```

---

## 🔧 Customization

* Modify knowledge base → [`data/knowledge_base.json`](data/knowledge_base.json)
* Change LLM model → `.env`
* Update prompts → [`utility/prompt.py`](utility/prompt.py)
* Adjust retrieval logic → [`knowledge_base_tool.py`](`knowledge_base_tool.py`)

---

## 📄 License

This project is licensed under the MIT License.

It includes modifications based on prior MIT-licensed work.
See the [`LICENSE`](LICENSE) file for full details.

---
