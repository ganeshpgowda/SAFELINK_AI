"""SafeLink AI - URL Feature Extraction Engine.

Analyzes URL lexical, structural, and statistical characteristics
without visiting or communicating with the destination server.
"""

import re
import math
import base64
import ipaddress
from urllib.parse import urlparse, parse_qs, unquote
from typing import Dict, Any, Tuple, List

from backend.config import (
    SUSPICIOUS_TLDS,
    KNOWN_SHORTENERS,
    TARGETED_BRANDS,
    SUSPICIOUS_KEYWORDS,
    STANDARD_PORTS,
)


def calculate_shannon_entropy(text: str) -> float:
    """Calculate the Shannon entropy of a string.
    
    Higher entropy indicates more randomness (e.g. DGA generated domains).
    """
    if not text:
        return 0.0
    frequencies = {}
    for char in text:
        frequencies[char] = frequencies.get(char, 0) + 1
    length = len(text)
    entropy = 0.0
    for count in frequencies.values():
        p = count / length
        entropy -= p * math.log2(p)
    return round(entropy, 4)


def is_ip_address(host: str) -> bool:
    """Check if the given host string is a valid IPv4 or IPv6 address."""
    if not host:
        return False
    # Strip port if present
    clean_host = host.split(":")[0].strip("[]")
    try:
        ipaddress.ip_address(clean_host)
        return True
    except ValueError:
        return False


def normalize_url(raw_url: str) -> str:
    """Normalizes the input URL to ensure valid parsing."""
    url = raw_url.strip()
    if not url:
        return ""
    # Support comparison inputs like 'nnicrosoft and microsoft' or 'g00gle and google'
    if " and " in url.lower():
        parts = [p.strip() for p in re.split(r"\s+and\s+", url, flags=re.IGNORECASE) if p.strip()]
        if parts:
            url = parts[0]
    elif " vs " in url.lower():
        parts = [p.strip() for p in re.split(r"\s+vs\s+", url, flags=re.IGNORECASE) if p.strip()]
        if parts:
            url = parts[0]
    # If no scheme is present, add http:// for uniform parsing
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url):
        url = "http://" + url
    return url


def parse_domain_parts(netloc: str) -> Tuple[str, str, str]:
    """Splits network location into (subdomain, root_domain, tld).
    
    Example: 'pay.login.paypal.co.uk' -> ('pay.login', 'paypal', 'co.uk')
             'account.update.xyz'     -> ('account', 'update', 'xyz')
    """
    if not netloc:
        return "", "", ""
    
    # Strip port
    host = netloc.split(":")[0].lower()
    
    # If host is an IP address
    if is_ip_address(host):
        return "", host, ""
    
    parts = host.split(".")
    if len(parts) <= 1:
        return "", host, ""
    
    # Handle known 2-level ccTLDs like .co.uk, .com.au, .gov.in, etc.
    two_level_tlds = {
        "co.uk", "com.au", "gov.in", "co.in", "ac.uk", "edu.au",
        "co.nz", "com.br", "org.uk", "net.au", "co.za", "com.mx"
    }
    
    if len(parts) >= 3 and f"{parts[-2]}.{parts[-1]}" in two_level_tlds:
        tld = f"{parts[-2]}.{parts[-1]}"
        root_domain = parts[-3]
        subdomain = ".".join(parts[:-3])
    else:
        tld = parts[-1]
        root_domain = parts[-2]
        subdomain = ".".join(parts[:-2])
        
    return subdomain, root_domain, tld


def check_brand_spoofing(root_domain: str, subdomain: str, path: str) -> Tuple[bool, str]:
    """Detects whether a high-profile brand is used deceptively.
    
    If a brand appears in the subdomain or path, but the root domain is NOT
    that brand, this is a strong sign of phishing/typosquatting.
    """
    root_clean = root_domain.lower()
    subdomain_clean = subdomain.lower()
    path_clean = path.lower()
    
    for brand in TARGETED_BRANDS:
        # Check if brand is in root domain (legitimate usage or brand match)
        if brand in root_clean:
            # Check for typosquatting variations, e.g. 'paypa1', 'faceb00k'
            continue
        
        # Check if brand appears in subdomain or path
        if brand in subdomain_clean or brand in path_clean:
            return True, brand
            
    # Also check common typosquatting substitutions in root domain
    typo_subs = [
        ("paypal", ["paypa1", "paypai", "pay-pal", "paypal-security"]),
        ("google", ["goog1e", "g00gle", "googie"]),
        ("apple", ["app1e", "apple-id", "apple-support"]),
        ("microsoft", ["micros0ft", "micro-soft"]),
        ("amazon", ["amaz0n", "amazon-security"]),
        ("netflix", ["netfl1x", "net-flix"]),
        ("chase", ["chase-bank", "chase-secure"]),
        ("whatsapp", ["whatsap", "whatssapp", "whatsapp-web-login"])
    ]
    for brand, typos in typo_subs:
        for typo in typos:
            if typo in root_clean:
                return True, f"{brand} (typosquatted as '{typo}')"
                
    return False, ""


