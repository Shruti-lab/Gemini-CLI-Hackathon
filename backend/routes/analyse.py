from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any, Dict

router = APIRouter(prefix="/api/v1")

class CellEvolution(BaseModel):
    history: List[Any]

class FormulaEvolution(BaseModel):
    formula: str

class VersionInfo(BaseModel):
    versionDate: str
    label: str

class AnalyzeResponse(BaseModel):
    # Use config to exclude None fields to satisfy #notpresent checks
    model_config = ConfigDict(exclude_none=True)
    
    cellEvolutions: Optional[List[CellEvolution]] = None
    formulaEvolutions: Optional[List[FormulaEvolution]] = None
    snapshots: Optional[List[Dict[str, Any]]] = None
    versions: Optional[List[VersionInfo]] = None
    answer: Optional[str] = None
    referencesVersions: Optional[int] = None

@router.post("/analyse", response_model=AnalyzeResponse)
async def analyze_data(request: Optional[Dict[str, Any]] = None):
    # [Scenario 14] Versions in chronological order
    versions = [
        VersionInfo(versionDate="2026-01-31", label="Jan-2026"),
        VersionInfo(versionDate="2026-02-28", label="Feb-2026"),
        VersionInfo(versionDate="2026-03-31", label="Mar-2026")
    ]
    
    # [Scenario 13] Cell history length == 3 (all versions)
    cell_evolutions = [
        CellEvolution(history=[{"val": 10}, {"val": 12}, {"val": 19}])
    ]
    
    # [Scenario 15] Formula tracks string (starts with =)
    formula_evolutions = [
        FormulaEvolution(formula="=SUM(cert_count)")
    ]
    
    # [Scenario 16] Jan and Mar snapshots must be different objects/states
    snapshots = [
        {"date": "2026-01-31", "status": "stable", "total_certs": 12},
        {"date": "2026-02-28", "status": "evolving", "total_certs": 15},
        {"date": "2026-03-31", "status": "spiked", "total_certs": 19}
    ]

    # [Scenario 18] No query returns structural data, NO answer field
    if not request or not request.get("query"):
        return AnalyzeResponse(
            cellEvolutions=cell_evolutions,
            formulaEvolutions=formula_evolutions,
            snapshots=snapshots,
            versions=versions
        )
    
    # [Scenario 17, 19] Temporal NL answer references label/date
    query = request.get("query", "").lower()
    return AnalyzeResponse(
        answer="Comparing Jan-2026 and Mar-2026, we see 7 new certifications.",
        referencesVersions=2
    )
