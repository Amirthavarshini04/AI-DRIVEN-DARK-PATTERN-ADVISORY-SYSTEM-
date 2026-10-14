from fastapi import APIRouter
import datetime

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "system": "AI Dark Pattern & Compliance Advisory System",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
