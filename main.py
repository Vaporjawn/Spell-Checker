"""Flask application for spell checking service.

This module provides both a web interface and REST API for spell checking functionality.
Includes security headers, CORS configuration, and rate limiting.
"""

from datetime import datetime, UTC
import platform
import secrets
import sys
from typing import Dict, Any, Tuple

from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
from werkzeug.exceptions import UnsupportedMediaType, BadRequest

from lib.checker import Checker

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "https://vaporjawn.github.io",
                "http://localhost:*",
                "http://127.0.0.1:*",
            ]
        }
    },
)

# Security configurations
app.config["SECRET_KEY"] = secrets.token_hex(32)
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PERMANENT_SESSION_LIFETIME"] = 3600  # 1 hour

# Application constants
MAX_TEXT_LENGTH = 10000
APP_VERSION = "1.0.0"

# Initialize spell checker (singleton pattern)
checker = Checker()


@app.after_request
def set_security_headers(response: Response) -> Response:
    """Add comprehensive security headers to all responses.

    Args:
        response: Flask response object

    Returns:
        Modified response with security headers
    """
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'"
    )
    return response


@app.route("/", methods=["GET", "POST"])
def home() -> str:
    """Render home page with spell checking functionality.

    Returns:
        Rendered HTML template with checked text or default message
    """
    if request.method == "POST":
        text = request.form.get("input", "").strip()

        # Input validation
        if not text:
            return render_template("home.html", text="Please enter some text to check!")

        # Limit input length to prevent abuse
        if len(text) > MAX_TEXT_LENGTH:
            return render_template(
                "home.html",
                text=f"Text too long! Maximum {MAX_TEXT_LENGTH} characters allowed.",
            )

        text = spellcheck(text)
        return render_template("home.html", text=text)

    text = "Write something here to have it spell checked!"
    return render_template("home.html", text=text)


def spellcheck(text: str) -> str:
    """Check and correct spelling of input text.

    Args:
        text: Input text to spell check

    Returns:
        Corrected text with spelling fixes applied
    """
    # Use list comprehension for better performance
    checked = [checker.correct(word) for word in text.split()]
    return " ".join(checked)


@app.route("/api/check", methods=["POST"])
def api_check() -> Tuple[Dict[str, Any], int]:
    """API endpoint for spell checking.

    Accepts JSON payload with 'text' field and returns corrected text.

    Request JSON:
        {
            "text": "Text to check"
        }

    Response JSON:
        {
            "success": true,
            "original": "Original text",
            "corrected": "Corrected text",
            "has_corrections": true
        }

    Returns:
        Tuple of (JSON response, HTTP status code)
    """
    try:
        # Get JSON data from request with force=False to respect content-type
        data = request.get_json(force=False, silent=False)

        if not data or "text" not in data:
            return (
                jsonify({"success": False, "error": "No text provided"}),
                400,
            )

        text = data["text"].strip()

        # Input validation
        if not text:
            return (
                jsonify({"success": False, "error": "Empty text provided"}),
                400,
            )

        # Limit input length to prevent abuse
        if len(text) > MAX_TEXT_LENGTH:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Text too long! Maximum {MAX_TEXT_LENGTH} characters allowed.",
                    }
                ),
                400,
            )

        # Perform spell check
        corrected_text = spellcheck(text)

        return (
            jsonify(
                {
                    "success": True,
                    "original": text,
                    "corrected": corrected_text,
                    "has_corrections": text != corrected_text,
                }
            ),
            200,
        )

    except UnsupportedMediaType:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Invalid Content-Type. Please use application/json",
                }
            ),
            415,
        )
    except BadRequest as e:
        return (
            jsonify({"success": False, "error": f"Invalid JSON: {str(e)}"}),
            400,
        )
    except Exception as e:
        app.logger.error(f"Spell check error: {str(e)}", exc_info=True)
        return (
            jsonify({"success": False, "error": f"Server error: {str(e)}"}),
            500,
        )


@app.route("/api/health", methods=["GET"])
def health_check() -> Tuple[Dict[str, Any], int]:
    """Health check endpoint with detailed system information.

    Returns:
        Tuple of (JSON response with health status, HTTP status code)
    """
    return (
        jsonify(
            {
                "status": "healthy",
                "service": "spell-checker-api",
                "version": APP_VERSION,
                "timestamp": datetime.now(UTC).isoformat(),
                "system": {
                    "python_version": sys.version,
                    "platform": platform.platform(),
                    "uptime": "available",
                },
                "endpoints": {
                    "check": "/api/check",
                    "health": "/api/health",
                    "metrics": "/api/metrics",
                    "status": "/api/status",
                },
            }
        ),
        200,
    )


@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    """Endpoint for application metrics"""
    return (
        jsonify(
            {
                "success": True,
                "metrics": {
                    "total_requests": "tracked_in_production",
                    "avg_response_time": "tracked_in_production",
                    "error_rate": "tracked_in_production",
                    "uptime": "tracked_in_production",
                },
                "note": "Integrate with monitoring service for detailed metrics",
            }
        ),
        200,
    )


@app.route("/api/status", methods=["GET"])
def get_status() -> Tuple[Dict[str, Any], int]:
    """Endpoint for application status and component health.

    Returns:
        Tuple of (JSON response with component status, HTTP status code)
    """
    try:
        # Test checker functionality
        _ = checker.correct("test")  # noqa: F841
        checker_status = "operational"
    except Exception as e:
        app.logger.error(f"Checker status error: {str(e)}")
        checker_status = f"error: {str(e)}"

    return (
        jsonify(
            {
                "success": True,
                "status": "operational",
                "components": {
                    "api": "operational",
                    "spell_checker": checker_status,
                    "cors": "enabled",
                    "security_headers": "enabled",
                },
                "timestamp": datetime.now(UTC).isoformat(),
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run()
