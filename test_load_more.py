#!/usr/bin/env python3
"""
Test script for Load More functionality
"""

import requests
import json

def test_load_more_api():
    """Test the load more videos API endpoint"""
    
    print("=" * 50)
    print("Testing Load More Videos API")
    print("=" * 50)
    
    # Test data
    test_data = {
        "topic": "Python Programming",
        "page": 1
    }
    
    try:
        # Test the load more endpoint
        response = requests.post(
            "http://localhost:5000/load-more-videos",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API call successful!")
            print(f"   Success: {data.get('success')}")
            print(f"   Videos returned: {len(data.get('videos', []))}")
            print(f"   Has more: {data.get('has_more')}")
            print(f"   Next page: {data.get('next_page')}")
            
            if data.get('videos'):
                print("\n📹 Sample videos:")
                for i, video in enumerate(data['videos'][:2], 1):
                    print(f"   {i}. {video['title'][:60]}...")
                    print(f"      Duration: {video['duration_mins']} min")
                    print(f"      Views: {video['views']:,}")
        else:
            print(f"❌ API call failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure the app is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error testing API: {e}")

def test_pagination():
    """Test pagination by making multiple requests"""
    
    print("\n" + "=" * 50)
    print("Testing Pagination")
    print("=" * 50)
    
    topic = "Machine Learning"
    
    for page in range(1, 4):  # Test 3 pages
        print(f"\n📄 Testing page {page}...")
        
        try:
            response = requests.post(
                "http://localhost:5000/load-more-videos",
                json={"topic": topic, "page": page},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Page {page}: {len(data.get('videos', []))} videos")
                print(f"   Has more: {data.get('has_more')}")
                
                if not data.get('has_more'):
                    print("   🎯 No more videos available")
                    break
            else:
                print(f"   ❌ Page {page} failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error on page {page}: {e}")

if __name__ == "__main__":
    test_load_more_api()
    test_pagination() 