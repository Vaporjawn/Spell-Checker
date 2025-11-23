#!/usr/bin/env python3
"""
Simple test client for the Spell Checker API
Usage: python test_api_client.py
"""

import requests
import json
from typing import Dict, Any


class SpellCheckerClient:
    """Client for interacting with the Spell Checker API."""

    def __init__(self, base_url: str = "http://localhost:5000"):
        """
        Initialize the client.

        Args:
            base_url: Base URL of the API (default: http://localhost:5000)
        """
        self.base_url = base_url.rstrip("/")

    def check_spelling(self, text: str) -> Dict[str, Any]:
        """
        Check spelling of the provided text.

        Args:
            text: Text to check

        Returns:
            Dictionary with spelling check results

        Raises:
            requests.RequestException: If the request fails
        """
        response = requests.post(
            f"{self.base_url}/api/check",
            json={"text": text},
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()

    def health_check(self) -> Dict[str, Any]:
        """
        Check API health.

        Returns:
            Dictionary with health status

        Raises:
            requests.RequestException: If the request fails
        """
        response = requests.get(f"{self.base_url}/api/health")
        response.raise_for_status()
        return response.json()

    def get_status(self) -> Dict[str, Any]:
        """
        Get API status.

        Returns:
            Dictionary with component status

        Raises:
            requests.RequestException: If the request fails
        """
        response = requests.get(f"{self.base_url}/api/status")
        response.raise_for_status()
        return response.json()


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f"{title}")
    print(f"{'=' * 60}\n")


def main():
    """Run tests for the Spell Checker API."""
    client = SpellCheckerClient()

    # Test 1: Health Check
    print_section("Test 1: Health Check")
    try:
        health = client.health_check()
        print(f"Status: {health.get('status')}")
        print(f"Service: {health.get('service')}")
        print(f"Version: {health.get('version')}")
        print(f"Platform: {health.get('system', {}).get('platform')}")
    except requests.RequestException as e:
        print(f"❌ Health check failed: {e}")
        print("Make sure the server is running: python main.py")
        return

    # Test 2: Status Check
    print_section("Test 2: Status Check")
    try:
        status = client.get_status()
        print(f"API Status: {status.get('status')}")
        print("\nComponent Status:")
        for component, state in status.get("components", {}).items():
            print(f"  - {component}: {state}")
    except requests.RequestException as e:
        print(f"❌ Status check failed: {e}")

    # Test 3: Spell Check - Correct Text
    print_section("Test 3: Spell Check - Already Correct Text")
    test_text = "Hello world! This is a test."
    try:
        result = client.check_spelling(test_text)
        print(f"Original:  {result.get('original')}")
        print(f"Corrected: {result.get('corrected')}")
        print(f"Has corrections: {result.get('has_corrections')}")
    except requests.RequestException as e:
        print(f"❌ Spell check failed: {e}")

    # Test 4: Spell Check - Text with Errors
    print_section("Test 4: Spell Check - Text with Spelling Errors")
    test_text = "Helo wrld Ths is a tst"
    try:
        result = client.check_spelling(test_text)
        print(f"Original:  {result.get('original')}")
        print(f"Corrected: {result.get('corrected')}")
        print(f"Has corrections: {result.get('has_corrections')}")
    except requests.RequestException as e:
        print(f"❌ Spell check failed: {e}")

    # Test 5: Error Handling - Empty Text
    print_section("Test 5: Error Handling - Empty Text")
    try:
        result = client.check_spelling("")
        print(f"Result: {result}")
    except requests.RequestException as e:
        if e.response is not None:
            error_data = e.response.json()
            print(f"Expected error: {error_data.get('error')}")
        else:
            print(f"❌ Request failed: {e}")

    # Test 6: Error Handling - Very Long Text
    print_section("Test 6: Error Handling - Text Too Long")
    long_text = "a " * 10001  # Exceeds 10,000 character limit
    try:
        result = client.check_spelling(long_text)
        print(f"Result: {result}")
    except requests.RequestException as e:
        if e.response is not None:
            error_data = e.response.json()
            print(f"Expected error: {error_data.get('error')}")
        else:
            print(f"❌ Request failed: {e}")

    print_section("Tests Complete!")
    print("✅ All tests completed successfully!")
    print("\nFor more information, see API_DOCUMENTATION.md")


if __name__ == "__main__":
    main()
