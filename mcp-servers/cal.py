"""
Calculator MCP Server — HTTP (Streamable HTTP transport)
=========================================================
Student-focused calculator server that exposes arithmetic and math
operations as MCP tools over HTTP.

Protocol : MCP Streamable HTTP (protocol version 2024-11-05)
Transport: { "url": "http://localhost:8004/mcp", "type": "http" }

Requirements:
    pip install mcp fastapi uvicorn

Run:
    python mcp-servers/cal.py
    OR: uvicorn mcp-servers.cal:mcp --port 8004

Tools available:
    add, subtract, multiply, divide, power, sqrt,
    modulo, factorial, percentage, subtract_many
"""

import math

from mcp.server.fastmcp import FastMCP

# Server is reachable at http://127.0.0.1:8004/mcp
mcp = FastMCP("calculator", host="127.0.0.1", port=8004, streamable_http_path="/mcp")


# ── Basic Arithmetic ──────────────────────────────────────────────────────────


@mcp.tool()
def add(a: float, b: float) -> str:
    """Add two numbers together (a + b)."""
    result = a + b
    return f"{a} + {b} = {result}"


@mcp.tool()
def subtract(a: float, b: float) -> str:
    """Subtract b from a (a - b)."""
    result = a - b
    return f"{a} - {b} = {result}"


@mcp.tool()
def multiply(a: float, b: float) -> str:
    """Multiply two numbers (a × b)."""
    result = a * b
    return f"{a} × {b} = {result}"


@mcp.tool()
def divide(a: float, b: float) -> str:
    """Divide a by b (a ÷ b). Raises an error if b is zero."""
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    result = a / b
    return f"{a} ÷ {b} = {result}"


# ── Advanced Operations ───────────────────────────────────────────────────────


@mcp.tool()
def power(base: float, exponent: float) -> str:
    """Raise base to the power of exponent (base ^ exponent)."""
    result = base**exponent
    return f"{base} ^ {exponent} = {result}"


@mcp.tool()
def sqrt(number: float) -> str:
    """Calculate the square root of a non-negative number (√number)."""
    if number < 0:
        raise ValueError("Cannot take the square root of a negative number")
    result = math.sqrt(number)
    return f"√{number} = {result}"


@mcp.tool()
def modulo(a: float, b: float) -> str:
    """Return the remainder when a is divided by b (a mod b)."""
    if b == 0:
        raise ValueError("Modulo by zero is not allowed")
    result = a % b
    return f"{a} mod {b} = {result}"


@mcp.tool()
def factorial(n: int) -> str:
    """
    Calculate the factorial of a non-negative integer n (n!).
    Allowed range: 0 – 20.

    Examples: factorial(5) → 5! = 120
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n > 20:
        raise ValueError("Input too large — maximum allowed value is 20")
    result = math.factorial(n)
    return f"{n}! = {result}"


@mcp.tool()
def percentage(value: float, percent: float) -> str:
    """
    Calculate what percent% of value is.

    Example: percentage(150, 20) → 20% of 150 = 30.0
    """
    result = round((value * percent) / 100, 6)
    return f"{percent}% of {value} = {result}"


@mcp.tool()
def subtract_many(numbers: list[float]) -> str:
    """
    Subtract all subsequent numbers from the first.

    Example: subtract_many([10, 3, 2]) → 10 - 3 - 2 = 5.0
    """
    if not numbers:
        raise ValueError("numbers list must not be empty")
    result = numbers[0]
    for n in numbers[1:]:
        result -= n
    expression = " - ".join(str(n) for n in numbers)
    return f"{expression} = {result}"


# ── Resource: server info ─────────────────────────────────────────────────────


@mcp.resource("info://server")
def server_info() -> str:
    """Return basic info about this MCP server."""
    return (
        "Calculator MCP Server | HTTP Streamable transport\n"
        "Endpoint : http://127.0.0.1:8004/mcp\n"
        "Tools    : add, subtract, multiply, divide, power, "
        "sqrt, modulo, factorial, percentage, subtract_many"
    )


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
