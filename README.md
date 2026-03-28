---

# 🚀 Multi-Agent Ticket Resolver Support System with Escalation

AI Agents Assist is an intelligent IT ticket resolution system powered by **local LLMs (Ollama)**, **FAISS-based vector search**, and **multi-agent orchestration (AutoGen)**. It provides instant solutions to IT issues and escalates unresolved tickets via email.

---

## ⚠️ Acknowledgements

This project is based on and inspired by the open-source repository:

* [Intelligent-It-Ticket-Resolver-Multiagent-Project](https://github.com/Sandesh-hase/Intelligent-It-Ticket-Resolver-Multiagent-Project) by Sandesh Hase

Licensed under the MIT License.

### 🔧 Key Enhancements & Modifications

* Replaced **Azure AI Search** with **FAISS (local vector search)**
* Replaced **Azure OpenAI** with **Ollama (local LLM inference)**
* Migrated UI from **Streamlit → Gradio**
* Switched dependency management from **pip → uv**
* Refactored agent orchestration and retrieval pipeline
* Enabled **fully offline AI capability (except email)**

---

## ⚡ Key Highlights

* 🧠 Fully local AI stack (no Azure dependency)
* ⚡ Fast semantic search using FAISS
* 🤖 Multi-agent collaboration (AutoGen)
* 📧 Automated escalation via email
* 🌐 Interactive Gradio UI with feedback loop

---

## ✨ Features

* **Natural Language IT Support**
* **Automated Ticket Classification**
* **Semantic Knowledge Retrieval (FAISS + embeddings)**
* **Escalation Workflow with ticket generation**
* **User Feedback Loop (resolve / escalate)**

---

## 🏗️ Project Structure

```bash
.
├── app.py                       # Gradio UI
├── group_chat.py               # Agent orchestration
├── agents/
│   ├── classifier_agent.py
│   ├── knowledge_base_agent.py
│   └── notification_agent.py
├── tools/
│   ├── knowledge_base_tool.py  # FAISS-based retrieval
│   └── send_email.py           # Email escalation
├── utility/
│   ├── llm_config.py           # Ollama config
│   └── prompt.py
├── data/
│   └── knowledge_base.json
├── .env
└── README.md
```

---

## ⚙️ Tech Stack

* **LLM:** Ollama (`llama3:8b`)
* **Framework:** AutoGen
* **Vector Search:** FAISS
* **Embeddings:** Sentence Transformers
* **UI:** Gradio

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
OLLAMA_MODEL=llama3:8b

EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

---

### 4️⃣ Start Ollama

```bash
ollama serve
ollama pull llama3:8b
```

---

### 5️⃣ Run the app

```bash
uv run app.py
```

---

### 6️⃣ Open browser

```
http://127.0.0.1:7860
```

---

## 🔄 How It Works

1. User submits IT issue
2. Classifier Agent categorizes issue
3. Knowledge Base Agent retrieves solutions using FAISS
4. User provides feedback

   * ✅ Resolved → Done
   * ❌ Not resolved → Escalation
5. Notification Agent sends email with ticket

---

## 🧠 Architecture Flow

```
User Input
   ↓
Classifier Agent
   ↓
Knowledge Base Agent
   ↓
FAISS (Local Vector Search)
   ↓
Solution OR Escalation
   ↓
Email Notification
```

---

## 📧 Email Setup

* Use Gmail App Password (not normal password)
* Enable 2FA before generating it

---

## 🔧 Customization

* Update knowledge base → [`data/knowledge_base.json`](data/knowledge_base.json)
* Modify prompts → [`utility/prompt.py`](utility/prompt.py)
* Change model → `.env`

---

## 📄 License

This project is licensed under the MIT License.

It includes modifications based on prior MIT-licensed work.
See the [`LICENSE`](LICENSE) file for full details.

---


