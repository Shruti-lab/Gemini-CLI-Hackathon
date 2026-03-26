# 📊 Excel AI Version Control System

A "Git-like" version control system for Excel files with AI-powered insights. This system tracks changes between weekly Excel trackers, detects additions, removals, and modifications, and uses the Gemini CLI to generate natural language summaries and answer queries about the changes.

## 🚀 Features

*   **File Versioning:** Upload Excel files and automatically assign version IDs (v1, v2, v3...).
*   **Excel Parsing:** Converts unstructured Excel data into structured JSON for analysis.
*   **Smart Diff Engine:** Automatically detects added rows, removed rows, and modified cell values.
*   **Time Travel:** Compare any two versions (e.g., v1 vs v5).
*   **AI Insights:** Uses Gemini CLI to summarize changes, detect trends, and highlight anomalies.
*   **Natural Language Query:** Ask questions like "What changed last week?" or "Who got a promotion?"

---

## 🛠️ Tech Stack

*   **Backend:** Python (FastAPI)
*   **Excel Processing:** Pandas, Openpyxl
*   **AI Engine:** [Gemini CLI](https://github.com/google/gemini-cli)
*   **Containerization:** Docker & Docker Compose

---

## 📋 Prerequisites

*   Python 3.10+
*   Node.js (for Gemini CLI)
*   Docker & Docker Compose (optional)
*   A **Google API Key** for Gemini.

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Shruti-lab/Gemini-CLI-Hackathon
cd Gemini-CLI-Hackathon
```

### 2. Configure Environment
Create a `.env` file in the root directory:
```bash
GOOGLE_API_KEY=your_api_key_here
```

### 3. Run with Docker (Recommended)
The easiest way to get started is using Docker Compose:
```bash
docker-compose up --build
```
The API will be available at `http://localhost:8000`.

### 4. Local Setup (Manual)
If you prefer to run locally without Docker:

**Install Gemini CLI:**
```bash
npm install -g @google/gemini-cli
```

**Install Python Dependencies:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

**Run the Backend:**
```bash
export GOOGLE_API_KEY=your_api_key_here
uvicorn backend.main:app --reload
```

---

## 💻 CLI Usage Guide

The `cli.py` script allows you to interact with the system directly from your terminal.

### 1. Upload a File
Upload an Excel file to create a new version:
```bash
python cli.py upload path/to/your/tracker_v1.xlsx
python cli.py upload path/to/your/tracker_v2.xlsx
```

### 2. Compare Versions
Generate a structured JSON diff between two versions:
```bash
python cli.py compare v1 v2
```

### 3. Get AI Insights
Generate a summary of what changed between versions:
```bash
python cli.py insights v1 v2
```

### 4. Natural Language Queries
Ask specific questions about the data changes:
```bash
python cli.py insights v1 v2 --question "Which entries were modified?"
python cli.py insights v1 v2 -q "Who received a salary hike?"
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/health` | Check if the service is ready |
| `POST` | `/upload` | Upload an Excel file |
| `GET`  | `/compare`| Get diff between two versions |
| `POST` | `/ask`    | Get AI insights or ask a question |

---

## 📂 Project Structure

```text
Gemini-CLI-Hackathon/
├── backend/
│   ├── main.py          # FastAPI Entry point
│   ├── routes/          # API Endpoints (upload, compare, ask)
│   ├── services/        # Logic (parser, diff engine, gemini_cli)
│   └── storage/         # Local file & metadata storage
├── cli.py               # Command Line Interface
├── Dockerfile           # Backend container definition
├── docker-compose.yml   # Multi-container orchestration
└── requirements.txt     # Python dependencies
```

---

## 🏁 Validation & Testing

To verify the installation, you can run the health check:
```bash
curl http://localhost:8000/health
```

Expected Output:
```json
{"status": "ok", "message": "Excel AI VCS is ready"}
```
