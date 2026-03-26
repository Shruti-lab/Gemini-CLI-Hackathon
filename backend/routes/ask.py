from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import json
from backend.services.parser import parse_excel
from backend.services.diff_engine import compare_versions
from backend.services.gemini_cli import generate_insights, ask_question

router = APIRouter()

METADATA_PATH = "backend/storage/metadata.json"

from typing import Optional

class AskRequest(BaseModel):
    v1: str
    v2: str
    question: Optional[str] = None

def load_metadata():
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r") as f:
            return json.load(f)
    return {}

@router.post("/ask")
async def get_insights(request: AskRequest):
    metadata = load_metadata()
    
    if request.v1 not in metadata:
        raise HTTPException(status_code=404, detail=f"Version {request.v1} not found.")
    if request.v2 not in metadata:
        raise HTTPException(status_code=404, detail=f"Version {request.v2} not found.")
        
    file1_path = metadata[request.v1]["file_path"]
    file2_path = metadata[request.v2]["file_path"]
    
    data1 = parse_excel(file1_path)
    data2 = parse_excel(file2_path)
    
    if data1 is None or data2 is None:
        raise HTTPException(status_code=500, detail="Error parsing Excel files.")
        
    diff = compare_versions(data1, data2)
    
    if request.question:
        answer = ask_question(diff, request.question)
    else:
        answer = generate_insights(diff)
        
    return {
        "v1": request.v1,
        "v2": request.v2,
        "question": request.question or "Summarize changes",
        "answer": answer
    }
