#!/usr/bin/env python3
"""
MCP Server for Technical Blog Creation

This server provides tools for creating technical blog posts with business rules validation.
It implements the Model Context Protocol (MCP) to enable integration with LLM applications.
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional, Sequence
from datetime import datetime
import re

# MCP imports
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

# Import enhanced blog generator
from blog_generator import EnhancedBlogGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-blog-server")

# Server instance
server = Server("mcp-blog-server")

class BlogBusinessRules:
    """Business rules validator for technical blog posts"""
    
    @staticmethod
    def validate_title(title: str) -> Dict[str, Any]:
        """Validate blog post title according to business rules"""
        errors = []
        warnings = []
        
        if len(title) < 40:
            errors.append(f"Title too short: {len(title)} characters (minimum 40)")
        elif len(title) > 80:
            errors.append(f"Title too long: {len(title)} characters (maximum 80)")
        
        if not re.search(r'[?:]', title):
            warnings.append("Title should ideally pose a question or clearly state the problem/solution")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "length": len(title)
        }
    
    @staticmethod
    def validate_introduction(intro: str) -> Dict[str, Any]:
        """Validate blog post introduction according to business rules"""
        errors = []
        warnings = []
        word_count = len(intro.split())
        
        if word_count < 150:
            errors.append(f"Introduction too short: {word_count} words (minimum 150)")
        elif word_count > 300:
            errors.append(f"Introduction too long: {word_count} words (maximum 300)")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "word_count": word_count
        }
    
    @staticmethod
    def validate_conclusion(conclusion: str) -> Dict[str, Any]:
        """Validate blog post conclusion according to business rules"""
        errors = []
        warnings = []
        word_count = len(conclusion.split())
        
        if word_count < 100:
            errors.append(f"Conclusion too short: {word_count} words (minimum 100)")
        elif word_count > 200:
            errors.append(f"Conclusion too long: {word_count} words (maximum 200)")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "word_count": word_count
        }
    
    @staticmethod
    def validate_content_structure(content: str) -> Dict[str, Any]:
        """Validate overall content structure"""
        errors = []
        warnings = []
        
        # Count main sections (headers starting with ##)
        main_sections = len(re.findall(r'^## ', content, re.MULTILINE))
        
        if main_sections < 3:
            errors.append(f"Insufficient main sections: {main_sections} (minimum 3)")
        
        # Check for code blocks
        code_blocks = len(re.findall(r'```', content))
        if code_blocks % 2 != 0:
            errors.append("Unclosed code block detected")
        
        # Check for links
        external_links = len(re.findall(r'\[.*?\]\(https?://.*?\)', content))
        if external_links < 3:
            warnings.append(f"Few external links: {external_links} (recommended minimum 3)")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "main_sections": main_sections,
            "external_links": external_links
        }

class BlogGenerator:
    """Technical blog post generator with business rules compliance"""
    
    def __init__(self):
        self.rules = BlogBusinessRules()
    
    def generate_blog_outline(self, topic: str, target_audience: str = "intermediate", 
                            keywords: List[str] = None) -> Dict[str, Any]:
        """Generate a blog post outline based on topic and parameters"""
        
        if keywords is None:
            keywords = []
        
        # Generate title suggestions
        title_templates = [
            f"A Complete Guide to {topic}",
            f"Understanding {topic}: Best Practices and Implementation",
            f"How to Master {topic}: A Developer's Guide",
            f"{topic} Explained: From Basics to Advanced Concepts",
            f"Building with {topic}: Practical Examples and Use Cases"
        ]
        
        # Generate section outline
        sections = [
            {
                "title": "Introduction",
                "description": f"Overview of {topic} and its importance in modern development",
                "estimated_words": 200
            },
            {
                "title": "Core Concepts",
                "description": f"Fundamental principles and concepts of {topic}",
                "estimated_words": 400
            },
            {
                "title": "Implementation Guide",
                "description": f"Step-by-step implementation of {topic} with examples",
                "estimated_words": 600
            },
            {
                "title": "Best Practices",
                "description": f"Industry best practices and common pitfalls to avoid",
                "estimated_words": 300
            },
            {
                "title": "Real-world Examples",
                "description": f"Practical use cases and examples of {topic} in action",
                "estimated_words": 400
            },
            {
                "title": "Conclusion",
                "description": f"Summary and next steps for learning more about {topic}",
                "estimated_words": 150
            }
        ]
        
        total_words = sum(section["estimated_words"] for section in sections)
        
        return {
            "topic": topic,
            "target_audience": target_audience,
            "keywords": keywords,
            "title_suggestions": title_templates,
            "sections": sections,
            "estimated_total_words": total_words,
            "generated_at": datetime.now().isoformat()
        }
    
    def validate_blog_post(self, blog_post: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a complete blog post against business rules"""
        
        validation_results = {
            "overall_valid": True,
            "validations": {},
            "summary": {
                "total_errors": 0,
                "total_warnings": 0
            }
        }
        
        # Validate title
        if "title" in blog_post:
            title_validation = self.rules.validate_title(blog_post["title"])
            validation_results["validations"]["title"] = title_validation
            if not title_validation["valid"]:
                validation_results["overall_valid"] = False
            validation_results["summary"]["total_errors"] += len(title_validation["errors"])
            validation_results["summary"]["total_warnings"] += len(title_validation["warnings"])
        
        # Validate introduction
        if "introduction" in blog_post:
            intro_validation = self.rules.validate_introduction(blog_post["introduction"])
            validation_results["validations"]["introduction"] = intro_validation
            if not intro_validation["valid"]:
                validation_results["overall_valid"] = False
            validation_results["summary"]["total_errors"] += len(intro_validation["errors"])
            validation_results["summary"]["total_warnings"] += len(intro_validation["warnings"])
        
        # Validate conclusion
        if "conclusion" in blog_post:
            conclusion_validation = self.rules.validate_conclusion(blog_post["conclusion"])
            validation_results["validations"]["conclusion"] = conclusion_validation
            if not conclusion_validation["valid"]:
                validation_results["overall_valid"] = False
            validation_results["summary"]["total_errors"] += len(conclusion_validation["errors"])
            validation_results["summary"]["total_warnings"] += len(conclusion_validation["warnings"])
        
        # Validate content structure
        if "content" in blog_post:
            structure_validation = self.rules.validate_content_structure(blog_post["content"])
            validation_results["validations"]["structure"] = structure_validation
            if not structure_validation["valid"]:
                validation_results["overall_valid"] = False
            validation_results["summary"]["total_errors"] += len(structure_validation["errors"])
            validation_results["summary"]["total_warnings"] += len(structure_validation["warnings"])
        
        return validation_results

