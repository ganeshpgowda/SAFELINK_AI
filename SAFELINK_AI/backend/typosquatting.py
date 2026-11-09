"""SafeLink AI - Advanced Typosquatting and Domain Similarity Engine.

Detects visual mimicry, character substitutions (e.g. nn -> m, 0 -> o, 1 -> l),
omissions, insertions, transpositions, unauthorized TLD-squatting, subdomain
deception, and edit-distance proximity to popular brands.
"""

import re
from typing import Dict, Any, List, Tuple, Optional

# Curated catalog of high-profile global and financial brands and their legitimate root domains
BRAND_CATALOG = {
    "microsoft": {"official_domains": ["microsoft.com", "microsoft365.com", "azure.com", "office.com", "live.com", "msn.com"], "display": "Microsoft"},
    "google": {"official_domains": ["google.com", "google.co.in", "google.co.uk", "youtube.com", "gmail.com"], "display": "Google"},
    "apple": {"official_domains": ["apple.com", "icloud.com"], "display": "Apple"},
    "amazon": {"official_domains": ["amazon.com", "amazon.in", "amazon.co.uk", "amazon.de", "aws.amazon.com"], "display": "Amazon"},
    "paypal": {"official_domains": ["paypal.com", "paypal.me"], "display": "PayPal"},
    "netflix": {"official_domains": ["netflix.com"], "display": "Netflix"},
    "facebook": {"official_domains": ["facebook.com", "fb.com", "meta.com"], "display": "Facebook / Meta"},
    "instagram": {"official_domains": ["instagram.com"], "display": "Instagram"},
    "whatsapp": {"official_domains": ["whatsapp.com"], "display": "WhatsApp"},
    "telegram": {"official_domains": ["telegram.org", "t.me"], "display": "Telegram"},
    "twitter": {"official_domains": ["twitter.com", "x.com"], "display": "Twitter / X"},
    "linkedin": {"official_domains": ["linkedin.com"], "display": "LinkedIn"},
    "chase": {"official_domains": ["chase.com"], "display": "Chase Bank"},
    "wellsfargo": {"official_domains": ["wellsfargo.com"], "display": "Wells Fargo"},
    "bankofamerica": {"official_domains": ["bankofamerica.com"], "display": "Bank of America"},
    "citibank": {"official_domains": ["citi.com", "citibank.com"], "display": "Citibank"},
    "binance": {"official_domains": ["binance.com"], "display": "Binance"},
    "coinbase": {"official_domains": ["coinbase.com"], "display": "Coinbase"},
    "dropbox": {"official_domains": ["dropbox.com"], "display": "Dropbox"},
    "github": {"official_domains": ["github.com"], "display": "GitHub"},
    "spotify": {"official_domains": ["spotify.com"], "display": "Spotify"},
    "steam": {"official_domains": ["steampowered.com", "steamcommunity.com"], "display": "Steam"},
    "ebay": {"official_domains": ["ebay.com"], "display": "eBay"},
    "walmart": {"official_domains": ["walmart.com"], "display": "Walmart"},
    "yahoo": {"official_domains": ["yahoo.com"], "display": "Yahoo"},
    "adobe": {"official_domains": ["adobe.com"], "display": "Adobe"},
    "roblox": {"official_domains": ["roblox.com"], "display": "Roblox"},
    "zoom": {"official_domains": ["zoom.us"], "display": "Zoom"},
}


def damerau_levenshtein_distance(s1: str, s2: str) -> int:
    """Calculates Damerau-Levenshtein distance between two strings,
    supporting insertions, deletions, substitutions, and adjacent transpositions.
    """
    d = {}
    len1 = len(s1)
    len2 = len(s2)
    for i in range(-1, len1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, len2 + 1):
        d[(-1, j)] = j + 1

    for i in range(len1):
        for j in range(len2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,        # deletion
                d[(i, j - 1)] + 1,        # insertion
                d[(i - 1, j - 1)] + cost  # substitution
            )
            if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[(i - 2, j - 2)] + 1)  # transposition

    return d[(len1 - 1, len2 - 1)]