def inspect_query_parameters(query: str) -> Dict[str, Any]:
    """Inspects query parameters for hidden nested URLs, base64 payloads, or open redirect targets."""
    if not query:
        return {"decoded_params": [], "nested_urls": []}
    
    decoded_params = []
    nested_urls = []
    
    try:
        parsed_params = parse_qs(query, keep_blank_values=True)
        for key, values in parsed_params.items():
            for val in values:
                clean_val = val.strip()
                if not clean_val:
                    continue
                
                # Check percent-encoded text
                unquoted = unquote(clean_val)
                if unquoted != clean_val and ("http://" in unquoted or "https://" in unquoted):
                    nested_urls.append(unquoted)
                    decoded_params.append({
                        "param": key,
                        "raw_value": clean_val[:60],
                        "type": "URL-Encoded Destination",
                        "decoded_value": unquoted
                    })
                
                # Check direct nested URLs
                elif "http://" in clean_val or "https://" in clean_val:
                    nested_urls.append(clean_val)
                    decoded_params.append({
                        "param": key,
                        "raw_value": clean_val[:60],
                        "type": "Direct Nested URL",
                        "decoded_value": clean_val
                    })
                
                # Check Base64 encoded payload
                elif len(clean_val) >= 8 and re.match(r'^[A-Za-z0-9+/=]+$', clean_val):
                    try:
                        b64_decoded = base64.b64decode(clean_val, validate=True).decode('utf-8', errors='ignore')
                        if b64_decoded and len(b64_decoded) >= 4 and all(c.isprintable() for c in b64_decoded[:30]):
                            if "http://" in b64_decoded or "https://" in b64_decoded:
                                nested_urls.append(b64_decoded)
                            decoded_params.append({
                                "param": key,
                                "raw_value": clean_val[:60],
                                "type": "Base64 Decoded Payload",
                                "decoded_value": b64_decoded
                            })
                    except Exception:
                        pass
    except Exception:
        pass
        
    return {
        "decoded_params": decoded_params,
        "nested_urls": list(set(nested_urls))
    }


