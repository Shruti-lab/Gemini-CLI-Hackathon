from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import json
import shutil
from datetime import datetime

router = APIRouter()

METADATA_PATH = "backend/storage/metadata.json"
FILES_DIR = "backend/storage/files"

def load_metadata():
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r") as f:
            return json.load(f)
    return {}

def save_metadata(metadata):
    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=4)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Check if the file is an Excel file
    if not (file.filename.endswith(".xlsx") or file.filename.endswith(".xls")):
        raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls) are allowed.")
    
    metadata = load_metadata()
    
    # Generate version ID
    version_count = len(metadata)
    version_id = f"v{version_count + 1}"
    
    # Save the file
    file_path = os.path.join(FILES_DIR, f"{version_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update metadata
    entry = {
        "version_id": version_id,
        "original_filename": file.filename,
        "file_path": file_path,
        "timestamp": datetime.now().isoformat()
    }
    metadata[version_id] = entry
    save_metadata(metadata)
    
    return {"message": "File uploaded successfully", "version_id": version_id, "metadata": entry}
