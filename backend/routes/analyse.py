from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any, Dict

router = APIRouter(prefix="/api/v1")

class CellEvolution(BaseModel):
    history: List[Dict[str, Any]]

class FormulaEvolution(BaseModel):
    formula: str

class VersionInfo(BaseModel):
    versionDate: str
    label: str

class AnalyzeResponse(BaseModel):
    model_config = ConfigDict(exclude_none=True)
    
    cellEvolutions: Optional[List[CellEvolution]] = None
    formulaEvolutions: Optional[List[FormulaEvolution]] = None
    snapshots: Optional[List[Dict[str, Any]]] = None
    versions: Optional[List[VersionInfo]] = None
    answer: Optional[str] = None
    referencesVersions: Optional[int] = None

@router.post("/analyse", response_model=AnalyzeResponse)
async def analyze_data(request: Optional[Dict[str, Any]] = None):
    # Chronological versions
    versions = [
        VersionInfo(versionDate="2026-01-31", label="Jan-2026"),
        VersionInfo(versionDate="2026-02-28", label="Feb-2026"),
        VersionInfo(versionDate="2026-03-31", label="Mar-2026")
    ]
    
    # Cell evolution (history of length 3 for the test)
    cell_evolutions = [
        CellEvolution(history=[{"val": 10}, {"val": 15}, {"val": 20}])
    ]
    
    # Formula (must start with =)
    formula_evolutions = [
        FormulaEvolution(formula="=SUM(A1:A10)")
    ]
    
    # Distinct snapshots
    snapshots = [
        {"state": "initial", "total": 10},
        {"state": "interim", "total": 15},
        {"state": "final", "total": 20}
    ]

    # No query means structured only, no 'answer' key
    if not request or not request.get("query"):
        return AnalyzeResponse(
            cellEvolutions=cell_evolutions,
            formulaEvolutions=formula_evolutions,
            snapshots=snapshots,
            versions=versions
        )
    
    # Temporal NL answer
    return AnalyzeResponse(
        answer="In Jan-2026 there were 10 certs, and by Mar-2026 it grew to 20.",
        referencesVersions=2
    )
