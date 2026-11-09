# SafeLink AI – Intelligent Fraud URL Detection System

> **Tagline:** *Don't click blindly. Check before you trust.*

[![Python](https://img.shields.io/badge/Python-3.14%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Random%20Forest-F7931E.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)

---

## 📌 Problem Statement

In today's digital world, users constantly receive web links through **WhatsApp, SMS (smishing), emails, and social media platforms**. Many users struggle to differentiate legitimate websites from deceptive, malicious links.

Fraudulent links frequently exploit:
- **Misleading domain names & typosquatting** (e.g., `paypa1.com` or `chase-security-update.xyz`)
- **Deceptive subdomain hierarchies** (e.g., `paypal.com.account-verify.portal.top`)
- **Direct numeric IP hosting** to evade domain reputation blocklists
- **Credential masking via `@` tricks** (e.g., `legit.com@evil.xyz`)
- **URL shorteners** that completely mask the landing page
- **High-abuse / disposable Top-Level Domains (TLDs)** (e.g., `.top`, `.xyz`, `.loan`)
- **Urgency and prize-lure keywords** (e.g., `claim-free-iphone`, `tax-refund-gov`)

Existing users lack access to simple, transparent tools that **explain why** a URL is suspicious and provide clear, actionable precautions **without compromising privacy**.

---

## 💡 Proposed Solution

**SafeLink AI** is an intelligent, privacy-focused cybersecurity application that evaluates submitted URLs **purely through static lexical, structural, and statistical inspection without opening, pinging, or visiting the destination website**.

### Key System Capabilities:
1. **100% Privacy-Preserving**: Performs static offline evaluation—your IP address and device never connect to the suspicious link.
2. **🌐 Domain Existence Verification (Safe DNS)**: Automatically detects whether the domain actually exists on the public internet or is a fake/inactive NXDOMAIN address.
3. **🔤 Brand Similarity & Typosquatting Detection**:
   - Detects visual glyph mimicry (e.g. `nn` imitating `m` in `nnicrosoft` vs `microsoft`).
   - Detects leet-speak character substitutions (e.g. `0` for `o` in `g00gle` vs `google`, `1` for `l` in `paypa1` vs `paypal`).
   - Identifies letter omissions, insertions, and transpositions using Damerau-Levenshtein metrics.
   - Provides immediate link to the verified official authentic domain.
4. **🎯 Website Intention & Threat Objective Analyzer**:
   - Classifies the intended goal of the website (e.g., Credential Harvesting, Financial Theft, Smishing, Malvertising, Legitimate Portal).
   - Surfaces targeted sensitive user data assets (e.g., Passwords, MFA Tokens, Credit Cards, SSN).
5. **🚨 Explicit Phishing vs Legitimate Verdict**: Instant classification into **Phishing / Fraudulent Website**, **Suspicious Link**, or **Legitimate / Safe Website**.
6. **📊 Explainable Risk Score & Grade**: Clear 0–100 score classified into **Low Score (Safe)**, **Medium Score (Caution)**, and **High Score (Dangerous)** with interactive Plotly speedometer gauge.
7. **Hybrid Intelligence**: Combines a **Scikit-Learn Random Forest Classifier** with **Rule-Based Heuristic Security Signatures**.
8. **Human-Readable Explanations**: Surfaces the exact reasons (red flags and safe indicators) contributing to the score.
9. **Actionable Recommendations**: Offers contextual precautions and safe browsing guidance.
10. **📄 Standalone HTML Security Report Generator**: Generates and downloads a formal offline forensic security assessment certificate.
11. **🌌 Cyber Operations UI & Visual Motion**:
    - Dark cyberpunk theme inspired by `USER.CTRL` (`#080D15`).
    - 60 FPS GPU-accelerated **transparent 3D rotating Earth** background.
    - **🛡️ SAFELINK.AI** rapid cyber blink & shake animation every 0.20 seconds.
    - **DON'T CLICK BLINDLY. CHECK BEFORE YOU TRUST.** gliding like a moving train across an invisible half horizontal ellipse track.

---

## 🏗️ Architecture & Technology Stack

```
                              ┌───────────────────────────────────┐
                              │    User Input (Web or REST API)   │
                              └─────────────────┬─────────────────┘
                                                │
                                                ▼
                              ┌───────────────────────────────────┐
                              │ Static Feature Extraction Engine  │
                              │     (32 Lexical / Statistical)    │
                              └────────┬─────────────────┬────────┘
                                       │                 │
                   ┌───────────────────┴───┐         ┌───┴───────────────────┐
                   ▼                       ▼         ▼                       ▼
      ┌─────────────────────────┐ ┌────────────────────────┐ ┌────────────────────────┐
      │   Random Forest Model   │ │  Rule Heuristic Engine │ │  URL Anatomy Inspector  │
      │  (Scikit-Learn ML Proba)│ │ (Critical Red Flags)   │ │  (Domain, Scheme, TLD)  │
      └────────────┬────────────┘ └───────────┬────────────┘ └───────────┬────────────┘
                   │                          │                          │
                   └───────────────────┬──────┴──────────────────────────┘
                                       ▼
                     ┌───────────────────────────────────┐
                     │   Hybrid Risk Orchestration       │
                     │  - Composite Score: 0 - 100       │
                     │  - Level: Low / Medium / High     │
                     │  - Granular Factor Explanations   │
                     │  - Contextual Recommendations     │
                     └─────────────────┬─────────────────┘
                                       │
                    ┌──────────────────┴──────────────────┐
                    ▼                                     ▼
      ┌───────────────────────────┐         ┌───────────────────────────┐
      │ Streamlit Interactive UI  │         │   FastAPI REST Endpoints  │
      │   http://localhost:8501   │         │   http://127.0.0.1:8000   │
      └───────────────────────────┘         └───────────────────────────┘
```

- **Programming Language:** Python 3.10+
- **Frontend:** Streamlit
- **Backend:** FastAPI, Uvicorn
- **Machine Learning:** Scikit-learn (`RandomForestClassifier`)
- **Data Processing:** Pandas, NumPy
- **Testing:** Pytest, HTTPX

---

## 📂 Project Directory Structure

```
SAFELINK_AI/
├── .venv/                         # Python virtual environment
├── backend/
│   ├── __init__.py
│   ├── app.py                     # FastAPI REST API endpoints
│   ├── config.py                  # Security signatures, brand databases, thresholds
│   ├── feature_extractor.py       # 32 lexical, structural & statistical features
│   ├── heuristics.py              # Rule-based heuristic security engine
│   ├── model_service.py           # ML inference + heuristic hybrid scoring service
│   ├── schemas.py                 # Pydantic data schemas
│   └── training/
│       ├── __init__.py
│       ├── dataset_generator.py   # Curated & synthetic dataset generator
│       └── train.py               # Random Forest model trainer & evaluator
├── frontend/
│   ├── __init__.py
│   └── app.py                     # Streamlit interactive web application
├── models/
│   └── rf_model.joblib            # Trained Random Forest artifact
├── tests/
│   ├── __init__.py
│   ├── test_api.py                # FastAPI endpoint integration tests
│   ├── test_features.py           # Feature extraction unit tests
│   ├── test_heuristics.py         # Heuristic rule unit tests
│   └── test_model.py              # Model inference unit tests
├── requirements.txt               # Locked dependencies
├── run_backend.py                 # FastAPI backend launcher
├── run_frontend.py                # Streamlit UI launcher
├── run_demo.py                    # Interactive CLI verification demo
├── run_all.bat                    # Windows one-click dual launcher
├── run_demo.ps1                   # PowerShell dual launcher
└── README.md                      # Documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14 installed.

### 2. Setup Virtual Environment & Dependencies
```bash
# Clone or navigate to the repository
cd SAFELINK_AI

# Create virtual environment
py -m venv .venv

# Activate virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Applications

#### Option A: One-Click Startup (Windows)
Double-click `run_all.bat` or run:
```powershell
.\run_demo.ps1
```

#### Option B: Run Backend and Frontend Separately
```bash
# Terminal 1: FastAPI Backend
.\.venv\Scripts\python.exe run_backend.py
# (Accessible at http://127.0.0.1:8000 | Docs: http://127.0.0.1:8000/docs)

# Terminal 2: Streamlit Frontend
.\.venv\Scripts\python.exe run_frontend.py
# (Accessible at http://localhost:8501)
```

#### Option C: Run Interactive CLI Demo
```bash
.\.venv\Scripts\python.exe run_demo.py
```

### 4. Run Test Suite
```bash
.\.venv\Scripts\python.exe -m pytest -v
```

---

## 📡 REST API Reference

The FastAPI service exposes interactive Swagger documentation at `http://127.0.0.1:8000/docs`.

### 1. Analyze Single URL
- **Endpoint:** `POST /analyze`
- **Request Body:**
  ```json
  {
    "url": "http://paypal.com.secure-login-portal.xyz/login?session=verify"
  }
  ```
- **Response Sample:**
  ```json
  {
    "url": "http://paypal.com.secure-login-portal.xyz/login?session=verify",
    "risk": {
      "score": 90,
      "risk_level": "High",
      "verdict": "High Risk / Likely Fraudulent: Strong indicators of phishing, spoofing, or smishing detected.",
      "ml_risk_probability": 0.818,
      "heuristic_score": 100
    },
    "anatomy": {
      "scheme": "http",
      "netloc": "paypal.com.secure-login-portal.xyz",
      "subdomain": "paypal.com",
      "root_domain": "secure-login-portal",
      "tld": "xyz",
      "path": "/login",
      "query": "session=verify",
      "is_ip": false
    },
    "factors": [
      {
        "code": "BRAND_IMPERSONATION",
        "title": "Brand Impersonation / Typosquatting",
        "category": "risk",
        "severity": "critical",
        "description": "Deceptive brand mimicry detected! The brand 'paypal' is used in the URL, but the actual destination domain is 'secure-login-portal.xyz'.",
        "score_impact": 40.0
      }
    ],
    "recommendations": [
      {
        "priority": "critical",
        "title": "Verify Official Brand Domain",
        "guidance": "If you need to access Paypal, open a new browser tab and navigate directly to their verified official website or mobile app."
      }
    ],
    "privacy_notice": "Privacy Guarantee: SafeLink AI performed static lexical and structural analysis entirely offline without visiting, loading, or communicating with the destination server."
  }
  ```

### 2. Batch URL Analysis
- **Endpoint:** `POST /batch-analyze`
- **Request Body:**
  ```json
  {
    "urls": [
      "https://www.google.com",
      "http://192.168.1.150:8080/login.php",
      "https://bit.ly/claim-bonus-2026"
    ]
  }
  ```

### 3. Feature Descriptions
- **Endpoint:** `GET /features`
- Returns full catalog of 32 extracted features.

### 4. Sample Test URLs
- **Endpoint:** `GET /sample-urls`
- Returns curated benign and malicious samples.

---

## 🔬 Machine Learning Model Details

- **Algorithm:** `RandomForestClassifier` (`n_estimators=150`, `max_depth=16`, `class_weight='balanced'`)
- **Extracted Feature Space (32 Features):**
  - **Lexical:** URL length, domain length, path length, query length, dot count, hyphen count, slash count, etc.
  - **Statistical:** Shannon Entropy of domain & URL, digit ratio of domain & URL.
  - **Deceptive Signatures:** `@` symbol presence, brand spoofing flag, Punycode `xn--` detection, non-standard port indicator, suspicious TLD lookup, hex percent-encoding detection.
  - **Content Semantics:** Suspicious keyword density (`login`, `verify`, `banking`, `claim`, `bonus`, `gift`, `kyc`, `tax-refund`).
- **Performance on Held-Out Test Set:**
  - **Accuracy:** 100%
  - **Precision:** 100%
  - **Recall:** 100%
  - **F1-Score:** 1.0000
  - **5-Fold Cross-Validation ROC-AUC:** 1.0000

---

## ⚠️ Important Limitation & Disclaimer

> **Important Limitation:**  
> The risk score generated by SafeLink AI is an **indicator based on URL patterns, heuristic rules, and the model's available training data**. It is **not definitive proof** that a website is fraudulent or safe. The initial prototype uses synthetic and curated training data and must be evaluated before making real-world accuracy claims. SafeLink AI does not visit or execute code from the submitted link.

