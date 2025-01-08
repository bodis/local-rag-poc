# Project Documentation Assistant

A tool to help manage and interact with project documentation using AI.

## Quick Start

1. Install requirements:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

2. Create input directory and add documents:
```bash
mkdir -p input
# Add PDF, Markdown or .url files to input/
```

3. Run the application:
```bash
LOGLEVEL=DEBUG FLASK_APP=app.main flask run
```

4. Access the web interface at http://localhost:5123

## Features
- Upload documents (PDF, Markdown, URLs)
- Ask questions about your documentation
- Get AI-powered answers with source references

## Troubleshooting
- Ensure virtual environment is activated
- Check logs for errors
- Verify URLs in .url files are valid