def extract_features(raw_url: str) -> Dict[str, Any]:
    """Extracts a comprehensive vector of lexical, structural, and statistical
    features from a submitted URL.
    
    Returns a dictionary of raw features suitable for ML model inference and
    rule evaluation.
    """
    normalized = normalize_url(raw_url)
    parsed = urlparse(normalized)
    
    url_str = normalized
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path
    query = parsed.query
    
    host_no_port = netloc.split(":")[0] if ":" in netloc else netloc
    port = parsed.port
    has_port = port is not None
    non_standard_port = has_port and (port not in STANDARD_PORTS)
    
    subdomain, root_domain, tld = parse_domain_parts(netloc)
    is_ip = is_ip_address(host_no_port)
    is_https = 1 if scheme == "https" else 0
    is_short = 1 if (host_no_port in KNOWN_SHORTENERS) else 0
    
    # Keyword analysis
    combined_search_area = f"{host_no_port} {path} {query}".lower()
    keyword_matches = [kw for kw in SUSPICIOUS_KEYWORDS if kw in combined_search_area]
    suspicious_keywords_count = len(keyword_matches)
    
    # Brand spoofing check
    is_brand_spoofed, spoofed_brand = check_brand_spoofing(root_domain, subdomain, path)
    
    # Counts and statistics
    url_length = len(url_str)
    domain_length = len(netloc)
    path_length = len(path)
    query_length = len(query)
    
    num_dots = url_str.count(".")
    num_dots_domain = netloc.count(".")
    num_subdomains = len(subdomain.split(".")) if subdomain else 0
    num_hyphens = url_str.count("-")
    num_hyphens_domain = netloc.count("-")
    num_underscores = url_str.count("_")
    num_at_symbols = url_str.count("@")
    num_slashes = url_str.count("/")
    num_question_marks = url_str.count("?")
    num_equal_signs = url_str.count("=")
    num_ampersands = url_str.count("&")
    num_percent_signs = url_str.count("%")
    
    num_digits = sum(c.isdigit() for c in url_str)
    num_digits_domain = sum(c.isdigit() for c in netloc)
    digit_ratio_url = round(num_digits / max(url_length, 1), 4)
    digit_ratio_domain = round(num_digits_domain / max(domain_length, 1), 4)
    
    entropy_domain = calculate_shannon_entropy(host_no_port)
    entropy_url = calculate_shannon_entropy(url_str)
    
    suspicious_tld_flag = 1 if (tld in SUSPICIOUS_TLDS) else 0
    has_punycode = 1 if "xn--" in netloc else 0
    has_hex = 1 if re.search(r"%[0-9a-fA-F]{2}", url_str) else 0
    has_consecutive_hyphens = 1 if "--" in netloc else 0
    
    # Construct feature map
    features = {
        "url_length": url_length,
        "domain_length": domain_length,
        "path_length": path_length,
        "query_length": query_length,
        "num_dots": num_dots,
        "num_dots_domain": num_dots_domain,
        "num_subdomains": num_subdomains,
        "num_hyphens": num_hyphens,
        "num_hyphens_domain": num_hyphens_domain,
        "num_underscores": num_underscores,
        "num_at_symbols": num_at_symbols,
        "num_slashes": num_slashes,
        "num_question_marks": num_question_marks,
        "num_equal_signs": num_equal_signs,
        "num_ampersands": num_ampersands,
        "num_percent_signs": num_percent_signs,
        "num_digits": num_digits,
        "num_digits_domain": num_digits_domain,
        "digit_ratio_url": digit_ratio_url,
        "digit_ratio_domain": digit_ratio_domain,
        "is_ip": 1 if is_ip else 0,
        "is_https": is_https,
        "is_shortened": is_short,
        "entropy_domain": entropy_domain,
        "entropy_url": entropy_url,
        "suspicious_tld": suspicious_tld_flag,
        "suspicious_keywords_count": suspicious_keywords_count,
        "brand_spoofing_detected": 1 if is_brand_spoofed else 0,
        "has_punycode": has_punycode,
        "has_non_standard_port": 1 if non_standard_port else 0,
        "has_hex_encoding": has_hex,
        "has_consecutive_hyphens": has_consecutive_hyphens,
    }
    
    # Parameter inspection for open redirects and base64 payloads
    param_inspection = inspect_query_parameters(query)

    # Metadata for explainability and anatomy view
    anatomy = {
        "scheme": scheme,
        "netloc": netloc,
        "subdomain": subdomain,
        "root_domain": root_domain,
        "tld": tld,
        "path": path,
        "query": query,
        "has_port": has_port,
        "port": port,
        "is_ip": is_ip,
        "keyword_matches": keyword_matches,
        "spoofed_brand": spoofed_brand,
        "decoded_parameters": param_inspection["decoded_params"],
        "nested_urls": param_inspection["nested_urls"],
    }
    
    return {
        "features": features,
        "anatomy": anatomy,
        "normalized_url": url_str
    }


# Standard list of numerical feature names used for ML Model training & inference
FEATURE_COLUMNS = [
    "url_length",
    "domain_length",
    "path_length",
    "query_length",
    "num_dots",
    "num_dots_domain",
    "num_subdomains",
    "num_hyphens",
    "num_hyphens_domain",
    "num_underscores",
    "num_at_symbols",
    "num_slashes",
    "num_question_marks",
    "num_equal_signs",
    "num_ampersands",
    "num_percent_signs",
    "num_digits",
    "num_digits_domain",
    "digit_ratio_url",
    "digit_ratio_domain",
    "is_ip",
    "is_https",
    "is_shortened",
    "entropy_domain",
    "entropy_url",
    "suspicious_tld",
    "suspicious_keywords_count",
    "brand_spoofing_detected",
    "has_punycode",
    "has_non_standard_port",
    "has_hex_encoding",
    "has_consecutive_hyphens",
]

