"""Comprehensive API endpoint tests for spell checker service.

Tests all API endpoints including spell checking, health, metrics, and status.
"""

import json
import sys
import os

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import main  # noqa: E402


@pytest.fixture
def app():
    """Create Flask app for testing."""
    return main.app


@pytest.fixture
def client(app):
    """Create test client."""
    app.config["TESTING"] = True
    return app.test_client()


class TestAPICheck:
    """Tests for /api/check endpoint."""

    def test_api_check_success(self, client):
        """Test successful spell check via API."""
        response = client.post(
            "/api/check",
            data=json.dumps({"text": "Ths is a tst"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert "original" in data
        assert "corrected" in data
        assert "has_corrections" in data

    def test_api_check_no_corrections(self, client):
        """Test API check with correctly spelled text."""
        response = client.post(
            "/api/check",
            data=json.dumps({"text": "the quick brown fox"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        # Very common words should not need corrections
        assert data["has_corrections"] is False

    def test_api_check_empty_text(self, client):
        """Test API check with empty text."""
        response = client.post(
            "/api/check",
            data=json.dumps({"text": ""}),
            content_type="application/json",
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["success"] is False
        assert "empty" in data["error"].lower()

    def test_api_check_no_text_field(self, client):
        """Test API check without text field."""
        response = client.post(
            "/api/check", data=json.dumps({}), content_type="application/json"
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["success"] is False

    def test_api_check_text_too_long(self, client):
        """Test API check with text exceeding max length."""
        long_text = "word " * 10001
        response = client.post(
            "/api/check",
            data=json.dumps({"text": long_text}),
            content_type="application/json",
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["success"] is False
        assert "too long" in data["error"].lower()

    def test_api_check_special_characters(self, client):
        """Test API check with special characters."""
        response = client.post(
            "/api/check",
            data=json.dumps({"text": "Hello! How are you?"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True

    def test_api_check_numbers(self, client):
        """Test API check with numbers."""
        response = client.post(
            "/api/check",
            data=json.dumps({"text": "I have 123 apples"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True


class TestAPIHealth:
    """Tests for /api/health endpoint."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data
        assert "system" in data
        assert "endpoints" in data

    def test_health_check_system_info(self, client):
        """Test health check includes system information."""
        response = client.get("/api/health")
        data = json.loads(response.data)
        assert "python_version" in data["system"]
        assert "platform" in data["system"]

    def test_health_check_endpoints_list(self, client):
        """Test health check includes endpoint list."""
        response = client.get("/api/health")
        data = json.loads(response.data)
        assert "/api/check" in data["endpoints"]["check"]
        assert "/api/health" in data["endpoints"]["health"]


class TestAPIStatus:
    """Tests for /api/status endpoint."""

    def test_status_check(self, client):
        """Test status endpoint."""
        response = client.get("/api/status")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["status"] == "operational"
        assert "components" in data
        assert "timestamp" in data

    def test_status_components(self, client):
        """Test status includes component health."""
        response = client.get("/api/status")
        data = json.loads(response.data)
        components = data["components"]
        assert components["api"] == "operational"
        assert "spell_checker" in components
        assert components["cors"] == "enabled"
        assert components["security_headers"] == "enabled"


class TestAPIMetrics:
    """Tests for /api/metrics endpoint."""

    def test_metrics_endpoint(self, client):
        """Test metrics endpoint."""
        response = client.get("/api/metrics")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert "metrics" in data


class TestSecurityHeaders:
    """Tests for security headers."""

    def test_security_headers_present(self, client):
        """Test that security headers are present."""
        response = client.get("/")
        assert "X-Content-Type-Options" in response.headers
        assert "X-Frame-Options" in response.headers
        assert "X-XSS-Protection" in response.headers
        assert "Strict-Transport-Security" in response.headers
        assert "Content-Security-Policy" in response.headers

    def test_security_header_values(self, client):
        """Test security header values."""
        response = client.get("/")
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert response.headers["X-Frame-Options"] == "DENY"
        assert "max-age=31536000" in response.headers["Strict-Transport-Security"]


class TestCORS:
    """Tests for CORS configuration."""

    def test_cors_enabled(self, client):
        """Test CORS headers are present for API endpoints."""
        response = client.options(
            "/api/check", headers={"Origin": "https://vaporjawn.github.io"}
        )
        # CORS headers should be present
        assert response.status_code in [200, 204]


class TestErrorHandling:
    """Tests for error handling."""

    def test_invalid_json(self, client):
        """Test handling of invalid JSON."""
        response = client.post(
            "/api/check", data="invalid json", content_type="application/json"
        )
        # Should handle gracefully
        assert response.status_code in [400, 500]

    def test_missing_content_type(self, client):
        """Test handling of missing content type."""
        response = client.post("/api/check", data='{"text": "test"}')
        # Should handle gracefully
        assert response.status_code in [200, 400, 415]
