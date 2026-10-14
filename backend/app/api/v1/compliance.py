from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.compliance.ccpa_library import get_all_guidelines, get_guideline_by_code
from app.database.models import ComplianceGuideline

router = APIRouter()

@router.get("/compliance/guidelines")
def list_guidelines():
    return get_all_guidelines()

@router.get("/compliance/guidelines/{category}")
def get_guideline_detail(category: str):
    guide = get_guideline_by_code(category)
    if not guide:
        raise HTTPException(status_code=404, detail=f"Compliance category '{category}' not found in CCPA 2023 Guidelines library.")
    return guide
