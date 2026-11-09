"""SafeLink AI - Model & Analysis Orchestration Service.

Combines Machine Learning (Random Forest) inference with Rule-Based Heuristics,
Domain Existence Verification, and Typosquatting Similarity Analysis
to compute an explainable risk score (0-100) and actionable safety guidance.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
import joblib
import pandas as pd
import numpy as np

from backend.config import (
    MODEL_PATH,
    LOW_RISK_MAX,
    MEDIUM_RISK_MAX,
    WEIGHT_ML,
    WEIGHT_HEURISTICS,
)
from backend.feature_extractor import extract_features, FEATURE_COLUMNS
from backend.heuristics import evaluate_heuristics
from backend.typosquatting import analyze_typosquatting
from backend.domain_verifier import check_domain_existence
from backend.intention_analyzer import analyze_website_intention
from backend.schemas import (
    URLAnalysisResponse,
    URLAnatomy,
    RiskAssessment,
    DomainExistence,
    TyposquattingAnalysis,
    WebsiteIntention,
    FactorExplanation,
    SafetyRecommendation,
)


class ModelService:
    """Singleton service for SafeLink AI model loading and inference."""

    _instance: Optional["ModelService"] = None

    def __init__(self):
        self.artifact: Optional[Dict[str, Any]] = None
        self.model = None
        self.feature_columns: List[str] = FEATURE_COLUMNS
        self.metrics: Dict[str, Any] = {}
        self.feature_importances: Dict[str, float] = {}
        self.load_model()

    @classmethod
    def get_instance(cls) -> "ModelService":
        if cls._instance is None:
            cls._instance = ModelService()
        return cls._instance

    def load_model(self) -> bool:
        """Loads serialized model artifact from disk."""
        if MODEL_PATH.exists():
            try:
                self.artifact = joblib.load(MODEL_PATH)
                self.model = self.artifact.get("model")
                self.feature_columns = self.artifact.get("feature_columns", FEATURE_COLUMNS)
                self.metrics = self.artifact.get("metrics", {})
                self.feature_importances = self.artifact.get("feature_importances", {})
                print(f"[ModelService] Random Forest model loaded successfully from {MODEL_PATH}")
                return True
            except Exception as e:
                print(f"[ModelService] Failed to load model artifact: {e}")
                self.model = None
                return False
        else:
            print(f"[ModelService] Model file not found at {MODEL_PATH}")
            self.model = None
            return False

    def is_loaded(self) -> bool:
        return self.model is not None

    def analyze(self, raw_url: str, check_dns: bool = True) -> URLAnalysisResponse:
        """Performs static lexical, structural, typosquatting similarity, DNS existence,
        and machine learning analysis on a submitted URL.
        """
        if not raw_url or not raw_url.strip():
            raise ValueError("URL cannot be empty.")

        # 1. Static feature extraction & anatomy parsing
        extracted = extract_features(raw_url)
        features = extracted["features"]
        anatomy_raw = extracted["anatomy"]
        normalized_url = extracted["normalized_url"]

        # 2. Typosquatting & Brand Similarity Analysis (e.g. nnicrosoft vs microsoft, g00gle vs google)
        typosquatting_data = analyze_typosquatting(
            root_domain=anatomy_raw["root_domain"],
            full_netloc=anatomy_raw["netloc"]
        )

        # 3. Domain Existence Check (Safe DNS resolution)
        if check_dns:
            existence_data = check_domain_existence(anatomy_raw["netloc"])
        else:
            existence_data = {
                "exists": True,
                "status": "Check Skipped",
                "resolved_ips": [],
                "explanation": "DNS verification was skipped."
            }

        # 4. Machine Learning Inference (Random Forest)
        if self.model is not None:
            feat_df = pd.DataFrame([features])[self.feature_columns]
            ml_proba = float(self.model.predict_proba(feat_df)[0][1])
            ml_score = int(round(ml_proba * 100))
        else:
            ml_proba = 0.5
            ml_score = 50

        # If typosquatting is verified, boost ML probability
        if typosquatting_data.get("is_typosquatting"):
            ml_proba = max(0.95, ml_proba)
            ml_score = max(95, ml_score)
        elif typosquatting_data.get("is_official_brand") and features.get("suspicious_keywords_count", 0) == 0:
            ml_proba = min(0.05, ml_proba)
            ml_score = min(5, ml_score)

        # 5. Rule-Based Heuristic Evaluation
        heuristic_score, factors, recommendations = evaluate_heuristics(
            features=features,
            anatomy=anatomy_raw,
            typosquatting=typosquatting_data,
            existence=existence_data
        )

        # 6. Composite Risk Score Calculation
        composite_score = int(round(
            (WEIGHT_ML * ml_score) + (WEIGHT_HEURISTICS * heuristic_score)
        ))

        # Security Overrides:
        # If typosquatting is detected, enforce High Risk score (>= 85)
        if typosquatting_data.get("is_typosquatting"):
            composite_score = max(85, composite_score)

        # If severe critical flags are present, enforce high risk minimum
        has_critical_red_flag = any(
            f.severity == "critical" and f.category == "risk" for f in factors
        )
        if has_critical_red_flag and composite_score < 75:
            composite_score = max(75, composite_score)

        # If domain is verified official brand with no subdomains / red flags, clamp to safe
        if typosquatting_data.get("is_official_brand") and not has_critical_red_flag and composite_score > 20:
            composite_score = min(15, composite_score)

        # Clamp between 0 and 100
        final_score = max(0, min(100, composite_score))

        # 7. Risk Classification, Grade, and Phishing Verdict
        if final_score <= LOW_RISK_MAX:
            risk_level = "Low"
            score_grade = "Low Score (Safe)"
            is_phishing = False
            phishing_classification = "Legitimate / Safe Website"
            verdict = "Low Risk / Safe: No prominent fraud or deceptive patterns detected."
        elif final_score <= MEDIUM_RISK_MAX:
            risk_level = "Medium"
            score_grade = "Medium Score (Caution)"
            is_phishing = False
            phishing_classification = "Suspicious Link"
            verdict = "Medium Risk / Suspicious: Unusual characteristics or masking detected. Exercise caution before trusting."
        else:
            risk_level = "High"
            score_grade = "High Score (Dangerous)"
            is_phishing = True
            phishing_classification = "Phishing / Fraudulent Website"
            if typosquatting_data.get("is_typosquatting"):
                verdict = f"Phishing / Fraudulent Website: Brand mimicry imposter targeting {typosquatting_data.get('target_brand')}!"
            else:
                verdict = "High Risk / Likely Fraudulent: Strong indicators of phishing, spoofing, or smishing detected."

        # 8. Schema Construction
        intention_raw = analyze_website_intention(
            url=raw_url,
            anatomy=anatomy_raw,
            features=features,
            typosquatting=typosquatting_data,
            risk_score=final_score,
        )

        intention = WebsiteIntention(
            category=intention_raw["category"],
            intent_summary=intention_raw["intent_summary"],
            targeted_data=intention_raw["targeted_data"],
            attack_strategy=intention_raw["attack_strategy"],
            risk_context=intention_raw["risk_context"],
            safe_alternative=intention_raw["safe_alternative"],
        )

        anatomy = URLAnatomy(
            scheme=anatomy_raw["scheme"],
            netloc=anatomy_raw["netloc"],
            subdomain=anatomy_raw["subdomain"],
            root_domain=anatomy_raw["root_domain"],
            tld=anatomy_raw["tld"],
            path=anatomy_raw["path"],
            query=anatomy_raw["query"],
            has_port=anatomy_raw["has_port"],
            port=anatomy_raw["port"],
            is_ip=anatomy_raw["is_ip"],
        )

        domain_existence = DomainExistence(
            exists=existence_data["exists"],
            status=existence_data["status"],
            resolved_ips=existence_data["resolved_ips"],
            explanation=existence_data["explanation"],
        )

        typosquatting = TyposquattingAnalysis(
            is_typosquatting=typosquatting_data["is_typosquatting"],
            is_official_brand=typosquatting_data["is_official_brand"],
            target_brand=typosquatting_data["target_brand"],
            official_domain=typosquatting_data["official_domain"],
            technique=typosquatting_data["technique"],
            similarity_percentage=typosquatting_data["similarity_percentage"],
            explanation=typosquatting_data["explanation"],
        )

        assessment = RiskAssessment(
            score=final_score,
            risk_level=risk_level,
            score_grade=score_grade,
            is_phishing=is_phishing,
            phishing_classification=phishing_classification,
            verdict=verdict,
            ml_risk_probability=round(ml_proba, 4),
            heuristic_score=heuristic_score,
        )

        # 9. Privacy Notice and Limitation Disclaimer
        privacy_notice = (
            "Privacy Guarantee: SafeLink AI performed static lexical and structural analysis "
            "entirely offline without visiting, loading, or communicating with the destination server. "
            "Your IP address and device were never exposed to the evaluated URL."
        )

        disclaimer = (
            "Important Limitation: The risk score is an indicator based on URL patterns, "
            "heuristic security rules, and the model's available training data. It is not definitive "
            "proof that a website is fraudulent or safe. Always verify senders through independent official channels."
        )

        return URLAnalysisResponse(
            url=raw_url,
            cleaned_url=normalized_url,
            analyzed_at=datetime.now().isoformat(),
            risk=assessment,
            domain_existence=domain_existence,
            typosquatting=typosquatting,
            intention=intention,
            anatomy=anatomy,
            factors=factors,
            recommendations=recommendations,
            features=features,
            privacy_notice=privacy_notice,
            disclaimer=disclaimer,
        )


# Global instance
model_service = ModelService.get_instance()