def normalize_visual_substitutions(text: str) -> Tuple[str, List[str]]:
    """Normalizes common visual, leet-speak, and character group substitutions:
    - 'nn' -> 'm' (e.g. nnicrosoft -> microsoft)
    - 'rn' -> 'm' (e.g. rnicrosoft -> microsoft)
    - 'vv' -> 'w' (e.g. vwhatsapp -> whatsapp)
    - 'cl' -> 'd' (e.g. cloogle -> doogle)
    - '0'  -> 'o' (e.g. g00gle -> google)
    - '1', 'l', '|', '!' -> 'l' or 'i' (e.g. paypa1 -> paypal)
    - '3'  -> 'e' (e.g. n3tflix -> netflix)
    - '4', '@' -> 'a' (e.g. @pple -> apple)
    - '5', '$' -> 's' (e.g. cha5e -> chase)
    """
    orig = text.lower()
    normalized = orig
    techniques = []

    # 1. Multi-character glyph mimics
    if "nn" in normalized:
        normalized = normalized.replace("nn", "m")
        techniques.append("Visual glyph mimicry: 'nn' mimics 'm'")
    if "rn" in normalized:
        normalized = normalized.replace("rn", "m")
        techniques.append("Visual glyph mimicry: 'rn' mimics 'm'")
    if "vv" in normalized:
        normalized = normalized.replace("vv", "w")
        techniques.append("Visual glyph mimicry: 'vv' mimics 'w'")
    if "cl" in normalized:
        normalized = normalized.replace("cl", "d")
        techniques.append("Visual glyph mimicry: 'cl' mimics 'd'")

    # 2. Leet-speak digit replacements
    leet_subs = [
        ("0", "o", "Leet-speak substitution: '0' for 'o'"),
        ("1", "l", "Leet-speak substitution: '1' for 'l'"),
        ("3", "e", "Leet-speak substitution: '3' for 'e'"),
        ("4", "a", "Leet-speak substitution: '4' for 'a'"),
        ("@", "a", "Symbol substitution: '@' for 'a'"),
        ("5", "s", "Leet-speak substitution: '5' for 's'"),
        ("$", "s", "Symbol substitution: '$' for 's'"),
        ("8", "b", "Leet-speak substitution: '8' for 'b'"),
    ]

    for char, replacement, desc in leet_subs:
        if char in normalized:
            normalized = normalized.replace(char, replacement)
            techniques.append(desc)

    # 3. Unicode Homoglyph substitutions (Cyrillic to Latin)
    homoglyphs = {
        'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 'у': 'y', 'х': 'x',
        'і': 'i', 'ј': 'j', 'ѕ': 's', 'ԁ': 'd', 'ԛ': 'q', 'ԝ': 'w'
    }
    has_homoglyph = False
    new_norm = []
    for c in normalized:
        if c in homoglyphs:
            new_norm.append(homoglyphs[c])
            has_homoglyph = True
        else:
            new_norm.append(c)
    normalized = "".join(new_norm)
    if has_homoglyph:
        techniques.append("Unicode Homoglyph: non-Latin character imitating Latin alphabet")

    return normalized, techniques


