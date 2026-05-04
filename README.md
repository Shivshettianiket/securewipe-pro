# 🔐 SecureWipe Pro
### India's First Indigenous Secure Data Sanitization Platform

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20App-lightgrey?style=flat-square&logo=flask)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Prototype-orange?style=flat-square)
![Standards](https://img.shields.io/badge/NIST%20SP%20800--88-Compliant-blue?style=flat-square)
---

> Built by **Team TechnoGreen** · BMIT Solapur · Presented at Uddyam Idea Hackathon 2026, PAH Solapur University
---

## 📚 Table of Contents

- [The VAJRA Algorithm](#-the-vajra-algorithm)
- [Comparison Table](#-comparison-vajra-vs-standard-methods)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Prerequisites](#-prerequisites--installation)
- [Standards Implemented](#-standards-implemented)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [System Architecture](#-how-it-works-system-architecture)
- [How VAJRA Works](#-how-vajra-works-technical)
- [Mathematical Model](#-mathematical-model)
- [Certificate](#-certificate-sample)
- [Recognition](#-recognition)
- [Roadmap](#-roadmap--future-enhancements)
- [Disclaimer](#-disclaimer)
- [License](#-license)
---

## 🔍 About

**SecureWipe Pro** is an open-source, hardware-level data sanitization platform built in Python and Flask.  
It goes beyond simple file deletion — permanently destroying data at the bit level on HDDs, SSDs, NVMe, and USB drives,  
making forensic recovery computationally infeasible.
---

## 🧠 The VAJRA Algorithm

**VAJRA** — *Verified Adaptive Junk-data Removal Algorithm* — is an indigenously designed data sanitization algorithm at the core of SecureWipe Pro.

Unlike standard wipe methods, VAJRA uses **Logistic Map chaos theory** to generate unpredictable, non-repeating overwrite patterns, combined with **Shannon Entropy verification** to mathematically confirm that all original data has been destroyed.
```
Standard wiping:   0x00 → 0xFF → 0x00  (predictable, reversible)
VAJRA wiping:      chaos-generated patterns → entropy verified → certificate issued
```
**Why it matters:** Predictable patterns can potentially be reversed with forensic tools. VAJRA's chaotic overwrite patterns make data recovery computationally infeasible.
---

## 📊 Comparison: VAJRA vs. Standard Methods

| Method | Pattern Type | Recoverability | Verification |
| :--- | :--- | :--- | :--- |
| **Zero Fill** | Static (0x00) | Possible (Magnetic Trace) | None |
