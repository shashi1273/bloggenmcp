from flask import Blueprint, request, jsonify
import sys
import os
import json
import datetime
import re

# Add the MCP server directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'mcp-blog-server'))

try:
    from blog_generator import BlogGenerator, EnhancedBlogGenerator
except ImportError:
    # Fallback if MCP server is not available
    BlogGenerator = None
    EnhancedBlogGenerator = None

blog_bp = Blueprint('blog', __name__)

# Initialize blog generators if available
blog_generator = BlogGenerator() if BlogGenerator else None
enhanced_generator = EnhancedBlogGenerator() if EnhancedBlogGenerator else None

@blog_bp.route('/generate-outline', methods=['POST'])
def generate_outline():
    """Generate a blog outline based on the provided parameters."""
    try:
        data = request.get_json()
        
        if not data or 'topic' not in data:
            return jsonify({'error': 'Topic is required'}), 400
        
        topic = data['topic']
        target_audience = data.get('target_audience', 'intermediate')
        keywords = data.get('keywords', [])
        desired_length = data.get('desired_length', 'medium')
        
        if isinstance(keywords, str):
            keywords = [k.strip() for k in keywords.split(',') if k.strip()]
        
        # Generate outline using the MCP server logic
        if blog_generator:
            outline = blog_generator.generate_outline(topic, target_audience, keywords, desired_length)
        else:
            # Fallback mock outline
            outline = {
                'topic': topic,
                'target_audience': target_audience,
                'keywords': keywords,
                'desired_length': desired_length,
                'title_suggestions': [
                    f"The Complete Guide to {topic}: Best Practices for {target_audience.title()} Developers",
                    f"Mastering {topic}: A Comprehensive {target_audience.title()} Tutorial",
                    f"{topic} Explained: Essential Concepts for {target_audience.title()} Users"
                ],
                'sections': [
                    {
                        'title': 'Introduction',
                        'description': f'Overview of {topic} and its importance in modern development',
                        'estimated_words': 200
                    },
                    {
                        'title': 'Core Concepts',
                        'description': f'Fundamental principles and concepts of {topic}',
                        'estimated_words': 400
                    },
                    {
                        'title': 'Implementation Guide',
                        'description': f'Step-by-step guide to implementing {topic}',
                        'estimated_words': 600
                    },
                    {
                        'title': 'Best Practices',
                        'description': f'Industry best practices and recommendations for {topic}',
                        'estimated_words': 300
                    },
                    {
                        'title': 'Real-world Examples',
                        'description': f'Practical examples and use cases of {topic}',
                        'estimated_words': 400
                    },
                    {
                        'title': 'Conclusion',
                        'description': f'Summary and next steps for {topic}',
                        'estimated_words': 150
                    }
                ],
                'estimated_total_words': 2050,
                'generated_at': datetime.datetime.now().isoformat()
            }
        
        return jsonify(outline)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blog_bp.route('/generate-complete', methods=['POST'])
def generate_complete_blog():
    """Generate a complete blog post based on the provided parameters."""
    try:
        data = request.get_json()
        
        if not data or 'topic' not in data:
            return jsonify({'error': 'Topic is required'}), 400
        
        topic = data['topic']
        target_audience = data.get('target_audience', 'intermediate')
        keywords = data.get('keywords', [])
        desired_length = data.get('desired_length', 'medium')
        
        if isinstance(keywords, str):
            keywords = [k.strip() for k in keywords.split(',') if k.strip()]
        
        # Generate complete blog using the MCP server logic
        if enhanced_generator:
            blog_post = enhanced_generator.generate_complete_blog(topic, target_audience, keywords, desired_length)
        else:
            # Fallback mock blog post
            blog_post = {
                'title': f"The Complete Guide to {topic}: Best Practices for {target_audience.title()} Developers",
                'introduction': f"In today's rapidly evolving technology landscape, {topic} has emerged as a critical component for modern development. This comprehensive guide will explore the fundamental concepts, practical implementations, and best practices that will help you master {topic} and leverage its full potential in your projects.",
                'content': f"""# {topic}: A Comprehensive Guide

## Introduction

In today's rapidly evolving technology landscape, {topic} has emerged as a critical component for modern development. This comprehensive guide will explore the fundamental concepts, practical implementations, and best practices that will help you master {topic} and leverage its full potential in your projects.

## Core Concepts

Understanding the fundamental principles of {topic} is essential for effective implementation. This section covers the key concepts that form the foundation of {topic} technology.

### Key Principles

The core principles of {topic} include scalability, reliability, and maintainability. These principles guide the design and implementation of {topic} solutions.

## Implementation Guide

This section provides step-by-step guidance for implementing {topic} in your projects. We'll cover the essential tools, configurations, and best practices.

### Getting Started

To begin with {topic}, you'll need to set up your development environment and install the necessary tools.

### Configuration

Proper configuration is crucial for successful {topic} implementation. This includes setting up the required parameters and optimizing for your specific use case.

## Best Practices

Following established best practices ensures reliable and maintainable {topic} implementations. This section covers industry-standard approaches and recommendations.

### Performance Optimization

Optimizing performance is essential for production {topic} deployments. Consider factors such as resource allocation, caching strategies, and monitoring.

### Security Considerations

Security should be a primary concern when implementing {topic}. Follow security best practices and regularly update your implementations.

## Real-world Examples

This section provides practical examples and use cases that demonstrate {topic} in action. These examples help bridge the gap between theory and practice.

### Example 1: Basic Implementation

A simple example showing how to implement {topic} for a basic use case.

### Example 2: Advanced Configuration

An advanced example demonstrating complex {topic} configurations and optimizations.

## Conclusion

Throughout this guide, we've explored the essential aspects of {topic}, from fundamental concepts to practical implementation strategies. By following the best practices and examples provided, you'll be well-equipped to successfully implement {topic} in your projects.

The key takeaways include understanding the core principles, following best practices, and continuously monitoring and optimizing your implementations. As {topic} continues to evolve, staying updated with the latest developments and community best practices will ensure your continued success.
""",
                'conclusion': f"Throughout this guide, we've explored the essential aspects of {topic}, from fundamental concepts to practical implementation strategies. By following the best practices and examples provided, you'll be well-equipped to successfully implement {topic} in your projects.",
                'word_count': 1250,
                'reading_time': 6,
                'sections': 5,
                'keywords': keywords,
                'generated_at': datetime.datetime.now().isoformat()
            }
        
        # Validate the generated content
        validation_results = validate_blog_content(blog_post)
        blog_post['validation'] = validation_results
        
        return jsonify(blog_post)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blog_bp.route('/validate', methods=['POST'])
