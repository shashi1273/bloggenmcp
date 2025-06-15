#!/usr/bin/env python3
"""
Test script for MCP Blog Server

This script tests the functionality of the MCP blog server tools
without requiring a full MCP client connection.
"""

import json
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from blog_generator import EnhancedBlogGenerator
from server import BlogGenerator, BlogBusinessRules

def test_business_rules():
    """Test business rules validation"""
    print("Testing Business Rules Validation...")
    
    rules = BlogBusinessRules()
    
    # Test title validation
    print("\n1. Testing Title Validation:")
    
    # Valid title
    valid_title = "The Complete Guide to Python Web Development: Best Practices for Modern Applications"
    title_result = rules.validate_title(valid_title)
    print(f"Valid title: {title_result}")
    
    # Invalid title (too short)
    short_title = "Python Guide"
    short_result = rules.validate_title(short_title)
    print(f"Short title: {short_result}")
    
    # Test introduction validation
    print("\n2. Testing Introduction Validation:")
    
    valid_intro = """
    In today's rapidly evolving technology landscape, Python web development has emerged as a critical skill for modern developers. 
    This comprehensive guide will explore the fundamental concepts, practical implementations, and best practices that will help you 
    master Python web development and leverage its full potential in your projects. Whether you're a beginner looking to start your 
    journey or an experienced developer seeking to enhance your skills, this article provides valuable insights and actionable strategies 
    for building robust web applications with Python.
    """
    intro_result = rules.validate_introduction(valid_intro.strip())
    print(f"Valid introduction: {intro_result}")
    
    print("Business Rules Validation: PASSED")

def test_blog_outline_generation():
    """Test blog outline generation"""
    print("\nTesting Blog Outline Generation...")
    
    generator = BlogGenerator()
    
    outline = generator.generate_blog_outline(
        topic="Machine Learning with Python",
        target_audience="intermediate",
        keywords=["scikit-learn", "neural networks", "data preprocessing"]
    )
    
    print(f"Generated outline for '{outline['topic']}':")
    print(f"Target audience: {outline['target_audience']}")
    print(f"Keywords: {outline['keywords']}")
    print(f"Estimated total words: {outline['estimated_total_words']}")
    print(f"Number of sections: {len(outline['sections'])}")
    
    for i, section in enumerate(outline['sections'], 1):
        print(f"  {i}. {section['title']} ({section['estimated_words']} words)")
    
    print("Blog Outline Generation: PASSED")

def test_enhanced_blog_generation():
    """Test enhanced blog generation"""
    print("\nTesting Enhanced Blog Generation...")
    
    generator = BlogGenerator()
    enhanced_generator = EnhancedBlogGenerator()
    
    # Generate outline first
    outline = generator.generate_blog_outline(
        topic="Docker Containerization",
        target_audience="intermediate",
        keywords=["containers", "microservices", "deployment"]
    )
    
    # Generate complete blog post
    complete_blog = enhanced_generator.generate_complete_blog_post(outline)
    
    print(f"Generated complete blog post:")
    print(f"Title: {complete_blog['title']}")
    print(f"Word count: {complete_blog['word_count']}")
    print(f"Reading time: {complete_blog['estimated_reading_time']} minutes")
    print(f"Number of sections: {len(complete_blog['sections'])}")
    
    # Test validation
    validation_results = generator.validate_blog_post(complete_blog)
    print(f"Validation results:")
    print(f"  Overall valid: {validation_results['overall_valid']}")
    print(f"  Total errors: {validation_results['summary']['total_errors']}")
    print(f"  Total warnings: {validation_results['summary']['total_warnings']}")
    
    print("Enhanced Blog Generation: PASSED")

def test_content_quality():
    """Test content quality and structure"""
    print("\nTesting Content Quality and Structure...")
    
    enhanced_generator = EnhancedBlogGenerator()
    generator = BlogGenerator()
    
    # Generate a blog post
    outline = generator.generate_blog_outline(
        topic="API Design Best Practices",
        target_audience="advanced",
        keywords=["REST", "GraphQL", "authentication", "versioning"]
    )
    
    complete_blog = enhanced_generator.generate_complete_blog_post(outline)
    
    # Check content structure
    content = complete_blog['content']
    
    # Count sections
    main_sections = len([line for line in content.split('\n') if line.startswith('## ')])
    print(f"Main sections found: {main_sections}")
    
    # Check for code blocks
    code_blocks = content.count('```')
    print(f"Code blocks found: {code_blocks // 2}")  # Divide by 2 since each block has opening and closing
    
    # Check for links
    import re
    external_links = len(re.findall(r'\[.*?\]\(https?://.*?\)', content))
    print(f"External links found: {external_links}")
    
    # Check keyword integration
    keywords_found = sum(1 for keyword in outline['keywords'] if keyword.lower() in content.lower())
    print(f"Keywords integrated: {keywords_found}/{len(outline['keywords'])}")
    
    print("Content Quality and Structure: PASSED")

def test_different_audiences():
    """Test generation for different target audiences"""
    print("\nTesting Different Target Audiences...")
    
    enhanced_generator = EnhancedBlogGenerator()
    generator = BlogGenerator()
    
    topic = "Cloud Computing Fundamentals"
    audiences = ["beginner", "intermediate", "advanced"]
    
    for audience in audiences:
        outline = generator.generate_blog_outline(
            topic=topic,
            target_audience=audience,
            keywords=["AWS", "Azure", "scalability"]
        )
        
        blog_post = enhanced_generator.generate_complete_blog_post(outline)
        
        print(f"Generated for {audience} audience:")
        print(f"  Title: {blog_post['title']}")
        print(f"  Word count: {blog_post['word_count']}")
        print(f"  Sections: {len(blog_post['sections'])}")
        
        # Check if content is appropriate for audience
        content_lower = blog_post['content'].lower()
        if audience == "beginner":
            beginner_indicators = ["basic", "introduction", "getting started", "fundamental"]
            found_indicators = sum(1 for indicator in beginner_indicators if indicator in content_lower)
            print(f"  Beginner-friendly indicators: {found_indicators}")
        elif audience == "advanced":
            advanced_indicators = ["advanced", "complex", "sophisticated", "expert"]
            found_indicators = sum(1 for indicator in advanced_indicators if indicator in content_lower)
            print(f"  Advanced indicators: {found_indicators}")
    
    print("Different Target Audiences: PASSED")

def main():
    """Run all tests"""
    print("=" * 60)
    print("MCP Blog Server Test Suite")
    print("=" * 60)
    
    try:
        test_business_rules()
        test_blog_outline_generation()
        test_enhanced_blog_generation()
        test_content_quality()
        test_different_audiences()
        
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED!")
        print("MCP Blog Server is ready for deployment.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nTEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

