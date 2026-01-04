#!/usr/bin/env python3
"""
Test script for Semantic Search Engine
Tests all API endpoints and validates functionality
"""

import requests
import time
import os
from pathlib import Path

BASE_URL = "http://localhost:8000"
SAMPLE_DOCS_DIR = "sample_documents"

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def test_server_running():
    """Test if server is running"""
    print_header("Testing Server Connection")
    try:
        response = requests.get(f"{BASE_URL}/stats", timeout=5)
        if response.status_code == 200:
            print_success("Server is running!")
            return True
        else:
            print_error(f"Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Cannot connect to server: {e}")
        print_info("Make sure the server is running: python main.py")
        return False

def test_upload_documents():
    """Test document upload functionality"""
    print_header("Testing Document Upload")
    
    if not os.path.exists(SAMPLE_DOCS_DIR):
        print_error(f"Sample documents directory not found: {SAMPLE_DOCS_DIR}")
        return False
    
    sample_files = list(Path(SAMPLE_DOCS_DIR).glob("*.txt"))
    
    if len(sample_files) == 0:
        print_error("No sample .txt files found")
        return False
    
    print_info(f"Found {len(sample_files)} sample documents")
    
    uploaded = 0
    for file_path in sample_files:
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.name, f, 'text/plain')}
                response = requests.post(f"{BASE_URL}/upload", files=files)
                
                if response.status_code == 200:
                    print_success(f"Uploaded: {file_path.name}")
                    uploaded += 1
                else:
                    print_error(f"Failed to upload {file_path.name}: {response.json()}")
        except Exception as e:
            print_error(f"Error uploading {file_path.name}: {e}")
    
    print_info(f"Successfully uploaded {uploaded}/{len(sample_files)} documents")
    return uploaded >= 5

def test_get_stats():
    """Test statistics endpoint"""
    print_header("Testing Statistics Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/stats")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Total documents: {data['total_documents']}")
            print_info(f"Index ready: {data['index_ready']}")
            print_info(f"Documents: {', '.join(data['document_names'])}")
            return data['total_documents'] >= 5
        else:
            print_error(f"Stats request failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error getting stats: {e}")
        return False

def test_search():
    """Test search functionality"""
    print_header("Testing Search Functionality")
    
    test_queries = [
        "machine learning and neural networks",
        "web development frameworks",
        "database management systems",
        "cloud computing and AWS",
        "python programming"
    ]
    
    successful_searches = 0
    
    for query in test_queries:
        print_info(f"Searching: '{query}'")
        try:
            response = requests.post(
                f"{BASE_URL}/search",
                json={"query": query, "top_k": 3}
            )
            
            if response.status_code == 200:
                results = response.json()
                print_success(f"Found {len(results)} results")
                
                for i, result in enumerate(results, 1):
                    score = result['similarity_score'] * 100
                    print(f"  {i}. {result['document_name']} - {score:.1f}% similar")
                
                successful_searches += 1
            else:
                print_error(f"Search failed: {response.json()}")
        except Exception as e:
            print_error(f"Search error: {e}")
        
        time.sleep(0.5)  # Small delay between requests
    
    print_info(f"Successful searches: {successful_searches}/{len(test_queries)}")
    return successful_searches == len(test_queries)

def test_semantic_search():
    """Test that semantic search actually works (not just keyword matching)"""
    print_header("Testing Semantic Understanding")
    
    # This query doesn't contain exact keywords but should find AI doc
    query = "neural networks and deep learning algorithms"
    
    print_info(f"Query: '{query}'")
    print_info("Expected: Should find artificial_intelligence.txt as top result")
    
    try:
        response = requests.post(
            f"{BASE_URL}/search",
            json={"query": query, "top_k": 3}
        )
        
        if response.status_code == 200:
            results = response.json()
            
            if len(results) > 0:
                top_result = results[0]
                
                if "artificial_intelligence" in top_result['document_name'].lower():
                    print_success("✨ Semantic search working correctly!")
                    print_info(f"Top result: {top_result['document_name']}")
                    print_info(f"Similarity: {top_result['similarity_score']*100:.1f}%")
                    return True
                else:
                    print_error(f"Expected AI doc, got: {top_result['document_name']}")
                    return False
            else:
                print_error("No results returned")
                return False
        else:
            print_error(f"Search failed: {response.json()}")
            return False
    except Exception as e:
        print_error(f"Test error: {e}")
        return False

def test_clear_documents():
    """Test clearing all documents"""
    print_header("Testing Clear Functionality")
    
    try:
        response = requests.delete(f"{BASE_URL}/clear")
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Documents cleared: {data['status']}")
            
            # Verify it's actually cleared
            stats_response = requests.get(f"{BASE_URL}/stats")
            if stats_response.status_code == 200:
                stats = stats_response.json()
                if stats['total_documents'] == 0:
                    print_success("Verification: All documents cleared")
                    return True
                else:
                    print_error(f"Documents still exist: {stats['total_documents']}")
                    return False
        else:
            print_error(f"Clear failed: {response.json()}")
            return False
    except Exception as e:
        print_error(f"Clear error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "🧪 SEMANTIC SEARCH ENGINE - TEST SUITE".center(60))
    print("=" * 60)
    
    tests = [
        ("Server Connection", test_server_running),
        ("Document Upload", test_upload_documents),
        ("Statistics", test_get_stats),
        ("Basic Search", test_search),
        ("Semantic Search", test_semantic_search),
        ("Clear Documents", test_clear_documents),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print_error(f"Test '{test_name}' crashed: {e}")
            results[test_name] = False
        
        time.sleep(0.5)
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "-" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("🎉 All tests passed! Your search engine is working perfectly!")
    else:
        print_error(f"⚠️  {total - passed} test(s) failed. Check the output above.")
    
    print("=" * 60 + "\n")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
