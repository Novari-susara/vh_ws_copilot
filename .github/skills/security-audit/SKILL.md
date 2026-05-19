---
name: security-audit
description: "Runs a comprehensive security audit on Python code. Checks OWASP Top 10, finds hardcoded secrets, reviews auth flows, and generates a findings report."
---

# Security Audit Skill

You are a security expert conducting a systematic audit of a Python FastAPI codebase.

## Audit Steps

### Step 1: Discover Entry Points
Use #tool:read to find all route definitions:
```bash
grep -r "@router\.\|@app\." src/ --include="*.py" -l
```
For each router file, identify endpoints that lack `Depends(get_current_user)`.

### Step 2: Check Authentication
Read `src/utils/auth.py` and `src/services/auth_service.py`:
- Is `SECRET_KEY` from environment variables?
- Is token algorithm pinned (not `algorithms=["HS256", "none"]`)?
- Are expired tokens rejected?

### Step 3: Scan for Hardcoded Secrets
```bash
grep -rn "password\|secret\|token\|api_key\|apikey" src/ --include="*.py" -i | grep -v "os.getenv\|os.environ\|#"
```

### Step 4: Check Input Validation
- Verify all endpoints accept Pydantic models (not raw dicts)
- Check for any `request.body()` usage without parsing
- Look for any SQL string concatenation

### Step 5: Review Logging
```bash
grep -rn "logger\.\|logging\." src/ --include="*.py"
```
Ensure no passwords, tokens, or PII appear in log statements.

### Step 6: CORS Configuration
Read `src/main.py` — check `CORSMiddleware` configuration:
- `allow_origins=["*"]` is dangerous in production
- `allow_credentials=True` with wildcard origin is a security hole

## Report Template
Save findings to `docs/security-audit-{date}.md`:

```markdown
# Security Audit Report
**Date:** {date}
**Project:** TaskManager API
**Auditor:** Copilot Security Audit Skill

## Executive Summary
{2-3 sentence summary}

## Findings

### CRITICAL Issues
{list}

### HIGH Issues  
{list}

### MEDIUM Issues
{list}

### LOW Issues / Recommendations
{list}

## OWASP Coverage
| Category | Status | Notes |
|----------|--------|-------|
| A01: Broken Access Control | ✅/⚠️/❌ | |
| A02: Cryptographic Failures | | |
| A03: Injection | | |
| A05: Security Misconfiguration | | |
| A07: Auth Failures | | |

## Recommendations
{prioritized action list}
```

## Usage
Invoke this skill when asked to "run a security audit", "check for vulnerabilities",
or "security review the codebase".
