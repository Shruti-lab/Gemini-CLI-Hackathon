# 📊 Excel AI Version Control System (PS2)

## 🧠 Problem Statement

Across L&D initiatives, teams maintain weekly Excel trackers that are manually updated, leading to:

* Multiple conflicting versions
* No audit trail of changes
* Time-consuming manual comparisons
* Lack of insights and trends
* Slow decision-making

---

###Note:- Right now we are already in the "Gemini-CLI-Hackathon" directory. 
 
## 🎯 Objective

Build a system that:

* Tracks Excel versions
* Compares versions automatically
* Generates insights using AI
* Supports natural language queries
There should be docker-compose.yml file created to run to build, start and run the services.

---

## ⚙️ Core Features

### 1. File Upload & Versioning

* Upload Excel files
* Automatically assign version IDs (v1, v2, v3...)
* Store metadata (timestamp, file path)

---

### 2. Excel Parsing Engine

* Read Excel files using Python
* Convert data into structured format (JSON)

---

### 3. Diff Engine (CORE)

Compare two Excel versions and detect:

* Added rows
* Removed rows
* Modified values

Output:

```
{
  "added": [],
  "removed": [],
  "modified": []
}
```

---

### 4. Time Travel Comparison

* Compare any two versions (v1 vs v5, etc.)

---

### 5. AI Insights Engine

Use Gemini CLI/ Gemini since I have the Gemini API key to:

* Summarize changes
* Detect trends
* Highlight anomalies

---

### 6. Natural Language Query

Allow queries like:

* "What changed last week?"
* "Which entries were modified?"

---

## 🧠 AI Integration

Use Gemini CLI or Gemini with API key for:

* Insights generation
* Summarization
* Question answering

Example:

```
gemini -f diff.json "Analyze these changes and provide insights"
```

---

## 🏗️ Tech Stack

* Backend: Python (FastAPI)
* Excel Processing: pandas, openpyxl
* Storage: Local filesystem or S3
* AI: Gemini CLI

---

## 📁 Project Structure

```
Gemini-CLI-Hackathon/
│
├── backend/
│   ├── main.py
│   ├── routes/
│   │   ├── upload.py
│   │   ├── compare.py
│   │   ├── ask.py
│   │
│   ├── services/
│   │   ├── parser.py
│   │   ├── diff_engine.py
│   │   ├── gemini_cli.py
│   │
│   ├── storage/
│   │   ├── files/
│   │   ├── metadata.json
│
├── cli.py
├── prompts/
│   ├── insights.txt
│
└── requirements.txt
```

---

## 🔄 Workflow

1. User uploads Excel file
2. System assigns version
3. User selects two versions to compare
4. System generates diff
5. Diff is passed to Gemini CLI
6. Gemini returns insights
7. User can ask questions

---

## 🔌 API Endpoints

### Health check endpoint returns 200 when service is ready
```
GET /health
```

### Upload File

```
POST /upload
```

### Compare Versions

```
GET /compare?v1=v1&v2=v2
```

### Get AI Insights

```
POST /ask
```

---

## 💻 CLI Commands

```
python cli.py upload file.xlsx
python cli.py compare v1 v2
python cli.py insights v1 v2
```

---

## 🎯 Expected Output

* Structured diff between versions
* AI-generated insights
* Natural language answers

---

## 🚀 Future Enhancements (Optional)

* Formula comparison
* Multi-sheet support
* Dashboard UI like python endpoint that shows versioning
* Alerts for major changes
* Full agentic workflow

---

## 🏁 Goal

Build a "Git-like system for Excel with AI-powered insights" using Gemini CLI.
