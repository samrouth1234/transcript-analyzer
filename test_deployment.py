#!/usr/bin/env python3
"""
Test script for the YouTube Transcript API
Run this to test if your deployment is working correctly
"""

import requests

def test_local():
    """Test the local development server"""
    print("Testing local development server...")
    try:
        # Test health endpoint
        response = requests.get("http://localhost:5000/api/v1/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print("❌ Health check failed")
            
        # Test transcript endpoint
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll for testing
        payload = {"url": test_url}
        
        response = requests.post(
            "http://localhost:5000/api/v1/transcript",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Transcript endpoint working")
            data = response.json()
            print(f"Video title: {data.get('title', 'Unknown')}")
        else:
            print(f"❌ Transcript endpoint failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error testing local server: {e}")

def test_production(base_url):
    """Test the production deployment"""
    print(f"Testing production deployment at {base_url}...")
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/api/v1/health")
        if response.status_code == 200:
            print("✅ Production health check passed")
        else:
            print("❌ Production health check failed")
            
        # Test transcript endpoint
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        payload = {"url": test_url}
        
        response = requests.post(
            f"{base_url}/api/v1/transcript",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Production transcript endpoint working")
            data = response.json()
            print(f"Video title: {data.get('title', 'Unknown')}")
        else:
            print(f"❌ Production transcript endpoint failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error testing production: {e}")

if __name__ == "__main__":
    print("YouTube Transcript API Test Script")
    print("=" * 40)
    
    # Test local
    test_local()
    print()
    
    # Test production (replace with your Vercel URL)
    production_url = input("Enter your production URL (or press Enter to skip): ").strip()
    if production_url:
        test_production(production_url)