# Initialize blog generator
blog_generator = BlogGenerator()
enhanced_generator = EnhancedBlogGenerator()

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools for blog creation"""
    return [
        Tool(
            name="generate_blog_outline",
            description="Generate a structured outline for a technical blog post with business rules compliance",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The main topic for the blog post"
                    },
                    "target_audience": {
                        "type": "string",
                        "enum": ["beginner", "intermediate", "advanced"],
                        "description": "Target audience level",
                        "default": "intermediate"
                    },
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional keywords to include in the blog post"
                    },
                    "desired_length": {
                        "type": "string",
                        "enum": ["short", "medium", "long"],
                        "description": "Desired length of the blog post",
                        "default": "medium"
                    }
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="generate_complete_blog",
            description="Generate a complete technical blog post with full content based on topic and requirements",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The main topic for the blog post"
                    },
                    "target_audience": {
                        "type": "string",
                        "enum": ["beginner", "intermediate", "advanced"],
                        "description": "Target audience level",
                        "default": "intermediate"
                    },
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Keywords to include in the blog post"
                    },
                    "desired_length": {
                        "type": "string",
                        "enum": ["short", "medium", "long"],
                        "description": "Desired length of the blog post",
                        "default": "medium"
                    },
                    "custom_requirements": {
                        "type": "object",
                        "description": "Additional custom requirements for the blog post"
                    }
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="validate_blog_post",
            description="Validate a blog post against business rules and quality standards",
            inputSchema={
                "type": "object",
                "properties": {
                    "blog_post": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "introduction": {"type": "string"},
                            "content": {"type": "string"},
                            "conclusion": {"type": "string"},
                            "keywords": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "description": "The blog post content to validate"
                    }
                },
                "required": ["blog_post"]
            }
        ),
        Tool(
            name="get_business_rules",
            description="Get the complete business rules and guidelines for technical blog creation",
            inputSchema={
                "type": "object",
                "properties": {
                    "section": {
                        "type": "string",
                        "enum": ["all", "structure", "quality", "seo", "validation"],
                        "description": "Specific section of business rules to retrieve",
                        "default": "all"
                    }
                }
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls for blog creation"""
    
    if name == "generate_blog_outline":
        topic = arguments.get("topic", "")
        target_audience = arguments.get("target_audience", "intermediate")
        keywords = arguments.get("keywords", [])
        desired_length = arguments.get("desired_length", "medium")
        
        if not topic:
            return [TextContent(
                type="text",
                text="Error: Topic is required for blog outline generation"
            )]
        
        outline = blog_generator.generate_blog_outline(
            topic=topic,
            target_audience=target_audience,
            keywords=keywords
        )
        
        # Adjust sections based on desired length
        if desired_length == "short":
            outline["sections"] = outline["sections"][:4]  # Fewer sections
        elif desired_length == "long":
            # Add more detailed sections
            outline["sections"].extend([
                {
                    "title": "Advanced Techniques",
                    "description": f"Advanced techniques and patterns for {topic}",
                    "estimated_words": 500
                },
                {
                    "title": "Performance Considerations",
                    "description": f"Performance optimization strategies for {topic}",
                    "estimated_words": 300
                }
            ])
        
        outline["estimated_total_words"] = sum(section["estimated_words"] for section in outline["sections"])
        
        return [TextContent(
            type="text",
            text=json.dumps(outline, indent=2)
        )]
    
    elif name == "generate_complete_blog":
        topic = arguments.get("topic", "")
        target_audience = arguments.get("target_audience", "intermediate")
        keywords = arguments.get("keywords", [])
        desired_length = arguments.get("desired_length", "medium")
        custom_requirements = arguments.get("custom_requirements", {})
        
        if not topic:
            return [TextContent(
                type="text",
                text="Error: Topic is required for blog generation"
            )]
        
        # First generate outline
        outline = blog_generator.generate_blog_outline(
            topic=topic,
            target_audience=target_audience,
            keywords=keywords
        )
        
        # Adjust sections based on desired length
        if desired_length == "short":
            outline["sections"] = outline["sections"][:4]
        elif desired_length == "long":
            outline["sections"].extend([
                {
                    "title": "Advanced Techniques",
                    "description": f"Advanced techniques and patterns for {topic}",
                    "estimated_words": 500
                },
                {
                    "title": "Performance Considerations",
                    "description": f"Performance optimization strategies for {topic}",
                    "estimated_words": 300
                }
            ])
        
        # Generate complete blog post
        complete_blog = enhanced_generator.generate_complete_blog_post(
            outline=outline,
            custom_requirements=custom_requirements
        )
        
        # Validate the generated blog post
        validation_results = blog_generator.validate_blog_post(complete_blog)
        complete_blog["validation"] = validation_results
        
        return [TextContent(
            type="text",
            text=json.dumps(complete_blog, indent=2)
        )]
    
    elif name == "validate_blog_post":
        blog_post = arguments.get("blog_post", {})
        
        if not blog_post:
            return [TextContent(
                type="text",
                text="Error: Blog post content is required for validation"
            )]
        
        validation_results = blog_generator.validate_blog_post(blog_post)
        
        return [TextContent(
            type="text",
            text=json.dumps(validation_results, indent=2)
        )]
    
    elif name == "get_business_rules":
        section = arguments.get("section", "all")
        
        business_rules = {
            "structure": {
                "title": {
                    "min_length": 40,
                    "max_length": 80,
                    "requirements": ["Must be SEO-friendly", "Should pose a question or state problem/solution"]
                },
                "introduction": {
                    "min_words": 150,
                    "max_words": 300,
                    "requirements": ["Must summarize the problem and solution", "Should hook the reader"]
                },
                "main_body": {
                    "min_sections": 3,
                    "requirements": ["Clear headings", "Logical flow", "Technical terms defined", "Code snippets formatted"]
                },
                "conclusion": {
                    "min_words": 100,
                    "max_words": 200,
                    "requirements": ["Summarize key points", "Provide actionable insights"]
                }
            },
            "quality": {
                "technical_accuracy": ["Cross-reference with reputable sources", "Verify code snippets"],
                "clarity": ["Average sentence length ≤ 20 words", "Paragraphs ≤ 5-7 sentences", "Use active voice"],
                "originality": ["Must be original content", "Proper citation required"],
                "tone": ["Informative and professional", "Helpful and encouraging"]
            },
            "seo": {
                "keywords": ["1-3% keyword density", "Keywords in first paragraph", "Use long-tail keywords"],
                "linking": ["Minimum 2 internal links", "Minimum 3 external links", "Descriptive anchor text"],
                "media": ["Descriptive alt text", "Optimized file sizes", "Media supports content"]
            },
            "validation": {
                "automated_checks": ["Length validation", "Keyword density", "Link validation"],
                "review_process": ["Technical accuracy review", "Clarity assessment", "Quality control"]
            }
        }
        
        if section == "all":
            result = business_rules
        else:
            result = business_rules.get(section, {})
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Error: Unknown tool '{name}'"
        )]

async def main():
    """Main server entry point"""
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-blog-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())

