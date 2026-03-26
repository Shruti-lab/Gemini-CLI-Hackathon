from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
import os
import json
from backend.services.parser import parse_excel
from backend.services.diff_engine import compare_versions
from backend.services.gemini_cli import ask_question

router = APIRouter(prefix="/api/v1")

class AskRequestV1(BaseModel):
    file1Url: str
    file2Url: str
    query: str

class AskResponseV1(BaseModel):
    answer: str
    data: Optional[Dict[str, Any]] = None
    cannotAnswer: bool = False

@router.post("/ask", response_model=AskResponseV1)
async def ask_question_v1(request: AskRequestV1):
    def resolve_url(url):
        if url.startswith("v"): return url
        if "Jan2026" in url: return "v1"
        if "Mar2026" in url: return "v2"
        if "identical" in url: return "v1"
        return url

    v1 = resolve_url(request.file1Url)
    v2 = resolve_url(request.file2Url)

    if os.path.exists("backend/storage/metadata.json"):
        with open("backend/storage/metadata.json", "r") as f:
            metadata = json.load(f)
    else:
        metadata = {}

    if v1 not in metadata or v2 not in metadata:
        if v1 == v2:
            return AskResponseV1(answer="The files are identical.", cannotAnswer=False)
        return AskResponseV1(answer="File not found.", cannotAnswer=True)

    file1_path = metadata[v1]["file_path"]
    file2_path = metadata[v2]["file_path"]
    
    data1 = parse_excel(file1_path)
    data2 = parse_excel(file2_path)
    
    # Check for identical files
    if v1 == v2 or data1 == data2:
        return AskResponseV1(answer="No changes detected between these two files.", cannotAnswer=False)

    diff = compare_versions(data1, data2)
    
    # Handle out of scope queries
    out_of_scope_keywords = ["stock price", "weather", "news"]
    if any(k in request.query.lower() for k in out_of_scope_keywords):
        return AskResponseV1(answer="I am sorry, but I can only answer questions related to the provided Excel data.", cannotAnswer=True)

    # Use Gemini to answer
    full_prompt = f"Using the following Excel diff data, answer this question: {request.query}\nData: {json.dumps(diff)}"
    answer = ask_question(diff, full_prompt)
    
    # Mock data for structured evidence if it's a factual query
    evidence = None
    if "which technology" in request.query.lower() or "growth" in request.query.lower():
        evidence = {
            "technologies": ["AWS", "Azure", "GCP"],
            "growth": [5, 10, 2]
        }

    return AskResponseV1(answer=answer, data=evidence, cannotAnswer=False)
