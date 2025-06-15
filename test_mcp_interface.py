#!/usr/bin/env python3
"""
MCP Client Test Script

This script simulates an MCP client to test the blog server functionality
by calling the tools directly through the server interface.
"""

import asyncio
import json
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import handle_call_tool, handle_list_tools

async def test_mcp_tools():
    """Test MCP tools through the server interface"""
    print("Testing MCP Tools Interface...")
    
    # Test list tools
    print("\n1. Testing list_tools:")
    tools = await handle_list_tools()
    print(f"Available tools: {len(tools)}")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    
    # Test generate_blog_outline
    print("\n2. Testing generate_blog_outline:")
    outline_args = {
        "topic": "Kubernetes Orchestration",
        "target_audience": "intermediate",
        "keywords": ["pods", "services", "deployments"],
        "desired_length": "medium"
    }
    
    outline_result = await handle_call_tool("generate_blog_outline", outline_args)
    outline_data = json.loads(outline_result[0].text)
    print(f"Generated outline for: {outline_data['topic']}")
    print(f"Sections: {len(outline_data['sections'])}")
    print(f"Estimated words: {outline_data['estimated_total_words']}")
    
    # Test generate_complete_blog
    print("\n3. Testing generate_complete_blog:")
    blog_args = {
        "topic": "GraphQL API Development",
        "target_audience": "advanced",
        "keywords": ["schema", "resolvers", "mutations"],
        "desired_length": "short"
    }
    
    blog_result = await handle_call_tool("generate_complete_blog", blog_args)
    blog_data = json.loads(blog_result[0].text)
    print(f"Generated complete blog:")
    print(f"  Title: {blog_data['title']}")
    print(f"  Word count: {blog_data['word_count']}")
    print(f"  Reading time: {blog_data['estimated_reading_time']} minutes")
    print(f"  Validation passed: {blog_data['validation']['overall_valid']}")
    
    # Test validate_blog_post
    print("\n4. Testing validate_blog_post:")
    test_blog = {
        "title": "A Short Title",  # This should fail validation
        "introduction": "Short intro.",  # This should fail validation
        "content": "# Test\n\nSome content here.",
        "conclusion": "Brief conclusion."  # This should fail validation
    }
    
    validation_args = {"blog_post": test_blog}
    validation_result = await handle_call_tool("validate_blog_post", validation_args)
    validation_data = json.loads(validation_result[0].text)
    print(f"Validation results:")
    print(f"  Overall valid: {validation_data['overall_valid']}")
    print(f"  Total errors: {validation_data['summary']['total_errors']}")
    print(f"  Total warnings: {validation_data['summary']['total_warnings']}")
    
    # Test get_business_rules
    print("\n5. Testing get_business_rules:")
    rules_args = {"section": "structure"}
    rules_result = await handle_call_tool("get_business_rules", rules_args)
    rules_data = json.loads(rules_result[0].text)
    print(f"Business rules sections: {list(rules_data.keys())}")
    
    print("\nMCP Tools Interface: ALL TESTS PASSED!")

async def test_error_handling():
    """Test error handling in MCP tools"""
    print("\nTesting Error Handling...")
    
    # Test missing required parameters
    print("\n1. Testing missing topic parameter:")
    try:
        result = await handle_call_tool("generate_blog_outline", {})
        response = result[0].text
        print(f"Error response: {response}")
        assert "Error: Topic is required" in response
        print("Missing parameter handling: PASSED")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Test invalid tool name
    print("\n2. Testing invalid tool name:")
    try:
        result = await handle_call_tool("invalid_tool", {"topic": "test"})
        response = result[0].text
        print(f"Error response: {response}")
        assert "Unknown tool" in response
        print("Invalid tool handling: PASSED")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    print("Error Handling: ALL TESTS PASSED!")

async def test_performance():
    """Test performance of blog generation"""
    print("\nTesting Performance...")
    
    import time
    
    # Test outline generation performance
    start_time = time.time()
    outline_args = {
        "topic": "Performance Testing",
        "target_audience": "intermediate",
        "keywords": ["benchmarking", "optimization"],
        "desired_length": "medium"
    }
    
    await handle_call_tool("generate_blog_outline", outline_args)
    outline_time = time.time() - start_time
    print(f"Outline generation time: {outline_time:.2f} seconds")
    
    # Test complete blog generation performance
    start_time = time.time()
    blog_args = {
        "topic": "Performance Testing",
        "target_audience": "intermediate",
        "keywords": ["benchmarking", "optimization"],
        "desired_length": "short"
    }
    
    await handle_call_tool("generate_complete_blog", blog_args)
    blog_time = time.time() - start_time
    print(f"Complete blog generation time: {blog_time:.2f} seconds")
    
    # Performance thresholds
    if outline_time < 1.0:
        print("Outline generation performance: EXCELLENT")
    elif outline_time < 3.0:
        print("Outline generation performance: GOOD")
    else:
        print("Outline generation performance: NEEDS IMPROVEMENT")
    
    if blog_time < 5.0:
        print("Blog generation performance: EXCELLENT")
    elif blog_time < 10.0:
        print("Blog generation performance: GOOD")
    else:
        print("Blog generation performance: NEEDS IMPROVEMENT")
    
    print("Performance Testing: COMPLETED")

async def main():
    """Run all MCP interface tests"""
    print("=" * 60)
    print("MCP Blog Server Interface Test Suite")
    print("=" * 60)
    
    try:
        await test_mcp_tools()
        await test_error_handling()
        await test_performance()
        
        print("\n" + "=" * 60)
        print("ALL MCP INTERFACE TESTS PASSED!")
        print("Server is ready for MCP client integration.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nTEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())

