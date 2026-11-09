"""Pydantic schemas for SafeLink AI REST API requests and responses.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict


class URLAnalysisRequest(BaseModel):
    """Single URL analysis request schema."""
    url: str = Field(..., description="The URL string to evaluate without visiting.")
    check_dns: bool = Field(True, description="Whether to perform safe offline DNS existence verification.")
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "url": "https://secure-login-paypal.com.account-update.xyz/login?ref=sms",
                "check_dns": True
            }
        }
    )


class BatchURLAnalysisRequest(BaseModel):
    """Batch URL analysis request schema."""
    urls: List[str] = Field(..., max_length=100, description="List of URLs to evaluate (max 100).")
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "urls": [
                    "https://www.google.com",
                    "http://nnicrosoft.com/login",
                    "http://192.168.1.50/verify-account/login.php",
                    "https://bit.ly/claim-bonus-2026"
                ]
            }
        }
    )


class URLAnatomy(BaseModel):
    """Structural breakdown of the evaluated URL."""
    scheme: str
    netloc: str
    subdomain: str
    root_domain: str
    tld: str
    path: str
    query: str
    has_port: bool
    port: Optional[int] = None
    is_ip: bool


class DomainExistence(BaseModel):
    """Domain existence and global DNS resolution status."""
    exists: bool = Field(..., description="Whether the domain resolves in global DNS.")
    status: str = Field(..., description="'Active / Resolving Domain', 'Non-Existent / Inactive (NXDOMAIN)', etc.")
    resolved_ips: List[str] = Field(default_factory=list, description="Resolved IP addresses if active.")
    explanation: str = Field(..., description="Plain-language explanation of domain existence.")


class TyposquattingAnalysis(BaseModel):
    """Analysis of similarity to popular brands (e.g. nnicrosoft vs microsoft, g00gle vs google)."""
    is_typosquatting: bool = Field(..., description="True if domain mimics or typo-squats a brand.")
    is_official_brand: bool = Field(..., description="True if domain is the verified official domain of that brand.")
    target_brand: Optional[str] = Field(None, description="The brand being imitated (e.g. Microsoft, Google).")
    official_domain: Optional[str] = Field(None, description="The legitimate official domain of the brand.")
    technique: Optional[str] = Field(None, description="Technique used (e.g. Visual substitution 'nn' for 'm').")
    similarity_percentage: float = Field(0.0, description="Similarity percentage (0-100%).")
    explanation: str = Field(..., description="Detailed explanation of the similarity check.")


class WebsiteIntention(BaseModel):
    """The identified primary purpose, threat objective, and targeted data of the website."""
    category: str = Field(..., description="Category of intention (e.g. Credential Harvesting, Financial Theft, Legitimate Search).")
    intent_summary: str = Field(..., description="1-2 sentence plain-language explanation of what the website aims to achieve.")
    targeted_data: List[str] = Field(default_factory=list, description="Specific sensitive data or user assets targeted.")
    attack_strategy: str = Field(..., description="Psychological or technical strategy employed by the link.")
    risk_context: str = Field(..., description="'Critical Threat', 'High Threat', 'Medium Risk', or 'Safe'.")
    safe_alternative: Optional[str] = Field(None, description="Legitimate official destination for the user if applicable.")


class FactorExplanation(BaseModel):
    """Detailed explanation of a detected risk or safety indicator."""
    code: str
    title: str
    category: str = Field(..., description="'risk' or 'safety' or 'neutral'")
    severity: str = Field(..., description="'critical', 'high', 'medium', 'low', or 'safe'")
    description: str
    score_impact: float = Field(..., description="Impact points on overall risk calculation.")


class SafetyRecommendation(BaseModel):
    """Actionable advice for the end-user."""
    priority: str = Field(..., description="'critical', 'warning', or 'info'")
    title: str
    guidance: str


class RiskAssessment(BaseModel):
    """Risk scoring, grade, and phishing classification."""
    score: int = Field(..., ge=0, le=100, description="Explainable composite risk score (0-100).")
    risk_level: str = Field(..., description="'Low', 'Medium', or 'High'")
    score_grade: str = Field(..., description="'Low Score (Safe)', 'Medium Score (Caution)', 'High Score (Dangerous)'")
    is_phishing: bool = Field(..., description="True if classified as a phishing / fraudulent website.")
    phishing_classification: str = Field(..., description="'Phishing / Fraudulent Website', 'Suspicious Link', or 'Legitimate / Safe Website'")
    verdict: str = Field(..., description="User-friendly verdict summary.")
    ml_risk_probability: float = Field(..., ge=0.0, le=1.0, description="Random Forest fraud probability.")
    heuristic_score: int = Field(..., ge=0, le=100, description="Rule-based heuristic risk score.")


class URLAnalysisResponse(BaseModel):
    """Complete URL analysis result returned by SafeLink AI."""
    url: str
    cleaned_url: str
    analyzed_at: str
    risk: RiskAssessment
    domain_existence: DomainExistence
    typosquatting: TyposquattingAnalysis
    intention: WebsiteIntention
    anatomy: URLAnatomy
    factors: List[FactorExplanation]
    recommendations: List[SafetyRecommendation]
    features: Dict[str, Any]
    privacy_notice: str
    disclaimer: str


class BatchSummary(BaseModel):
    total_analyzed: int
    low_risk_count: int
    medium_risk_count: int
    high_risk_count: int
    phishing_count: int
    inactive_domains_count: int


class BatchURLAnalysisResponse(BaseModel):
    summary: BatchSummary
    results: List[URLAnalysisResponse]


class FeatureInfo(BaseModel):
    name: str
    category: str
    description: str
    type: str


class HealthResponse(BaseModel):
    status: str
    service: str
    model_loaded: bool
    version: str
    timestamp: str