def analyze_typosquatting(root_domain: str, full_netloc: str) -> Dict[str, Any]:
    """Analyzes a domain against the high-profile brand catalog to detect
    typosquatting, lookalike domains, leet-speak, unauthorized TLD-squatting,
    subdomain brand spoofing, and edit-distance spoofs.
    """
    clean_root = root_domain.lower().strip()
    clean_host = full_netloc.lower().split(":")[0].strip()

    # Normalize substitutions (e.g. nnicrosoft -> microsoft, g00gle -> google)
    normalized_root, detected_techniques = normalize_visual_substitutions(clean_root)

    best_match: Optional[Dict[str, Any]] = None
    min_distance = 999
    max_similarity = 0.0

    for brand_key, brand_info in BRAND_CATALOG.items():
        official_domains = brand_info["official_domains"]
        display_name = brand_info["display"]

        # Check if this host is an authentic official domain or official bare brand name
        is_exact_official = any(
            clean_host == off or clean_host.endswith("." + off)
            for off in official_domains
        )
        is_bare_brand_name = (clean_host == brand_key and clean_root == brand_key)

        if is_exact_official or is_bare_brand_name:
            # Genuine official domain!
            return {
                "is_typosquatting": False,
                "is_official_brand": True,
                "target_brand": display_name,
                "official_domain": official_domains[0],
                "technique": "None (Verified Official Domain)",
                "similarity_percentage": 100.0,
                "explanation": f"Verified authentic official address for {display_name}."
            }

        # 1. TLD-Squatting / Rogue TLD Check (e.g. google.xyz, microsoft.top, paypal.club)
        # Root domain matches brand exactly, but host is NOT in official domains
        if clean_root == brand_key:
            return {
                "is_typosquatting": True,
                "is_official_brand": False,
                "target_brand": display_name,
                "official_domain": official_domains[0],
                "technique": f"Unauthorized TLD-Squatting (Brand registered on unofficial domain)",
                "similarity_percentage": 99.0,
                "explanation": (
                    f"CRITICAL: Domain '{clean_host}' illegitimately registers the protected brand name '{display_name}' "
                    f"on an unofficial top-level domain. The authentic official domain is '{official_domains[0]}'."
                )
            }

        # 2. Visual Substitution & Glyphs (e.g., nnicrosoft -> microsoft, g00gle -> google)
        if normalized_root == brand_key and clean_root != brand_key:
            tech_str = "; ".join(detected_techniques) if detected_techniques else "Visual character mimicry"
            return {
                "is_typosquatting": True,
                "is_official_brand": False,
                "target_brand": display_name,
                "official_domain": official_domains[0],
                "technique": tech_str,
                "similarity_percentage": 98.0,
                "explanation": (
                    f"CRITICAL: Domain '{clean_root}' is a visual clone of '{display_name}' "
                    f"using {tech_str}. The legitimate official domain is '{official_domains[0]}'."
                )
            }

        # 3. Subdomain Brand Impersonation (e.g., microsoft.com.attacker.xyz or paypal.com.login-verify.top)
        subdomain_spoof = False
        for off in official_domains:
            if off in clean_host and not (clean_host == off or clean_host.endswith("." + off)):
                subdomain_spoof = True
                break
        if not subdomain_spoof and brand_key in clean_host and clean_root != brand_key:
            host_parts = clean_host.replace("-", ".").split(".")
            if brand_key in host_parts:
                subdomain_spoof = True

        if subdomain_spoof:
            return {
                "is_typosquatting": True,
                "is_official_brand": False,
                "target_brand": display_name,
                "official_domain": official_domains[0],
                "technique": "Subdomain brand spoofing (Brand name used in deceptive subdomain prefix)",
                "similarity_percentage": 96.0,
                "explanation": (
                    f"CRITICAL: Host '{clean_host}' deceives users by embedding '{display_name}' into its subdomain prefix. "
                    f"The actual destination server is controlled by '{clean_root}', NOT {display_name}."
                )
            }

        # 4. Brand Combo-Squatting (e.g., microsoft-login.com, chase-security.com, paypal-verify.com)
        if brand_key in normalized_root and clean_root != brand_key:
            return {
                "is_typosquatting": True,
                "is_official_brand": False,
                "target_brand": display_name,
                "official_domain": official_domains[0],
                "technique": "Brand combo-squatting (Brand name combined with security/login keywords)",
                "similarity_percentage": 95.0,
                "explanation": (
                    f"Domain '{clean_root}' illegitimately incorporates the brand '{display_name}' "
                    f"into its name. The legitimate official domain is '{official_domains[0]}'."
                )
            }

        # 5. Damerau-Levenshtein Distance (Omissions, insertions, transpositions)
        dist_raw = damerau_levenshtein_distance(clean_root, brand_key)
        dist_norm = damerau_levenshtein_distance(normalized_root, brand_key)
        dist = min(dist_raw, dist_norm)

        max_len = max(len(clean_root), len(brand_key))
        sim = round((1.0 - (dist / max(max_len, 1))) * 100, 1)

        # Flag edit distance of 1 or 2 as dangerous typosquatting (e.g. 'micosoft' -> distance 1)
        if dist <= 2 and len(clean_root) >= 4 and clean_root != brand_key:
            if dist < min_distance or sim > max_similarity:
                min_distance = dist
                max_similarity = sim
                
                if dist_raw == 1:
                    if len(clean_root) < len(brand_key):
                        tech = "Character omission (missing letter)"
                    elif len(clean_root) > len(brand_key):
                        tech = "Character insertion (added letter)"
                    else:
                        tech = "Character substitution or adjacent transposition"
                else:
                    tech = f"Edit distance variation ({dist} character edits)"

                if detected_techniques:
                    tech = f"{tech} with {'; '.join(detected_techniques)}"

                best_match = {
                    "is_typosquatting": True,
                    "is_official_brand": False,
                    "target_brand": display_name,
                    "official_domain": official_domains[0],
                    "technique": tech,
                    "similarity_percentage": sim,
                    "explanation": (
                        f"CRITICAL: Domain '{clean_root}' closely mimics '{display_name}' "
                        f"({sim}% similarity, {tech}). The legitimate official domain is '{official_domains[0]}'."
                    )
                }

    if best_match:
        return best_match

    # No typosquatting detected
    return {
        "is_typosquatting": False,
        "is_official_brand": False,
        "target_brand": None,
        "official_domain": None,
        "technique": None,
        "similarity_percentage": 0.0,
        "explanation": "No typosquatting or brand mimicry detected against monitored high-profile brands."
    }
