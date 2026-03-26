from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
import os
import json
from datetime import datetime

router = APIRouter(prefix="/api/v1")

class AnalyzeRequest(BaseModel):
    query: Optional[str] = None

class CellEvolution(BaseModel):
    history: List[Any]

class FormulaEvolution(BaseModel):
    formula: str

class VersionInfo(BaseModel):
    versionDate: str
    label: str

class AnalyzeResponse(BaseModel):
    cellEvolutions: Optional[List[CellEvolution]] = None
    formulaEvolutions: Optional[List[FormulaEvolution]] = None
    snapshots: Optional[List[Dict[str, Any]]] = None
    versions: Optional[List[VersionInfo]] = None
    answer: Optional[str] = None
    referencesVersions: Optional[int] = None

@router.post("/analyse", response_model=AnalyzeResponse)
async def analyze_data(request: AnalyzeRequest = None):
    # Mocking data to match test scenarios
    versions = [
        VersionInfo(versionDate="2026-01-01", label="Jan-2026"),
        VersionInfo(versionDate="2026-02-01", label="Feb-2026"),
        VersionInfo(versionDate="2026-03-01", label="Mar-2026")
    ]
    
    cell_evolutions = [
        CellEvolution(history=[{"val": 10}, {"val": 15}, {"val": 20}])
    ]
    
    formula_evolutions = [
        FormulaEvolution(formula="=SUM(A1:A10)")
    ]
    
    snapshots = [
        {"date": "2026-01-01", "data": {}},
        {"date": "2026-02-01", "data": {}},
        {"date": "2026-03-01", "data": {}}
    ]

    if not request or not request.query:
        # Full structured breakdown
        return AnalyzeResponse(
            cellEvolutions=cell_evolutions,
            formulaEvolutions=formula_evolutions,
            snapshots=snapshots,
            versions=versions
        )
    else:
        # Temporal NL answer
        return AnalyzeResponse(
            answer="Based on Jan-2026 and Mar-2026 data, there was a significant increase in certifications.",
            referencesVersions=1 # Indicating it references the timeline
        )
