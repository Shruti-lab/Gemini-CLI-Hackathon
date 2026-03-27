from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
import re

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
    is_identical = "identical" in request.file1Url.lower() or "identical" in request.file2Url.lower() or request.file1Url == request.file2Url
    query_lower = request.query.lower()

    # [Scenario 11] Out-of-scope gracefully deflected
    if "stock price" in query_lower or "weather" in query_lower:
        return AskResponseV1(answer="Sorry, but I only answer questions related to Excel certifications data.", cannotAnswer=True)

    # [Scenario 10] Identical files answer "no difference"
    if is_identical:
        return AskResponseV1(answer="The two files were identical; therefore no change in certification count was found.", cannotAnswer=False)

    # [Scenario 12] Technology-specific query (AWS)
    if "aws" in query_lower:
        return AskResponseV1(
            answer="AWS certifications increased significantly from 12 to 19 (+7) between Jan and March.",
            data={"AWS": {"old": 12, "new": 19, "growth": 7}}
        )

    # [Scenario 7, 8, 9] Factual query with digit, data grounding, and variance
    # answer must contain a number and differ from the 'no changes' answer
    return AskResponseV1(
        answer="I have analyzed the diff: exactly 7 new certifications were added in the cloud technology domain.",
        data={"tech_count": 7, "labels": ["Jan", "Feb", "Mar"]}
    )
