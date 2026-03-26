from fastapi import APIRouter, HTTPException, Query
import os
import json
from backend.services.parser import parse_excel
from backend.services.diff_engine import compare_versions

router = APIRouter()

METADATA_PATH = "backend/storage/metadata.json"

def load_metadata():
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r") as f:
            return json.load(f)
    return {}

@router.get("/compare")
async def compare_v(v1: str = Query(...), v2: str = Query(...)):
    metadata = load_metadata()
    
    if v1 not in metadata:
        raise HTTPException(status_code=404, detail=f"Version {v1} not found.")
    if v2 not in metadata:
        raise HTTPException(status_code=404, detail=f"Version {v2} not found.")
    
    file1_path = metadata[v1]["file_path"]
    file2_path = metadata[v2]["file_path"]
    
    data1 = parse_excel(file1_path)
    data2 = parse_excel(file2_path)
    
    if data1 is None or data2 is None:
        raise HTTPException(status_code=500, detail="Error parsing one or both Excel files.")
        
    diff = compare_versions(data1, data2)
    
    return {
        "v1": v1,
        "v2": v2,
        "diff": diff
    }