def validate_blog():
    """Validate a blog post against business rules."""
    try:
        data = request.get_json()
        
        if not data or 'blog_post' not in data:
            return jsonify({'error': 'Blog post data is required'}), 400
        
        blog_post = data['blog_post']
        validation_results = validate_blog_content(blog_post)
        
        return jsonify(validation_results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blog_bp.route('/business-rules', methods=['GET'])
def get_business_rules():
    """Get the current business rules and guidelines."""
    try:
        if blog_generator:
            rules = blog_generator.get_business_rules()
        else:
            # Fallback mock business rules
            rules = {
                'title': {
                    'min_length': 40,
                    'max_length': 80,
                    'requirements': [
                        'Should be descriptive and engaging',
                        'Should include relevant keywords',
                        'Should clearly indicate the target audience'
                    ]
                },
                'introduction': {
                    'min_words': 150,
                    'max_words': 300,
                    'requirements': [
                        'Should provide clear context',
                        'Should state the value proposition',
                        'Should outline what will be covered'
                    ]
                },
                'main_body': {
                    'min_sections': 3,
                    'requirements': [
                        'Should have logical organization',
                        'Should include practical examples',
                        'Should maintain consistent tone'
                    ]
                },
                'conclusion': {
                    'min_words': 100,
                    'max_words': 200,
                    'requirements': [
                        'Should summarize key points',
                        'Should provide actionable next steps',
                        'Should not introduce new information'
                    ]
                },
                'seo': {
                    'keyword_density': {
                        'min': 1,
                        'max': 3
                    },
                    'requirements': [
                        'Minimum 2 internal links',
                        'Minimum 3 external links to authoritative sources',
                        'Proper heading structure (H1, H2, H3)',
                        'Meta description optimization'
                    ]
                }
            }
        
        return jsonify(rules)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def validate_blog_content(blog_post):
    """Validate blog post content against business rules."""
    validation_results = {
        'overall_valid': True,
        'summary': {
            'total_errors': 0,
            'total_warnings': 0
        },
        'validations': {}
    }
    
    # Validate title
    title = blog_post.get('title', '')
    title_validation = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'length': len(title)
    }
    
    if len(title) < 40:
        title_validation['valid'] = False
        title_validation['errors'].append(f'Title too short: {len(title)} characters (minimum 40)')
        validation_results['summary']['total_errors'] += 1
        validation_results['overall_valid'] = False
    elif len(title) > 80:
        title_validation['valid'] = False
        title_validation['errors'].append(f'Title too long: {len(title)} characters (maximum 80)')
        validation_results['summary']['total_errors'] += 1
        validation_results['overall_valid'] = False
    
    validation_results['validations']['title'] = title_validation
    
    # Validate introduction
    introduction = blog_post.get('introduction', '')
    intro_word_count = len(introduction.split()) if introduction else 0
    intro_validation = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'word_count': intro_word_count
    }
    
    if intro_word_count < 150:
        intro_validation['valid'] = False
        intro_validation['errors'].append(f'Introduction too short: {intro_word_count} words (minimum 150)')
        validation_results['summary']['total_errors'] += 1
        validation_results['overall_valid'] = False
    elif intro_word_count > 300:
        intro_validation['warnings'].append(f'Introduction quite long: {intro_word_count} words (recommended maximum 300)')
        validation_results['summary']['total_warnings'] += 1
    
    validation_results['validations']['introduction'] = intro_validation
    
    # Validate content structure
    content = blog_post.get('content', '')
    sections = len(re.findall(r'^##\s+', content, re.MULTILINE)) if content else 0
    structure_validation = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'main_sections': sections
    }
    
    if sections < 3:
        structure_validation['valid'] = False
        structure_validation['errors'].append(f'Insufficient main sections: {sections} (minimum 3)')
        validation_results['summary']['total_errors'] += 1
        validation_results['overall_valid'] = False
    
    # Check for external links
    external_links = len(re.findall(r'https?://(?!localhost)', content)) if content else 0
    if external_links < 3:
        structure_validation['warnings'].append('Consider adding more external links to authoritative sources')
        validation_results['summary']['total_warnings'] += 1
    
    validation_results['validations']['structure'] = structure_validation
    
    return validation_results

