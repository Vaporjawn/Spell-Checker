"""
Test script for API integration
Tests the /api/check endpoint with various inputs
"""

import requests
import json


def test_local_api(base_url="http://localhost:5000"):
    """Test the local API endpoint"""
    print(f"\n🧪 Testing API at {base_url}")
    print("=" * 60)

    # Test 1: Health check
    print("\n1. Testing health check endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        assert response.status_code == 200
        print("   ✅ Health check passed!")
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return False

    # Test 2: Simple spell check
    print("\n2. Testing simple spell check...")
    test_cases = [
        {"input": "teh quik brown fox", "description": "Common typos"},
        {"input": "This is sampl text with erors", "description": "Multiple errors"},
        {"input": "correct spelling already", "description": "Already correct text"},
        {"input": "speling mistke exampl", "description": "Various spelling mistakes"},
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\n   Test Case {i}: {test['description']}")
        print(f"   Input: '{test['input']}'")

        try:
            response = requests.post(
                f"{base_url}/api/check",
                json={"text": test["input"]},
                headers={"Content-Type": "application/json"},
                timeout=5,
            )

            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"   Original: '{data.get('original', 'N/A')}'")
                print(f"   Corrected: '{data.get('corrected', 'N/A')}'")
                print(f"   Has corrections: {data.get('has_corrections', False)}")

                if data.get("success"):
                    print("   ✅ Test passed!")
                else:
                    print(f"   ❌ Test failed: {data.get('error')}")
            else:
                print(f"   ❌ HTTP Error: {response.text}")

        except Exception as e:
            print(f"   ❌ Request failed: {e}")

    # Test 3: Error handling
    print("\n3. Testing error handling...")

    # Empty text
    print("\n   Test: Empty text")
    try:
        response = requests.post(
            f"{base_url}/api/check",
            json={"text": ""},
            headers={"Content-Type": "application/json"},
            timeout=5,
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        assert response.status_code == 400
        print("   ✅ Empty text handling works!")
    except Exception as e:
        print(f"   ❌ Test failed: {e}")

    # Missing text field
    print("\n   Test: Missing text field")
    try:
        response = requests.post(
            f"{base_url}/api/check",
            json={},
            headers={"Content-Type": "application/json"},
            timeout=5,
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        assert response.status_code == 400
        print("   ✅ Missing field handling works!")
    except Exception as e:
        print(f"   ❌ Test failed: {e}")

    # Very long text
    print("\n   Test: Very long text (10,001 chars)")
    try:
        long_text = "a" * 10001
        response = requests.post(
            f"{base_url}/api/check",
            json={"text": long_text},
            headers={"Content-Type": "application/json"},
            timeout=5,
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        assert response.status_code == 400
        print("   ✅ Length limit handling works!")
    except Exception as e:
        print(f"   ❌ Test failed: {e}")

    print("\n" + "=" * 60)
    print("✅ All API integration tests completed!")
    print("\n📝 Next steps:")
    print("   1. Ensure Flask server is running: python main.py")
    print("   2. Test frontend by opening docs/index.html")
    print("   3. Check browser console for API connection status")
    print("   4. Try entering text and clicking 'Check Spelling'")

    return True


if __name__ == "__main__":
    print("\n🚀 API Integration Test Suite")
    print("=" * 60)
    print("\n⚠️  Prerequisites:")
    print("   - Flask server must be running on localhost:5000")
    print("   - Run: python main.py")
    print("\n" + "=" * 60)

    input("\nPress Enter to start tests (or Ctrl+C to cancel)...")

    try:
        test_local_api()
    except KeyboardInterrupt:
        print("\n\n❌ Tests cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Test suite failed: {e}")
