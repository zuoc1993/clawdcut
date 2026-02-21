#!/usr/bin/env python3
"""Test Pixabay Audio API diagnostic script."""

import os
import sys

# Step 1: Check environment variable
print("=" * 60)
print("STEP 1: Checking PIXABAY_API_KEY environment variable")
print("=" * 60)

api_key = os.environ.get("PIXABAY_API_KEY", "")
if api_key:
    print(f"✓ PIXABAY_API_KEY is SET")
    print(f"  First 3 characters: {api_key[:3]}...")
    print(f"  Full length: {len(api_key)} characters")
else:
    print("✗ PIXABAY_API_KEY is NOT SET")
    print("  Please set the environment variable before running this test.")

print()

# Step 2: Test Pixabay Audio API
print("=" * 60)
print("STEP 2: Testing Pixabay Audio API")
print("=" * 60)

if not api_key:
    print("Skipping API test - no API key available")
    sys.exit(1)

import httpx

url = "https://pixabay.com/api/audio/"
params = {"key": api_key, "q": "music", "per_page": 3}

print(f"Request URL: {url}")
print(f"Parameters: {params}")
print()

try:
    resp = httpx.get(url, params=params, timeout=30.0)
    print(f"Status Code: {resp.status_code}")
    print(f"Response Headers: {dict(resp.headers)}")
    print()
    print(f"Response Body (first 500 chars):")
    print("-" * 40)
    print(resp.text[:500])
    print("-" * 40)
except Exception as e:
    print(f"Error during request: {e}")

print()

# Step 3: Try alternative approach - without params in URL
print("=" * 60)
print("STEP 3: Trying alternative - direct URL with key")
print("=" * 60)

alt_url = f"https://pixabay.com/api/audio/?key={api_key}&q=music&per_page=3"
print(f"Alternative URL: {alt_url[:80]}...")

try:
    resp2 = httpx.get(alt_url, timeout=30.0)
    print(f"Status Code: {resp2.status_code}")
    print(f"Response Body (first 500 chars):")
    print("-" * 40)
    print(resp2.text[:500])
    print("-" * 40)
except Exception as e:
    print(f"Error during alternative request: {e}")

print()

# Step 4: Try the main Pixabay API (images) to compare
print("=" * 60)
print("STEP 4: Testing Pixabay Image API (for comparison)")
print("=" * 60)

image_url = "https://pixabay.com/api/"
image_params = {"key": api_key, "q": "nature", "per_page": 3}

try:
    resp3 = httpx.get(image_url, params=image_params, timeout=30.0)
    print(f"Status Code: {resp3.status_code}")
    print(f"Response Body (first 500 chars):")
    print("-" * 40)
    print(resp3.text[:500])
    print("-" * 40)
except Exception as e:
    print(f"Error during image API request: {e}")
