import datetime
import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class Scan(Base):
    __tablename__ = "scans"

    id = Column(String, primary_key=True, default=generate_uuid)
    url = Column(String, nullable=True)
    scan_type = Column(String, default="text") # "text" or "url"
    language = Column(String, default="auto") # "en", "hi", "ta", "auto"
    status = Column(String, default="completed") # "completed", "partially_scanned", "insufficient_content", "failed"
    risk_score = Column(Float, default=0.0) # 0 to 100
    risk_category = Column(String, default="Low Risk") # "Low Risk", "Moderate Risk", "High Risk", "Critical Risk"
    findings_count = Column(Integer, default=0)
    fetch_method = Column(String, default="http_client") # "browser_headless", "http_client", "text_input"
    content_length_analyzed = Column(Integer, default=0)
    page_title = Column(String, nullable=True)
    warnings = Column(JSON, default=list)
    raw_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    findings = relationship("Finding", back_populates="scan", cascade="all, delete-orphan")

class Finding(Base):
    __tablename__ = "findings"

    id = Column(String, primary_key=True, default=generate_uuid)
    scan_id = Column(String, ForeignKey("scans.id"), nullable=False)
    category = Column(String, nullable=False)
    severity = Column(String, default="Medium") # "Low", "Medium", "High", "Critical"
    confidence = Column(Float, default=0.85)
    text_snippet = Column(Text, nullable=False)
    dom_selector = Column(String, nullable=True)
    rationale = Column(Text, nullable=False)
    consumer_impact = Column(Text, nullable=False)
    ccpa_clause = Column(String, nullable=False)
    ccpa_category = Column(String, nullable=False)
    recommendation = Column(Text, nullable=False)
    is_reviewed = Column(Boolean, default=False)
    
    scan = relationship("Scan", back_populates="findings")
    remediations = relationship("RemediationAttempt", back_populates="finding", cascade="all, delete-orphan")
    feedback = relationship("UserFeedback", back_populates="finding", cascade="all, delete-orphan")

class ComplianceGuideline(Base):
    __tablename__ = "compliance_guidelines"

    id = Column(String, primary_key=True, default=generate_uuid)
    category_code = Column(String, unique=True, nullable=False)
    category_name = Column(String, nullable=False)
    clause_reference = Column(String, nullable=False)
    plain_explanation = Column(Text, nullable=False)
    problematic_examples = Column(JSON, nullable=False)
    compliant_alternative = Column(Text, nullable=False)
    official_url = Column(String, nullable=False)
    last_reviewed = Column(String, default="2023-11-30")

class RemediationAttempt(Base):
    __tablename__ = "remediation_attempts"

    id = Column(String, primary_key=True, default=generate_uuid)
    finding_id = Column(String, ForeignKey("findings.id"), nullable=False)
    original_text = Column(Text, nullable=False)
    proposed_text = Column(Text, nullable=False)
    rationale = Column(Text, nullable=False)
    before_risk = Column(Float, nullable=False)
    after_risk = Column(Float, nullable=False)
    status = Column(String, default="verified") # "verified", "unverified", "inconclusive"
    is_verified = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    finding = relationship("Finding", back_populates="remediations")

class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(String, primary_key=True, default=generate_uuid)
    finding_id = Column(String, ForeignKey("findings.id"), nullable=False)
    is_false_positive = Column(Boolean, default=True)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    finding = relationship("Finding", back_populates="feedback")

class DatasetSample(Base):
    __tablename__ = "dataset_samples"

    id = Column(String, primary_key=True, default=generate_uuid)
    sample_code = Column(String, nullable=False)
    language = Column(String, nullable=False)
    snippet = Column(Text, nullable=False)
    context = Column(String, nullable=True)
    dark_pattern_category = Column(String, nullable=False)
    ccpa_ref = Column(String, nullable=False)
    severity = Column(String, default="Medium")
    split = Column(String, default="train") # "train", "val", "test"

class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(String, primary_key=True, default=generate_uuid)
    version_tag = Column(String, nullable=False)
    model_type = Column(String, nullable=False)
    trained_at = Column(DateTime, default=datetime.datetime.utcnow)
    metrics_json = Column(JSON, nullable=False)
