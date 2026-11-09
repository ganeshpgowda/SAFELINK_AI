"""SafeLink AI - Rule-Based Heuristic Security Engine.

Evaluates high-fidelity heuristic rules and security indicators, providing
explainable impact factors and safety recommendations.
"""

from typing import List, Dict, Any, Tuple, Optional
from backend.config import (
    SUSPICIOUS_TLDS,
    LEGITIMATE_COMMON_TLDS,
    KNOWN_SHORTENERS,
)
from backend.schemas import FactorExplanation, SafetyRecommendation


def evaluate_heuristics(
    features: Dict[str, Any],
    anatomy: Dict[str, Any],
    typosquatting: Optional[Dict[str, Any]] = None,
    existence: Optional[Dict[str, Any]] = None
) -> Tuple[int, List[FactorExplanation], List[SafetyRecommendation]]:
    """Evaluates rule-based security heuristics on extracted features.
    
    Returns:
        (heuristic_score, factor_explanations, safety_recommendations)
    """
    factors: List[FactorExplanation] = []
    recommendations: List[SafetyRecommendation] = []
    raw_score = 0.0

    # 1. Advanced Typosquatting & Brand Mimicry (Critical)
    if typosquatting and typosquatting.get("is_typosquatting"):
        impact = 45.0
        raw_score += impact
        brand = typosquatting.get("target_brand", "known brand")
        official = typosquatting.get("official_domain", "")
        tech = typosquatting.get("technique", "character substitution")
        factors.append(FactorExplanation(
            code="TYPOSQUATTING_MIMICRY",
            title=f"Brand Mimicry / Typosquatting ({brand})",
            category="risk",
            severity="critical",
            description=f"CRITICAL PHISHING RISK: Domain impersonates '{brand}' using {tech}. The official authentic domain is '{official}'.",
            score_impact=impact
        ))
        recommendations.append(SafetyRecommendation(
            priority="critical",
            title=f"Imposter Domain for {brand}",
            guidance=f"DO NOT enter credentials or passwords here. Navigate directly to the verified official website: https://{official}."
        ))

    # 2. Hostname is a raw IP address (Critical)
    if features.get("is_ip") == 1:
        impact = 35.0
        raw_score += impact
        factors.append(FactorExplanation(
            code="IP_AS_HOSTNAME",
            title="IP Address Used as Hostname",
            category="risk",
            severity="critical",
            description="The URL uses a raw numeric IP address instead of a domain name. Legitimate consumer services virtually never use raw IP links.",
            score_impact=impact
        ))
        recommendations.append(SafetyRecommendation(
            priority="critical",
            title="Do Not Open Raw IP Links",
            guidance="Never input passwords, credentials, or sensitive banking information into a website identified only by an IP address."
        ))

    # 3. Subdomain Brand Spoofing (e.g. paypal.com.evil.xyz)
    if features.get("brand_spoofing_detected") == 1:
        impact = 40.0
        is_already_typo = bool(typosquatting and typosquatting.get("is_typosquatting"))
        if not is_already_typo:
            raw_score += impact
        spoofed = anatomy.get("spoofed_brand", "known brand")
        root = anatomy.get("root_domain", "")
        tld = anatomy.get("tld", "")
        dest = f"{root}.{tld}" if tld else root
        factors.append(FactorExplanation(
            code="BRAND_IMPERSONATION",
            title="Brand Impersonation in Subdomain / Path",
            category="risk",
            severity="critical",
            description=f"Deceptive brand mimicry detected! The brand '{spoofed}' is used in the URL prefix, but the actual destination domain is '{dest}'.",
            score_impact=impact if not is_already_typo else 0.0
        ))
        recommendations.append(SafetyRecommendation(
            priority="critical",
            title="Verify Official Brand Domain",
            guidance=f"If you need to access {spoofed.capitalize()}, open a new browser tab and navigate directly to their verified official website or mobile app."
        ))

    # 4. Domain Existence / DNS Resolution Status
    if existence and not existence.get("exists"):
        status = existence.get("status", "Inactive")
        impact = 20.0
        raw_score += impact
        factors.append(FactorExplanation(
            code="DOMAIN_NON_EXISTENT",
            title=f"Domain Does Not Exist ({status})",
            category="risk",
            severity="high",
            description=existence.get("explanation", "The domain cannot be resolved in global DNS."),
            score_impact=impact
        ))
        recommendations.append(SafetyRecommendation(
            priority="warning",
            title="Unregistered or Defunct Link",
            guidance="The link cannot be reached. It may be an expired malicious campaign or a fabricated address."
        ))

    # 5. '@' Symbol in URL (Credential Spoofing)
    if features.get("num_at_symbols", 0) > 0:
        impact = 30.0
        raw_score += impact
        factors.append(FactorExplanation(
            code="AT_SYMBOL_OBFUSCATION",
            title="'@' Symbol Spoofing Trick",
            category="risk",
            severity="critical",
            description="The '@' symbol in a URL causes browsers to ignore all text before it, routing you exclusively to the host that follows it.",
            score_impact=impact
        ))
        recommendations.append(SafetyRecommendation(
            priority="critical",
            title="Inspect Destination After '@'",
            guidance="Be aware that any trusted domain shown before '@' is completely ignored by your browser."
        ))

    # 6. Punycode / Homograph Attack
    if features.get("has_punycode") == 1:
        impact = 25.0
        raw_score += impact
        factors.append(FactorExplanation(
            code="PUNYCODE_HOMOGRAPH",
            title="Punycode / Homograph Attack Indicator",
            category="risk",
            severity="high",
            description="Domain contains 'xn--', which encodes non-ASCII characters. Fraudsters use this to mimic letters (e.g. Cyrillic 'а' replacing Latin 'a').",
            score_impact=impact
        ))
        recommendations.append(SafetyRecommendation(
            priority="warning",
            title="Inspect Character Encoding",
            guidance="Check if the domain is disguising non-English characters to visually imitate a familiar brand name."
        ))

    # 7. Insecure HTTP with Sensitive Keywords
    if features.get("is_https") == 0 and features.get("suspicious_keywords_count", 0) > 0:
        impact = 25.0
        raw_score += impact
        matched_kws = ", ".join(anatomy.get("keyword_matches", []))
        factors.append(FactorExplanation(
            code="INSECURE_SENSITIVE_HTTP",
            title="Insecure HTTP Requesting Sensitive Actions",
            category="risk",
            severity="high",
            description=f"The link is unencrypted (HTTP) yet targets sensitive actions ({matched_kws}). Legitimate portals require HTTPS.",
            score_impact=impact
        ))
        recommendations.append(SafetyRecommendation(
            priority="critical",
            title="Never Submit Credentials Over HTTP",
            guidance="Because the connection is unencrypted, any data or login credentials you enter can be intercepted in transit."
        ))

    # 8. Suspicious / High-Abuse Top-Level Domain (TLD)
    if features.get("suspicious_tld") == 1:
        impact = 20.0
        raw_score += impact
        tld = anatomy.get("tld", "")
        factors.append(FactorExplanation(
            code="SUSPICIOUS_TLD",
            title="High-Abuse Top-Level Domain",
            category="risk",
            severity="medium",
            description=f"Uses the '.{tld}' top-level domain, which has historically elevated rates of disposable phishing and malware campaigns.",
            score_impact=impact
        ))
        recommendations.append(SafetyRecommendation(
            priority="warning",
            title="Scrutinize Unfamiliar Extensions",
            guidance=f"Be cautious of links ending in '.{tld}', especially if received unexpectedly via text or messaging apps."
        ))

    # 9. URL Shortener Masking
    if features.get("is_shortened") == 1:
        impact = 18.0
        raw_score += impact
        factors.append(FactorExplanation(
            code="URL_SHORTENER_MASK",
            title="URL Shortener Masking Destination",
            category="risk",
            severity="medium",
            description="The URL uses a link shortening service. The real destination domain, path, and security posture are completely hidden.",
            score_impact=impact
        ))
        recommendations.append(SafetyRecommendation(
            priority="warning",
            title="Expand Shortened Links First",
            guidance="Use a link unshortener or preview tool to inspect the true landing page before clicking short links from unknown senders."
        ))

    # 10. Excessive Subdomains
    subdomains_count = features.get("num_subdomains", 0)
    if subdomains_count >= 3:
        impact = min(20.0, subdomains_count * 5.0)
        raw_score += impact
        factors.append(FactorExplanation(
            code="EXCESSIVE_SUBDOMAINS",
            title=f"Excessive Subdomains ({subdomains_count})",
            category="risk",
            severity="medium",
            description="The URL contains multiple nested subdomains, a pattern frequently used to create misleading prefixes resembling trusted entities.",
            score_impact=impact
        ))

    # 11. Excessive Hyphens in Domain
    hyphens_domain = features.get("num_hyphens_domain", 0)
    if hyphens_domain >= 3:
        impact = 12.0
        raw_score += impact
        factors.append(FactorExplanation(
            code="EXCESSIVE_HYPHENS_DOMAIN",
            title="Multiple Hyphens in Domain",
            category="risk",
            severity="low",
            description=f"Domain contains {hyphens_domain} hyphens. Attackers frequently use hyphens (e.g. 'paypal-security-update') to evade filters.",
            score_impact=impact
        ))

    # 12. High Domain Entropy (Randomness / DGA)
    entropy = features.get("entropy_domain", 0.0)
    if entropy >= 3.8 and features.get("is_ip") == 0:
        impact = 15.0
        raw_score += impact
        factors.append(FactorExplanation(
            code="HIGH_DOMAIN_ENTROPY",
            title="High Character Randomness (Entropy)",
            category="risk",
            severity="medium",
            description=f"Domain name displays high character entropy ({entropy:.2f}), suggesting machine-generated or disposable domain names.",
            score_impact=impact
        ))

    # 13. Non-standard Port
    if features.get("has_non_standard_port") == 1:
        impact = 15.0
        raw_score += impact
        port = anatomy.get("port")
        factors.append(FactorExplanation(
            code="NON_STANDARD_PORT",
            title=f"Non-Standard Port ({port})",
            category="risk",
            severity="medium",
            description=f"The link points to port {port} instead of standard web traffic ports (80/443), often indicating rogue or compromised servers.",
            score_impact=impact
        ))

    # 14. High Digit Ratio in Domain
    digit_ratio = features.get("digit_ratio_domain", 0.0)
    if digit_ratio > 0.35 and features.get("is_ip") == 0:
        impact = 10.0
        raw_score += impact
        factors.append(FactorExplanation(
            code="HIGH_DIGIT_RATIO",
            title="Unusual Number of Digits in Domain",
            category="risk",
            severity="low",
            description=f"{digit_ratio*100:.0f}% of the domain consists of numerical digits, commonly observed in automated fraudulent domains.",
            score_impact=impact
        ))

    # POSITIVE / SAFETY INDICATORS (Offsetting or reassuring factors)
    if features.get("is_https") == 1:
        factors.append(FactorExplanation(
            code="HTTPS_ENABLED",
            title="HTTPS Transport Encryption Active",
            category="safety",
            severity="safe",
            description="The URL uses SSL/TLS encryption for transit security. (Note: Phishing sites can also have SSL certificates, so evaluate holistically.)",
            score_impact=-5.0
        ))

    tld = anatomy.get("tld", "").lower()
    if tld in LEGITIMATE_COMMON_TLDS and features.get("suspicious_tld") == 0:
        factors.append(FactorExplanation(
            code="REPUTABLE_TLD",
            title=f"Standard Top-Level Domain (.{tld})",
            category="safety",
            severity="safe",
            description=f"The domain uses the widely recognized and monitored '.{tld}' top-level domain.",
            score_impact=-5.0
        ))

    if features.get("suspicious_keywords_count", 0) == 0:
        factors.append(FactorExplanation(
            code="NO_SUSPICIOUS_KEYWORDS",
            title="No Urgency or Phishing Keywords Found",
            category="safety",
            severity="safe",
            description="The URL does not contain typical deceptive keywords such as 'verify', 'account', 'gift', or 'banking'.",
            score_impact=-5.0
        ))

    if features.get("num_dots_domain", 0) <= 1 and features.get("is_ip") == 0 and subdomains_count == 0:
        factors.append(FactorExplanation(
            code="CLEAN_DOMAIN_STRUCTURE",
            title="Clean, Direct Domain Structure",
            category="safety",
            severity="safe",
            description="The domain has a clean structure with no nested subdomains or prefix tampering.",
            score_impact=-5.0
        ))

    if typosquatting and typosquatting.get("is_official_brand"):
        factors.append(FactorExplanation(
            code="VERIFIED_OFFICIAL_BRAND",
            title=f"Verified Official Domain ({typosquatting.get('target_brand')})",
            category="safety",
            severity="safe",
            description=f"The domain matches the verified, authentic official address for {typosquatting.get('target_brand')}.",
            score_impact=-20.0
        ))

    # Default general recommendation if none triggered
    if not recommendations:
        recommendations.append(SafetyRecommendation(
            priority="info",
            title="Standard Browsing Caution",
            guidance="While no prominent red flags were detected, always ensure you trust the message sender before submitting personal information."
        ))

    # Clamp heuristic score to [0, 100]
    final_heuristic_score = int(max(0, min(100, round(raw_score))))
    return final_heuristic_score, factors, recommendations
