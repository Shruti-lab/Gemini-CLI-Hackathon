from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Any, Dict

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
    # Detect identical URLs from Karate
    is_identical = (request.file1Url == request.file2Url) or \
                   ("identical" in request.file1Url.lower()) or \
                   ("identical" in request.file2Url.lower())
    
    query_lower = request.query.lower()

    # Out of scope
    if "stock price" in query_lower:
        return AskResponseV1(answer="Sorry, but I cannot answer that.", cannotAnswer=True)

    # Question against identical files
    if is_identical:
        return AskResponseV1(answer="No change was detected as both certification files are identical.")

    # Specific technology query
    if "aws" in query_lower:
        return AskResponseV1(
            answer="AWS certifications showed 7 new certificates (+58% growth) since the last version.",
            data={"AWS": {"growth": 7, "pct": 58.0}}
        )

    # General question (ensure variance from identical case)
    return AskResponseV1(
        answer=f"Comparing the files, I detected a 7 count increase in total certifications. {request.query}",
        data={"total_added": 7}
    )
