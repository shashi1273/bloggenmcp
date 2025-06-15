# MCP Technical Blog Server

A sophisticated Model Context Protocol (MCP) server that provides automated technical blog creation with comprehensive business rules validation and quality assurance.

## Features

- **Automated Blog Generation**: Create complete technical blog posts with intelligent content generation
- **Business Rules Validation**: Comprehensive quality assurance with customizable validation rules
- **MCP Protocol Compliance**: Full compatibility with MCP-enabled clients and development environments
- **Multi-Audience Support**: Generate content for beginner, intermediate, and advanced audiences
- **SEO Optimization**: Built-in search engine optimization with keyword integration
- **Flexible Architecture**: Modular design supporting customization and extension

## Quick Start

### Prerequisites

- Python 3.11 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. Clone or download the server files:
```bash
git clone <repository-url>
cd mcp-blog-server
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run tests to verify installation:
```bash
python test_server.py
```

### Basic Usage

Start the MCP server:
```bash
python server.py
```

The server implements the following MCP tools:

- `generate_blog_outline`: Create structured outlines for technical blog posts
- `generate_complete_blog`: Generate complete blog posts with full content
- `validate_blog_post`: Validate content against business rules
- `get_business_rules`: Retrieve current business rules and guidelines

## Example Usage

### Generate a Blog Outline

```json
{
  "tool": "generate_blog_outline",
  "arguments": {
    "topic": "Docker Containerization",
    "target_audience": "intermediate",
    "keywords": ["containers", "microservices", "deployment"],
    "desired_length": "medium"
  }
}
```

### Generate Complete Blog Post

```json
{
  "tool": "generate_complete_blog",
  "arguments": {
    "topic": "API Design Best Practices",
    "target_audience": "advanced",
    "keywords": ["REST", "GraphQL", "authentication"],
    "desired_length": "long"
  }
}
```

## Business Rules

The server enforces comprehensive business rules for content quality:

### Structure Requirements
- **Title**: 40-80 characters, SEO-optimized
- **Introduction**: 150-300 words with clear value proposition
- **Main Content**: Minimum 3 sections with logical organization
- **Conclusion**: 100-200 words with actionable insights

### Quality Standards
- Technical accuracy validation
- Readability optimization (max 20 words per sentence)
- Consistent tone and style
- Proper code formatting and examples

### SEO Optimization
- 1-3% keyword density
- Strategic keyword placement
- Minimum 2 internal links and 3 external links
- Optimized meta content

## Architecture

The server implements a multi-layered architecture:

- **MCP Protocol Layer**: Handles client communication via JSON-RPC 2.0
- **Business Rules Engine**: Validates content against quality standards
- **Content Generation Engine**: Creates comprehensive technical content
- **Validation Framework**: Ensures compliance and quality assurance

## Deployment

### Development Deployment

For local development and testing:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python test_server.py
python test_mcp_interface.py

# Start server
python server.py
```

### Production Deployment

For production environments, use the automated deployment script:

```bash
sudo ./deploy.sh
```

This script:
- Creates system user and service
- Configures security settings
- Sets up logging and monitoring
- Enables automatic startup
- Creates management commands

### Container Deployment

Build and run with Docker:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "server.py"]
```

## Configuration

### Environment Variables

- `MCP_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `MCP_CONFIG_FILE`: Path to configuration file
- `MCP_CACHE_DIR`: Directory for content caching

### Business Rules Customization

Modify the `BlogBusinessRules` class to implement custom validation:

```python
class CustomBusinessRules(BlogBusinessRules):
    @staticmethod
    def validate_title(title: str) -> Dict[str, Any]:
        # Custom title validation logic
        pass
```

## Testing

The server includes comprehensive test suites:

```bash
# Core functionality tests
python test_server.py

# MCP interface tests
python test_mcp_interface.py

# Performance tests
python -m pytest tests/performance/
```

## Integration

### MCP Client Integration

The server works with any MCP-compatible client:

- **Claude Desktop**: Add server to MCP configuration
- **VS Code**: Use MCP extension
- **Custom Applications**: Implement MCP client protocol

### API Integration

For non-MCP integrations, the server can be extended with REST API endpoints:

```python
from flask import Flask
from server import handle_call_tool

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_blog():
    # Handle HTTP requests
    pass
```

## Performance

- **Outline Generation**: < 1 second
- **Complete Blog Generation**: < 5 seconds
- **Validation**: < 0.5 seconds
- **Memory Usage**: ~50MB base, scales with content complexity

## Security

- Isolated execution environment
- Input validation and sanitization
- Configurable access controls
- Comprehensive audit logging
- Regular security updates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guidelines
- Include comprehensive tests
- Update documentation
- Maintain backward compatibility

## Troubleshooting

### Common Issues

**Import Errors**: Ensure all dependencies are installed in the correct Python environment

**MCP Connection Issues**: Verify client configuration and server accessibility

**Validation Failures**: Check business rules configuration and content requirements

**Performance Issues**: Monitor resource usage and consider scaling options

### Debugging

Enable debug logging:
```bash
export MCP_LOG_LEVEL=DEBUG
python server.py
```

Check server logs:
```bash
tail -f /var/log/mcp-blog-server/server.log
```

## License

MIT License - see LICENSE file for details.

## Support

- Documentation: See `documentation.md` for comprehensive guide
- Issues: Report bugs and feature requests via project repository
- Community: Join discussions and get help from other users

## Changelog

### Version 1.0.0 (June 15, 2025)
- Initial release
- Complete MCP protocol implementation
- Comprehensive business rules framework
- Multi-audience content generation
- Production deployment capabilities
- Full test suite and documentation

