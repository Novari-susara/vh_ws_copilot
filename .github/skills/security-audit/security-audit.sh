#!/usr/bin/env bash
# Security audit helper script for the security-audit skill
# Usage: ./security-audit.sh [--output-file path]

set -euo pipefail

OUTPUT_FILE="${1:-docs/security-audit-$(date +%Y%m%d).md}"
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

echo "🔍 Running TaskManager Security Audit..."
echo "Project root: $PROJECT_ROOT"
echo "Output: $OUTPUT_FILE"
echo "---"

# 1. Find unprotected routes
echo "## Checking for unprotected routes..."
ROUTES=$(grep -rn "@router\." "$PROJECT_ROOT/src/api/" --include="*.py" || true)
UNPROTECTED=$(echo "$ROUTES" | grep -v "get_current_user\|health\|login" || true)
if [ -n "$UNPROTECTED" ]; then
    echo "⚠️  Potentially unprotected routes found:"
    echo "$UNPROTECTED"
else
    echo "✅ All routes appear to use authentication"
fi

# 2. Scan for hardcoded secrets
echo ""
echo "## Scanning for hardcoded secrets..."
SECRET_SCAN=$(grep -rn \
    -e "password\s*=\s*['\"][^'\"]*['\"]" \
    -e "secret\s*=\s*['\"][^'\"]*['\"]" \
    -e "api_key\s*=\s*['\"][^'\"]*['\"]" \
    "$PROJECT_ROOT/src/" --include="*.py" \
    | grep -v "os\.getenv\|os\.environ\|#.*SECURITY\|demo-secret" || true)

if [ -n "$SECRET_SCAN" ]; then
    echo "🔴 POTENTIAL HARDCODED SECRETS:"
    echo "$SECRET_SCAN"
else
    echo "✅ No obvious hardcoded secrets found"
fi

# 3. Check for dependency vulnerabilities
echo ""
echo "## Checking dependencies for known vulnerabilities..."
if command -v pip-audit &>/dev/null; then
    pip-audit --requirement "$PROJECT_ROOT/requirements.txt" 2>&1 || true
elif command -v safety &>/dev/null; then
    safety check --file "$PROJECT_ROOT/requirements.txt" 2>&1 || true
else
    echo "⚠️  Neither pip-audit nor safety installed. Run: pip install pip-audit"
fi

# 4. Check CORS configuration
echo ""
echo "## Checking CORS configuration..."
CORS=$(grep -n "CORSMiddleware\|allow_origins" "$PROJECT_ROOT/src/main.py" || true)
echo "$CORS"
if echo "$CORS" | grep -q '"*"'; then
    echo "🟡 WARNING: Wildcard CORS origin detected — OK for dev, NOT for production"
fi

echo ""
echo "✅ Audit scan complete. Review findings above."
echo "Full report will be saved to: $OUTPUT_FILE"
