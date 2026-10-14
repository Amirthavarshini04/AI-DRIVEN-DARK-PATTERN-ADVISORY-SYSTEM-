import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.seed import init_and_seed_db

from app.api.v1 import health, scans, findings, compliance, remediation, analytics, reports

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Driven Dark Pattern Detection and Legal Compliance Advisory System for Indian E-Commerce Platforms under CCPA Guidelines 2023."
)

# Enable CORS for Next.js frontend and Chrome Extension origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seed database on startup
@app.on_event("startup")
def on_startup():
    init_and_seed_db()

# Include Routers under /api/v1
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["Health"])
app.include_router(scans.router, prefix=settings.API_V1_STR, tags=["Scans"])
app.include_router(findings.router, prefix=settings.API_V1_STR, tags=["Findings"])
app.include_router(compliance.router, prefix=settings.API_V1_STR, tags=["Compliance"])
app.include_router(remediation.router, prefix=settings.API_V1_STR, tags=["Remediation"])
app.include_router(analytics.router, prefix=settings.API_V1_STR, tags=["Analytics"])
app.include_router(reports.router, prefix=settings.API_V1_STR, tags=["Reports"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
